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
        """Analyze user input and extract detailed requirements"""

        prompt_text = input_data.get('prompt', '').strip()

        if not prompt_text:
            return {
                'success': False,
                'error': 'No prompt provided',
                'raw_prompt': ''
            }

        prompt = f"""You are an expert website requirements analyst. Analyze this website request and extract SPECIFIC, DETAILED requirements:

USER REQUEST: "{prompt_text}"

Project Name: {input_data.get('project_name', 'Website')}

Provide a DETAILED analysis in this EXACT format:

WEBSITE TYPE: [business/portfolio/e-commerce/blog/landing page/SaaS/app]

KEY FEATURES (list specific features needed):
- Feature 1
- Feature 2
- Feature 3
(minimum 5 specific features)

REQUIRED COMPONENTS (be specific about what to build):
- Navigation with [specific menu items]
- Hero section with [specific CTA]
- [Specific forms needed - contact, signup, etc.]
- [Interactive elements - modals, tabs, accordions, carousels]
- [Any special functionality]

SECTIONS NEEDED (in order):
1. [Section name] - [What it contains]
2. [Section name] - [What it contains]
(minimum 5 sections)

INTERACTIVITY REQUIRED:
- [List JavaScript features needed: form validation, animations, etc.]
- [List user interactions: clicks, hovers, scrolls]

TARGET AUDIENCE: [Who is this for?]

STYLE & TONE: [Professional, playful, corporate, creative, etc.]

COLOR PREFERENCE: [Primary colors to use]

Be EXTREMELY specific and detailed. Think like a professional web developer planning a real project.
"""

        try:
            analysis = await self.api_manager.generate_text(prompt, 2500)

            return {
                'success': True,
                'raw_prompt': prompt_text,
                'analysis': analysis,
                'project_name': input_data.get('project_name', 'Website'),
                'preferences': input_data.get('preferences', {}),
                'detailed_requirements': self._extract_requirements(analysis)
            }

        except Exception as e:
            return {
                'success': False,
                'error': f"Understanding analysis failed: {str(e)}",
                'raw_prompt': prompt_text,
                'fallback_analysis': self._get_fallback_analysis(input_data)
            }

    def _extract_requirements(self, analysis: str) -> Dict[str, Any]:
        """Extract structured requirements from analysis"""
        requirements = {
            'features': [],
            'components': [],
            'sections': [],
            'interactivity': []
        }

        # Simple extraction - look for bullet points and lists
        lines = analysis.split('\n')
        current_section = None

        for line in lines:
            line = line.strip()
            if 'KEY FEATURES' in line.upper():
                current_section = 'features'
            elif 'REQUIRED COMPONENTS' in line.upper():
                current_section = 'components'
            elif 'SECTIONS NEEDED' in line.upper():
                current_section = 'sections'
            elif 'INTERACTIVITY' in line.upper():
                current_section = 'interactivity'
            elif line.startswith('-') or line.startswith('•') or (len(line) > 2 and line[0].isdigit() and line[1] == '.'):
                if current_section and line:
                    cleaned = line.lstrip('-•0123456789. ').strip()
                    if cleaned:
                        requirements[current_section].append(cleaned)

        return requirements

    def _get_fallback_analysis(self, input_data: Dict) -> str:
        """Provide comprehensive fallback analysis"""
        style = input_data.get('preferences', {}).get('style', 'modern')
        project_name = input_data.get('project_name', 'Website')

        return f"""WEBSITE TYPE: business landing page

KEY FEATURES:
- Responsive mobile-first design
- Contact form with email validation
- Image gallery or portfolio showcase
- Call-to-action buttons
- Social media integration
- Newsletter subscription

REQUIRED COMPONENTS:
- Navigation bar with smooth scrolling
- Hero section with headline and CTA button
- Contact form with validation (name, email, message)
- Footer with social links
- Modal popup for special offers

SECTIONS NEEDED:
1. Hero - Eye-catching headline with background image/gradient
2. About - Company/project information
3. Features - Key offerings in card layout
4. Gallery - Visual showcase
5. Contact - Form and contact information
6. Footer - Copyright and social links

INTERACTIVITY REQUIRED:
- Smooth scroll navigation
- Form validation with error messages
- Animated elements on scroll
- Hover effects on buttons and cards
- Modal open/close functionality

TARGET AUDIENCE: General users seeking {style} solutions

STYLE & TONE: {style.capitalize()}, professional, user-friendly

COLOR PREFERENCE: {style} color palette with gradients
"""
