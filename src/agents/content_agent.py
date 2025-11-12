"""
Content Agent for WebsiteNow - FIXED VERSION
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

        analysis = understanding_result.get('analysis', understanding_result.get('fallback_analysis', ''))
        project_name = understanding_result.get('project_name', 'My Website')

        prompt = f"""Generate engaging website content based on this:

{analysis}

Generate brief content for:
1. Hero headline and subheadline
2. About/intro section (2-3 sentences)
3. 3 key features/services (title + 1 sentence each)
4. Call to action text

Keep it professional and concise.
"""

        try:
            content = await self.api_manager.generate_text(prompt, 2000)

            return {
                'success': True,
                'content': content,
                'project_name': project_name
            }

        except Exception as e:
            # Fallback content
            return {
                'success': True,
                'content': f"""Hero: Welcome to {project_name}
Subheadline: Professional solutions for your needs

About: We provide high-quality services designed to help you succeed.

Features:
1. Quality Service - Dedicated to excellence
2. Fast Delivery - Quick and efficient results
3. Expert Team - Professional and experienced

Call to Action: Get Started Today""",
                'project_name': project_name,
                'note': 'Using fallback content due to API error'
            }
