import os
import time
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv
import threading
from queue import Queue
import hashlib

# Load environment variables
load_dotenv()

@dataclass
class APIStatus:
    name: str
    status: str  # 'online', 'offline', 'rate_limited'
    response_time: float
    remaining_quota: Optional[int]
    last_used: datetime
    success_rate: float
    error_count: int = 0

@dataclass
class APIRequest:
    prompt: str
    model_type: str
    priority: int = 1
    callback: Optional[callable] = None
    request_id: str = ""
    timestamp: datetime = None

class APIManager:
    def __init__(self):
        self.apis = {}
        self.api_status = {}
        self.request_queue = Queue()
        self.cache = {}
        self.cache_duration = timedelta(hours=1)
        self.setup_apis()
        self.start_monitoring()
        
    def setup_apis(self):
        """Initialize all available APIs"""
        # Anthropic Claude
        if os.getenv('ANTHROPIC_API_KEY'):
            self.apis['anthropic'] = {
                'key': os.getenv('ANTHROPIC_API_KEY'),
                'base_url': 'https://api.anthropic.com/v1',
                'models': ['claude-3-sonnet-20240229', 'claude-3-haiku-20240307'],
                'priority': 1,
                'rate_limit': 50,
                'current_usage': 0
            }
        
        # Google Gemini
        if os.getenv('GEMINI_API_KEY'):
            self.apis['gemini'] = {
                'key': os.getenv('GEMINI_API_KEY'),
                'base_url': 'https://generativelanguage.googleapis.com/v1beta',
                'models': ['gemini-1.5-flash', 'gemini-1.5-pro'],
                'priority': 2,
                'rate_limit': 60,
                'current_usage': 0
            }
        
        # Groq
        if os.getenv('GROQ_API_KEY'):
            self.apis['groq'] = {
                'key': os.getenv('GROQ_API_KEY'),
                'base_url': 'https://api.groq.com/openai/v1',
                'models': ['llama-3.1-70b-versatile', 'mixtral-8x7b-32768'],
                'priority': 3,
                'rate_limit': 14400,  # Very generous
                'current_usage': 0
            }
        
        # DeepSeek
        if os.getenv('DEEPSEEK_API_KEY'):
            self.apis['deepseek'] = {
                'key': os.getenv('DEEPSEEK_API_KEY'),
                'base_url': 'https://api.deepseek.com/v1',
                'models': ['deepseek-coder', 'deepseek-chat'],
                'priority': 4,
                'rate_limit': 100,
                'current_usage': 0
            }
        
        # OpenRouter
        if os.getenv('OPENROUTER_API_KEY'):
            self.apis['openrouter'] = {
                'key': os.getenv('OPENROUTER_API_KEY'),
                'base_url': 'https://openrouter.ai/api/v1',
                'models': ['anthropic/claude-3-sonnet', 'google/gemini-pro'],
                'priority': 5,
                'rate_limit': 1000,
                'current_usage': 0
            }
        
        # Mistral
        if os.getenv('MISTRAL_API_KEY'):
            self.apis['mistral'] = {
                'key': os.getenv('MISTRAL_API_KEY'),
                'base_url': 'https://api.mistral.ai/v1',
                'models': ['mistral-medium', 'mistral-small'],
                'priority': 6,
                'rate_limit': 100,
                'current_usage': 0
            }
        
        # Initialize status tracking
        for api_name in self.apis:
            self.api_status[api_name] = APIStatus(
                name=api_name,
                status='online',
                response_time=0.0,
                remaining_quota=None,
                last_used=datetime.now(),
                success_rate=1.0
            )
    
    def get_cache_key(self, prompt: str, model_type: str) -> str:
        """Generate cache key for request"""
        content = f"{prompt}:{model_type}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def check_cache(self, cache_key: str) -> Optional[str]:
        """Check if response is cached"""
        if cache_key in self.cache:
            cached_time, response = self.cache[cache_key]
            if datetime.now() - cached_time < self.cache_duration:
                return response
            else:
                del self.cache[cache_key]
        return None
    
    def add_to_cache(self, cache_key: str, response: str):
        """Add response to cache"""
        self.cache[cache_key] = (datetime.now(), response)
        
        # Clean old cache entries
        if len(self.cache) > 1000:
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k][0])
            del self.cache[oldest_key]
    
    def select_best_api(self, model_type: str = "text") -> Optional[str]:
        """Intelligently select the best available API"""
        available_apis = []
        
        for api_name, api_config in self.apis.items():
            status = self.api_status[api_name]
            
            # Skip offline or rate-limited APIs
            if status.status in ['offline', 'rate_limited']:
                continue
            
            # Check if API has suitable models
            has_suitable_model = any(
                self.is_model_suitable(model, model_type) 
                for model in api_config['models']
            )
            
            if not has_suitable_model:
                continue
            
            # Calculate priority score
            priority_score = (
                api_config['priority'] * 0.3 +  # Lower priority number = higher preference
                status.success_rate * 0.4 +      # Higher success rate = better
                (1 / (status.response_time + 1)) * 0.3  # Faster response time = better
            )
            
            available_apis.append((api_name, priority_score))
        
        if not available_apis:
            return None
        
        # Select API with highest priority score
        best_api = max(available_apis, key=lambda x: x[1])[0]
        return best_api
    
    def is_model_suitable(self, model: str, model_type: str) -> bool:
        """Check if model is suitable for the requested task"""
        model_lower = model.lower()
        
        if model_type == "text":
            return any(word in model_lower for word in ['gpt', 'claude', 'llama', 'mistral', 'gemini'])
        elif model_type == "code":
            return 'coder' in model_lower or 'code' in model_lower
        elif model_type == "image":
            return 'vision' in model_lower or 'gemini' in model_lower
        
        return True
    
    async def generate_text(self, prompt: str, model_type: str = "text") -> str:
        """Generate text using the best available API"""
        # Check cache first
        cache_key = self.get_cache_key(prompt, model_type)
        cached_response = self.check_cache(cache_key)
        if cached_response:
            return cached_response
        
        # Select best API
        best_api = self.select_best_api(model_type)
        if not best_api:
            raise Exception("No suitable API available")
        
        # Make API call
        try:
            response = await self.call_api(best_api, prompt, model_type)
            self.add_to_cache(cache_key, response)
            return response
        except Exception as e:
            # Try next available API
            logging.error(f"API {best_api} failed: {e}")
            self.api_status[best_api].status = 'offline'
            self.api_status[best_api].error_count += 1
            
            # Try fallback APIs
            for api_name in self.apis:
                if api_name != best_api and self.api_status[api_name].status == 'online':
                    try:
                        response = await self.call_api(api_name, prompt, model_type)
                        self.add_to_cache(cache_key, response)
                        return response
                    except Exception as e2:
                        logging.error(f"Fallback API {api_name} also failed: {e2}")
                        continue
            
            raise Exception("All APIs failed")
    
    async def call_api(self, api_name: str, prompt: str, model_type: str) -> str:
        """Make actual API call"""
        api_config = self.apis[api_name]
        status = self.api_status[api_name]
        
        start_time = time.time()
        
        try:
            if api_name == 'anthropic':
                response = await self.call_anthropic(api_config, prompt)
            elif api_name == 'gemini':
                response = await self.call_gemini(api_config, prompt)
            elif api_name == 'groq':
                response = await self.call_groq(api_config, prompt)
            elif api_name == 'deepseek':
                response = await self.call_deepseek(api_config, prompt)
            elif api_name == 'openrouter':
                response = await self.call_openrouter(api_config, prompt)
            elif api_name == 'mistral':
                response = await self.call_mistral(api_config, prompt)
            else:
                raise ValueError(f"Unknown API: {api_name}")
            
            # Update status
            status.response_time = time.time() - start_time
            status.last_used = datetime.now()
            status.success_rate = min(1.0, status.success_rate * 0.9 + 0.1)  # Exponential moving average
            status.error_count = 0
            
            return response
            
        except Exception as e:
            status.response_time = time.time() - start_time
            status.error_count += 1
            status.success_rate = max(0.0, status.success_rate * 0.9)
            raise e
    
    async def call_anthropic(self, api_config: Dict, prompt: str) -> str:
        """Call Anthropic Claude API"""
        headers = {
            'Authorization': f'Bearer {api_config["key"]}',
            'Content-Type': 'application/json',
            'Anthropic-Version': '2023-06-01'
        }
        
        data = {
            'model': api_config['models'][0],  # Use first available model
            'max_tokens': 4000,
            'messages': [{'role': 'user', 'content': prompt}]
        }
        
        response = requests.post(
            f"{api_config['base_url']}/messages",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['content'][0]['text']
        else:
            raise Exception(f"Anthropic API error: {response.status_code}")
    
    async def call_gemini(self, api_config: Dict, prompt: str) -> str:
        """Call Google Gemini API"""
        headers = {
            'Content-Type': 'application/json',
        }
        
        data = {
            'contents': [{'parts': [{'text': prompt}]}],
            'generationConfig': {
                'temperature': 0.7,
                'topK': 1,
                'topP': 1,
                'maxOutputTokens': 4000
            }
        }
        
        response = requests.post(
            f"{api_config['base_url']}/models/{api_config['models'][0]}:generateContent",
            headers=headers,
            json=data,
            params={'key': api_config['key']},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            raise Exception(f"Gemini API error: {response.status_code}")
    
    async def call_groq(self, api_config: Dict, prompt: str) -> str:
        """Call Groq API"""
        headers = {
            'Authorization': f'Bearer {api_config["key"]}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': api_config['models'][0],
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 4000
        }
        
        response = requests.post(
            f"{api_config['base_url']}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            raise Exception(f"Groq API error: {response.status_code}")
    
    async def call_deepseek(self, api_config: Dict, prompt: str) -> str:
        """Call DeepSeek API"""
        headers = {
            'Authorization': f'Bearer {api_config["key"]}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': api_config['models'][0],
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 4000
        }
        
        response = requests.post(
            f"{api_config['base_url']}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            raise Exception(f"DeepSeek API error: {response.status_code}")
    
    async def call_openrouter(self, api_config: Dict, prompt: str) -> str:
        """Call OpenRouter API"""
        headers = {
            'Authorization': f'Bearer {api_config["key"]}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'http://localhost:5000',
            'X-Title': 'KimiGPT'
        }
        
        data = {
            'model': api_config['models'][0],
            'messages': [{'role': 'user', 'content': prompt}]
        }
        
        response = requests.post(
            f"{api_config['base_url']}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            raise Exception(f"OpenRouter API error: {response.status_code}")
    
    async def call_mistral(self, api_config: Dict, prompt: str) -> str:
        """Call Mistral API"""
        headers = {
            'Authorization': f'Bearer {api_config["key"]}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': api_config['models'][0],
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 4000
        }
        
        response = requests.post(
            f"{api_config['base_url']}/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            raise Exception(f"Mistral API error: {response.status_code}")
    
    def start_monitoring(self):
        """Start background monitoring thread"""
        def monitor():
            while True:
                self.check_api_health()
                time.sleep(60)  # Check every minute
        
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()
    
    def check_api_health(self):
        """Check health of all APIs"""
        for api_name in self.apis:
            try:
                # Simple health check (could be more sophisticated)
                status = self.api_status[api_name]
                
                # Reset rate limits if enough time has passed
                if status.status == 'rate_limited':
                    if datetime.now() - status.last_used > timedelta(minutes=5):
                        status.status = 'online'
                
                # Mark as offline if too many errors
                if status.error_count > 10:
                    status.status = 'offline'
                
            except Exception as e:
                logging.error(f"Health check failed for {api_name}: {e}")
                self.api_status[api_name].status = 'offline'
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of all APIs"""
        return {
            'apis': {
                name: {
                    'status': status.status,
                    'response_time': status.response_time,
                    'success_rate': status.success_rate,
                    'error_count': status.error_count,
                    'last_used': status.last_used.isoformat()
                }
                for name, status in self.api_status.items()
            },
            'cache_size': len(self.cache),
            'total_apis': len(self.apis),
            'online_apis': sum(1 for status in self.api_status.values() if status.status == 'online')
        }

# Global API manager instance
api_manager = APIManager()