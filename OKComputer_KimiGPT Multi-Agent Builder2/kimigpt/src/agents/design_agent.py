import json
import random
from typing import Dict, Any, List, Tuple
from src.agents.base_agent import BaseAgent
from src.api.api_manager import api_manager

class DesignAgent(BaseAgent):
    def __init__(self):
        super().__init__("Design Agent", "design_001")
        
        # Predefined color palettes
        self.color_palettes = {
            'modern_blue': {
                'primary': '#2563eb',
                'secondary': '#64748b',
                'accent': '#06b6d4',
                'background': '#ffffff',
                'text': '#1e293b',
                'success': '#10b981',
                'warning': '#f59e0b',
                'error': '#ef4444'
            },
            'warm_earth': {
                'primary': '#dc2626',
                'secondary': '#ea580c',
                'accent': '#d97706',
                'background': '#fef3c7',
                'text': '#92400e',
                'success': '#059669',
                'warning': '#d97706',
                'error': '#dc2626'
            },
            'minimalist_gray': {
                'primary': '#374151',
                'secondary': '#6b7280',
                'accent': '#9ca3af',
                'background': '#f9fafb',
                'text': '#111827',
                'success': '#059669',
                'warning': '#d97706',
                'error': '#dc2626'
            },
            'nature_green': {
                'primary': '#059669',
                'secondary': '#10b981',
                'accent': '#34d399',
                'background': '#ecfdf5',
                'text': '#064e3b',
                'success': '#059669',
                'warning': '#f59e0b',
                'error': '#ef4444'
            },
            'luxury_purple': {
                'primary': '#7c3aed',
                'secondary': '#8b5cf6',
                'accent': '#a78bfa',
                'background': '#faf5ff',
                'text': '#581c87',
                'success': '#059669',
                'warning': '#f59e0b',
                'error': '#ef4444'
            },
            'sunset_orange': {
                'primary': '#ea580c',
                'secondary': '#f97316',
                'accent': '#fb923c',
                'background': '#fff7ed',
                'text': '#9a3412',
                'success': '#16a34a',
                'warning': '#ca8a04',
                'error': '#dc2626'
            }
        }
        
        # Typography pairings
        self.typography_pairs = {
            'modern_sans': {
                'heading': 'Inter, system-ui, sans-serif',
                'body': 'Inter, system-ui, sans-serif',
                'accent': 'JetBrains Mono, monospace'
            },
            'classic_serif': {
                'heading': 'Playfair Display, serif',
                'body': 'Source Sans Pro, sans-serif',
                'accent': 'Fira Code, monospace'
            },
            'minimalist': {
                'heading': 'Helvetica Neue, sans-serif',
                'body': 'Helvetica Neue, sans-serif',
                'accent': 'Menlo, monospace'
            },
            'creative': {
                'heading': 'Poppins, sans-serif',
                'body': 'Open Sans, sans-serif',
                'accent': 'Space Mono, monospace'
            },
            'elegant': {
                'heading': 'Cormorant Garamond, serif',
                'body': 'Proza Libre, sans-serif',
                'accent': 'Courier Prime, monospace'
            }
        }
        
        # Layout templates
        self.layout_templates = {
            'hero_centered': {
                'type': 'hero_centered',
                'sections': ['hero', 'features', 'cta'],
                'grid_system': 'centered',
                'max_width': '1200px'
            },
            'sidebar_left': {
                'type': 'sidebar_left',
                'sections': ['sidebar', 'main', 'footer'],
                'grid_system': '12-column',
                'max_width': '1400px'
            },
            'fullscreen_hero': {
                'type': 'fullscreen_hero',
                'sections': ['hero_full', 'content', 'gallery'],
                'grid_system': 'fluid',
                'max_width': '100%'
            },
            'card_based': {
                'type': 'card_based',
                'sections': ['header', 'cards', 'footer'],
                'grid_system': 'css-grid',
                'max_width': '1200px'
            },
            'minimalist': {
                'type': 'minimalist',
                'sections': ['hero_minimal', 'content', 'footer'],
                'grid_system': 'centered',
                'max_width': '800px'
            }
        }
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create design system based on requirements"""
        self.update_status("processing")
        
        try:
            requirements = input_data.get('requirements', {})
            user_preferences = input_data.get('user_preferences', {})
            uploaded_images = input_data.get('uploaded_images', [])
            
            # Extract design preferences
            project_type = requirements.get('project_type', 'general')
            style = user_preferences.get('style', requirements.get('style', 'modern'))
            color_scheme = user_preferences.get('color_scheme', requirements.get('color_scheme', 'blue'))
            
            # Generate design system
            design_system = await self.create_design_system(
                project_type, style, color_scheme, uploaded_images
            )
            
            # Create layout specification
            layout_spec = await self.create_layout_spec(
                project_type, requirements.get('features', []), requirements.get('pages', ['home'])
            )
            
            # Generate responsive breakpoints
            breakpoints = self.generate_breakpoints()
            
            # Create component library
            components = await self.create_component_library(design_system, project_type)
            
            # Generate animation specifications
            animations = self.generate_animations(style)
            
            design_spec = {
                'design_system': design_system,
                'layout': layout_spec,
                'breakpoints': breakpoints,
                'components': components,
                'animations': animations,
                'accessibility': self.generate_accessibility_specs(),
                'performance': self.generate_performance_specs(),
                'metadata': {
                    'created_at': datetime.now().isoformat(),
                    'version': '1.0',
                    'style_guide': style,
                    'project_type': project_type
                }
            }
            
            self.update_status("completed")
            
            return {
                'success': True,
                'design_spec': design_spec,
                'color_palette': design_system['colors'],
                'typography': design_system['typography'],
                'layout_template': layout_spec['template'],
                'component_count': len(components),
                'accessibility_score': 95  # Target accessibility score
            }
            
        except Exception as e:
            self.log_activity(f"Design generation failed: {str(e)}", "error")
            self.update_status("error")
            return {
                'success': False,
                'error': str(e),
                'fallback_design': self.get_fallback_design()
            }
    
    async def create_design_system(self, project_type: str, style: str, 
                                 color_scheme: str, images: List[Dict]) -> Dict[str, Any]:
        """Create comprehensive design system"""
        
        # Select color palette
        colors = self.select_color_palette(color_scheme, style, images)
        
        # Select typography
        typography = self.select_typography(style, project_type)
        
        # Generate spacing system
        spacing = self.generate_spacing_system()
        
        # Create visual hierarchy
        hierarchy = self.create_visual_hierarchy(typography, colors)
        
        # Generate design tokens
        tokens = self.generate_design_tokens(colors, spacing, typography)
        
        return {
            'colors': colors,
            'typography': typography,
            'spacing': spacing,
            'hierarchy': hierarchy,
            'tokens': tokens,
            'shadows': self.generate_shadows(style),
            'borders': self.generate_borders(style),
            'transitions': self.generate_transitions()
        }
    
    def select_color_palette(self, color_scheme: str, style: str, images: List[Dict]) -> Dict[str, str]:
        """Select or generate color palette"""
        
        # Try to extract colors from images if available
        if images:
            # This would be implemented by the image agent
            # For now, use predefined palettes
            pass
        
        # Select from predefined palettes based on scheme and style
        if color_scheme in self.color_palettes:
            base_palette = self.color_palettes[color_scheme].copy()
        else:
            base_palette = self.color_palettes['modern_blue'].copy()
        
        # Adjust palette based on style
        if style == 'minimalist':
            # Reduce saturation for minimalist style
            base_palette = self.adjust_saturation(base_palette, 0.7)
        elif style == 'playful':
            # Increase saturation for playful style
            base_palette = self.adjust_saturation(base_palette, 1.3)
        
        # Add dark mode variants
        base_palette['dark_primary'] = self.darken_color(base_palette['primary'], 0.8)
        base_palette['dark_background'] = '#0f172a'  # Dark slate
        base_palette['dark_text'] = '#f8fafc'  # Light gray
        
        return base_palette
    
    def select_typography(self, style: str, project_type: str) -> Dict[str, str]:
        """Select typography based on style and project type"""
        
        # Special typography for specific project types
        if project_type == 'portfolio' and style == 'artistic':
            return self.typography_pairs['elegant']
        elif project_type == 'technology' and style == 'modern':
            return self.typography_pairs['modern_sans']
        elif style == 'minimalist':
            return self.typography_pairs['minimalist']
        elif style == 'playful':
            return self.typography_pairs['creative']
        else:
            return self.typography_pairs['modern_sans']
    
    def generate_spacing_system(self) -> Dict[str, str]:
        """Generate consistent spacing system"""
        return {
            'xs': '0.25rem',    # 4px
            'sm': '0.5rem',     # 8px
            'md': '1rem',       # 16px
            'lg': '1.5rem',     # 24px
            'xl': '2rem',       # 32px
            '2xl': '3rem',      # 48px
            '3xl': '4rem',      # 64px
            '4xl': '6rem',      # 96px
            'section': '5rem',  # 80px
            'container': '2rem' # 32px
        }
    
    def create_visual_hierarchy(self, typography: Dict[str, str], colors: Dict[str, str]) -> Dict[str, Any]:
        """Create visual hierarchy for text elements"""
        return {
            'h1': {
                'font_family': typography['heading'],
                'font_size': '3rem',  # 48px
                'font_weight': '700',
                'line_height': '1.2',
                'color': colors['text'],
                'margin_bottom': '1rem'
            },
            'h2': {
                'font_family': typography['heading'],
                'font_size': '2.25rem',  # 36px
                'font_weight': '600',
                'line_height': '1.3',
                'color': colors['text'],
                'margin_bottom': '0.75rem'
            },
            'h3': {
                'font_family': typography['heading'],
                'font_size': '1.875rem',  # 30px
                'font_weight': '600',
                'line_height': '1.4',
                'color': colors['text'],
                'margin_bottom': '0.5rem'
            },
            'h4': {
                'font_family': typography['heading'],
                'font_size': '1.5rem',  # 24px
                'font_weight': '500',
                'line_height': '1.4',
                'color': colors['text'],
                'margin_bottom': '0.5rem'
            },
            'body_large': {
                'font_family': typography['body'],
                'font_size': '1.125rem',  # 18px
                'font_weight': '400',
                'line_height': '1.6',
                'color': colors['text'],
                'margin_bottom': '1rem'
            },
            'body': {
                'font_family': typography['body'],
                'font_size': '1rem',  # 16px
                'font_weight': '400',
                'line_height': '1.6',
                'color': colors['text'],
                'margin_bottom': '1rem'
            },
            'body_small': {
                'font_family': typography['body'],
                'font_size': '0.875rem',  # 14px
                'font_weight': '400',
                'line_height': '1.5',
                'color': colors['secondary'],
                'margin_bottom': '0.75rem'
            },
            'caption': {
                'font_family': typography['body'],
                'font_size': '0.75rem',  # 12px
                'font_weight': '400',
                'line_height': '1.4',
                'color': colors['secondary'],
                'margin_bottom': '0.5rem'
            }
        }
    
    def generate_design_tokens(self, colors: Dict[str, str], spacing: Dict[str, str], 
                             typography: Dict[str, str]) -> Dict[str, Any]:
        """Generate design tokens for consistent theming"""
        return {
            'colors': colors,
            'spacing': spacing,
            'typography': typography,
            'border_radius': {
                'none': '0',
                'sm': '0.125rem',    # 2px
                'md': '0.375rem',    # 6px
                'lg': '0.5rem',      # 8px
                'xl': '0.75rem',     # 12px
                '2xl': '1rem',       # 16px
                'full': '9999px'     # Pill shape
            },
            'opacity': {
                '0': '0',
                '25': '0.25',
                '50': '0.5',
                '75': '0.75',
                '100': '1'
            }
        }
    
    def generate_shadows(self, style: str) -> Dict[str, str]:
        """Generate shadow styles"""
        if style == 'minimalist':
            return {
                'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
                'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
                'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1)'
            }
        else:
            return {
                'sm': '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
                'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
                'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
                '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)'
            }
    
    def generate_borders(self, style: str) -> Dict[str, str]:
        """Generate border styles"""
        return {
            'none': '0',
            'sm': '1px',
            'md': '2px',
            'lg': '4px',
            'xl': '8px'
        }
    
    def generate_transitions(self) -> Dict[str, str]:
        """Generate transition specifications"""
        return {
            'fast': '150ms ease-in-out',
            'normal': '300ms ease-in-out',
            'slow': '500ms ease-in-out',
            'slower': '700ms ease-in-out'
        }
    
    async def create_layout_spec(self, project_type: str, features: List[str], pages: List[str]) -> Dict[str, Any]:
        """Create layout specification"""
        
        # Select appropriate template
        template = self.select_template(project_type, features)
        
        # Generate navigation structure
        navigation = self.generate_navigation(pages, features)
        
        # Create responsive grid system
        grid_system = self.create_grid_system(template)
        
        # Generate section layouts
        sections = self.generate_sections(project_type, features)
        
        return {
            'template': template,
            'navigation': navigation,
            'grid_system': grid_system,
            'sections': sections,
            'responsive_behavior': self.generate_responsive_behavior(template),
            'accessibility_features': self.generate_accessibility_layout()
        }
    
    def select_template(self, project_type: str, features: List[str]) -> str:
        """Select appropriate layout template"""
        if 'ecommerce' in features or 'blog' in features:
            return 'sidebar_left'
        elif project_type == 'portfolio':
            return 'hero_centered'
        elif project_type == 'landing':
            return 'fullscreen_hero'
        elif project_type == 'business':
            return 'card_based'
        else:
            return 'hero_centered'  # Default
    
    def generate_navigation(self, pages: List[str], features: List[str]) -> Dict[str, Any]:
        """Generate navigation structure"""
        nav_items = []
        
        # Standard navigation items
        for page in pages:
            if page == 'home':
                nav_items.append({'name': 'Home', 'url': '#home', 'priority': 1})
            elif page == 'about':
                nav_items.append({'name': 'About', 'url': '#about', 'priority': 2})
            elif page == 'services':
                nav_items.append({'name': 'Services', 'url': '#services', 'priority': 3})
            elif page == 'portfolio':
                nav_items.append({'name': 'Portfolio', 'url': '#portfolio', 'priority': 3})
            elif page == 'blog':
                nav_items.append({'name': 'Blog', 'url': '#blog', 'priority': 4})
            elif page == 'contact':
                nav_items.append({'name': 'Contact', 'url': '#contact', 'priority': 5})
        
        # Add feature-based navigation
        if 'gallery' in features:
            nav_items.append({'name': 'Gallery', 'url': '#gallery', 'priority': 3})
        
        if 'pricing' in features:
            nav_items.append({'name': 'Pricing', 'url': '#pricing', 'priority': 4})
        
        # Sort by priority
        nav_items.sort(key=lambda x: x['priority'])
        
        return {
            'items': nav_items,
            'style': 'horizontal',  # or 'vertical', 'hamburger'
            'sticky': True,
            'transparent': True,
            'mobile_breakpoint': '768px'
        }
    
    def create_grid_system(self, template: str) -> Dict[str, Any]:
        """Create responsive grid system"""
        return {
            'type': 'css-grid',
            'columns': {
                'mobile': 1,
                'tablet': 2,
                'desktop': 3,
                'large': 4
            },
            'gaps': {
                'small': '1rem',
                'medium': '1.5rem',
                'large': '2rem'
            },
            'container': {
                'max_width': '1200px',
                'padding': '0 1rem'
            }
        }
    
    def generate_sections(self, project_type: str, features: List[str]) -> List[Dict[str, Any]]:
        """Generate section layouts"""
        sections = []
        
        # Hero section (always present)
        sections.append({
            'name': 'hero',
            'type': 'hero',
            'layout': 'centered',
            'height': '100vh',
            'content': ['heading', 'subheading', 'cta_button']
        })
        
        # Feature sections based on project type
        if project_type == 'business':
            sections.append({
                'name': 'services',
                'type': 'services',
                'layout': 'grid',
                'columns': 3,
                'content': ['service_cards']
            })
            
            sections.append({
                'name': 'about',
                'type': 'content',
                'layout': 'split',
                'content': ['text', 'image']
            })
        
        elif project_type == 'portfolio':
            sections.append({
                'name': 'portfolio',
                'type': 'gallery',
                'layout': 'masonry',
                'content': ['project_cards']
            })
            
            sections.append({
                'name': 'skills',
                'type': 'skills',
                'layout': 'progress_bars',
                'content': ['skill_items']
            })
        
        elif project_type == 'ecommerce':
            sections.append({
                'name': 'products',
                'type': 'products',
                'layout': 'grid',
                'columns': 4,
                'content': ['product_cards']
            })
            
            sections.append({
                'name': 'testimonials',
                'type': 'testimonials',
                'layout': 'carousel',
                'content': ['review_cards']
            })
        
        # Common sections
        if 'testimonials' in features:
            sections.append({
                'name': 'testimonials',
                'type': 'testimonials',
                'layout': 'carousel',
                'content': ['review_cards']
            })
        
        if 'team' in features:
            sections.append({
                'name': 'team',
                'type': 'team',
                'layout': 'grid',
                'columns': 4,
                'content': ['member_cards']
            })
        
        if 'pricing' in features:
            sections.append({
                'name': 'pricing',
                'type': 'pricing',
                'layout': 'comparison',
                'content': ['price_cards']
            })
        
        # Contact section (if contact form requested)
        if 'contact_form' in features:
            sections.append({
                'name': 'contact',
                'type': 'contact',
                'layout': 'split',
                'content': ['contact_form', 'contact_info']
            })
        
        # Footer section (always present)
        sections.append({
            'name': 'footer',
            'type': 'footer',
            'layout': 'multi_column',
            'content': ['links', 'social', 'copyright']
        })
        
        return sections
    
    def generate_breakpoints(self) -> Dict[str, str]:
        """Generate responsive breakpoints"""
        return {
            'xs': '0px',      # Mobile first
            'sm': '640px',    # Small tablets
            'md': '768px',    # Tablets
            'lg': '1024px',   # Small laptops
            'xl': '1280px',   # Desktops
            '2xl': '1536px'   # Large screens
        }
    
    def generate_responsive_behavior(self, template: str) -> Dict[str, Any]:
        """Generate responsive behavior specifications"""
        return {
            'mobile_first': True,
            'fluid_typography': True,
            'flexible_images': True,
            'responsive_tables': True,
            'adaptive_navigation': True,
            'touch_friendly': True,
            'performance_optimized': True
        }
    
    def generate_accessibility_layout(self) -> Dict[str, Any]:
        """Generate accessibility specifications"""
        return {
            'semantic_html': True,
            'aria_labels': True,
            'keyboard_navigation': True,
            'screen_reader_friendly': True,
            'color_contrast': 'AA',
            'focus_indicators': True,
            'skip_links': True,
            'alt_text': True
        }
    
    async def create_component_library(self, design_system: Dict[str, Any], project_type: str) -> List[Dict[str, Any]]:
        """Create component library specifications"""
        components = []
        
        # Basic components
        basic_components = [
            'button', 'input', 'card', 'modal', 'dropdown', 'tooltip',
            'accordion', 'tabs', 'carousel', 'progress_bar', 'badge',
            'alert', 'breadcrumb', 'pagination', 'navbar', 'footer'
        ]
        
        for component_name in basic_components:
            component = {
                'name': component_name,
                'variants': self.generate_component_variants(component_name, design_system),
                'responsive': True,
                'accessible': True,
                'animated': True
            }
            components.append(component)
        
        # Project-specific components
        if project_type == 'ecommerce':
            components.extend([
                {'name': 'product_card', 'type': 'ecommerce'},
                {'name': 'shopping_cart', 'type': 'ecommerce'},
                {'name': 'checkout_form', 'type': 'ecommerce'},
                {'name': 'product_filter', 'type': 'ecommerce'}
            ])
        
        elif project_type == 'portfolio':
            components.extend([
                {'name': 'project_card', 'type': 'portfolio'},
                {'name': 'skill_bar', 'type': 'portfolio'},
                {'name': 'timeline', 'type': 'portfolio'}
            ])
        
        return components
    
    def generate_component_variants(self, component: str, design_system: Dict[str, Any]) -> List[str]:
        """Generate component variants"""
        if component == 'button':
            return ['primary', 'secondary', 'outline', 'ghost', 'danger', 'success']
        elif component == 'card':
            return ['default', 'elevated', 'outlined', 'filled']
        elif component == 'input':
            return ['default', 'filled', 'outlined', 'underlined']
        else:
            return ['default']
    
    def generate_animations(self, style: str) -> Dict[str, Any]:
        """Generate animation specifications"""
        if style == 'minimalist':
            return {
                'enabled': True,
                'duration': '300ms',
                'easing': 'ease-in-out',
                'effects': ['fade', 'slide', 'scale'],
                'scroll_animations': False,
                'hover_effects': True
            }
        else:
            return {
                'enabled': True,
                'duration': '500ms',
                'easing': 'ease-out',
                'effects': ['fade', 'slide', 'scale', 'rotate', 'bounce'],
                'scroll_animations': True,
                'hover_effects': True,
                'micro_interactions': True
            }
    
    def generate_accessibility_specs(self) -> Dict[str, Any]:
        """Generate accessibility specifications"""
        return {
            'wcag_level': 'AA',
            'color_contrast': {
                'normal_text': 4.5,
                'large_text': 3.0
            },
            'keyboard_navigation': True,
            'screen_reader_support': True,
            'focus_indicators': True,
            'skip_links': True,
            'alt_text_required': True,
            'semantic_html': True
        }
    
    def generate_performance_specs(self) -> Dict[str, Any]:
        """Generate performance specifications"""
        return {
            'target_lighthouse_score': 90,
            'first_contentful_paint': '< 2s',
            'largest_contentful_paint': '< 3s',
            'cumulative_layout_shift': '< 0.1',
            'first_input_delay': '< 100ms',
            'image_optimization': True,
            'code_splitting': True,
            'lazy_loading': True
        }
    
    def adjust_saturation(self, palette: Dict[str, str], factor: float) -> Dict[str, str]:
        """Adjust color saturation (simplified implementation)"""
        # This would implement actual color manipulation
        # For now, return the original palette
        return palette
    
    def darken_color(self, color: str, factor: float) -> str:
        """Darken a color (simplified implementation)"""
        # This would implement actual color manipulation
        # For now, return a darker version
        return '#1e293b'  # Dark slate
    
    def get_fallback_design(self) -> Dict[str, Any]:
        """Get fallback design system"""
        return {
            'design_system': {
                'colors': self.color_palettes['modern_blue'],
                'typography': self.typography_pairs['modern_sans'],
                'spacing': self.generate_spacing_system()
            },
            'layout': {
                'template': 'hero_centered',
                'navigation': {'items': []},
                'grid_system': self.create_grid_system('hero_centered')
            }
        }