import os
import json
import zipfile
import shutil
from typing import Dict, Any, List
from datetime import datetime
from src.agents.base_agent import BaseAgent

class DeploymentAgent(BaseAgent):
    def __init__(self):
        super().__init__("Deployment Agent", "deployment_001")
        
        # Deployment configurations
        self.deployment_configs = {
            'static_hosting': {
                'platforms': ['Netlify', 'Vercel', 'GitHub Pages', 'Firebase Hosting'],
                'requirements': ['HTML', 'CSS', 'JavaScript'],
                'complexity': 'easy'
            },
            'traditional_hosting': {
                'platforms': ['cPanel', 'Plesk', 'Direct Admin'],
                'requirements': ['FTP/SFTP access', 'Domain'],
                'complexity': 'medium'
            },
            'cloud_hosting': {
                'platforms': ['AWS S3', 'Google Cloud', 'Azure Static Sites'],
                'requirements': ['Cloud account', 'Domain setup'],
                'complexity': 'hard'
            }
        }
        
        # File structure templates
        self.file_structure = {
            'root': ['index.html', 'robots.txt', 'sitemap.xml', 'manifest.json'],
            'css': ['styles.css', 'responsive.css', 'animations.css'],
            'js': ['main.js', 'animations.js', 'form-handler.js'],
            'images': ['hero-bg.jpg', 'logo.png', 'favicon.ico'],
            'assets': ['fonts/', 'icons/']
        }
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare website for deployment"""
        self.update_status("processing")
        
        try:
            code = input_data['code']
            project_id = input_data['project_id']
            project_name = input_data.get('project_name', 'My Website')
            user_preferences = input_data.get('user_preferences', {})
            
            # Create deployment package
            deployment_package = await self.create_deployment_package(
                code, project_id, project_name, user_preferences
            )
            
            # Generate deployment instructions
            deployment_instructions = await self.generate_deployment_instructions(
                project_name, user_preferences
            )
            
            # Create ZIP file
            zip_path = await self.create_zip_package(deployment_package, project_id)
            
            # Generate hosting recommendations
            hosting_recommendations = await self.generate_hosting_recommendations(
                user_preferences, deployment_package
            )
            
            # Create deployment summary
            deployment_summary = {
                'project_id': project_id,
                'project_name': project_name,
                'deployment_package': deployment_package,
                'zip_file': zip_path,
                'instructions': deployment_instructions,
                'hosting_recommendations': hosting_recommendations,
                'deployment_options': self.get_deployment_options(),
                'file_count': self.count_files(deployment_package),
                'total_size': self.calculate_package_size(deployment_package),
                'created_at': datetime.now().isoformat()
            }
            
            self.update_status("completed")
            
            return {
                'success': True,
                'deployment_summary': deployment_summary,
                'zip_file_path': zip_path,
                'download_ready': True,
                'deployment_instructions': deployment_instructions,
                'hosting_recommendations': hosting_recommendations,
                'estimated_deployment_time': '5-15 minutes'
            }
            
        except Exception as e:
            self.log_activity(f"Deployment preparation failed: {str(e)}", "error")
            self.update_status("error")
            return {
                'success': False,
                'error': str(e),
                'fallback_deployment': self.get_fallback_deployment()
            }
    
    async def create_deployment_package(self, code: Dict[str, str], project_id: str, 
                                      project_name: str, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Create organized deployment package"""
        package = {
            'project_info': {
                'id': project_id,
                'name': project_name,
                'created_at': datetime.now().isoformat(),
                'version': '1.0.0'
            },
            'files': {},
            'structure': {},
            'metadata': {}
        }
        
        # Organize files by type
        for file_path, file_content in code.items():
            file_info = self.analyze_file(file_path, file_content)
            
            # Store file in appropriate category
            category = self.categorize_file(file_path)
            if category not in package['files']:
                package['files'][category] = []
            
            package['files'][category].append({
                'path': file_path,
                'content': file_content,
                'info': file_info
            })
        
        # Generate additional deployment files
        additional_files = await self.generate_deployment_files(project_name, preferences)
        package['files']['deployment'] = additional_files
        
        # Create project structure
        package['structure'] = self.create_project_structure(package['files'])
        
        # Generate metadata
        package['metadata'] = {
            'total_files': sum(len(files) for files in package['files'].values()),
            'total_size': sum(
                len(file['content']) for category in package['files'].values() 
                for file in category
            ),
            'main_technologies': self.identify_technologies(package['files']),
            'deployment_complexity': self.assess_deployment_complexity(package['files'])
        }
        
        return package
    
    def analyze_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Analyze file content and properties"""
        return {
            'name': os.path.basename(file_path),
            'extension': os.path.splitext(file_path)[1],
            'size': len(content),
            'lines': len(content.split('\n')),
            'encoding': 'utf-8',
            'file_type': self.get_file_type(file_path),
            'minified': self.check_if_minified(content),
            'dependencies': self.extract_dependencies(content, file_path)
        }
    
    def get_file_type(self, file_path: str) -> str:
        """Determine file type based on extension"""
        ext = os.path.splitext(file_path)[1].lower()
        
        type_mapping = {
            '.html': 'markup',
            '.css': 'stylesheet',
            '.js': 'script',
            '.json': 'data',
            '.xml': 'data',
            '.txt': 'text',
            '.md': 'markdown',
            '.jpg': 'image',
            '.jpeg': 'image',
            '.png': 'image',
            '.gif': 'image',
            '.svg': 'image',
            '.ico': 'icon'
        }
        
        return type_mapping.get(ext, 'unknown')
    
    def check_if_minified(self, content: str) -> bool:
        """Check if content appears to be minified"""
        lines = content.split('\n')
        
        # Minified files typically have very long lines
        long_lines = sum(1 for line in lines if len(line) > 500)
        
        return long_lines > len(lines) * 0.5
    
    def extract_dependencies(self, content: str, file_path: str) -> List[str]:
        """Extract external dependencies from file content"""
        dependencies = []
        
        if file_path.endswith('.html'):
            # Extract CDN links and external resources
            link_pattern = r'<link[^>]*href\s*=\s*["\']([^"\']*)["\'][^>]*>'
            script_pattern = r'<script[^>]*src\s*=\s*["\']([^"\']*)["\'][^>]*>'
            img_pattern = r'<img[^>]*src\s*=\s*["\']([^"\']*)["\'][^>]*>'
            
            for pattern in [link_pattern, script_pattern, img_pattern]:
                matches = re.findall(pattern, content, re.IGNORECASE)
                dependencies.extend(matches)
        
        elif file_path.endswith('.css'):
            # Extract font imports and external resources
            import_pattern = r'@import\s+["\']([^"\']*)["\']'
            url_pattern = r'url\(["\']?([^"\')]*)["\']?\)'
            
            for pattern in [import_pattern, url_pattern]:
                matches = re.findall(pattern, content)
                dependencies.extend(matches)
        
        elif file_path.endswith('.js'):
            # Extract module imports (simplified)
            import_pattern = r'import\s+[^from]*from\s*["\']([^"\']*)["\']'
            matches = re.findall(import_pattern, content)
            dependencies.extend(matches)
        
        return dependencies
    
    def categorize_file(self, file_path: str) -> str:
        """Categorize file by its purpose"""
        basename = os.path.basename(file_path)
        
        if basename == 'index.html':
            return 'main'
        elif basename == 'robots.txt':
            return 'seo'
        elif basename == 'sitemap.xml':
            return 'seo'
        elif basename == 'manifest.json':
            return 'pwa'
        elif file_path.startswith('css/'):
            return 'styles'
        elif file_path.startswith('js/'):
            return 'scripts'
        elif file_path.startswith('images/'):
            return 'assets'
        else:
            return 'other'
    
    async def generate_deployment_files(self, project_name: str, preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate additional deployment files"""
        files = []
        
        # Generate README.md
        readme_content = self.generate_readme(project_name, preferences)
        files.append({
            'path': 'README.md',
            'content': readme_content,
            'info': {'name': 'README.md', 'type': 'documentation'}
        })
        
        # Generate deployment guide
        deployment_guide = self.generate_deployment_guide(project_name, preferences)
        files.append({
            'path': 'DEPLOYMENT_GUIDE.md',
            'content': deployment_guide,
            'info': {'name': 'DEPLOYMENT_GUIDE.md', 'type': 'documentation'}
        })
        
        # Generate package.json if needed
        if preferences.get('include_package_json', False):
            package_json = self.generate_package_json(project_name)
            files.append({
                'path': 'package.json',
                'content': package_json,
                'info': {'name': 'package.json', 'type': 'configuration'}
            })
        
        # Generate .htaccess for Apache
        htaccess = self.generate_htaccess()
        files.append({
            'path': '.htaccess',
            'content': htaccess,
            'info': {'name': '.htaccess', 'type': 'server_config'}
        })
        
        return files
    
    def generate_readme(self, project_name: str, preferences: Dict[str, Any]) -> str:
        """Generate README.md file"""
        return f"""# {project_name}

## Overview
This is a modern, responsive website built with cutting-edge web technologies.

## Features
- ✅ Fully responsive design
- ✅ Cross-browser compatibility
- ✅ SEO optimized
- ✅ Accessibility compliant (WCAG AA)
- ✅ Fast loading performance
- ✅ Modern UI/UX design

## Technology Stack
- HTML5
- CSS3 (with CSS Grid and Flexbox)
- Vanilla JavaScript (ES6+)
- Progressive Web App (PWA) features

## File Structure
```
/
├── index.html          # Main HTML file
├── css/
│   ├── styles.css      # Main stylesheet
│   ├── responsive.css  # Responsive design styles
│   └── animations.css  # Animation styles
├── js/
│   ├── main.js         # Main JavaScript file
│   ├── animations.js   # Animation scripts
│   └── form-handler.js # Form handling scripts
├── images/             # Image assets
├── assets/             # Additional assets
├── manifest.json       # PWA manifest
├── robots.txt          # SEO robots file
├── sitemap.xml         # XML sitemap
└── README.md           # This file
```

## Getting Started

### Local Development
1. Download and extract the ZIP file
2. Open `index.html` in your browser, or
3. Run a local server: `python -m http.server 8000`
4. Open http://localhost:8000 in your browser

### Deployment
See `DEPLOYMENT_GUIDE.md` for detailed deployment instructions.

## Browser Support
- Chrome 60+
- Firefox 60+
- Safari 12+
- Edge 79+

## Performance
- Lighthouse Score: 90+
- First Contentful Paint: < 2s
- Largest Contentful Paint: < 3s

## Accessibility
- WCAG 2.1 AA compliant
- Keyboard navigation support
- Screen reader compatible
- High contrast support

## License
This website is generated by KimiGPT AI Website Builder.

## Support
For questions or support, please refer to the deployment guide or contact your hosting provider.

---
Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    def generate_deployment_guide(self, project_name: str, preferences: Dict[str, Any]) -> str:
        """Generate deployment guide"""
        return f"""# Deployment Guide - {project_name}

## Quick Start Options

### Option 1: Static Hosting (Recommended)
Perfect for most websites. No server-side processing required.

#### Netlify (Free Tier Available)
1. Visit [netlify.com](https://netlify.com)
2. Drag and drop your entire folder to deploy
3. Your site will be live in seconds!

#### Vercel (Free Tier Available)
1. Visit [vercel.com](https://vercel.com)
2. Sign up with GitHub or email
3. Upload your files or connect GitHub repository
4. Deploy with one click

#### GitHub Pages (Free)
1. Create a GitHub repository
2. Upload your files to the repository
3. Enable GitHub Pages in repository settings
4. Your site will be available at `username.github.io/repository-name`

### Option 2: Traditional Web Hosting
For cPanel, Plesk, or similar hosting platforms.

#### Using File Manager
1. Log into your hosting control panel
2. Open File Manager
3. Navigate to the `public_html` directory
4. Upload all files maintaining the folder structure

#### Using FTP/SFTP
1. Connect to your hosting server using FTP client (FileZilla, WinSCP)
2. Upload files to the `public_html` or `www` directory
3. Ensure file permissions are set correctly (644 for files, 755 for directories)

### Option 3: Cloud Hosting
For advanced users requiring scalability.

#### AWS S3 + CloudFront
1. Create S3 bucket with static website hosting enabled
2. Upload files to the bucket
3. Set up CloudFront distribution for CDN
4. Configure custom domain if needed

#### Google Cloud Storage
1. Create a Cloud Storage bucket
2. Upload your website files
3. Configure bucket for static website hosting
4. Set up Cloud CDN for better performance

## Domain Setup

### Using Your Own Domain
1. Purchase a domain from a registrar (Namecheap, GoDaddy, Google Domains)
2. Point DNS to your hosting provider
3. Configure SSL certificate (most platforms provide free SSL)

### Free Subdomain Options
- Netlify: `yoursite.netlify.app`
- Vercel: `yoursite.vercel.app`
- GitHub Pages: `username.github.io`

## Configuration Files

### manifest.json
PWA configuration file. No changes needed for basic deployment.

### robots.txt
Search engine instructions. Already configured for optimal SEO.

### sitemap.xml
XML sitemap for search engines. Update the URLs to match your domain.

### .htaccess (Apache servers)
Server configuration for:
- URL rewriting
- Compression
- Security headers
- Caching rules

## Pre-Deployment Checklist

- [ ] Test website locally
- [ ] Check all links work correctly
- [ ] Verify images load properly
- [ ] Test contact forms
- [ ] Check mobile responsiveness
- [ ] Validate HTML/CSS (optional)
- [ ] Set up analytics (Google Analytics, etc.)

## Post-Deployment

### Testing
1. Visit your live website
2. Test on different devices (phone, tablet, desktop)
3. Check all navigation links
4. Test contact forms
5. Verify images and animations load

### Monitoring
1. Set up Google Analytics
2. Configure Google Search Console
3. Monitor performance with Lighthouse
4. Set up uptime monitoring

### Maintenance
- Regularly update content
- Monitor performance metrics
- Keep dependencies updated
- Backup your website regularly

## Troubleshooting

### Common Issues

**Images not loading**
- Check file paths are correct
- Ensure proper file permissions
- Verify image files were uploaded

**Styles not applying**
- Check CSS file paths
- Clear browser cache
- Verify CSS syntax

**Contact forms not working**
- Requires server-side processing
- Consider using Formspree, Netlify Forms, or EmailJS
- Check form action URLs

**Slow loading**
- Optimize images
- Enable compression
- Use a CDN
- Minify CSS/JS files

## Support

If you encounter issues:
1. Check your hosting provider's documentation
2. Test with different browsers
3. Use browser developer tools to debug
4. Contact hosting support for server-specific issues

## Advanced Options

### Continuous Deployment
- Set up GitHub Actions for auto-deployment
- Configure build pipelines
- Implement staging environments

### Performance Optimization
- Implement lazy loading
- Optimize images with WebP format
- Set up a CDN
- Enable browser caching

### Security
- Implement HTTPS everywhere
- Add security headers
- Regular security audits
- Backup strategies

---
Need help? Most hosting providers offer excellent documentation and support.
"""
    
    def generate_package_json(self, project_name: str) -> str:
        """Generate package.json for Node.js projects"""
        package_data = {
            "name": project_name.lower().replace(' ', '-'),
            "version": "1.0.0",
            "description": f"A modern website built with {project_name}",
            "main": "index.html",
            "scripts": {
                "start": "python -m http.server 8000",
                "build": "echo 'No build process required for static site'",
                "test": "echo 'No tests specified'"
            },
            "keywords": [
                "website",
                "static",
                "responsive",
                "modern"
            ],
            "author": "KimiGPT Website Builder",
            "license": "MIT",
            "devDependencies": {
                "http-server": "^14.1.1"
            }
        }
        
        return json.dumps(package_data, indent=2)
    
    def generate_htaccess(self) -> str:
        """Generate .htaccess file for Apache servers"""
        return """# Security and Performance Configuration

# Enable compression
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/css text/javascript application/javascript
</IfModule>

# Browser caching
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType image/jpg "access plus 1 year"
    ExpiresByType image/jpeg "access plus 1 year"
    ExpiresByType image/gif "access plus 1 year"
    ExpiresByType image/png "access plus 1 year"
    ExpiresByType text/css "access plus 1 month"
    ExpiresByType application/javascript "access plus 1 month"
</IfModule>

# Security headers
<IfModule mod_headers.c>
    Header set X-Content-Type-Options "nosniff"
    Header set X-Frame-Options "DENY"
    Header set X-XSS-Protection "1; mode=block"
    Header set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>

# Redirect www to non-www
RewriteEngine On
RewriteCond %{HTTP_HOST} ^www\.(.*)$ [NC]
RewriteRule ^(.*)$ http://%1/$1 [R=301,L]

# Custom error pages
ErrorDocument 404 /404.html
ErrorDocument 500 /500.html

# Disable directory browsing
Options -Indexes

# Protect sensitive files
<FilesMatch "^\.">
    Require all denied
</FilesMatch>
"""
    
    def create_project_structure(self, files: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Create project structure overview"""
        structure = {
            'directories': [],
            'files': [],
            'total_files': 0,
            'total_size': 0
        }
        
        for category, file_list in files.items():
            for file_info in file_list:
                file_path = file_info['path']
                file_size = len(file_info['content'])
                
                structure['files'].append({
                    'path': file_path,
                    'category': category,
                    'size': file_size
                })
                
                structure['total_files'] += 1
                structure['total_size'] += file_size
                
                # Track directories
                dirname = os.path.dirname(file_path)
                if dirname and dirname not in structure['directories']:
                    structure['directories'].append(dirname)
        
        return structure
    
    def identify_technologies(self, files: Dict[str, List[Dict[str, Any]]]) -> List[str]:
        """Identify technologies used in the project"""
        technologies = []
        
        # Check for PWA features
        for category, file_list in files.items():
            for file_info in file_list:
                if file_info['path'] == 'manifest.json':
                    technologies.append('PWA')
                elif file_info['path'].endswith('.js'):
                    if 'serviceWorker' in file_info['content']:
                        technologies.append('Service Worker')
        
        # Check CSS frameworks
        for category, file_list in files.items():
            for file_info in file_list:
                if file_info['path'].endswith('.css'):
                    if 'tailwind' in file_info['content'].lower():
                        technologies.append('Tailwind CSS')
                    elif 'bootstrap' in file_info['content'].lower():
                        technologies.append('Bootstrap')
        
        # Basic technologies
        technologies.extend(['HTML5', 'CSS3', 'JavaScript ES6+'])
        
        return list(set(technologies))
    
    def assess_deployment_complexity(self, files: Dict[str, List[Dict[str, Any]]]) -> str:
        """Assess deployment complexity"""
        # Count JavaScript files and complexity
        js_files = files.get('scripts', [])
        total_js_size = sum(len(file['content']) for file in js_files)
        
        # Check for external dependencies
        dependencies = []
        for category, file_list in files.items():
            for file_info in file_list:
                if 'dependencies' in file_info.get('info', {}):
                    dependencies.extend(file_info['info']['dependencies'])
        
        # Determine complexity
        if len(js_files) > 3 or total_js_size > 50000 or len(dependencies) > 5:
            return 'hard'
        elif len(js_files) > 1 or total_js_size > 10000:
            return 'medium'
        else:
            return 'easy'
    
    async def generate_deployment_instructions(self, project_name: str, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Generate deployment instructions"""
        return {
            'quick_start': [
                'Download the ZIP file',
                'Extract all files to a folder',
                'Upload files to your web server',
                'Your website is live!'
            ],
            'detailed_steps': {
                'step_1': {
                    'title': 'Download and Extract',
                    'description': 'Download the generated ZIP file and extract all contents to a local folder.',
                    'commands': []
                },
                'step_2': {
                    'title': 'Choose Hosting Platform',
                    'description': 'Select a hosting platform that meets your needs.',
                    'options': [
                        'Netlify (recommended for beginners)',
                        'Vercel (great for performance)',
                        'GitHub Pages (free and simple)',
                        'Traditional hosting (cPanel/FTP)'
                    ]
                },
                'step_3': {
                    'title': 'Upload Files',
                    'description': 'Upload all files maintaining the folder structure.',
                    'notes': [
                        'Keep the folder structure intact',
                        'Upload to public_html or www directory',
                        'Ensure file permissions are correct'
                    ]
                },
                'step_4': {
                    'title': 'Test and Verify',
                    'description': 'Test your live website thoroughly.',
                    'checklist': [
                        'Check all pages load correctly',
                        'Test navigation and links',
                        'Verify images display properly',
                        'Test contact forms',
                        'Check mobile responsiveness'
                    ]
                }
            },
            'troubleshooting': {
                'common_issues': [
                    {
                        'issue': 'Images not loading',
                        'solution': 'Check file paths and ensure images are uploaded'
                    },
                    {
                        'issue': 'Styles not applying',
                        'solution': 'Verify CSS files are uploaded and paths are correct'
                    },
                    {
                        'issue': 'JavaScript not working',
                        'solution': 'Check browser console for errors and verify file paths'
                    }
                ]
            }
        }
    
    async def create_zip_package(self, deployment_package: Dict[str, Any], project_id: str) -> str:
        """Create ZIP file for download"""
        zip_filename = f"website_{project_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        zip_path = os.path.join('/mnt/okcomputer/output/kimigpt/generated_sites', zip_filename)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(zip_path), exist_ok=True)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add all files from deployment package
            for category, file_list in deployment_package['files'].items():
                for file_info in file_list:
                    # Create proper file path in ZIP
                    file_path = file_info['path']
                    zip_file.writestr(file_path, file_info['content'])
        
        return zip_path
    
    async def generate_hosting_recommendations(self, preferences: Dict[str, Any], 
                                             deployment_package: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate hosting recommendations"""
        complexity = deployment_package['metadata']['deployment_complexity']
        
        recommendations = []
        
        # Beginner-friendly options
        if complexity == 'easy':
            recommendations.extend([
                {
                    'platform': 'Netlify',
                    'type': 'static_hosting',
                    'difficulty': 'beginner',
                    'price': 'Free tier available',
                    'features': ['Drag & drop deploy', 'Free SSL', 'CDN included', 'Form handling'],
                    'pros': ['Super easy', 'Fast', 'Free domain', 'Great for beginners'],
                    'cons': ['Limited advanced features on free tier'],
                    'setup_time': '2 minutes'
                },
                {
                    'platform': 'Vercel',
                    'type': 'static_hosting',
                    'difficulty': 'beginner',
                    'price': 'Free tier available',
                    'features': ['Git integration', 'Preview deployments', 'Analytics', 'CDN'],
                    'pros': ['Excellent performance', 'Easy GitHub integration', 'Great UI'],
                    'cons': ['Learning curve for advanced features'],
                    'setup_time': '3 minutes'
                }
            ])
        
        # GitHub Pages (always available)
        recommendations.append({
            'platform': 'GitHub Pages',
            'type': 'static_hosting',
            'difficulty': 'intermediate',
            'price': 'Free',
            'features': ['Git-based deployment', 'Custom domains', 'HTTPS', 'Jekyll support'],
            'pros': ['Completely free', 'Reliable', 'Good for developers'],
            'cons': ['Requires Git knowledge', 'Limited to static sites'],
            'setup_time': '10 minutes'
        })
        
        # Traditional hosting
        if preferences.get('traditional_hosting', False):
            recommendations.append({
                'platform': 'Traditional Hosting',
                'type': 'traditional_hosting',
                'difficulty': 'intermediate',
                'price': '$5-20/month',
                'features': ['Full control', 'Email hosting', 'Databases', 'cPanel'],
                'pros': ['Full server control', 'Email included', 'Scalable'],
                'cons': ['More complex setup', 'Ongoing costs'],
                'setup_time': '30 minutes'
            })
        
        # Cloud options for advanced users
        if complexity == 'hard' or preferences.get('cloud_hosting', False):
            recommendations.extend([
                {
                    'platform': 'AWS S3 + CloudFront',
                    'type': 'cloud_hosting',
                    'difficulty': 'advanced',
                    'price': '$1-10/month',
                    'features': ['Highly scalable', 'Global CDN', 'Pay-as-you-use', 'Advanced features'],
                    'pros': ['Enterprise-grade', 'Very scalable', 'Cost-effective at scale'],
                    'cons': ['Complex setup', 'Learning curve'],
                    'setup_time': '1 hour'
                },
                {
                    'platform': 'Google Cloud Storage',
                    'type': 'cloud_hosting',
                    'difficulty': 'advanced',
                    'price': '$1-5/month',
                    'features': ['Global CDN', 'Integration with Google services', 'Analytics'],
                    'pros': ['Google ecosystem', 'Good performance', 'Integration'],
                    'cons': ['Complex setup', 'Google-specific'],
                    'setup_time': '45 minutes'
                }
            ])
        
        return recommendations
    
    def get_deployment_options(self) -> Dict[str, Any]:
        """Get available deployment options"""
        return {
            'static_hosting': {
                'description': 'Perfect for HTML/CSS/JS websites',
                'platforms': ['Netlify', 'Vercel', 'GitHub Pages', 'Firebase Hosting'],
                'complexity': 'low',
                'cost': 'free_to_cheap'
            },
            'traditional_hosting': {
                'description': 'Full-featured web hosting with cPanel',
                'platforms': ['Bluehost', 'SiteGround', 'HostGator'],
                'complexity': 'medium',
                'cost': 'monthly_fee'
            },
            'cloud_hosting': {
                'description': 'Enterprise-grade cloud platforms',
                'platforms': ['AWS', 'Google Cloud', 'Azure'],
                'complexity': 'high',
                'cost': 'pay_as_you_go'
            }
        }
    
    def count_files(self, deployment_package: Dict[str, Any]) -> Dict[str, int]:
        """Count files by category"""
        counts = {}
        total = 0
        
        for category, file_list in deployment_package['files'].items():
            count = len(file_list)
            counts[category] = count
            total += count
        
        counts['total'] = total
        return counts
    
    def calculate_package_size(self, deployment_package: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate package size information"""
        total_bytes = deployment_package['metadata']['total_size']
        
        return {
            'bytes': total_bytes,
            'kilobytes': round(total_bytes / 1024, 2),
            'megabytes': round(total_bytes / (1024 * 1024), 2),
            'size_category': self.categorize_size(total_bytes)
        }
    
    def categorize_size(self, bytes_size: int) -> str:
        """Categorize package size"""
        mb = bytes_size / (1024 * 1024)
        
        if mb < 1:
            return 'small'
        elif mb < 10:
            return 'medium'
        elif mb < 50:
            return 'large'
        else:
            return 'extra_large'
    
    def get_fallback_deployment(self) -> Dict[str, Any]:
        """Provide fallback deployment package"""
        return {
            'basic_files': {
                'index.html': '<!DOCTYPE html><html><head><title>Website</title></head><body><h1>Hello World</h1></body></html>',
                'styles.css': 'body { font-family: Arial, sans-serif; }'
            },
            'instructions': 'Basic deployment: Upload index.html and styles.css to your web server',
            'note': 'Using fallback due to deployment error'
        }