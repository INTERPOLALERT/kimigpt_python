import os
import json
import asyncio
import threading
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid

# Import agents
from src.agents.orchestrator import OrchestratorAgent
from src.api.api_manager import api_manager

app = Flask(__name__)
app.secret_key = 'kimi-gpt-secret-key-2024'

# Configuration
UPLOAD_FOLDER = '/mnt/okcomputer/output/kimigpt/uploads'
GENERATED_SITES_FOLDER = '/mnt/okcomputer/output/kimigpt/generated_sites'
ALLOWED_EXTENSIONS = {
    'image': {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'},
    'document': {'pdf', 'docx', 'txt'},
    'video': {'mp4', 'webm', 'mov'},
    'audio': {'mp3', 'wav', 'ogg'}
}

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_SITES_FOLDER, exist_ok=True)

# Global orchestrator instance
orchestrator = OrchestratorAgent()

# Store for active projects and their status
active_projects = {}
project_results = {}

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/generator')
def generator():
    """Website generation page"""
    return render_template('generator.html')

@app.route('/preview/<project_id>')
def preview(project_id):
    """Preview page for generated website"""
    if project_id in project_results:
        return render_template('preview.html', project_id=project_id)
    return redirect(url_for('generator'))

@app.route('/settings')
def settings():
    """Settings and configuration page"""
    api_status = api_manager.get_status()
    return render_template('settings.html', api_status=api_status)

@app.route('/api/status')
def api_status():
    """Get API status"""
    return jsonify(api_manager.get_status())

