"""
QA Agent for WebsiteNow - FIXED VERSION
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

        # Perform basic validation checks
        validation_results = {
            'html_present': bool(html_code),
            'has_doctype': '<!DOCTYPE' in html_code or '<!doctype' in html_code,
            'has_html_tag': '<html' in html_code.lower(),
            'has_head': '<head>' in html_code.lower() or '<head ' in html_code.lower(),
            'has_body': '<body' in html_code.lower(),
            'has_title': '<title>' in html_code.lower(),
            'has_viewport': 'viewport' in html_code.lower(),
            'has_charset': 'charset' in html_code.lower(),
            'responsive': 'media' in html_code.lower() or '@media' in html_code.lower() or 'responsive' in html_code.lower(),
            'file_count': len(files),
            'code_length': len(html_code)
        }

        # Calculate score
        score = sum(1 for k, v in validation_results.items() if isinstance(v, bool) and v)
        total_checks = sum(1 for v in validation_results.values() if isinstance(v, bool))
        percentage = (score / total_checks * 100) if total_checks > 0 else 0

        # Determine quality level
        if percentage >= 90:
            quality_level = 'Excellent'
        elif percentage >= 75:
            quality_level = 'Good'
        elif percentage >= 60:
            quality_level = 'Fair'
        else:
            quality_level = 'Needs Improvement'

        return {
            'success': True,
            'validation': validation_results,
            'score': score,
            'total_checks': total_checks,
            'percentage': round(percentage, 1),
            'quality_level': quality_level,
            'recommendations': self._get_recommendations(validation_results)
        }

    def _get_recommendations(self, validation_results: Dict[str, Any]) -> list:
        """Get recommendations based on validation results"""
        recommendations = []

        if not validation_results.get('has_doctype'):
            recommendations.append("Add DOCTYPE declaration")

        if not validation_results.get('has_viewport'):
            recommendations.append("Add viewport meta tag for mobile responsiveness")

        if not validation_results.get('responsive'):
            recommendations.append("Consider adding responsive design features")

        if not validation_results.get('has_charset'):
            recommendations.append("Add character encoding declaration")

        if not recommendations:
            recommendations.append("Code quality is excellent! ✓")

        return recommendations
