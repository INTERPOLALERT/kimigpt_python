import re
import json
from typing import Dict, Any, List
from src.agents.base_agent import BaseAgent

class QAAgent(BaseAgent):
    def __init__(self):
        super().__init__("Quality Assurance Agent", "qa_001")
        
        # Accessibility guidelines (WCAG 2.1 AA)
        self.wcag_guidelines = {
            'color_contrast': {
                'normal_text': 4.5,
                'large_text': 3.0,
                'ui_components': 3.0
            },
            'focus_indicators': True,
            'alt_text_required': True,
            'semantic_html': True,
            'keyboard_navigation': True,
            'screen_reader_support': True
        }
        
        # Performance thresholds
        self.performance_thresholds = {
            'lighthouse_score': 85,
            'first_contentful_paint': 3000,  # milliseconds
            'largest_contentful_paint': 4000,  # milliseconds
            'first_input_delay': 100,  # milliseconds
            'cumulative_layout_shift': 0.1
        }
        
        # SEO requirements
        self.seo_requirements = {
            'title_length': {'min': 30, 'max': 60},
            'meta_description_length': {'min': 120, 'max': 160},
            'heading_structure': True,
            'alt_text_coverage': 0.9,  # 90% of images should have alt text
            'internal_links': 3,  # minimum number of internal links
            'structured_data': True
        }
        
        # Code quality standards
        self.code_standards = {
            'html_validation': True,
            'css_validation': True,
            'javascript_validation': True,
            'no_inline_styles': True,
            'semantic_html': True,
            'proper_nesting': True
        }
        
        # Security checks
        self.security_checks = {
            'no_inline_javascript': True,
            'secure_forms': True,
            'proper_headers': True,
            'input_sanitization': True,
            'xss_prevention': True
        }
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive quality assurance on generated website"""
        self.update_status("processing")
        
        try:
            code = input_data['code']
            design = input_data['design']
            requirements = input_data['requirements']
            
            # Initialize results
            qa_results = {
                'passed': True,
                'score': 0,
                'tests_performed': [],
                'issues': [],
                'warnings': [],
                'recommendations': []
            }
            
            # Perform accessibility testing
            accessibility_results = await self.test_accessibility(code, design)
            qa_results['tests_performed'].append('accessibility')
            qa_results['accessibility'] = accessibility_results
            
            if not accessibility_results['passed']:
                qa_results['passed'] = False
                qa_results['issues'].extend(accessibility_results['issues'])
            
            # Perform performance testing
            performance_results = await self.test_performance(code, design)
            qa_results['tests_performed'].append('performance')
            qa_results['performance'] = performance_results
            
            if not performance_results['passed']:
                qa_results['passed'] = False
                qa_results['issues'].extend(performance_results['issues'])
            
            # Perform SEO testing
            seo_results = await self.test_seo(code, requirements)
            qa_results['tests_performed'].append('seo')
            qa_results['seo'] = seo_results
            
            if not seo_results['passed']:
                qa_results['passed'] = False
                qa_results['issues'].extend(seo_results['issues'])
            
            # Perform code quality testing
            code_results = await self.test_code_quality(code)
            qa_results['tests_performed'].append('code_quality')
            qa_results['code_quality'] = code_results
            
            if not code_results['passed']:
                qa_results['passed'] = False
                qa_results['issues'].extend(code_results['issues'])
            
            # Perform security testing
            security_results = await self.test_security(code)
            qa_results['tests_performed'].append('security')
            qa_results['security'] = security_results
            
            if not security_results['passed']:
                qa_results['passed'] = False
                qa_results['issues'].extend(security_results['issues'])
            
            # Cross-browser compatibility testing
            compatibility_results = await self.test_compatibility(code)
            qa_results['tests_performed'].append('compatibility')
            qa_results['compatibility'] = compatibility_results
            
            if not compatibility_results['passed']:
                qa_results['passed'] = False
                qa_results['issues'].extend(compatibility_results['issues'])
            
            # Responsive design testing
            responsive_results = await self.test_responsive_design(code, design)
            qa_results['tests_performed'].append('responsive')
            qa_results['responsive'] = responsive_results
            
            if not responsive_results['passed']:
                qa_results['passed'] = False
                qa_results['issues'].extend(responsive_results['issues'])
            
            # Calculate overall score
            qa_results['score'] = self.calculate_overall_score(qa_results)
            
            # Generate recommendations
            qa_results['recommendations'] = self.generate_recommendations(qa_results)
            
            # Generate feedback for improvement
            qa_results['feedback'] = self.generate_feedback(qa_results)
            
            self.update_status("completed")
            
            return qa_results
            
        except Exception as e:
            self.log_activity(f"QA testing failed: {str(e)}", "error")
            self.update_status("error")
            return {
                'passed': False,
                'error': str(e),
                'score': 0,
                'tests_performed': [],
                'issues': [f'QA system error: {str(e)}'],
                'warnings': [],
                'recommendations': ['Please check the QA system configuration']
            }
    
    async def test_accessibility(self, code: Dict[str, str], design: Dict[str, Any]) -> Dict[str, Any]:
        """Test accessibility compliance"""
        results = {
            'passed': True,
            'score': 100,
            'issues': [],
            'warnings': [],
            'tests': {}
        }
        
        html_code = code.get('index.html', '')
        css_code = code.get('styles.css', '')
        
        # Test color contrast
        color_contrast_passed, contrast_issues = self.test_color_contrast(design)
        results['tests']['color_contrast'] = {
            'passed': color_contrast_passed,
            'score': 100 if color_contrast_passed else 70
        }
        
        if not color_contrast_passed:
            results['issues'].extend(contrast_issues)
            results['passed'] = False
            results['score'] -= 30
        
        # Test for alt text on images
        alt_text_passed, alt_text_issues = self.test_alt_text(html_code)
        results['tests']['alt_text'] = {
            'passed': alt_text_passed,
            'score': 100 if alt_text_passed else 80
        }
        
        if not alt_text_passed:
            results['issues'].extend(alt_text_issues)
            results['passed'] = False
            results['score'] -= 20
        
        # Test for semantic HTML
        semantic_html_passed, semantic_issues = self.test_semantic_html(html_code)
        results['tests']['semantic_html'] = {
            'passed': semantic_html_passed,
            'score': 100 if semantic_html_passed else 85
        }
        
        if not semantic_html_passed:
            results['issues'].extend(semantic_issues)
            results['passed'] = False
            results['score'] -= 15
        
        # Test for proper heading structure
        headings_passed, heading_issues = self.test_heading_structure(html_code)
        results['tests']['headings'] = {
            'passed': headings_passed,
            'score': 100 if headings_passed else 80
        }
        
        if not headings_passed:
            results['issues'].extend(heading_issues)
            results['passed'] = False
            results['score'] -= 20
        
        # Test for form accessibility
        forms_passed, form_issues = self.test_form_accessibility(html_code)
        results['tests']['forms'] = {
            'passed': forms_passed,
            'score': 100 if forms_passed else 90
        }
        
        if not forms_passed:
            results['issues'].extend(form_issues)
            results['passed'] = False
            results['score'] -= 10
        
        return results
    
    def test_color_contrast(self, design: Dict[str, Any]) -> tuple:
        """Test color contrast ratios"""
        issues = []
        passed = True
        
        colors = design.get('design_system', {}).get('colors', {})
        
        if not colors:
            issues.append('No color palette found in design specification')
            return False, issues
        
        # Test text on background contrast
        text_color = colors.get('text', '#000000')
        bg_color = colors.get('background', '#ffffff')
        
        contrast_ratio = self.calculate_contrast_ratio(text_color, bg_color)
        
        if contrast_ratio < self.wcag_guidelines['color_contrast']['normal_text']:
            issues.append(f'Text/background contrast ratio {contrast_ratio:.2f} is below WCAG AA standard (4.5:1)')
            passed = False
        
        # Test primary color on background
        primary_color = colors.get('primary', '#0000ff')
        primary_contrast = self.calculate_contrast_ratio(primary_color, bg_color)
        
        if primary_contrast < self.wcag_guidelines['color_contrast']['ui_components']:
            issues.append(f'Primary color/background contrast ratio {primary_contrast:.2f} is below WCAG standard (3:1)')
            passed = False
        
        return passed, issues
    
    def calculate_contrast_ratio(self, color1: str, color2: str) -> float:
        """Calculate contrast ratio between two colors"""
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        def get_luminance(rgb):
            r, g, b = [x / 255.0 for x in rgb]
            r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
            g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
            b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
            return 0.2126 * r + 0.7152 * g + 0.0722 * b
        
        try:
            rgb1 = hex_to_rgb(color1)
            rgb2 = hex_to_rgb(color2)
            
            l1 = get_luminance(rgb1)
            l2 = get_luminance(rgb2)
            
            lighter = max(l1, l2)
            darker = min(l1, l2)
            
            return (lighter + 0.05) / (darker + 0.05)
        except:
            return 1.0  # Default to poor contrast
    
    def test_alt_text(self, html_code: str) -> tuple:
        """Test for alt text on images"""
        issues = []
        passed = True
        
        # Find all img tags
        img_pattern = r'<img\s+[^>]*>'
        alt_pattern = r'alt\s*=\s*["\']([^"\']*)["\']'
        
        img_tags = re.findall(img_pattern, html_code, re.IGNORECASE)
        
        for img_tag in img_tags:
            alt_match = re.search(alt_pattern, img_tag, re.IGNORECASE)
            
            if not alt_match:
                issues.append(f'Image tag missing alt attribute: {img_tag[:50]}...')
                passed = False
            elif not alt_match.group(1).strip():
                issues.append(f'Image has empty alt text: {img_tag[:50]}...')
                passed = False
        
        return passed, issues
    
    def test_semantic_html(self, html_code: str) -> tuple:
        """Test for semantic HTML structure"""
        issues = []
        passed = True
        
        # Check for proper semantic elements
        semantic_elements = ['header', 'nav', 'main', 'section', 'article', 'aside', 'footer']
        
        for element in semantic_elements:
            if f'<{element}' not in html_code.lower():
                issues.append(f'Missing semantic element: {element}')
                passed = False
        
        # Check for div soup (too many divs without semantic meaning)
        div_count = len(re.findall(r'<div', html_code, re.IGNORECASE))
        semantic_count = sum(len(re.findall(f'<{elem}', html_code, re.IGNORECASE)) for elem in semantic_elements)
        
        if div_count > semantic_count * 3:
            issues.append('Excessive use of div elements - consider more semantic HTML')
            passed = False
        
        return passed, issues
    
    def test_heading_structure(self, html_code: str) -> tuple:
        """Test heading structure (h1-h6)"""
        issues = []
        passed = True
        
        # Check for h1 tag
        h1_tags = re.findall(r'<h1[^>]*>([^<]+)</h1>', html_code, re.IGNORECASE)
        
        if len(h1_tags) == 0:
            issues.append('No H1 tag found - every page should have one H1')
            passed = False
        elif len(h1_tags) > 1:
            issues.append(f'Multiple H1 tags found ({len(h1_tags)}) - should only have one')
            passed = False
        
        # Check heading hierarchy
        headings = re.findall(r'<h([1-6])[^>]*>([^<]+)</h\1>', html_code, re.IGNORECASE)
        
        prev_level = 0
        for level_str, text in headings:
            level = int(level_str)
            if level > prev_level + 1 and prev_level > 0:
                issues.append(f'Heading level skipped: H{prev_level} to H{level}')
                passed = False
            prev_level = level
        
        return passed, issues
    
    def test_form_accessibility(self, html_code: str) -> tuple:
        """Test form accessibility"""
        issues = []
        passed = True
        
        # Find forms
        form_pattern = r'<form[^>]*>(.*?)</form>'
        forms = re.findall(form_pattern, html_code, re.IGNORECASE | re.DOTALL)
        
        for form_content in forms:
            # Check for labels
            input_pattern = r'<input[^>]*>'
            inputs = re.findall(input_pattern, form_content, re.IGNORECASE)
            
            for input_tag in inputs:
                input_type = re.search(r'type\s*=\s*["\']([^"\']*)["\']', input_tag, re.IGNORECASE)
                
                if input_type and input_type.group(1) not in ['submit', 'button', 'hidden']:
                    # Check for associated label
                    input_id = re.search(r'id\s*=\s*["\']([^"\']*)["\']', input_tag, re.IGNORECASE)
                    
                    if input_id:
                        label_pattern = r'<label[^>]*for\s*=\s*["\']' + re.escape(input_id.group(1)) + r'["\'][^>]*>'
                        if not re.search(label_pattern, form_content, re.IGNORECASE):
                            issues.append(f'Input field missing associated label: {input_tag[:50]}...')
                            passed = False
                    else:
                        # Check for label wrapping input
                        if not re.search(r'<label[^>]*>.*?' + re.escape(input_tag), form_content, re.IGNORECASE):
                            issues.append(f'Input field missing label: {input_tag[:50]}...')
                            passed = False
        
        return passed, issues
    
    async def test_performance(self, code: Dict[str, str], design: Dict[str, Any]) -> Dict[str, Any]:
        """Test performance metrics"""
        results = {
            'passed': True,
            'score': 100,
            'issues': [],
            'warnings': [],
            'tests': {}
        }
        
        html_code = code.get('index.html', '')
        css_code = code.get('styles.css', '')
        js_code = code.get('main.js', '')
        
        # Test image optimization
        images_passed, image_issues = self.test_image_optimization(html_code, design)
        results['tests']['image_optimization'] = {
            'passed': images_passed,
            'score': 100 if images_passed else 75
        }
        
        if not images_passed:
            results['issues'].extend(image_issues)
            results['passed'] = False
            results['score'] -= 25
        
        # Test CSS optimization
        css_passed, css_issues = self.test_css_optimization(css_code)
        results['tests']['css_optimization'] = {
            'passed': css_passed,
            'score': 100 if css_passed else 85
        }
        
        if not css_passed:
            results['issues'].extend(css_issues)
            results['passed'] = False
            results['score'] -= 15
        
        # Test JavaScript optimization
        js_passed, js_issues = self.test_javascript_optimization(js_code)
        results['tests']['javascript_optimization'] = {
            'passed': js_passed,
            'score': 100 if js_passed else 80
        }
        
        if not js_passed:
            results['issues'].extend(js_issues)
            results['passed'] = False
            results['score'] -= 20
        
        # Test resource loading
        loading_passed, loading_issues = self.test_resource_loading(html_code)
        results['tests']['resource_loading'] = {
            'passed': loading_passed,
            'score': 100 if loading_passed else 90
        }
        
        if not loading_passed:
            results['issues'].extend(loading_issues)
            results['passed'] = False
            results['score'] -= 10
        
        return results
    
    def test_image_optimization(self, html_code: str, design: Dict[str, Any]) -> tuple:
        """Test image optimization"""
        issues = []
        passed = True
        
        # Find images
        img_pattern = r'<img\s+[^>]*>'
        img_tags = re.findall(img_pattern, html_code, re.IGNORECASE)
        
        for img_tag in img_tags:
            # Check for width and height attributes
            if 'width' not in img_tag.lower() or 'height' not in img_tag.lower():
                issues.append(f'Image missing width/height attributes: {img_tag[:50]}...')
                passed = False
            
            # Check for lazy loading
            if 'loading="lazy"' not in img_tag.lower():
                issues.append(f'Image missing lazy loading: {img_tag[:50]}...')
                passed = False
        
        return passed, issues
    
    def test_css_optimization(self, css_code: str) -> tuple:
        """Test CSS optimization"""
        issues = []
        passed = True
        
        # Check for unused CSS (simplified check)
        if len(css_code) > 50000:  # More than 50KB
            issues.append('CSS file is very large - consider optimizing unused styles')
            passed = False
        
        # Check for duplicate properties
        property_pattern = r'(\w+-)?\w+\s*:\s*[^;]+;'
        properties = re.findall(property_pattern, css_code)
        
        if len(properties) != len(set(properties)):
            issues.append('Duplicate CSS properties found')
            passed = False
        
        return passed, issues
    
    def test_javascript_optimization(self, js_code: str) -> tuple:
        """Test JavaScript optimization"""
        issues = []
        passed = True
        
        # Check for console.log statements (should be removed in production)
        if 'console.log' in js_code:
            issues.append('Console.log statements found - should be removed in production')
            passed = False
        
        # Check for large JavaScript files
        if len(js_code) > 100000:  # More than 100KB
            issues.append('JavaScript file is very large - consider code splitting')
            passed = False
        
        return passed, issues
    
    def test_resource_loading(self, html_code: str) -> tuple:
        """Test resource loading optimization"""
        issues = []
        passed = True
        
        # Check for preload hints
        if 'rel="preload"' not in html_code.lower():
            issues.append('Consider using preload hints for critical resources')
            passed = False
        
        # Check for defer/async on scripts
        script_pattern = r'<script\s+[^>]*src\s*=\s*["\'][^"\']*["\'][^>]*>'
        scripts = re.findall(script_pattern, html_code, re.IGNORECASE)
        
        for script in scripts:
            if 'defer' not in script.lower() and 'async' not in script.lower():
                issues.append(f'Script missing defer/async attribute: {script[:50]}...')
                passed = False
        
        return passed, issues
    
    async def test_seo(self, code: Dict[str, str], requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Test SEO optimization"""
        results = {
            'passed': True,
            'score': 100,
            'issues': [],
            'warnings': [],
            'tests': {}
        }
        
        html_code = code.get('index.html', '')
        
        # Test title tag
        title_passed, title_issues = self.test_title_tag(html_code)
        results['tests']['title'] = {
            'passed': title_passed,
            'score': 100 if title_passed else 80
        }
        
        if not title_passed:
            results['issues'].extend(title_issues)
            results['passed'] = False
            results['score'] -= 20
        
        # Test meta description
        meta_passed, meta_issues = self.test_meta_description(html_code)
        results['tests']['meta_description'] = {
            'passed': meta_passed,
            'score': 100 if meta_passed else 80
        }
        
        if not meta_passed:
            results['issues'].extend(meta_issues)
            results['passed'] = False
            results['score'] -= 20
        
        # Test heading structure for SEO
        seo_headings_passed, seo_heading_issues = self.test_seo_headings(html_code)
        results['tests']['seo_headings'] = {
            'passed': seo_headings_passed,
            'score': 100 if seo_headings_passed else 85
        }
        
        if not seo_headings_passed:
            results['issues'].extend(seo_heading_issues)
            results['passed'] = False
            results['score'] -= 15
        
        # Test internal linking
        links_passed, link_issues = self.test_internal_links(html_code)
        results['tests']['internal_links'] = {
            'passed': links_passed,
            'score': 100 if links_passed else 90
        }
        
        if not links_passed:
            results['issues'].extend(link_issues)
            results['passed'] = False
            results['score'] -= 10
        
        return results
    
    def test_title_tag(self, html_code: str) -> tuple:
        """Test title tag optimization"""
        issues = []
        passed = True
        
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', html_code, re.IGNORECASE)
        
        if not title_match:
            issues.append('Missing title tag')
            passed = False
        else:
            title = title_match.group(1).strip()
            title_length = len(title)
            
            if title_length < self.seo_requirements['title_length']['min']:
                issues.append(f'Title too short ({title_length} chars) - should be at least {self.seo_requirements["title_length"]["min"]} characters')
                passed = False
            elif title_length > self.seo_requirements['title_length']['max']:
                issues.append(f'Title too long ({title_length} chars) - should be at most {self.seo_requirements["title_length"]["max"]} characters')
                passed = False
        
        return passed, issues
    
    def test_meta_description(self, html_code: str) -> tuple:
        """Test meta description optimization"""
        issues = []
        passed = True
        
        meta_desc_match = re.search(r'<meta[^>]*name\s*=\s*["\']description["\'][^>]*content\s*=\s*["\']([^"\']*)["\'][^>]*>', html_code, re.IGNORECASE)
        
        if not meta_desc_match:
            issues.append('Missing meta description')
            passed = False
        else:
            description = meta_desc_match.group(1).strip()
            desc_length = len(description)
            
            if desc_length < self.seo_requirements['meta_description_length']['min']:
                issues.append(f'Meta description too short ({desc_length} chars)')
                passed = False
            elif desc_length > self.seo_requirements['meta_description_length']['max']:
                issues.append(f'Meta description too long ({desc_length} chars)')
                passed = False
        
        return passed, issues
    
    def test_seo_headings(self, html_code: str) -> tuple:
        """Test heading structure for SEO"""
        issues = []
        passed = True
        
        # Check for keywords in headings (simplified)
        headings = re.findall(r'<h[1-6][^>]*>([^<]+)</h[1-6]>', html_code, re.IGNORECASE)
        
        if len(headings) < 3:
            issues.append('Insufficient heading structure for SEO - should have multiple headings')
            passed = False
        
        return passed, issues
    
    def test_internal_links(self, html_code: str) -> tuple:
        """Test internal linking structure"""
        issues = []
        passed = True
        
        # Count internal links (simplified)
        internal_links = len(re.findall(r'<a[^>]*href\s*=\s*["\']#[^"\']*["\'][^>]*>', html_code, re.IGNORECASE))
        
        if internal_links < self.seo_requirements['internal_links']:
            issues.append(f'Insufficient internal links ({internal_links}) - should have at least {self.seo_requirements["internal_links"]}')
            passed = False
        
        return passed, issues
    
    async def test_code_quality(self, code: Dict[str, str]) -> Dict[str, Any]:
        """Test code quality"""
        results = {
            'passed': True,
            'score': 100,
            'issues': [],
            'warnings': [],
            'tests': {}
        }
        
        html_code = code.get('index.html', '')
        css_code = code.get('styles.css', '')
        js_code = code.get('main.js', '')
        
        # Test HTML structure
        html_passed, html_issues = self.test_html_structure(html_code)
        results['tests']['html_structure'] = {
            'passed': html_passed,
            'score': 100 if html_passed else 85
        }
        
        if not html_passed:
            results['issues'].extend(html_issues)
            results['passed'] = False
            results['score'] -= 15
        
        # Test CSS organization
        css_passed, css_issues = self.test_css_organization(css_code)
        results['tests']['css_organization'] = {
            'passed': css_passed,
            'score': 100 if css_passed else 90
        }
        
        if not css_passed:
            results['issues'].extend(css_issues)
            results['passed'] = False
            results['score'] -= 10
        
        # Test JavaScript quality
        js_passed, js_issues = self.test_javascript_quality(js_code)
        results['tests']['javascript_quality'] = {
            'passed': js_passed,
            'score': 100 if js_passed else 90
        }
        
        if not js_passed:
            results['issues'].extend(js_issues)
            results['passed'] = False
            results['score'] -= 10
        
        return results
    
    def test_html_structure(self, html_code: str) -> tuple:
        """Test HTML structure quality"""
        issues = []
        passed = True
        
        # Check for doctype
        if not re.search(r'<!DOCTYPE html>', html_code, re.IGNORECASE):
            issues.append('Missing DOCTYPE declaration')
            passed = False
        
        # Check for basic HTML structure
        if '<html' not in html_code.lower():
            issues.append('Missing HTML tag')
            passed = False
        
        if '<head>' not in html_code.lower():
            issues.append('Missing HEAD section')
            passed = False
        
        if '<body>' not in html_code.lower():
            issues.append('Missing BODY section')
            passed = False
        
        return passed, issues
    
    def test_css_organization(self, css_code: str) -> tuple:
        """Test CSS organization"""
        issues = []
        passed = True
        
        # Check for commented sections
        if css_code.count('/*') < 3:
            issues.append('Consider adding more comments to organize CSS')
            passed = False
        
        # Check for consistent formatting
        if '{' in css_code and not re.search(r'\{\s*\n', css_code):
            issues.append('Consider formatting CSS with line breaks for readability')
        
        return passed, issues
    
    def test_javascript_quality(self, js_code: str) -> tuple:
        """Test JavaScript code quality"""
        issues = []
        passed = True
        
        # Check for function documentation
        functions = re.findall(r'function\s+(\w+)', js_code)
        comments = js_code.count('//') + js_code.count('/*')
        
        if len(functions) > 3 and comments < len(functions):
            issues.append('Consider adding more comments to document JavaScript functions')
            passed = False
        
        return passed, issues
    
    async def test_security(self, code: Dict[str, str]) -> Dict[str, Any]:
        """Test security measures"""
        results = {
            'passed': True,
            'score': 100,
            'issues': [],
            'warnings': [],
            'tests': {}
        }
        
        html_code = code.get('index.html', '')
        js_code = code.get('main.js', '')
        
        # Test for inline JavaScript
        inline_js_passed, inline_js_issues = self.test_inline_javascript(html_code)
        results['tests']['inline_javascript'] = {
            'passed': inline_js_passed,
            'score': 100 if inline_js_passed else 90
        }
        
        if not inline_js_passed:
            results['issues'].extend(inline_js_issues)
            results['passed'] = False
            results['score'] -= 10
        
        # Test form security
        form_security_passed, form_security_issues = self.test_form_security(html_code, js_code)
        results['tests']['form_security'] = {
            'passed': form_security_passed,
            'score': 100 if form_security_passed else 85
        }
        
        if not form_security_passed:
            results['issues'].extend(form_security_issues)
            results['passed'] = False
            results['score'] -= 15
        
        return results
    
    def test_inline_javascript(self, html_code: str) -> tuple:
        """Test for inline JavaScript"""
        issues = []
        passed = True
        
        # Check for inline event handlers
        inline_events = ['onclick', 'onload', 'onmouseover', 'onmouseout', 'onsubmit']
        
        for event in inline_events:
            if event in html_code.lower():
                issues.append(f'Inline JavaScript event handler found: {event}')
                passed = False
        
        return passed, issues
    
    def test_form_security(self, html_code: str, js_code: str) -> tuple:
        """Test form security measures"""
        issues = []
        passed = True
        
        # Check for form validation
        if 'validate' not in js_code.lower() and 'validation' not in js_code.lower():
            issues.append('No form validation detected')
            passed = False
        
        return passed, issues
    
    async def test_compatibility(self, code: Dict[str, str]) -> Dict[str, Any]:
        """Test cross-browser compatibility"""
        results = {
            'passed': True,
            'score': 100,
            'issues': [],
            'warnings': [],
            'tests': {}
        }
        
        css_code = code.get('styles.css', '')
        js_code = code.get('main.js', '')
        
        # Test CSS compatibility
        css_compat_passed, css_compat_issues = self.test_css_compatibility(css_code)
        results['tests']['css_compatibility'] = {
            'passed': css_compat_passed,
            'score': 100 if css_compat_passed else 90
        }
        
        if not css_compat_passed:
            results['issues'].extend(css_compat_issues)
            results['passed'] = False
            results['score'] -= 10
        
        # Test JavaScript compatibility
        js_compat_passed, js_compat_issues = self.test_js_compatibility(js_code)
        results['tests']['js_compatibility'] = {
            'passed': js_compat_passed,
            'score': 100 if js_compat_passed else 90
        }
        
        if not js_compat_passed:
            results['issues'].extend(js_compat_issues)
            results['passed'] = False
            results['score'] -= 10
        
        return results
    
    def test_css_compatibility(self, css_code: str) -> tuple:
        """Test CSS compatibility"""
        issues = []
        passed = True
        
        # Check for modern CSS features without fallbacks
        modern_features = ['grid', 'flex', 'clamp', 'min', 'max']
        
        for feature in modern_features:
            if feature in css_code.lower():
                # Check for vendor prefixes or fallbacks (simplified)
                if f'-webkit-{feature}' not in css_code.lower() and feature == 'flex':
                    issues.append(f'CSS {feature} used without vendor prefixes - may affect older browsers')
        
        return passed, issues
    
    def test_js_compatibility(self, js_code: str) -> tuple:
        """Test JavaScript compatibility"""
        issues = []
        passed = True
        
        # Check for ES6+ features without transpilation
        es6_features = ['=>', 'let ', 'const ', 'class ', 'async ', 'await ']
        
        for feature in es6_features:
            if feature in js_code:
                issues.append(f'ES6+ feature detected ({feature.strip()}) - consider browser compatibility')
        
        return passed, issues
    
    async def test_responsive_design(self, code: Dict[str, str], design: Dict[str, Any]) -> Dict[str, Any]:
        """Test responsive design implementation"""
        results = {
            'passed': True,
            'score': 100,
            'issues': [],
            'warnings': [],
            'tests': {}
        }
        
        css_code = code.get('styles.css', '')
        html_code = code.get('index.html', '')
        
        # Test media queries
        media_queries_passed, media_issues = self.test_media_queries(css_code)
        results['tests']['media_queries'] = {
            'passed': media_queries_passed,
            'score': 100 if media_queries_passed else 80
        }
        
        if not media_queries_passed:
            results['issues'].extend(media_issues)
            results['passed'] = False
            results['score'] -= 20
        
        # Test viewport meta tag
        viewport_passed, viewport_issues = self.test_viewport(html_code)
        results['tests']['viewport'] = {
            'passed': viewport_passed,
            'score': 100 if viewport_passed else 100  # Critical issue
        }
        
        if not viewport_passed:
            results['issues'].extend(viewport_issues)
            results['passed'] = False
            results['score'] -= 100  # Critical for mobile
        
        return results
    
    def test_media_queries(self, css_code: str) -> tuple:
        """Test media queries for responsive design"""
        issues = []
        passed = True
        
        # Check for common breakpoints
        breakpoints = ['768px', '1024px', '1200px']
        found_breakpoints = []
        
        for breakpoint in breakpoints:
            if breakpoint in css_code:
                found_breakpoints.append(breakpoint)
        
        if len(found_breakpoints) < 2:
            issues.append(f'Insufficient media query breakpoints - only found {len(found_breakpoints)}')
            passed = False
        
        return passed, issues
    
    def test_viewport(self, html_code: str) -> tuple:
        """Test viewport meta tag"""
        issues = []
        passed = True
        
        if 'viewport' not in html_code.lower():
            issues.append('Missing viewport meta tag - critical for mobile responsiveness')
            passed = False
        
        return passed, issues
    
    def calculate_overall_score(self, qa_results: Dict[str, Any]) -> int:
        """Calculate overall QA score"""
        total_score = 0
        test_count = 0
        
        for test_name, test_result in qa_results.items():
            if isinstance(test_result, dict) and 'score' in test_result:
                total_score += test_result['score']
                test_count += 1
        
        return int(total_score / test_count) if test_count > 0 else 0
    
    def generate_recommendations(self, qa_results: Dict[str, Any]) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []
        
        # Accessibility recommendations
        if 'accessibility' in qa_results and not qa_results['accessibility']['passed']:
            recommendations.append('Improve color contrast to meet WCAG AA standards')
            recommendations.append('Add alt text to all images')
            recommendations.append('Ensure proper heading structure')
        
        # Performance recommendations
        if 'performance' in qa_results and not qa_results['performance']['passed']:
            recommendations.append('Optimize images for web delivery')
            recommendations.append('Minify CSS and JavaScript files')
            recommendations.append('Implement lazy loading for images')
        
        # SEO recommendations
        if 'seo' in qa_results and not qa_results['seo']['passed']:
            recommendations.append('Optimize title and meta description length')
            recommendations.append('Add more internal linking')
            recommendations.append('Implement structured data markup')
        
        # Security recommendations
        if 'security' in qa_results and not qa_results['security']['passed']:
            recommendations.append('Remove inline JavaScript')
            recommendations.append('Implement proper form validation')
            recommendations.append('Add security headers')
        
        return recommendations
    
    def generate_feedback(self, qa_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed feedback for improvement"""
        return {
            'summary': f"QA Score: {qa_results.get('score', 0)}/100",
            'status': 'PASS' if qa_results.get('passed', False) else 'FAIL',
            'tests_run': len(qa_results.get('tests_performed', [])),
            'critical_issues': len([issue for issue in qa_results.get('issues', []) if 'critical' in issue.lower()]),
            'improvement_areas': self.identify_improvement_areas(qa_results),
            'next_steps': self.generate_next_steps(qa_results)
        }
    
    def identify_improvement_areas(self, qa_results: Dict[str, Any]) -> List[str]:
        """Identify areas that need improvement"""
        areas = []
        
        for test_name, test_result in qa_results.items():
            if isinstance(test_result, dict) and not test_result.get('passed', True):
                areas.append(test_name.replace('_', ' ').title())
        
        return areas
    
    def generate_next_steps(self, qa_results: Dict[str, Any]) -> List[str]:
        """Generate next steps for improvement"""
        steps = []
        
        if not qa_results.get('passed', False):
            steps.append('Review and fix critical issues first')
            steps.append('Run accessibility tests with screen readers')
            steps.append('Test on multiple devices and browsers')
            steps.append('Validate HTML and CSS using W3C validators')
            steps.append('Perform user testing with diverse user groups')
        else:
            steps.append('Website meets quality standards')
            steps.append('Consider advanced optimizations for better performance')
            steps.append('Set up monitoring for ongoing quality assurance')
        
        return steps