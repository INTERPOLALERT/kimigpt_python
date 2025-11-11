"""
Design Agent for KimiGPT - FIXED VERSION
Creates design specifications and visual guidelines
"""

from typing import Dict, Any
from src.api.api_manager import APIManager


class DesignAgent:
    """Creates website design specifications"""

    def __init__(self, api_manager: APIManager):
        self.api_manager = api_manager

    async def create_design(self, understanding_result: Dict[str, Any], preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Create design specifications based on requirements"""

        analysis = understanding_result.get('analysis', understanding_result.get('fallback_analysis', ''))
        style = preferences.get('style', 'Modern & Clean')
        color_scheme = preferences.get('color_scheme', 'blue')

        prompt = f"""You are a web designer. Based on this analysis create design specs:

{analysis}

Style: {style}
Colors: {color_scheme}

Provide concise design specifications:
1. Color Palette (3-4 colors with hex codes)
2. Typography (font recommendations)
3. Layout Structure
4. Visual Style

Keep it brief and actionable.
"""

        try:
            design_spec = await self.api_manager.generate_text(prompt, 1500)

            return {
                'success': True,
                'design_specification': design_spec,
                'style': style,
                'color_scheme': color_scheme
            }

        except Exception as e:
            # Fallback design
            return {
                'success': True,
                'design_specification': f"""Design Specifications:
- Style: {style}
- Colors: {color_scheme} theme with white background
- Typography: Modern sans-serif fonts
- Layout: Responsive grid layout with clear sections
- Visual Style: Clean, professional, user-friendly""",
                'style': style,
                'color_scheme': color_scheme,
                'note': 'Using fallback design due to API error'
            }
