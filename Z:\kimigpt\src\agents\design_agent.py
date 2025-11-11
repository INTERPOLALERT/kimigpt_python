"""
Design Agent for KimiGPT
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

        analysis = understanding_result.get('analysis', '')
        style = preferences.get('style', 'modern')
        color_scheme = preferences.get('color_scheme', 'blue')

        prompt = f"""
You are an expert web designer. Based on the following requirements analysis, create detailed design specifications.

Requirements Analysis:
{analysis}

User Preferences:
- Style: {style}
- Color Scheme: {color_scheme}

Create a comprehensive design specification including:
1. Color Palette (primary, secondary, accent colors with hex codes)
2. Typography (fonts for headings, body text, sizes)
3. Layout Structure (sections, grid layout, spacing)
4. Visual Style Guidelines
5. Component Designs (buttons, cards, forms)
6. Responsive Design Considerations
7. Animation and Interaction Ideas

Provide specific, actionable design specifications that a developer can implement.
"""

        try:
            design_spec = await self.api_manager.generate_text(prompt, "text", 3000)

            return {
                'success': True,
                'design_specification': design_spec,
                'style': style,
                'color_scheme': color_scheme
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
