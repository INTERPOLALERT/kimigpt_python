"""
Understanding Agent for KimiGPT
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

        prompt = f"""
You are an expert website requirements analyst. Analyze the following website request and extract structured requirements.

User Request:
{input_data.get('prompt', '')}

Project Name: {input_data.get('project_name', 'Website')}

Extract and provide:
1. Website Type (e.g., business, portfolio, e-commerce, blog, landing page)
2. Target Audience
3. Key Features Required
4. Sections Needed (e.g., hero, about, services, contact, gallery)
5. Tone and Style (e.g., professional, creative, minimal, playful)
6. Color Preferences (from description)
7. Any Specific Technologies or Features Mentioned

Provide your analysis in a structured format.
"""

        try:
            analysis = await self.api_manager.generate_text(prompt, "text", 2000)

            return {
                'success': True,
                'raw_prompt': input_data.get('prompt', ''),
                'analysis': analysis,
                'files_uploaded': len(input_data.get('files', [])),
                'preferences': input_data.get('preferences', {})
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'raw_prompt': input_data.get('prompt', '')
            }
