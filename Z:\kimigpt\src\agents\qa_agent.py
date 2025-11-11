"""
QA Agent for KimiGPT
Validates and tests generated code
"""

from typing import Dict, Any
from src.api.api_manager import APIManager


class QAAgent:
    """Quality assurance agent"""

    def __init__(self, api_manager: APIManager):
        self.api_manager = api_manager

    async def validate(self, code_result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate generated code"""

        files = code_result.get('files', {})
        html_code = files.get('index.html', '')

        if not html_code:
            return {
                'success': False,
                'error': 'No HTML code to validate'
            }

        # Perform basic validation
        validation_results = {
            'html_present': bool(html_code),
            'has_doctype': html_code.strip().startswith('<!DOCTYPE'),
            'has_head': '<head>' in html_code.lower(),
            'has_body': '<body>' in html_code.lower(),
            'has_title': '<title>' in html_code.lower(),
            'has_viewport': 'viewport' in html_code.lower(),
            'responsive': 'media' in html_code.lower() or '@media' in html_code.lower(),
            'file_count': len(files)
        }

        # Calculate score
        score = sum(1 for v in validation_results.values() if v is True)
        total_checks = len([v for v in validation_results.values() if isinstance(v, bool)])
        percentage = (score / total_checks * 100) if total_checks > 0 else 0

        return {
            'success': True,
            'validation': validation_results,
            'score': score,
            'total_checks': total_checks,
            'percentage': round(percentage, 1),
            'quality_level': 'Excellent' if percentage >= 90 else 'Good' if percentage >= 70 else 'Fair',
            'recommendations': self.get_recommendations(validation_results)
        }

    def get_recommendations(self, validation_results: Dict[str, Any]) -> list:
        """Get recommendations based on validation results"""
        recommendations = []

        if not validation_results.get('has_doctype'):
            recommendations.append("Add DOCTYPE declaration")

        if not validation_results.get('has_viewport'):
            recommendations.append("Add viewport meta tag for mobile responsiveness")

        if not validation_results.get('responsive'):
            recommendations.append("Add media queries for responsive design")

        if not recommendations:
            recommendations.append("Code quality is excellent!")

        return recommendations
