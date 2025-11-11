import json
import re
from typing import Dict, Any, List
from datetime import datetime
from src.agents.base_agent import BaseAgent
from src.api.api_manager import api_manager

class ContentAgent(BaseAgent):
    def __init__(self):
        super().__init__("Content Generation Agent", "content_001")
        
        # Content templates for different website types
        self.content_templates = {
            'business': {
                'hero_title': 'Transform Your Business with Innovation',
                'hero_subtitle': 'We deliver cutting-edge solutions that drive growth and efficiency for modern enterprises.',
                'about_title': 'About Our Company',
                'about_content': 'Founded on principles of excellence and innovation, our company has been serving clients with dedication and expertise. We believe in creating value through technology and human-centered design.',
                'services': [
                    {'title': 'Strategic Consulting', 'description': 'Expert guidance to navigate complex business challenges and identify growth opportunities.'},
                    {'title': 'Digital Transformation', 'description': 'Modernize your operations with the latest technologies and digital workflows.'},
                    {'title': 'Performance Optimization', 'description': 'Enhance efficiency and productivity across all aspects of your business.'}
                ]
            },
            'portfolio': {
                'hero_title': 'Creative Portfolio',
                'hero_subtitle': 'Showcasing innovative designs and creative solutions that inspire and engage.',
                'about_title': 'About the Creator',
                'about_content': 'Passionate creator with years of experience in design and development. Dedicated to crafting unique experiences that leave lasting impressions.',
                'skills': [
                    {'name': 'UI/UX Design', 'level': 90},
                    {'name': 'Web Development', 'level': 85},
                    {'name': 'Brand Identity', 'level': 80},
                    {'name': 'Motion Graphics', 'level': 75}
                ]
            },
            'ecommerce': {
                'hero_title': 'Discover Amazing Products',
                'hero_subtitle': 'Curated collection of premium products designed to enhance your lifestyle.',
                'about_title': 'Our Story',
                'about_content': 'We believe in quality, sustainability, and exceptional customer service. Every product is carefully selected to meet our high standards.',
                'products': [
                    {'name': 'Premium Product A', 'price': '$99.99', 'description': 'High-quality product with exceptional features and modern design.'},
                    {'name': 'Essential Item B', 'price': '$49.99', 'description': 'Must-have item that combines functionality with style.'},
                    {'name': 'Luxury Product C', 'price': '$199.99', 'description': 'Premium offering for those who appreciate the finer things.'}
                ]
            },
            'blog': {
                'hero_title': 'Insights & Inspiration',
                'hero_subtitle': 'Thought-provoking articles and insights on topics that matter to you.',
                'about_title': 'About This Blog',
                'about_content': 'A platform for sharing knowledge, experiences, and perspectives on various topics. Join our community of curious minds.',
                'categories': ['Technology', 'Lifestyle', 'Business', 'Creativity']
            },
            'restaurant': {
                'hero_title': 'Exquisite Culinary Experience',
                'hero_subtitle': 'Where tradition meets innovation in every carefully crafted dish.',
                'about_title': 'Our Culinary Journey',
                'about_content': 'Dedicated to bringing you the finest culinary experiences using fresh, local ingredients and time-honored techniques.',
                'menu_categories': ['Appetizers', 'Main Courses', 'Desserts', 'Beverages']
            }
        }
        
        # SEO keywords for different industries
        self.seo_keywords = {
            'technology': ['software', 'technology', 'innovation', 'digital', 'solutions', 'development'],
            'healthcare': ['health', 'wellness', 'medical', 'care', 'treatment', 'professional'],
            'education': ['learning', 'education', 'training', 'courses', 'development', 'skills'],
            'finance': ['financial', 'investment', 'planning', 'wealth', 'management', 'advisory'],
            'creative': ['design', 'creative', 'art', 'portfolio', 'innovation', 'visual'],
            'retail': ['shopping', 'products', 'store', 'online', 'retail', 'quality'],
            'consulting': ['consulting', 'advisory', 'strategy', 'business', 'expertise', 'solutions']
        }
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate website content based on requirements and design"""
        self.update_status("processing")
        
        try:
            requirements = input_data['requirements']
            design_spec = input_data.get('design_spec', {})
            project_type = requirements.get('project_type', 'general')
            
            # Generate main content sections
            hero_content = await self.generate_hero_content(requirements, design_spec)
            about_content = await self.generate_about_content(requirements, design_spec)
            feature_content = await self.generate_feature_content(requirements, design_spec)
            
            # Generate additional sections based on project type
            additional_sections = await self.generate_additional_sections(project_type, requirements)
            
            # Generate SEO content
            seo_content = await self.generate_seo_content(requirements, design_spec)
            
            # Generate footer content
            footer_content = await self.generate_footer_content(requirements)
            
            # Create content structure
            content_structure = {
                'hero': hero_content,
                'about': about_content,
                'features': feature_content,
                'additional_sections': additional_sections,
                'footer': footer_content,
                'seo': seo_content
            }
            
            # Generate page titles and meta descriptions
            page_content = await self.generate_page_content(project_type, requirements)
            content_structure['pages'] = page_content
            
            # Create content guidelines for consistency
            content_guidelines = self.generate_content_guidelines(requirements, design_spec)
            content_structure['guidelines'] = content_guidelines
            
            self.update_status("completed")
            
            return {
                'success': True,
                'content': content_structure,
                'word_count': self.calculate_word_count(content_structure),
                'readability_score': 85,  # Target readability score
                'seo_optimized': True,
                'content_sections': len(content_structure),
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.log_activity(f"Content generation failed: {str(e)}", "error")
            self.update_status("error")
            return {
                'success': False,
                'error': str(e),
                'fallback_content': self.get_fallback_content()
            }
    
    async def generate_hero_content(self, requirements: Dict[str, Any], design_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Generate hero section content"""
        project_type = requirements.get('project_type', 'general')
        style = design_spec.get('style', 'modern')
        
        # Get template content
        template_content = self.content_templates.get(project_type, self.content_templates['business'])
        
        # Enhance with AI if needed
        if requirements.get('ai_enhancement', True):
            prompt = f"""
            Generate compelling hero section content for a {project_type} website with {style} style.
            
            Requirements:
            - Project type: {project_type}
            - Target audience: {requirements.get('target_audience', 'general')}
            - Tone: {style}
            - Features: {', '.join(requirements.get('features', []))}
            
            Generate:
            1. A powerful headline (5-8 words)
            2. A compelling subtitle (10-15 words)
            3. 2-3 call-to-action button texts
            4. Optional tagline or supporting text
            
            Make it engaging, clear, and action-oriented.
            """
            
            try:
                ai_content = await api_manager.generate_text(prompt, "text")
                # Parse AI response and enhance template
                enhanced_content = self.parse_ai_content(ai_content, template_content)
            except:
                enhanced_content = template_content
        else:
            enhanced_content = template_content
        
        return {
            'title': enhanced_content.get('hero_title', 'Welcome to Our Website'),
            'subtitle': enhanced_content.get('hero_subtitle', 'We create amazing experiences'),
            'buttons': [
                {'text': 'Get Started', 'url': '#contact', 'type': 'primary'},
                {'text': 'Learn More', 'url': '#about', 'type': 'secondary'}
            ],
            'tagline': enhanced_content.get('tagline', ''),
            'background_text': enhanced_content.get('background_text', ''),
            'animations': {
                'title_animation': 'fadeInUp',
                'subtitle_animation': 'fadeInUp',
                'button_animation': 'fadeInUp'
            }
        }
    
    def parse_ai_content(self, ai_response: str, template_content: Dict[str, Any]) -> Dict[str, Any]:
        """Parse AI-generated content and merge with template"""
        try:
            # Try to extract structured content from AI response
            lines = ai_response.split('\n')
            enhanced = template_content.copy()
            
            for line in lines:
                line = line.strip()
                if line.lower().startswith('headline:') or line.lower().startswith('title:'):
                    enhanced['hero_title'] = line.split(':', 1)[1].strip()
                elif line.lower().startswith('subtitle:'):
                    enhanced['hero_subtitle'] = line.split(':', 1)[1].strip()
                elif line.lower().startswith('button') or 'cta' in line.lower():
                    # Extract button text
                    button_text = line.split(':', 1)[1].strip() if ':' in line else line
                    if 'button' not in enhanced:
                        enhanced['buttons'] = []
                    enhanced['buttons'].append({'text': button_text})
            
            return enhanced
            
        except Exception:
            return template_content
    
    async def generate_about_content(self, requirements: Dict[str, Any], design_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Generate about section content"""
        project_type = requirements.get('project_type', 'general')
        template_content = self.content_templates.get(project_type, self.content_templates['business'])
        
        about_content = {
            'title': template_content.get('about_title', 'About Us'),
            'content': template_content.get('about_content', 'We are dedicated to excellence and innovation.'),
            'mission_statement': f"Our mission is to deliver exceptional {project_type} solutions.",
            'vision_statement': f"To be the leading provider of {project_type} services.",
            'values': ['Quality', 'Innovation', 'Customer Focus', 'Integrity'],
            'stats': [
                {'number': '100+', 'label': 'Happy Clients'},
                {'number': '5+', 'label': 'Years Experience'},
                {'number': '500+', 'label': 'Projects Completed'}
            ],
            'team_intro': 'Meet the talented individuals who make it all possible.'
        }
        
        return about_content
    
    async def generate_feature_content(self, requirements: Dict[str, Any], design_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Generate features/services section content"""
        project_type = requirements.get('project_type', 'general')
        features = requirements.get('features', [])
        
        # Generate features based on requested features
        feature_items = []
        
        if 'ecommerce' in features:
            feature_items.extend([
                {'title': 'Secure Shopping', 'description': 'Safe and secure payment processing with multiple options.'},
                {'title': 'Fast Shipping', 'description': 'Quick delivery with real-time tracking and updates.'},
                {'title': 'Easy Returns', 'description': 'Hassle-free return policy for your peace of mind.'}
            ])
        
        if 'portfolio' in features or 'gallery' in features:
            feature_items.extend([
                {'title': 'Visual Showcase', 'description': 'Beautiful presentation of our work and achievements.'},
                {'title': 'Interactive Experience', 'description': 'Engaging and intuitive user interface design.'},
                {'title': 'Responsive Design', 'description': 'Perfect display on all devices and screen sizes.'}
            ])
        
        if 'contact_form' in features:
            feature_items.extend([
                {'title': '24/7 Support', 'description': 'Always available to help with your questions and concerns.'},
                {'title': 'Quick Response', 'description': 'Fast and efficient communication with our team.'},
                {'title': 'Personalized Service', 'description': 'Tailored solutions to meet your specific needs.'}
            ])
        
        # Add default features if none specified
        if not feature_items:
            template_content = self.content_templates.get(project_type, self.content_templates['business'])
            feature_items = template_content.get('services', [
                {'title': 'Professional Service', 'description': 'High-quality service delivered with expertise and care.'},
                {'title': 'Innovative Solutions', 'description': 'Cutting-edge approaches to solve your challenges.'},
                {'title': 'Reliable Support', 'description': 'Consistent and dependable support when you need it most.'}
            ])
        
        return {
            'section_title': 'Our Features',
            'section_subtitle': 'Discover what makes us different',
            'features': feature_items,
            'layout': 'grid',
            'columns': min(3, len(feature_items))
        }
    
    async def generate_additional_sections(self, project_type: str, requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate additional sections based on project type"""
        additional_sections = []
        features = requirements.get('features', [])
        
        # Services section for business websites
        if project_type == 'business':
            additional_sections.append({
                'name': 'services',
                'title': 'Our Services',
                'content': await self.generate_services_content(requirements)
            })
        
        # Portfolio/Gallery section
        if 'gallery' in features or 'portfolio' in features:
            additional_sections.append({
                'name': 'portfolio',
                'title': 'Our Work',
                'content': await self.generate_portfolio_content(requirements)
            })
        
        # Team section
        if 'team' in features:
            additional_sections.append({
                'name': 'team',
                'title': 'Our Team',
                'content': await self.generate_team_content(requirements)
            })
        
        # Testimonials section
        if 'testimonials' in features:
            additional_sections.append({
                'name': 'testimonials',
                'title': 'What Our Clients Say',
                'content': await self.generate_testimonials_content(requirements)
            })
        
        # Pricing section
        if 'pricing' in features:
            additional_sections.append({
                'name': 'pricing',
                'title': 'Pricing Plans',
                'content': await self.generate_pricing_content(requirements)
            })
        
        # Blog section
        if 'blog' in features:
            additional_sections.append({
                'name': 'blog',
                'title': 'Latest Articles',
                'content': await self.generate_blog_content(requirements)
            })
        
        # Contact section (if not main contact form)
        if 'contact' in features or 'contact_form' in features:
            additional_sections.append({
                'name': 'contact_info',
                'title': 'Contact Information',
                'content': await self.generate_contact_content(requirements)
            })
        
        return additional_sections
    
    async def generate_services_content(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate services content"""
        return {
            'services': [
                {
                    'title': 'Consultation',
                    'description': 'Expert advice and strategic planning',
                    'price': 'Starting at $99',
                    'features': ['Initial assessment', 'Strategy development', 'Implementation plan']
                },
                {
                    'title': 'Implementation',
                    'description': 'Full service delivery and execution',
                    'price': 'Starting at $299',
                    'features': ['Project management', 'Quality assurance', 'Ongoing support']
                },
                {
                    'title': 'Premium Package',
                    'description': 'Complete solution with premium features',
                    'price': 'Starting at $599',
                    'features': ['Everything in Implementation', 'Priority support', 'Advanced features']
                }
            ]
        }
    
    async def generate_portfolio_content(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate portfolio content"""
        return {
            'projects': [
                {
                    'title': 'Project Alpha',
                    'description': 'A groundbreaking solution that exceeded client expectations',
                    'category': 'Web Development',
                    'year': '2024'
                },
                {
                    'title': 'Project Beta',
                    'description': 'Innovative design that set new industry standards',
                    'category': 'UI/UX Design',
                    'year': '2024'
                },
                {
                    'title': 'Project Gamma',
                    'description': 'Complex challenge solved with creative thinking',
                    'category': 'Strategy',
                    'year': '2023'
                }
            ]
        }
    
    async def generate_team_content(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate team content"""
        return {
            'team_members': [
                {
                    'name': 'Alex Johnson',
                    'position': 'CEO & Founder',
                    'bio': 'Visionary leader with 15+ years of industry experience.',
                    'expertise': ['Leadership', 'Strategy', 'Innovation']
                },
                {
                    'name': 'Sarah Chen',
                    'position': 'Creative Director',
                    'bio': 'Award-winning designer passionate about user experience.',
                    'expertise': ['Design', 'UX/UI', 'Brand Strategy']
                },
                {
                    'name': 'Mike Rodriguez',
                    'position': 'Technical Lead',
                    'bio': 'Full-stack developer specializing in scalable solutions.',
                    'expertise': ['Development', 'Architecture', 'DevOps']
                }
            ]
        }
    
    async def generate_testimonials_content(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate testimonials content"""
        return {
            'testimonials': [
                {
                    'quote': 'Outstanding service and exceptional results. Highly recommended!',
                    'author': 'Jane Smith',
                    'company': 'Tech Startup Inc.',
                    'rating': 5
                },
                {
                    'quote': 'Professional, reliable, and delivered beyond our expectations.',
                    'author': 'Robert Davis',
                    'company': 'Creative Agency',
                    'rating': 5
                },
                {
                    'quote': 'The attention to detail and quality of work was impressive.',
                    'author': 'Maria Garcia',
                    'company': 'Local Business',
                    'rating': 5
                }
            ]
        }
    
    async def generate_pricing_content(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate pricing content"""
        return {
            'pricing_plans': [
                {
                    'name': 'Starter',
                    'price': '$29/month',
                    'description': 'Perfect for individuals and small projects',
                    'features': ['Basic features', 'Email support', '1GB storage'],
                    'popular': False
                },
                {
                    'name': 'Professional',
                    'price': '$99/month',
                    'description': 'Ideal for growing businesses',
                    'features': ['All Starter features', 'Priority support', '10GB storage', 'Advanced analytics'],
                    'popular': True
                },
                {
                    'name': 'Enterprise',
                    'price': '$299/month',
                    'description': 'For large organizations with complex needs',
                    'features': ['All Professional features', 'Dedicated support', 'Unlimited storage', 'Custom integrations'],
                    'popular': False
                }
            ]
        }
    
    async def generate_blog_content(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate blog content"""
        return {
            'articles': [
                {
                    'title': 'Getting Started: A Beginner\'s Guide',
                    'excerpt': 'Everything you need to know to get started with our services and make the most of your experience.',
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'read_time': '5 min read',
                    'category': 'Getting Started'
                },
                {
                    'title': 'Advanced Tips and Best Practices',
                    'excerpt': 'Take your skills to the next level with these advanced techniques and industry insights.',
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'read_time': '8 min read',
                    'category': 'Advanced'
                },
                {
                    'title': 'Industry Trends and Future Outlook',
                    'excerpt': 'Stay ahead of the curve with our analysis of current trends and future predictions.',
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'read_time': '6 min read',
                    'category': 'Trends'
                }
            ]
        }
    
    async def generate_contact_content(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate contact content"""
        return {
            'contact_info': {
                'email': 'hello@example.com',
                'phone': '+1 (555) 123-4567',
                'address': '123 Business Street, City, State 12345',
                'business_hours': 'Monday - Friday: 9:00 AM - 6:00 PM'
            },
            'social_links': [
                {'platform': 'LinkedIn', 'url': 'https://linkedin.com/company/example'},
                {'platform': 'Twitter', 'url': 'https://twitter.com/example'},
                {'platform': 'Facebook', 'url': 'https://facebook.com/example'}
            ],
            'contact_form_fields': [
                {'name': 'name', 'type': 'text', 'required': True, 'placeholder': 'Your Name'},
                {'name': 'email', 'type': 'email', 'required': True, 'placeholder': 'Your Email'},
                {'name': 'subject', 'type': 'text', 'required': True, 'placeholder': 'Subject'},
                {'name': 'message', 'type': 'textarea', 'required': True, 'placeholder': 'Your Message'}
            ]
        }
    
    async def generate_seo_content(self, requirements: Dict[str, Any], design_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Generate SEO-optimized content"""
        project_type = requirements.get('project_type', 'general')
        business_name = requirements.get('business_name', 'Our Company')
        
        # Generate title
        title = f"{business_name} - Professional {project_type.title()} Services"
        
        # Generate meta description
        meta_description = f"Leading {project_type} services by {business_name}. We deliver exceptional results with innovation, quality, and customer satisfaction. Get started today!"
        
        # Generate keywords
        base_keywords = self.seo_keywords.get(project_type, ['service', 'professional', 'quality'])
        custom_keywords = requirements.get('keywords', [])
        keywords = list(set(base_keywords + custom_keywords))[:15]  # Limit to 15 keywords
        
        # Generate Open Graph content
        og_content = {
            'title': title,
            'description': meta_description,
            'type': 'website',
            'url': 'https://example.com',
            'image': 'https://example.com/og-image.jpg'
        }
        
        # Generate structured data
        structured_data = {
            '@context': 'https://schema.org',
            '@type': 'Organization',
            'name': business_name,
            'description': meta_description,
            'url': 'https://example.com',
            'address': {
                '@type': 'PostalAddress',
                'addressCountry': 'US'
            }
        }
        
        return {
            'title': title,
            'meta_description': meta_description,
            'keywords': keywords,
            'og_content': og_content,
            'structured_data': structured_data,
            'canonical_url': 'https://example.com',
            'robots': 'index, follow'
        }
    
    async def generate_footer_content(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate footer content"""
        business_name = requirements.get('business_name', 'Our Company')
        project_type = requirements.get('project_type', 'general')
        
        return {
            'brand_name': business_name,
            'brand_description': f'Leading provider of {project_type} services with a commitment to excellence and innovation.',
            'quick_links': [
                {'text': 'About Us', 'url': '#about'},
                {'text': 'Services', 'url': '#services'},
                {'text': 'Contact', 'url': '#contact'},
                {'text': 'Privacy Policy', 'url': '/privacy'}
            ],
            'social_links': [
                {'platform': 'Facebook', 'url': '#', 'icon': 'facebook'},
                {'platform': 'Twitter', 'url': '#', 'icon': 'twitter'},
                {'platform': 'LinkedIn', 'url': '#', 'icon': 'linkedin'},
                {'platform': 'Instagram', 'url': '#', 'icon': 'instagram'}
            ],
            'copyright': f'© 2024 {business_name}. All rights reserved.',
            'additional_info': 'Built with passion and precision'
        }
    
    async def generate_page_content(self, project_type: str, requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate content for multiple pages"""
        pages = requirements.get('pages', ['home'])
        page_content = []
        
        for page in pages:
            if page == 'home':
                page_content.append({
                    'page': 'home',
                    'title': f"{requirements.get('business_name', 'Home')} - Welcome",
                    'content': 'Home page content'
                })
            elif page == 'about':
                page_content.append({
                    'page': 'about',
                    'title': f"About {requirements.get('business_name', 'Us')}",
                    'content': await self.generate_about_page_content(requirements)
                })
            elif page == 'services':
                page_content.append({
                    'page': 'services',
                    'title': 'Our Services',
                    'content': await self.generate_services_page_content(requirements)
                })
            elif page == 'contact':
                page_content.append({
                    'page': 'contact',
                    'title': 'Contact Us',
                    'content': await self.generate_contact_page_content(requirements)
                })
        
        return page_content
    
    async def generate_about_page_content(self, requirements: Dict[str, Any]) -> str:
        """Generate detailed about page content"""
        return """
        <h2>Our Story</h2>
        <p>Founded with a vision to transform the industry, we have been at the forefront of innovation for years. Our journey began with a simple belief: that exceptional service and cutting-edge solutions can create extraordinary results.</p>
        
        <h2>Our Mission</h2>
        <p>We are committed to delivering excellence in everything we do. Our mission is to exceed expectations, drive innovation, and create lasting value for our clients and community.</p>
        
        <h2>Our Values</h2>
        <ul>
            <li><strong>Excellence:</strong> We strive for the highest quality in all our work</li>
            <li><strong>Innovation:</strong> We embrace change and continuously seek better solutions</li>
            <li><strong>Integrity:</strong> We operate with honesty and transparency</li>
            <li><strong>Collaboration:</strong> We work together to achieve shared goals</li>
        </ul>
        """
    
    async def generate_services_page_content(self, requirements: Dict[str, Any]) -> str:
        """Generate detailed services page content"""
        return """
        <h2>Comprehensive Solutions</h2>
        <p>We offer a full range of services designed to meet your unique needs and exceed your expectations.</p>
        
        <h3>Service Categories</h3>
        <div class="services-grid">
            <div class="service-item">
                <h4>Consultation</h4>
                <p>Expert advice and strategic guidance to help you make informed decisions.</p>
            </div>
            <div class="service-item">
                <h4>Implementation</h4>
                <p>Professional execution and delivery of your projects with attention to detail.</p>
            </div>
            <div class="service-item">
                <h4>Support</h4>
                <p>Ongoing assistance and maintenance to ensure continued success.</p>
            </div>
        </div>
        """
    
    async def generate_contact_page_content(self, requirements: Dict[str, Any]) -> str:
        """Generate detailed contact page content"""
        return """
        <h2>Get In Touch</h2>
        <p>We'd love to hear from you. Whether you have a question about our services, pricing, or anything else, our team is ready to answer all your questions.</p>
        
        <h3>Contact Information</h3>
        <div class="contact-info">
            <p><strong>Email:</strong> hello@example.com</p>
            <p><strong>Phone:</strong> +1 (555) 123-4567</p>
            <p><strong>Address:</strong> 123 Business Street, City, State 12345</p>
            <p><strong>Business Hours:</strong> Monday - Friday, 9:00 AM - 6:00 PM</p>
        </div>
        """
    
    def generate_content_guidelines(self, requirements: Dict[str, Any], design_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Generate content guidelines for consistency"""
        return {
            'tone_of_voice': 'Professional yet approachable',
            'writing_style': 'Clear, concise, and engaging',
            'target_reading_level': '8th grade level',
            'sentence_length': '15-20 words average',
            'paragraph_length': '3-4 sentences',
            'key_messages': [
                'Quality and excellence in everything we do',
                'Customer-focused approach',
                'Innovation and continuous improvement'
            ],
            'avoid_words': ['cheap', 'basic', 'simple'],
            'preferred_words': ['premium', 'comprehensive', 'innovative'],
            'call_to_action_style': 'Direct but not pushy',
            'accessibility_notes': 'Use clear headings, short paragraphs, and descriptive link text'
        }
    
    def calculate_word_count(self, content_structure: Dict[str, Any]) -> Dict[str, int]:
        """Calculate word count for different content sections"""
        word_counts = {}
        total_words = 0
        
        def count_words_in_dict(data: Dict[str, Any]) -> int:
            count = 0
            for value in data.values():
                if isinstance(value, str):
                    count += len(value.split())
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, str):
                            count += len(item.split())
                        elif isinstance(item, dict):
                            count += count_words_in_dict(item)
                elif isinstance(value, dict):
                    count += count_words_in_dict(value)
            return count
        
        for section, content in content_structure.items():
            if isinstance(content, dict):
                section_words = count_words_in_dict(content)
                word_counts[section] = section_words
                total_words += section_words
        
        word_counts['total'] = total_words
        return word_counts
    
    def get_fallback_content(self) -> Dict[str, Any]:
        """Provide fallback content if generation fails"""
        return {
            'hero': {
                'title': 'Welcome to Our Website',
                'subtitle': 'We provide quality services',
                'buttons': [{'text': 'Contact Us', 'url': '#contact'}]
            },
            'about': {
                'title': 'About Us',
                'content': 'We are dedicated to providing excellent service.'
            },
            'features': {
                'features': [
                    {'title': 'Quality Service', 'description': 'Professional and reliable'},
                    {'title': 'Expert Team', 'description': 'Experienced professionals'},
                    {'title': 'Customer Focus', 'description': 'Your satisfaction is our priority'}
                ]
            },
            'note': 'Using fallback content due to generation error'
        }