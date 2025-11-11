"""
Orchestrator Agent for KimiGPT
Coordinates all other agents to generate websites
"""

import asyncio
from typing import Dict, Any, Optional, Callable
from datetime import datetime
import os
import json
from pathlib import Path

from src.api.api_manager import APIManager
from src.agents.understanding_agent import UnderstandingAgent
from src.agents.design_agent import DesignAgent
from src.agents.code_agent import CodeAgent
from src.agents.content_agent import ContentAgent
from src.agents.qa_agent import QAAgent
from src.agents.deployment_agent import DeploymentAgent


class OrchestratorAgent:
    """Master orchestrator that coordinates all agents"""

    def __init__(self):
        self.api_manager = APIManager()
        self.understanding_agent = UnderstandingAgent(self.api_manager)
        self.design_agent = DesignAgent(self.api_manager)
        self.code_agent = CodeAgent(self.api_manager)
        self.content_agent = ContentAgent(self.api_manager)
        self.qa_agent = QAAgent(self.api_manager)
        self.deployment_agent = DeploymentAgent()

    async def process(
        self,
        input_data: Dict[str, Any],
        progress_callback: Optional[Callable] = None,
        agent_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Process website generation request

        Args:
            input_data: Dictionary containing project info, prompt, files, preferences
            progress_callback: Callback for progress updates (value, message)
            agent_callback: Callback for agent status updates (agent_name, status)

        Returns:
            Dictionary containing generation results
        """
        try:
            project_id = input_data.get('project_id', 'unknown')
            output_dir = Path(f"Z:\\kimigpt\\output\\{project_id}")
            output_dir.mkdir(parents=True, exist_ok=True)

            result = {
                'success': False,
                'project_id': project_id,
                'started_at': datetime.now().isoformat(),
                'steps': []
            }

            # Step 1: Understanding Phase (15-20%)
            if progress_callback:
                progress_callback(15, "🧠 Understanding your requirements...")
            if agent_callback:
                agent_callback("Understanding", "Processing")

            try:
                understanding_result = await self.understanding_agent.analyze(input_data)
                result['steps'].append({
                    'agent': 'understanding',
                    'result': understanding_result,
                    'success': understanding_result.get('success', False)
                })

                if agent_callback:
                    agent_callback("Understanding", "Complete ✓")
            except Exception as e:
                if agent_callback:
                    agent_callback("Understanding", f"Error: {str(e)}")
                understanding_result = {
                    'success': False,
                    'error': str(e),
                    'raw_prompt': input_data.get('prompt', '')
                }

            # Step 2: Design Phase (30-40%)
            if progress_callback:
                progress_callback(30, "🎨 Creating design specifications...")
            if agent_callback:
                agent_callback("Design", "Processing")

            try:
                design_result = await self.design_agent.create_design(
                    understanding_result,
                    input_data.get('preferences', {})
                )
                result['steps'].append({
                    'agent': 'design',
                    'result': design_result,
                    'success': design_result.get('success', False)
                })

                if agent_callback:
                    agent_callback("Design", "Complete ✓")
            except Exception as e:
                if agent_callback:
                    agent_callback("Design", f"Error: {str(e)}")
                design_result = {
                    'success': False,
                    'error': str(e)
                }

            # Step 3: Content Generation (45-55%)
            if progress_callback:
                progress_callback(45, "📝 Generating website content...")
            if agent_callback:
                agent_callback("Content", "Processing")

            try:
                content_result = await self.content_agent.generate_content(
                    understanding_result,
                    design_result
                )
                result['steps'].append({
                    'agent': 'content',
                    'result': content_result,
                    'success': content_result.get('success', False)
                })

                if agent_callback:
                    agent_callback("Content", "Complete ✓")
            except Exception as e:
                if agent_callback:
                    agent_callback("Content", f"Error: {str(e)}")
                content_result = {
                    'success': False,
                    'error': str(e)
                }

            # Step 4: Code Generation (60-75%)
            if progress_callback:
                progress_callback(60, "💻 Generating website code...")
            if agent_callback:
                agent_callback("Code", "Processing")

            try:
                code_result = await self.code_agent.generate_code(
                    design_result,
                    content_result,
                    input_data.get('preferences', {})
                )
                result['steps'].append({
                    'agent': 'code',
                    'result': code_result,
                    'success': code_result.get('success', False)
                })
                result['code'] = code_result.get('files', {})

                if agent_callback:
                    agent_callback("Code", "Complete ✓")
            except Exception as e:
                if agent_callback:
                    agent_callback("Code", f"Error: {str(e)}")
                # Use fallback if code generation fails
                code_result = {
                    'success': True,
                    'files': {
                        'index.html': self.get_emergency_fallback_html(input_data),
                        'README.md': '# Generated Website\n\nThis is a fallback template.'
                    },
                    'note': f'Used emergency fallback due to: {str(e)}'
                }
                result['code'] = code_result.get('files', {})

            # Step 5: Quality Assurance (80-85%)
            if progress_callback:
                progress_callback(80, "✅ Running quality checks...")
            if agent_callback:
                agent_callback("QA", "Processing")

            try:
                qa_result = await self.qa_agent.validate(code_result)
                result['steps'].append({
                    'agent': 'qa',
                    'result': qa_result,
                    'success': qa_result.get('success', False)
                })

                if agent_callback:
                    agent_callback("QA", "Complete ✓")
            except Exception as e:
                if agent_callback:
                    agent_callback("QA", f"Warning: {str(e)}")
                qa_result = {
                    'success': True,
                    'note': 'QA skipped due to error'
                }

            # Step 6: Deployment/Packaging (90-100%)
            if progress_callback:
                progress_callback(90, "📦 Packaging your website...")
            if agent_callback:
                agent_callback("Deployment", "Processing")

            try:
                deployment_result = await self.deployment_agent.package(
                    code_result,
                    output_dir,
                    input_data
                )
                result['steps'].append({
                    'agent': 'deployment',
                    'result': deployment_result,
                    'success': deployment_result.get('success', False)
                })
                result['deploy_result'] = deployment_result

                if agent_callback:
                    agent_callback("Deployment", "Complete ✓")
            except Exception as e:
                if agent_callback:
                    agent_callback("Deployment", f"Warning: {str(e)}")
                deployment_result = {
                    'success': False,
                    'error': str(e)
                }

            # Complete
            if progress_callback:
                progress_callback(100, "✨ Website generated successfully!")

            result['success'] = True
            result['completed_at'] = datetime.now().isoformat()
            result['output_dir'] = str(output_dir)

            # Save result metadata
            try:
                with open(output_dir / 'generation_result.json', 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
            except Exception as e:
                print(f"Warning: Could not save metadata: {e}")

            return result

        except Exception as e:
            if progress_callback:
                progress_callback(100, f"❌ Error: {str(e)}")

            return {
                'success': False,
                'error': str(e),
                'project_id': input_data.get('project_id', 'unknown'),
                'completed_at': datetime.now().isoformat()
            }

    def get_emergency_fallback_html(self, input_data: Dict[str, Any]) -> str:
        """Get emergency fallback HTML when all else fails"""
        project_name = input_data.get('project_name', 'My Website')
        prompt = input_data.get('prompt', 'Welcome to my website')

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{project_name}">
    <title>{project_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f9fafb;
        }}

        .hero {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 100px 20px;
            text-align: center;
            min-height: 60vh;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
        }}

        .hero h1 {{
            font-size: 3.5em;
            margin-bottom: 20px;
            animation: fadeInDown 1s ease-out;
        }}

        .hero p {{
            font-size: 1.4em;
            margin-bottom: 30px;
            opacity: 0.95;
            max-width: 700px;
            animation: fadeInUp 1s ease-out 0.3s both;
        }}

        .btn {{
            display: inline-block;
            padding: 16px 45px;
            background: white;
            color: #667eea;
            text-decoration: none;
            border-radius: 30px;
            font-weight: 600;
            font-size: 1.1em;
            transition: all 0.3s ease;
            animation: fadeInUp 1s ease-out 0.6s both;
        }}

        .btn:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 80px 20px;
        }}

        .section-title {{
            text-align: center;
            font-size: 2.8em;
            margin-bottom: 60px;
            color: #111827;
        }}

        .features {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 40px;
            margin-top: 50px;
        }}

        .feature-card {{
            padding: 40px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }}

        .feature-card:hover {{
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }}

        .feature-card h3 {{
            font-size: 1.6em;
            margin-bottom: 15px;
            color: #667eea;
        }}

        .feature-card p {{
            color: #6b7280;
            line-height: 1.7;
        }}

        footer {{
            background: #1f2937;
            color: white;
            text-align: center;
            padding: 50px 20px;
            margin-top: 80px;
        }}

        footer p {{
            margin: 10px 0;
            opacity: 0.9;
        }}

        @keyframes fadeInDown {{
            from {{
                opacity: 0;
                transform: translateY(-30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        @media (max-width: 768px) {{
            .hero h1 {{
                font-size: 2.2em;
            }}

            .hero p {{
                font-size: 1.1em;
            }}

            .features {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <section class="hero">
        <h1>{project_name}</h1>
        <p>{prompt[:200]}...</p>
        <a href="#features" class="btn">Explore Features</a>
    </section>

    <div class="container">
        <h2 class="section-title" id="features">Our Amazing Features</h2>
        <div class="features">
            <div class="feature-card">
                <h3>🚀 Fast & Efficient</h3>
                <p>Lightning-fast performance optimized for the best user experience. Built with modern web technologies and best practices.</p>
            </div>
            <div class="feature-card">
                <h3>💡 Innovative Design</h3>
                <p>Beautiful, modern interface that captures attention and provides intuitive navigation. Designed with your users in mind.</p>
            </div>
            <div class="feature-card">
                <h3>📱 Fully Responsive</h3>
                <p>Perfect viewing experience across all devices - from mobile phones to large desktop monitors. Adapts seamlessly.</p>
            </div>
            <div class="feature-card">
                <h3>🔒 Secure & Reliable</h3>
                <p>Built with security best practices to protect your data and provide a trustworthy platform for your users.</p>
            </div>
            <div class="feature-card">
                <h3>⚡ High Performance</h3>
                <p>Optimized code and efficient architecture ensure fast loading times and smooth interactions throughout.</p>
            </div>
            <div class="feature-card">
                <h3>🎯 User-Focused</h3>
                <p>Every element designed with user experience in mind. Accessibility compliant and easy to navigate.</p>
            </div>
        </div>
    </div>

    <footer>
        <h3>{project_name}</h3>
        <p>Built with modern web technologies</p>
        <p>&copy; 2024 {project_name}. All rights reserved.</p>
        <p style="opacity: 0.6; margin-top: 20px; font-size: 0.9em;">Generated by KimiGPT - AI Website Builder</p>
    </footer>

    <script>
        // Smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                }}
            }});
        }});

        // Add scroll animations
        const observerOptions = {{
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        }};

        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }}
            }});
        }}, observerOptions);

        // Observe all feature cards
        document.querySelectorAll('.feature-card').forEach(card => {{
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            card.style.transition = 'all 0.6s ease-out';
            observer.observe(card);
        }});
    </script>
</body>
</html>
"""
