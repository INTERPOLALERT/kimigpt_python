"""
Understanding Agent for KimiGPT - FIXED VERSION
Analyzes user input and extracts requirements
"""

from typing import Dict, Any
from src.api.api_manager import APIManager


class UnderstandingAgent:
    """Analyzes and understands user requirements"""

    def __init__(self, api_manager: APIManager):
        self.api_manager = api_manager

    async def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user input and extract requirements"""

        prompt_text = input_data.get('prompt', '').strip()

        if not prompt_text:
            return {
                'success': False,
                'error': 'No prompt provided',
                'raw_prompt': ''
            }

        prompt = f"""You are an expert website requirements analyst. Analyze this website request:

"{prompt_text}"

Project Name: {input_data.get('project_name', 'Website')}

Extract and provide a brief analysis covering:
1. Website Type (business/portfolio/e-commerce/blog/landing page)
2. Key Features Required
3. Main Sections Needed
4. Style and Tone

Keep it concise (2-3 sentences per point).
"""

        try:
            analysis = await self.api_manager.generate_text(prompt, 1000)

            return {
                'success': True,
                'raw_prompt': prompt_text,
                'analysis': analysis,
                'project_name': input_data.get('project_name', 'Website'),
                'preferences': input_data.get('preferences', {})
            }

        except Exception as e:
            return {
                'success': False,
                'error': f"Understanding analysis failed: {str(e)}",
                'raw_prompt': prompt_text,
                'fallback_analysis': f"User wants to create a {input_data.get('preferences', {}).get('style', 'modern')} website."
            }
