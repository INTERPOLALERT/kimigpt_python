"""
Content Agent for KimiGPT
Generates website content (text, copy, descriptions)
"""

from typing import Dict, Any
from src.api.api_manager import APIManager


class ContentAgent:
    """Generates website content"""

    def __init__(self, api_manager: APIManager):
        self.api_manager = api_manager

    async def generate_content(self, understanding_result: Dict[str, Any], design_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate website content"""

        analysis = understanding_result.get('analysis', '')
        design_spec = design_result.get('design_specification', '')

        prompt = f"""
You are an expert copywriter. Generate engaging website content based on the following specifications.

Requirements:
{analysis}

Design Specifications:
{design_spec}

Generate content for:
1. Hero Section (headline, subheadline, call-to-action)
2. About/Introduction Section
3. Features/Services Section (3-6 items with titles and descriptions)
4. Testimonials (2-3 examples)
5. Call-to-Action Sections
6. Footer Content
7. Meta Title and Description for SEO

Make the content:
- Engaging and professional
- Appropriate for the target audience
- SEO-friendly
- Action-oriented
- Clear and concise

Provide the content in a structured format with clear labels for each section.
"""

        try:
            content = await self.api_manager.generate_text(prompt, "text", 4000)

            return {
                'success': True,
                'content': content,
                'sections': self.parse_content_sections(content)
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def parse_content_sections(self, content: str) -> Dict[str, Any]:
        """Parse content into structured sections"""
        # Simple parsing - can be enhanced
        return {
            'hero': {
                'headline': 'Welcome to Your Website',
                'subheadline': 'Professional solutions for your business',
                'cta': 'Get Started'
            },
            'about': 'About our services',
            'features': [],
            'testimonials': [],
            'footer': 'Copyright 2024'
        }