@app.route('/api/generate', methods=['POST'])
def generate_website():
    """Generate website from user input"""
    try:
        # Get form data
        prompt = request.form.get('prompt', '')
        preferences = json.loads(request.form.get('preferences', '{}'))
        
        # Generate unique project ID
        project_id = f"project_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Handle file uploads
        uploaded_files = []
        if 'files' in request.files:
            files = request.files.getlist('files')
            for file in files:
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(file_path)
                    
                    uploaded_files.append({
                        'filename': filename,
                        'path': file_path,
                        'size': os.path.getsize(file_path),
                        'type': file.content_type
                    })
        
        # Prepare input data
        input_data = {
            'project_id': project_id,
            'project_name': preferences.get('project_name', 'My Website'),
            'prompt': prompt,
            'preferences': preferences,
            'files': uploaded_files,
            'framework': preferences.get('framework', 'vanilla'),
            'complexity': preferences.get('complexity', 'moderate')
        }
        
        # Store project in active projects
        active_projects[project_id] = {
            'status': 'starting',
            'progress': 0,
            'started_at': datetime.now().isoformat(),
            'input': input_data
        }
        
        # Start generation in background thread
        def generate_in_background():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(run_generation(project_id, input_data))
            loop.close()
        
        thread = threading.Thread(target=generate_in_background)
        thread.start()
        
        return jsonify({
            'success': True,
            'project_id': project_id,
            'message': 'Website generation started',
            'redirect_url': url_for('preview', project_id=project_id)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

async def run_generation(project_id: str, input_data: Dict[str, Any]):
    """Run website generation process"""
    try:
        # Update status
        active_projects[project_id]['status'] = 'processing'
        active_projects[project_id]['progress'] = 10
        
        # Run orchestrator
        result = await orchestrator.process(input_data)
        
        # Store results
        project_results[project_id] = {
            'result': result,
            'completed_at': datetime.now().isoformat(),
            'status': 'completed' if result.get('success', False) else 'failed'
        }
        
        # Update active project status
        active_projects[project_id]['status'] = 'completed'
        active_projects[project_id]['progress'] = 100
        active_projects[project_id]['result'] = result
        
    except Exception as e:
        active_projects[project_id]['status'] = 'error'
        active_projects[project_id]['error'] = str(e)
        active_projects[project_id]['progress'] = 100

@app.route('/api/projects/<project_id>/status')
def project_status(project_id):
    """Get project generation status"""
    if project_id in active_projects:
        project = active_projects[project_id]
        return jsonify({
            'project_id': project_id,
            'status': project['status'],
            'progress': project.get('progress', 0),
            'started_at': project['started_at'],
            'estimated_time': '30-60 seconds'
        })
    
    return jsonify({
        'error': 'Project not found'
    }), 404

@app.route('/api/projects/<project_id>/result')
def project_result(project_id):
    """Get project generation result"""
    if project_id in project_results:
        result = project_results[project_id]['result']
        return jsonify(result)
    
    return jsonify({
        'error': 'Project result not found'
    }), 404

@app.route('/api/projects/<project_id>/download')
def download_project(project_id):
    """Download generated website as ZIP"""
    if project_id in project_results:
        result = project_results[project_id]['result']
        
        if result.get('success', False) and 'deploy_result' in result:
            zip_path = result['deploy_result'].get('zip_file_path')
            
            if zip_path and os.path.exists(zip_path):
                return send_file(zip_path, as_attachment=True)
        
        return jsonify({
            'error': 'ZIP file not available'
        }), 404
    
    return jsonify({
        'error': 'Project not found'
    }), 404

@app.route('/api/projects/<project_id>/preview')
def preview_website(project_id):
    """Serve preview of generated website"""
    if project_id in project_results:
        result = project_results[project_id]['result']
        
        if result.get('success', False) and 'code' in result:
            code = result['code']
            
            # Serve the main HTML file
            if 'index.html' in code:
                return code['index.html']
        
        return jsonify({
            'error': 'Preview not available'
        }), 404
    
    return jsonify({
        'error': 'Project not found'
    }), 404

@app.route('/api/templates')
def get_templates():
    """Get available templates and styles"""
    templates = [
        {
            'id': 'modern_business',
            'name': 'Modern Business',
            'description': 'Professional business website template',
            'preview': '/static/images/templates/modern_business.jpg',
            'features': ['hero_section', 'services', 'team', 'contact']
        },
        {
            'id': 'creative_portfolio',
            'name': 'Creative Portfolio',
            'description': 'Showcase your creative work',
            'preview': '/static/images/templates/creative_portfolio.jpg',
            'features': ['gallery', 'about', 'skills', 'contact']
        },
        {
            'id': 'ecommerce_store',
            'name': 'E-commerce Store',
            'description': 'Online store with product showcase',
            'preview': '/static/images/templates/ecommerce_store.jpg',
            'features': ['products', 'cart', 'checkout', 'gallery']
        },
        {
            'id': 'minimalist_blog',
            'name': 'Minimalist Blog',
            'description': 'Clean and simple blog layout',
            'preview': '/static/images/templates/minimalist_blog.jpg',
            'features': ['blog', 'articles', 'search', 'newsletter']
        }
    ]
    
    return jsonify({
        'templates': templates,
        'total': len(templates)
    })

@app.route('/api/examples')
def get_examples():
    """Get example prompts and use cases"""
    examples = [
        {
            'category': 'Business',
            'prompts': [
                'Create a modern business website for a consulting firm with blue color scheme',
                'Build a professional portfolio site for a marketing agency',
                'Design a corporate website with services, team, and contact sections'
            ]
        },
        {
            'category': 'E-commerce',
            'prompts': [
                'Create an online store for handmade jewelry with product gallery',
                'Build a fashion boutique website with shopping cart functionality',
                'Design a tech gadget store with product filtering and search'
            ]
        },
        {
            'category': 'Portfolio',
            'prompts': [
                'Create a photographer portfolio with image galleries and about section',
                'Build a designer portfolio with project showcase and skills',
                'Design an artist portfolio with artwork display and biography'
            ]
        },
        {
            'category': 'Personal',
            'prompts': [
                'Create a personal blog with clean design and article sections',
                'Build a resume website with professional layout and contact form',
                'Design a wedding website with RSVP form and photo gallery'
            ]
        }
    ]
    
    return jsonify({
        'examples': examples
    })

@app.route('/api/system/info')
def system_info():
    """Get system information"""
    return jsonify({
        'version': '1.0.0',
        'name': 'KimiGPT Website Builder',
        'description': 'Multi-Agent AI Website Builder',
        'features': [
            'Multi-agent AI system',
            'Smart API rotation',
            'Real-time preview',
            'Multi-modal input support',
            'Accessibility compliance',
            'SEO optimization',
            'Performance optimization'
        ],
        'supported_formats': {
            'images': ['jpg', 'png', 'gif', 'webp', 'svg'],
            'documents': ['pdf', 'docx', 'txt'],
            'videos': ['mp4', 'webm', 'mov'],
            'audio': ['mp3', 'wav', 'ogg']
        }
    })

if __name__ == '__main__':
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )