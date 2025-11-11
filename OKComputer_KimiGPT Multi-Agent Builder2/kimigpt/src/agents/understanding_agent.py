import re
from typing import Dict, Any, List
from src.agents.base_agent import BaseAgent
from src.api.api_manager import api_manager

class UnderstandingAgent(BaseAgent):
    def __init__(self):
        super().__init__("Understanding Agent", "understanding_001")
        self.website_types = {
            'portfolio': ['portfolio', 'personal', 'showcase', 'gallery'],
            'business': ['business', 'company', 'corporate', 'enterprise'],
            'ecommerce': ['store', 'shop', 'ecommerce', 'sell', 'products'],
            'blog': ['blog', 'news', 'articles', 'posts'],
            'landing': ['landing', 'promo', 'campaign', 'sales'],
            'restaurant': ['restaurant', 'cafe', 'food', 'menu'],
            'education': ['education', 'school', 'course', 'learning'],
            'healthcare': ['healthcare', 'medical', 'clinic', 'health'],
            'real_estate': ['real estate', 'property', 'housing', 'rental'],
            'technology': ['tech', 'software', 'app', 'startup']
        }
        
        self.style_keywords = {
            'modern': ['modern', 'contemporary', 'clean', 'minimalist'],
            'classic': ['classic', 'traditional', 'elegant', 'sophisticated'],
            'playful': ['playful', 'fun', 'colorful', 'creative'],
            'professional': ['professional', 'business', 'corporate', 'serious'],
            'artistic': ['artistic', 'creative', 'unique', 'bold'],
            'minimalist': ['minimalist', 'simple', 'clean', 'minimal']
        }
        
        self.color_schemes = {
            'blue': ['blue', 'navy', 'ocean', 'sky'],
            'green': ['green', 'nature', 'eco', 'forest'],
            'red': ['red', 'passion', 'energy', 'fire'],
            'purple': ['purple', 'royal', 'luxury', 'elegant'],
            'black': ['black', 'dark', 'elegant', 'sophisticated'],
            'white': ['white', 'light', 'clean', 'minimal'],
            'colorful': ['colorful', 'rainbow', 'vibrant', 'bright']
        }
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process user input and extract requirements"""
        self.update_status("processing")
        
        try:
            prompt = input_data.get('prompt', '')
            preferences = input_data.get('preferences', {})
            uploaded_files = input_data.get('files', [])
            
            # Extract basic requirements
            requirements = {
                'prompt': prompt,
                'project_type': self.detect_website_type(prompt),
                'style': self.detect_style(prompt),
                'color_scheme': self.detect_color_scheme(prompt),
                'features': self.extract_features(prompt),
                'pages': self.detect_pages(prompt),
                'target_audience': self.detect_target_audience(prompt),
                'complexity_level': self.detect_complexity(prompt),
                'responsive': True,  # Always responsive
                'seo_optimized': True,  # Always SEO optimized
                'accessibility': True  # Always accessible
            }
            
            # Merge user preferences
            if preferences:
                requirements.update(preferences)
            
            # Process uploaded files
            if uploaded_files:
                file_analysis = await self.analyze_uploaded_files(uploaded_files)
                requirements['file_analysis'] = file_analysis
            
            # Enhance with AI analysis
            enhanced_requirements = await self.enhance_with_ai(requirements)
            
            # Create structured task list
            task_list = self.create_task_list(enhanced_requirements)
            enhanced_requirements['tasks'] = task_list
            
            self.update_status("completed")
            
            return {
                'requirements': enhanced_requirements,
                'project_type': enhanced_requirements['project_type'],
                'complexity': enhanced_requirements['complexity_level'],
                'estimated_time': self.estimate_time(enhanced_requirements),
                'priority_features': self.prioritize_features(enhanced_requirements['features'])
            }
            
        except Exception as e:
            self.log_activity(f"Understanding failed: {str(e)}", "error")
            self.update_status("error")
            return {
                'error': str(e),
                'requirements': {
                    'project_type': 'general',
                    'style': 'modern',
                    'features': ['basic_layout', 'navigation', 'responsive'],
                    'complexity_level': 'simple'
                }
            }
    
    def detect_website_type(self, prompt: str) -> str:
        """Detect the type of website from prompt"""
        prompt_lower = prompt.lower()
        
        for website_type, keywords in self.website_types.items():
            if any(keyword in prompt_lower for keyword in keywords):
                return website_type
        
        return 'general'  # Default type
    
    def detect_style(self, prompt: str) -> str:
        """Detect design style preference"""
        prompt_lower = prompt.lower()
        
        style_scores = {}
        for style, keywords in self.style_keywords.items():
            score = sum(1 for keyword in keywords if keyword in prompt_lower)
            if score > 0:
                style_scores[style] = score
        
        if style_scores:
            return max(style_scores, key=style_scores.get)
        
        return 'modern'  # Default style
    
    def detect_color_scheme(self, prompt: str) -> str:
        """Detect preferred color scheme"""
        prompt_lower = prompt.lower()
        
        for scheme, keywords in self.color_schemes.items():
            if any(keyword in prompt_lower for keyword in keywords):
                return scheme
        
        return 'blue'  # Default color scheme
    
    def extract_features(self, prompt: str) -> List[str]:
        """Extract requested features from prompt"""
        features = []
        prompt_lower = prompt.lower()
        
        # Common features
        feature_keywords = {
            'contact_form': ['contact', 'form', 'message', 'email'],
            'gallery': ['gallery', 'portfolio', 'images', 'photos'],
            'blog': ['blog', 'news', 'articles', 'posts'],
            'ecommerce': ['shop', 'store', 'cart', 'buy', 'products'],
            'search': ['search', 'find', 'lookup'],
            'social_media': ['social', 'facebook', 'twitter', 'instagram'],
            'testimonials': ['testimonial', 'review', 'feedback'],
            'team': ['team', 'staff', 'people', 'about us'],
            'services': ['service', 'offer', 'what we do'],
            'pricing': ['price', 'cost', 'plan', 'subscription'],
            'booking': ['book', 'appointment', 'schedule', 'reserve'],
            'newsletter': ['newsletter', 'subscribe', 'email list'],
            'chat': ['chat', 'live support', 'help'],
            'multilingual': ['language', 'translate', 'multi-language'],
            'dark_mode': ['dark', 'night mode', 'dark theme'],
            'animations': ['animation', 'effect', 'transition', 'motion'],
            'video': ['video', 'youtube', 'vimeo'],
            'map': ['map', 'location', 'address', 'directions']
        }
        
        for feature, keywords in feature_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                features.append(feature)
        
        # Always include basic features
        basic_features = ['navigation', 'responsive', 'seo_optimized', 'accessible']
        features.extend(basic_features)
        
        return list(set(features))  # Remove duplicates
    
    def detect_pages(self, prompt: str) -> List[str]:
        """Detect required pages"""
        pages = ['home']  # Always have home page
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['about', 'company', 'story']):
            pages.append('about')
        
        if any(word in prompt_lower for word in ['contact', 'reach', 'get in touch']):
            pages.append('contact')
        
        if any(word in prompt_lower for word in ['service', 'product', 'what we offer']):
            pages.append('services')
        
        if any(word in prompt_lower for word in ['portfolio', 'work', 'projects']):
            pages.append('portfolio')
        
        if any(word in prompt_lower for word in ['blog', 'news', 'articles']):
            pages.append('blog')
        
        if any(word in prompt_lower for word in ['shop', 'store', 'products']):
            pages.extend(['shop', 'product'])
        
        return pages
    
    def detect_target_audience(self, prompt: str) -> str:
        """Detect target audience"""
        prompt_lower = prompt.lower()
        
        audiences = {
            'general': ['everyone', 'all ages', 'general public'],
            'business': ['business', 'professional', 'corporate', 'enterprise'],
            'youth': ['young', 'teen', 'student', 'youth'],
            'seniors': ['senior', 'elderly', 'older', 'retirement'],
            'parents': ['parent', 'family', 'children', 'kids'],
            'tech': ['tech', 'developer', 'programmer', 'geek'],
            'creative': ['creative', 'artist', 'designer', 'photographer'],
            'health': ['health', 'medical', 'patient', 'doctor'],
            'education': ['student', 'teacher', 'school', 'education'],
            'luxury': ['luxury', 'premium', 'high-end', 'exclusive']
        }
        
        for audience, keywords in audiences.items():
            if any(keyword in prompt_lower for keyword in keywords):
                return audience
        
        return 'general'
    
    def detect_complexity(self, prompt: str) -> str:
        """Detect complexity level"""
        prompt_lower = prompt.lower()
        
        # Simple indicators
        simple_indicators = ['simple', 'basic', 'minimal', 'easy', 'quick']
        complex_indicators = ['complex', 'advanced', 'detailed', 'sophisticated', 'feature-rich']
        
        simple_count = sum(1 for word in simple_indicators if word in prompt_lower)
        complex_count = sum(1 for word in complex_indicators if word in prompt_lower)
        
        if simple_count > complex_count:
            return 'simple'
        elif complex_count > simple_count:
            return 'advanced'
        else:
            return 'moderate'
    
    async def analyze_uploaded_files(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze uploaded files for additional context"""
        analysis = {
            'images': [],
            'documents': [],
            'videos': [],
            'audio': []
        }
        
        for file_info in files:
            file_type = file_info.get('type', '').split('/')[0]
            
            if file_type == 'image':
                analysis['images'].append({
                    'filename': file_info.get('filename'),
                    'size': file_info.get('size'),
                    'format': file_info.get('format'),
                    'extracted_colors': [],  # Will be filled by image agent
                    'content_analysis': ''   # Will be filled by image agent
                })
            elif file_type == 'application':
                analysis['documents'].append({
                    'filename': file_info.get('filename'),
                    'size': file_info.get('size'),
                    'format': file_info.get('format')
                })
            elif file_type == 'video':
                analysis['videos'].append({
                    'filename': file_info.get('filename'),
                    'size': file_info.get('size'),
                    'duration': file_info.get('duration')
                })
            elif file_type == 'audio':
                analysis['audio'].append({
                    'filename': file_info.get('filename'),
                    'size': file_info.get('size'),
                    'duration': file_info.get('duration')
                })
        
        return analysis
    
    async def enhance_with_ai(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI to enhance and validate requirements"""
        try:
            prompt = f"""
            Analyze these website requirements and suggest improvements:
            
            Project Type: {requirements['project_type']}
            Style: {requirements['style']}
            Color Scheme: {requirements['color_scheme']}
            Features: {', '.join(requirements['features'])}
            Pages: {', '.join(requirements['pages'])}
            Target Audience: {requirements['target_audience']}
            Complexity: {requirements['complexity_level']}
            
            Please provide:
            1. Suggested additional features based on project type
            2. Recommended color palette (hex codes)
            3. Typography suggestions
            4. Layout recommendations
            5. Any missing essential features
            
            Return as JSON format.
            """
            
            response = await api_manager.generate_text(prompt, "text")
            
            # Parse AI suggestions
            try:
                # Try to extract JSON from response
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response[json_start:json_end]
                    ai_suggestions = json.loads(json_str)
                    requirements['ai_suggestions'] = ai_suggestions
                else:
                    requirements['ai_suggestions'] = {'raw_response': response}
            except:
                requirements['ai_suggestions'] = {'raw_response': response}
            
            return requirements
            
        except Exception as e:
            self.log_activity(f"AI enhancement failed: {str(e)}", "warning")
            return requirements  # Return original if AI fails
    
    def create_task_list(self, requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create a structured task list for other agents"""
        tasks = []
        
        # Design tasks
        tasks.append({
            'agent': 'design',
            'task': 'create_design_system',
            'priority': 1,
            'description': 'Create design system with colors, typography, and layout',
            'dependencies': []
        })
        
        # Image processing tasks (if images uploaded)
        if requirements.get('file_analysis', {}).get('images'):
            tasks.append({
                'agent': 'image',
                'task': 'process_uploaded_images',
                'priority': 2,
                'description': 'Process and optimize uploaded images',
                'dependencies': ['create_design_system']
            })
        
        # Content generation tasks
        tasks.append({
            'agent': 'content',
            'task': 'generate_website_copy',
            'priority': 3,
            'description': 'Generate website copy and content',
            'dependencies': ['create_design_system']
        })
        
        # Code generation tasks
        tasks.append({
            'agent': 'code',
            'task': 'generate_html_css_js',
            'priority': 4,
            'description': 'Generate HTML, CSS, and JavaScript code',
            'dependencies': ['process_uploaded_images', 'generate_website_copy']
        })
        
        # QA tasks
        tasks.append({
            'agent': 'qa',
            'task': 'validate_generated_code',
            'priority': 5,
            'description': 'Validate code quality and accessibility',
            'dependencies': ['generate_html_css_js']
        })
        
        # Deployment tasks
        tasks.append({
            'agent': 'deployment',
            'task': 'package_for_deployment',
            'priority': 6,
            'description': 'Package files for deployment',
            'dependencies': ['validate_generated_code']
        })
        
        return tasks
    
    def estimate_time(self, requirements: Dict[str, Any]) -> str:
        """Estimate generation time based on complexity"""
        complexity = requirements.get('complexity_level', 'moderate')
        feature_count = len(requirements.get('features', []))
        page_count = len(requirements.get('pages', []))
        
        base_time = 10  # Base time in seconds
        
        if complexity == 'simple':
            complexity_multiplier = 1
        elif complexity == 'advanced':
            complexity_multiplier = 3
        else:
            complexity_multiplier = 2
        
        feature_time = feature_count * 2
        page_time = page_count * 3
        
        total_time = base_time + (complexity_multiplier * 5) + feature_time + page_time
        
        if total_time < 20:
            return f"{total_time} seconds"
        elif total_time < 60:
            return f"{total_time} seconds"
        else:
            minutes = total_time // 60
            seconds = total_time % 60
            return f"{minutes}m {seconds}s"
    
    def prioritize_features(self, features: List[str]) -> List[str]:
        """Prioritize features based on importance"""
        priority_order = [
            'navigation', 'responsive', 'seo_optimized', 'accessible',
            'contact_form', 'gallery', 'about_section', 'services',
            'testimonials', 'team', 'pricing', 'blog', 'ecommerce',
            'search', 'social_media', 'newsletter', 'chat',
            'multilingual', 'dark_mode', 'animations', 'video', 'map'
        ]
        
        # Sort features by priority
        prioritized = sorted(features, key=lambda x: 
            priority_order.index(x) if x in priority_order else len(priority_order))
        
        return prioritized