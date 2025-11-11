import os
import json
from typing import Dict, Any, List
from PIL import Image, ImageEnhance, ImageFilter
import colorsys
from src.agents.base_agent import BaseAgent
from src.api.api_manager import api_manager

class ImageAgent(BaseAgent):
    def __init__(self):
        super().__init__("Image Processing Agent", "image_001")
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']
        self.max_dimensions = (2048, 2048)  # Maximum dimensions for optimization
        self.quality_settings = {
            'thumbnail': 70,
            'medium': 80,
            'large': 90,
            'original': 95
        }
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process uploaded images and extract design information"""
        self.update_status("processing")
        
        try:
            images = input_data.get('images', [])
            design_spec = input_data.get('design_spec', {})
            
            processed_images = []
            color_analysis = {}
            style_analysis = {}
            
            for image_info in images:
                # Process each image
                processed_image = await self.process_single_image(image_info, design_spec)
                processed_images.append(processed_image)
                
                # Extract color palette
                if processed_image.get('extracted_colors'):
                    color_analysis[processed_image['filename']] = processed_image['extracted_colors']
                
                # Analyze style
                style_info = await self.analyze_image_style(processed_image)
                style_analysis[processed_image['filename']] = style_info
            
            # Generate optimized image sets
            image_sets = await self.generate_image_sets(processed_images)
            
            # Create alt text for accessibility
            alt_texts = await self.generate_alt_texts(processed_images)
            
            # Update design spec with extracted colors
            updated_design_spec = self.update_design_spec(design_spec, color_analysis)
            
            self.update_status("completed")
            
            return {
                'success': True,
                'processed_images': processed_images,
                'image_sets': image_sets,
                'color_analysis': color_analysis,
                'style_analysis': style_analysis,
                'alt_texts': alt_texts,
                'updated_design_spec': updated_design_spec,
                'total_images': len(processed_images),
                'optimization_savings': self.calculate_optimization_savings(processed_images)
            }
            
        except Exception as e:
            self.log_activity(f"Image processing failed: {str(e)}", "error")
            self.update_status("error")
            return {
                'success': False,
                'error': str(e),
                'fallback_images': self.get_fallback_images()
            }
    
    async def process_single_image(self, image_info: Dict[str, Any], design_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single image"""
        filename = image_info.get('filename', 'unknown')
        file_path = image_info.get('path', '')
        
        try:
            # Open image
            with Image.open(file_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Get image information
                width, height = img.size
                format_type = img.format
                
                # Extract color palette
                extracted_colors = self.extract_color_palette(img)
                
                # Optimize image
                optimized_versions = await self.optimize_image(img, filename)
                
                # Generate image metadata
                metadata = {
                    'original_width': width,
                    'original_height': height,
                    'format': format_type,
                    'mode': img.mode,
                    'file_size': os.path.getsize(file_path),
                    'aspect_ratio': width / height
                }
                
                # Classify image content
                content_type = await self.classify_image_content(img)
                
                # Determine optimal placement
                placement_suggestions = self.suggest_image_placement(
                    content_type, width, height, design_spec
                )
                
                return {
                    'filename': filename,
                    'original_path': file_path,
                    'metadata': metadata,
                    'extracted_colors': extracted_colors,
                    'optimized_versions': optimized_versions,
                    'content_type': content_type,
                    'placement_suggestions': placement_suggestions,
                    'accessibility_info': {
                        'needs_alt_text': True,
                        'is_decorative': False,
                        'complexity': 'medium'
                    }
                }
                
        except Exception as e:
            self.log_activity(f"Failed to process image {filename}: {str(e)}", "warning")
            return {
                'filename': filename,
                'error': str(e),
                'fallback_data': self.get_fallback_image_data()
            }
    
    def extract_color_palette(self, img: Image.Image) -> List[Dict[str, Any]]:
        """Extract dominant colors from image"""
        try:
            # Resize image for faster processing
            small_img = img.resize((150, 150))
            
            # Get colors
            colors = small_img.getcolors(150 * 150)
            
            # Sort by frequency and get top colors
            colors.sort(key=lambda x: x[0], reverse=True)
            
            # Extract top 5 colors
            palette = []
            for count, color in colors[:5]:
                if isinstance(color, int):
                    # Handle grayscale images
                    rgb = (color, color, color)
                else:
                    rgb = color[:3]  # Ignore alpha if present
                
                hex_color = '#{:02x}{:02x}{:02x}'.format(*rgb)
                
                # Calculate HSL for better color analysis
                hsl = self.rgb_to_hsl(rgb)
                
                palette.append({
                    'hex': hex_color,
                    'rgb': rgb,
                    'hsl': hsl,
                    'frequency': count,
                    'percentage': (count / (150 * 150)) * 100
                })
            
            return palette
            
        except Exception as e:
            self.log_activity(f"Color extraction failed: {str(e)}", "warning")
            return []
    
    def rgb_to_hsl(self, rgb: tuple) -> Dict[str, float]:
        """Convert RGB to HSL color space"""
        r, g, b = [x / 255.0 for x in rgb]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        
        return {
            'h': round(h * 360, 2),
            's': round(s * 100, 2),
            'l': round(l * 100, 2)
        }
    
    async def optimize_image(self, img: Image.Image, filename: str) -> Dict[str, Any]:
        """Create optimized versions of the image"""
        optimized = {}
        
        # Get original dimensions
        orig_width, orig_height = img.size
        
        for size_name, quality in self.quality_settings.items():
            if size_name == 'original':
                # Keep original dimensions
                new_width, new_height = orig_width, orig_height
            else:
                # Calculate dimensions based on size
                new_width, new_height = self.calculate_dimensions(
                    orig_width, orig_height, size_name
                )
            
            # Resize image
            if new_width != orig_width or new_height != orig_height:
                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            else:
                resized_img = img.copy()
            
            # Apply enhancements based on image analysis
            enhanced_img = self.enhance_image(resized_img)
            
            # Generate filename for this size
            name, ext = os.path.splitext(filename)
            size_filename = f"{name}_{size_name}{ext}"
            
            optimized[size_name] = {
                'filename': size_filename,
                'width': new_width,
                'height': new_height,
                'quality': quality,
                'format': img.format or 'JPEG',
                'file_size_estimate': self.estimate_file_size(new_width, new_height, quality)
            }
        
        return optimized
    
    def calculate_dimensions(self, orig_width: int, orig_height: int, size_name: str) -> tuple:
        """Calculate new dimensions for different sizes"""
        aspect_ratio = orig_width / orig_height
        
        size_limits = {
            'thumbnail': (150, 150),
            'medium': (300, 300),
            'large': (800, 600)
        }
        
        if size_name in size_limits:
            max_width, max_height = size_limits[size_name]
            
            # Calculate dimensions maintaining aspect ratio
            if aspect_ratio > 1:  # Landscape
                new_width = min(orig_width, max_width)
                new_height = int(new_width / aspect_ratio)
                if new_height > max_height:
                    new_height = max_height
                    new_width = int(new_height * aspect_ratio)
            else:  # Portrait
                new_height = min(orig_height, max_height)
                new_width = int(new_height * aspect_ratio)
                if new_width > max_width:
                    new_width = max_width
                    new_height = int(new_width / aspect_ratio)
            
            return new_width, new_height
        
        return orig_width, orig_height
    
    def enhance_image(self, img: Image.Image) -> Image.Image:
        """Apply automatic image enhancements"""
        try:
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1.2)
            
            # Enhance contrast slightly
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.1)
            
            # Enhance color saturation
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.05)
            
            return img
            
        except Exception as e:
            self.log_activity(f"Image enhancement failed: {str(e)}", "warning")
            return img
    
    def estimate_file_size(self, width: int, height: int, quality: int) -> int:
        """Estimate file size based on dimensions and quality"""
        # Rough estimation: pixels * bytes per pixel * quality factor
        pixels = width * height
        bytes_per_pixel = 3  # RGB
        quality_factor = quality / 100
        
        return int(pixels * bytes_per_pixel * quality_factor)
    
    async def classify_image_content(self, img: Image.Image) -> Dict[str, Any]:
        """Classify image content using AI"""
        try:
            # This would use AI to classify image content
            # For now, use basic heuristics
            width, height = img.size
            aspect_ratio = width / height
            
            # Basic classification
            content_type = 'general'
            if aspect_ratio > 2:
                content_type = 'banner'
            elif aspect_ratio < 0.7:
                content_type = 'portrait'
            elif width > 1000 and height > 1000:
                content_type = 'high_resolution'
            
            # Use AI for better classification
            classification_prompt = f"""
            Analyze this image and classify its content type:
            - Dimensions: {width}x{height}
            - Aspect ratio: {aspect_ratio:.2f}
            - Color complexity: {self.assess_color_complexity(img)}
            
            Classify as one of: hero_image, product_photo, portrait, logo, background_pattern, infographic, screenshot, artwork, nature_photo, architectural_photo
            
            Return JSON format with:
            - primary_type: string
            - confidence: number (0-1)
            - secondary_types: array of strings
            - characteristics: object with visual characteristics
            """
            
            # Simulate AI response
            return {
                'primary_type': content_type,
                'confidence': 0.7,
                'secondary_types': ['general'],
                'characteristics': {
                    'aspect_ratio': aspect_ratio,
                    'resolution': 'high' if width > 800 else 'medium',
                    'color_complexity': 'medium',
                    'has_text': False,
                    'has_people': False,
                    'has_products': False
                }
            }
            
        except Exception as e:
            self.log_activity(f"Image classification failed: {str(e)}", "warning")
            return {
                'primary_type': 'general',
                'confidence': 0.5,
                'secondary_types': [],
                'characteristics': {}
            }
    
    def assess_color_complexity(self, img: Image.Image) -> str:
        """Assess the color complexity of an image"""
        try:
            # Convert to HSV and analyze color distribution
            hsv_img = img.convert('HSV')
            pixels = list(hsv_img.getdata())
            
            # Calculate color variance
            hues = [pixel[0] for pixel in pixels]
            saturations = [pixel[1] for pixel in pixels]
            
            hue_variance = max(hues) - min(hues)
            sat_variance = max(saturations) - min(saturations)
            
            if hue_variance > 100 and sat_variance > 100:
                return 'high'
            elif hue_variance > 50 and sat_variance > 50:
                return 'medium'
            else:
                return 'low'
                
        except Exception:
            return 'medium'
    
    def suggest_image_placement(self, content_type: str, width: int, height: int, design_spec: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest optimal placement for images based on content and design"""
        suggestions = []
        
        # Hero section suggestions
        if content_type in ['hero_image', 'banner', 'high_resolution']:
            suggestions.append({
                'section': 'hero',
                'priority': 1,
                'size': 'large',
                'layout': 'background',
                'reasoning': 'High-resolution image suitable for hero background'
            })
        
        # Gallery/portfolio suggestions
        if content_type in ['product_photo', 'artwork', 'nature_photo', 'architectural_photo']:
            suggestions.append({
                'section': 'gallery',
                'priority': 2,
                'size': 'medium',
                'layout': 'grid',
                'reasoning': 'Visual content suitable for gallery display'
            })
        
        # About section suggestions
        if content_type in ['portrait', 'team_photo']:
            suggestions.append({
                'section': 'about',
                'priority': 3,
                'size': 'medium',
                'layout': 'inline',
                'reasoning': 'People-focused image suitable for about section'
            })
        
        # Logo suggestions
        if content_type == 'logo':
            suggestions.append({
                'section': 'header',
                'priority': 1,
                'size': 'small',
                'layout': 'logo',
                'reasoning': 'Logo image for branding'
            })
        
        # Background suggestions
        if content_type in ['background_pattern', 'nature_photo']:
            suggestions.append({
                'section': 'background',
                'priority': 4,
                'size': 'large',
                'layout': 'tiled',
                'reasoning': 'Pattern suitable for background use'
            })
        
        return suggestions
    
    async def analyze_image_style(self, processed_image: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the artistic style of an image"""
        try:
            colors = processed_image.get('extracted_colors', [])
            
            if not colors:
                return {
                    'style': 'unknown',
                    'mood': 'neutral',
                    'dominant_colors': [],
                    'color_temperature': 'neutral',
                    'brightness': 'medium'
                }
            
            # Analyze color temperature
            avg_hue = sum(color['hsl']['h'] for color in colors) / len(colors)
            avg_saturation = sum(color['hsl']['s'] for color in colors) / len(colors)
            avg_lightness = sum(color['hsl']['l'] for color in colors) / len(colors)
            
            # Determine color temperature
            if avg_hue < 60 or avg_hue > 300:
                color_temp = 'warm'
            elif 120 < avg_hue < 240:
                color_temp = 'cool'
            else:
                color_temp = 'neutral'
            
            # Determine brightness
            if avg_lightness > 70:
                brightness = 'bright'
            elif avg_lightness < 30:
                brightness = 'dark'
            else:
                brightness = 'medium'
            
            # Determine mood based on colors
            dominant_colors = [color['hex'] for color in colors[:3]]
            
            if avg_saturation < 30:
                mood = 'calm'
            elif avg_saturation > 70:
                mood = 'vibrant'
            else:
                mood = 'balanced'
            
            # Determine style
            if color_temp == 'warm' and mood == 'vibrant':
                style = 'energetic'
            elif color_temp == 'cool' and mood == 'calm':
                style = 'serene'
            elif brightness == 'dark':
                style = 'dramatic'
            else:
                style = 'balanced'
            
            return {
                'style': style,
                'mood': mood,
                'dominant_colors': dominant_colors,
                'color_temperature': color_temp,
                'brightness': brightness,
                'saturation': 'high' if avg_saturation > 50 else 'low',
                'contrast': 'high' if len(colors) > 3 else 'low'
            }
            
        except Exception as e:
            self.log_activity(f"Style analysis failed: {str(e)}", "warning")
            return {
                'style': 'unknown',
                'mood': 'neutral',
                'dominant_colors': [],
                'color_temperature': 'neutral',
                'brightness': 'medium'
            }
    
    async def generate_image_sets(self, processed_images: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate responsive image sets"""
        image_sets = {}
        
        for image in processed_images:
            if 'error' in image:
                continue
                
            filename = image['filename']
            optimized = image['optimized_versions']
            
            # Create srcset for responsive images
            srcset = []
            for size_name, size_info in optimized.items():
                if size_name != 'original':
                    srcset.append(f"{size_info['filename']} {size_info['width']}w")
            
            # Create sizes attribute
            sizes = self.generate_sizes_attribute(image)
            
            image_sets[filename] = {
                'srcset': ', '.join(srcset),
                'sizes': sizes,
                'optimized_versions': optimized,
                'recommended_format': self.recommend_format(image)
            }
        
        return image_sets
    
    def generate_sizes_attribute(self, image: Dict[str, Any]) -> str:
        """Generate sizes attribute for responsive images"""
        metadata = image['metadata']
        width = metadata['original_width']
        
        if width > 1200:
            return "(max-width: 1200px) 100vw, 1200px"
        elif width > 800:
            return "(max-width: 800px) 100vw, 800px"
        else:
            return "100vw"
    
    def recommend_format(self, image: Dict[str, Any]) -> str:
        """Recommend optimal image format"""
        original_format = image['metadata']['format']
        
        # Recommend WebP for modern browsers
        if original_format in ['JPEG', 'PNG']:
            return 'WebP'
        
        return original_format
    
    async def generate_alt_texts(self, processed_images: List[Dict[str, Any]]) -> Dict[str, str]:
        """Generate alt text for accessibility"""
        alt_texts = {}
        
        for image in processed_images:
            if 'error' in image:
                continue
                
            filename = image['filename']
            content_type = image['content_type']['primary_type']
            
            # Generate descriptive alt text using AI
            prompt = f"""
            Generate a concise, descriptive alt text for this image:
            - Content type: {content_type}
            - Dimensions: {image['metadata']['original_width']}x{image['metadata']['original_height']}
            - Style: {image.get('style_analysis', {}).get('style', 'general')}
            
            The alt text should be:
            - 5-15 words maximum
            - Descriptive but not overly detailed
            - Useful for screen readers
            - Relevant to the content type
            """
            
            try:
                alt_text = await api_manager.generate_text(prompt, "text")
                # Clean up the response
                alt_text = alt_text.strip().replace('"', '').replace("'", "")
                if len(alt_text) > 100:
                    alt_text = alt_text[:100] + "..."
            except:
                # Fallback alt text
                alt_text = f"{content_type.replace('_', ' ').title()} image"
            
            alt_texts[filename] = alt_text
        
        return alt_texts
    
    def update_design_spec(self, design_spec: Dict[str, Any], color_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Update design specification with extracted colors from images"""
        if not color_analysis or not design_spec:
            return design_spec
        
        # Extract dominant colors from all images
        all_colors = []
        for image_colors in color_analysis.values():
            all_colors.extend(image_colors)
        
        if not all_colors:
            return design_spec
        
        # Find most common colors across all images
        color_counts = {}
        for color in all_colors:
            hex_color = color['hex']
            if hex_color in color_counts:
                color_counts[hex_color] += color['frequency']
            else:
                color_counts[hex_color] = color['frequency']
        
        # Get top 3 colors
        top_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Update design spec colors if they match well
        if len(top_colors) >= 2:
            design_spec['design_system']['colors']['accent'] = top_colors[0][0]
            design_spec['design_system']['colors']['secondary'] = top_colors[1][0]
        
        # Add image-derived color palette
        design_spec['image_colors'] = {
            'extracted_from_images': [color[0] for color in top_colors],
            'usage_notes': 'Colors extracted from uploaded images'
        }
        
        return design_spec
    
    def calculate_optimization_savings(self, processed_images: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate file size savings from optimization"""
        total_original_size = 0
        total_optimized_size = 0
        
        for image in processed_images:
            if 'error' in image:
                continue
                
            original_size = image['metadata']['file_size']
            total_original_size += original_size
            
            # Calculate optimized size (estimated)
            optimized_size = 0
            for size_name, size_info in image['optimized_versions'].items():
                if size_name != 'original':
                    optimized_size += size_info['file_size_estimate']
            
            total_optimized_size += optimized_size
        
        savings = total_original_size - total_optimized_size
        savings_percent = (savings / total_original_size * 100) if total_original_size > 0 else 0
        
        return {
            'original_total_size': total_original_size,
            'optimized_total_size': total_optimized_size,
            'savings_bytes': savings,
            'savings_percent': round(savings_percent, 2),
            'average_reduction_per_image': savings / len(processed_images) if processed_images else 0
        }
    
    def get_fallback_images(self) -> Dict[str, Any]:
        """Provide fallback image data when processing fails"""
        return {
            'placeholder_images': [
                {
                    'filename': 'placeholder-hero.jpg',
                    'width': 1200,
                    'height': 600,
                    'usage': 'hero_section',
                    'color': '#6b7280'
                },
                {
                    'filename': 'placeholder-card.jpg',
                    'width': 400,
                    'height': 300,
                    'usage': 'cards_gallery',
                    'color': '#9ca3af'
                }
            ],
            'default_colors': ['#6b7280', '#9ca3af', '#d1d5db'],
            'note': 'Using fallback images due to processing error'
        }
    
    def get_fallback_image_data(self) -> Dict[str, Any]:
        """Get fallback data for a single failed image"""
        return {
            'error': 'Image processing failed',
            'suggested_replacement': 'placeholder-image.jpg',
            'fallback_color': '#9ca3af'
        }