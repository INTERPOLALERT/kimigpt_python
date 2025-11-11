"""
API Manager for KimiGPT - FIXED VERSION
Handles all AI API interactions with smart rotation and failover
ONLY FREE-TIER APIs INCLUDED
"""

import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import requests
from concurrent.futures import ThreadPoolExecutor
import asyncio
from src.core.config_manager import ConfigManager
import hashlib


@dataclass
class APIStatus:
    name: str
    status: str  # 'online', 'offline', 'rate_limited'
    response_time: float
    remaining_quota: Optional[int]
    last_used: datetime
    success_rate: float
    error_count: int = 0


class APIManager:
    """Manage AI API calls with smart rotation"""

    def __init__(self):
        self.config_manager = ConfigManager()
        self.apis = {}
        self.api_status = {}
        self.cache = {}
        self.cache_duration = timedelta(hours=1)
        self.executor = ThreadPoolExecutor(max_workers=3)
        self.setup_apis()

    def setup_apis(self):
        """Initialize all available APIs (FREE TIER ONLY)"""
        api_keys = self.config_manager.get_all_api_keys()

        # Anthropic Claude
        if api_keys.get('ANTHROPIC_API_KEY'):
            self.apis['anthropic'] = {
                'key': api_keys['ANTHROPIC_API_KEY'],
                'base_url': 'https://api.anthropic.com/v1',
                'models': ['claude-3-haiku-20240307'],
                'priority': 1,
                'rate_limit': 50
            }

        # Google Gemini
        if api_keys.get('GEMINI_API_KEY'):
            self.apis['gemini'] = {
                'key': api_keys['GEMINI_API_KEY'],
                'base_url': 'https://generativelanguage.googleapis.com/v1beta',
                'models': ['gemini-1.5-flash'],
                'priority': 2,
                'rate_limit': 60
            }

        # Groq (Most generous free tier!)
        if api_keys.get('GROQ_API_KEY'):
            self.apis['groq'] = {
                'key': api_keys['GROQ_API_KEY'],
                'base_url': 'https://api.groq.com/openai/v1',
                'models': ['llama-3.1-70b-versatile'],
                'priority': 3,
                'rate_limit': 14400
            }

        # DeepSeek
        if api_keys.get('DEEPSEEK_API_KEY'):
            self.apis['deepseek'] = {
                'key': api_keys['DEEPSEEK_API_KEY'],
                'base_url': 'https://api.deepseek.com/v1',
                'models': ['deepseek-coder'],
                'priority': 4,
                'rate_limit': 100
            }

        # OpenRouter
        if api_keys.get('OPENROUTER_API_KEY'):
            self.apis['openrouter'] = {
                'key': api_keys['OPENROUTER_API_KEY'],
                'base_url': 'https://openrouter.ai/api/v1',
                'models': ['anthropic/claude-3-haiku'],
                'priority': 5,
                'rate_limit': 1000
            }

        # Cohere
        if api_keys.get('COHERE_API_KEY'):
            self.apis['cohere'] = {
                'key': api_keys['COHERE_API_KEY'],
                'base_url': 'https://api.cohere.ai/v1',
                'models': ['command'],
                'priority': 6,
                'rate_limit': 100
            }

        # Together AI (Most generous free tier!)
        if api_keys.get('TOGETHER_API_KEY'):
            self.apis['together'] = {
                'key': api_keys['TOGETHER_API_KEY'],
                'base_url': 'https://api.together.xyz/v1',
                'models': ['mistralai/Mixtral-8x7B-Instruct-v0.1'],
                'priority': 7,
                'rate_limit': 1000
            }

        # Perplexity AI
        if api_keys.get('PERPLEXITY_API_KEY'):
            self.apis['perplexity'] = {
                'key': api_keys['PERPLEXITY_API_KEY'],
                'base_url': 'https://api.perplexity.ai',
                'models': ['llama-3.1-sonar-small-128k-online'],
                'priority': 8,
                'rate_limit': 50
            }

        # Replicate
        if api_keys.get('REPLICATE_API_KEY'):
            self.apis['replicate'] = {
                'key': api_keys['REPLICATE_API_KEY'],
                'base_url': 'https://api.replicate.com/v1',
                'models': ['meta/llama-2-70b-chat'],
                'priority': 9,
                'rate_limit': 100
            }

        # AI21 Labs
        if api_keys.get('AI21_API_KEY'):
            self.apis['ai21'] = {
                'key': api_keys['AI21_API_KEY'],
                'base_url': 'https://api.ai21.com/studio/v1',
                'models': ['j2-mid'],
                'priority': 10,
                'rate_limit': 100
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

    def select_best_api(self) -> Optional[str]:
        """Intelligently select the best available API"""
        available_apis = []

        for api_name, api_config in self.apis.items():
            status = self.api_status[api_name]

            # Skip offline or rate-limited APIs
            if status.status in ['offline', 'rate_limited']:
                continue

            # Calculate priority score (lower priority number = higher preference)
            priority_score = api_config['priority']

            available_apis.append((api_name, priority_score))

        if not available_apis:
            return None

        # Select API with best (lowest) priority
        best_api = min(available_apis, key=lambda x: x[1])[0]
        return best_api

    async def generate_text(self, prompt: str, max_tokens: int = 4000) -> str:
        """Generate text using the best available API"""
        # Select best API
        best_api = self.select_best_api()
        if not best_api:
            raise Exception("No suitable API available. Please configure at least one API key.")

        # Run the synchronous call in an executor
        loop = asyncio.get_event_loop()
        try:
            response = await loop.run_in_executor(
                self.executor,
                self._call_api_sync,
                best_api,
                prompt,
                max_tokens
            )
            return response
        except Exception as e:
            # Mark as offline and try next API
            self.api_status[best_api].status = 'offline'
            self.api_status[best_api].error_count += 1

            # Try fallback APIs
            for api_name in self.apis:
                if api_name != best_api and self.api_status[api_name].status == 'online':
                    try:
                        response = await loop.run_in_executor(
                            self.executor,
                            self._call_api_sync,
                            api_name,
                            prompt,
                            max_tokens
                        )
                        return response
                    except Exception as e2:
                        continue

            raise Exception(f"All APIs failed. Last error: {str(e)}")

    def _call_api_sync(self, api_name: str, prompt: str, max_tokens: int) -> str:
        """Synchronous API call (runs in executor)"""
        api_config = self.apis[api_name]
        status = self.api_status[api_name]

        start_time = time.time()

        try:
            if api_name == 'anthropic':
                response = self._call_anthropic(api_config, prompt, max_tokens)
            elif api_name == 'gemini':
                response = self._call_gemini(api_config, prompt, max_tokens)
            elif api_name == 'groq':
                response = self._call_groq(api_config, prompt, max_tokens)
            elif api_name == 'deepseek':
                response = self._call_deepseek(api_config, prompt, max_tokens)
            elif api_name == 'openrouter':
                response = self._call_openrouter(api_config, prompt, max_tokens)
            elif api_name == 'cohere':
                response = self._call_cohere(api_config, prompt, max_tokens)
            elif api_name == 'together':
                response = self._call_together(api_config, prompt, max_tokens)
            elif api_name == 'perplexity':
                response = self._call_perplexity(api_config, prompt, max_tokens)
            elif api_name == 'replicate':
                response = self._call_replicate(api_config, prompt, max_tokens)
            elif api_name == 'ai21':
                response = self._call_ai21(api_config, prompt, max_tokens)
            else:
                raise ValueError(f"Unknown API: {api_name}")

            # Update status
            status.response_time = time.time() - start_time
            status.last_used = datetime.now()
            status.success_rate = min(1.0, status.success_rate * 0.9 + 0.1)
            status.error_count = 0
            status.status = 'online'

            return response

        except Exception as e:
            status.response_time = time.time() - start_time
            status.error_count += 1
            status.success_rate = max(0.0, status.success_rate * 0.9)
            raise e

    def _call_anthropic(self, api_config: Dict, prompt: str, max_tokens: int) -> str:
        """Call Anthropic Claude API"""
        headers = {
            'x-api-key': api_config["key"],
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01'
        }

        data = {
            'model': api_config['models'][0],
            'max_tokens': max_tokens,
            'messages': [{'role': 'user', 'content': prompt}]
        }

        response = requests.post(
            f"{api_config['base_url']}/messages",
            headers=headers,
            json=data,
            timeout=60
        )

        if response.status_code == 200:
            return response.json()['content'][0]['text']
        else:
            raise Exception(f"Anthropic API error: {response.status_code}")

    def _call_gemini(self, api_config: Dict, prompt: str, max_tokens: int) -> str:
        """Call Google Gemini API"""
        headers = {
            'Content-Type': 'application/json',
        }

        data = {
            'contents': [{'parts': [{'text': prompt}]}],
            'generationConfig': {
                'temperature': 0.7,
                'topK': 40,
                'topP': 0.95,
                'maxOutputTokens': max_tokens
            }
        }

        response = requests.post(
            f"{api_config['base_url']}/models/{api_config['models'][0]}:generateContent",
            headers=headers,
            json=data,
            params={'key': api_config['key']},
            timeout=60
        )

        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            raise Exception(f"Gemini API error: {response.status_code}")

    def _call_groq(self, api_config: Dict, prompt: str, max_tokens: int) -> str:
        """Call Groq API"""
        headers = {
            'Authorization': f'Bearer {api_config["key"]}',
            'Content-Type': 'application/json'
        }

        data = {
            'model': api_config['models'][0],
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': max_tokens
        }

        response = requests.post(
            f"{api_config['base_url']}/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            raise Exception(f"Groq API error: {response.status_code}")

    def _call_deepseek(self, api_config: Dict, prompt: str, max_tokens: int) -> str:
        """Call DeepSeek API"""
        headers = {
            'Authorization': f'Bearer {api_config["key"]}',
            'Content-Type': 'application/json'
        }

        data = {
            'model': api_config['models'][0],
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': max_tokens
        }

        response = requests.post(
            f"{api_config['base_url']}/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            raise Exception(f"DeepSeek API error: {response.status_code}")

    def _call_openrouter(self, api_config: Dict, prompt: str, max_tokens: int) -> str:
        """Call OpenRouter API"""
        headers = {
            'Authorization': f'Bearer {api_config["key"]}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'http://localhost',
            'X-Title': 'KimiGPT'
        }

        data = {
            'model': api_config['models'][0],
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': max_tokens
        }

        response = requests.post(
            f"{api_config['base_url']}/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            raise Exception(f"OpenRouter API error: {response.status_code}")

    def _call_cohere(self, api_config: Dict, prompt: str, max_tokens: int) -> str:
        """Call Cohere API"""
        headers = {
            'Authorization': f'Bearer {api_config["key"]}',
            'Content-Type': 'application/json'
        }

        data = {
            'model': api_config['models'][0],
            'prompt': prompt,
            'max_tokens': max_tokens,
            'temperature': 0.7
        }

        response = requests.post(
            f"{api_config['base_url']}/generate",
            headers=headers,
            json=data,
            timeout=60
        )

        if response.status_code == 200:
            return response.json()['generations'][0]['text']
        else:
            raise Exception(f"Cohere API error: {response.status_code}")

    def _call_together(self, api_config: Dict, prompt: str, max_tokens: int) -> str:
        """Call Together AI API"""
        headers = {
            'Authorization': f'Bearer {api_config["key"]}',
            'Content-Type': 'application/json'
        }

        data = {
            'model': api_config['models'][0],
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': max_tokens,
            'temperature': 0.7
        }

        response = requests.post(
            f"{api_config['base_url']}/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            raise Exception(f"Together AI error: {response.status_code}")

    def _call_perplexity(self, api_config: Dict, prompt: str, max_tokens: int) -> str:
        """Call Perplexity API"""
        headers = {
            'Authorization': f'Bearer {api_config["key"]}',
            'Content-Type': 'application/json'
        }

        data = {
            'model': api_config['models'][0],
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': max_tokens
        }

        response = requests.post(
            f"{api_config['base_url']}/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            raise Exception(f"Perplexity API error: {response.status_code}")

    def _call_replicate(self, api_config: Dict, prompt: str, max_tokens: int) -> str:
        """Call Replicate API"""
        headers = {
            'Authorization': f'Token {api_config["key"]}',
            'Content-Type': 'application/json'
        }

        data = {
            'version': 'meta/llama-2-70b-chat',
            'input': {
                'prompt': prompt,
                'max_new_tokens': max_tokens,
                'temperature': 0.7
            }
        }

        response = requests.post(
            f"{api_config['base_url']}/predictions",
            headers=headers,
            json=data,
            timeout=60
        )

        if response.status_code == 201:
            # Replicate is async, need to poll for result
            prediction_url = response.json()['urls']['get']
            import time
            for _ in range(30):  # Wait up to 30 seconds
                time.sleep(1)
                result = requests.get(prediction_url, headers=headers)
                if result.json()['status'] == 'succeeded':
                    return ''.join(result.json()['output'])
            raise Exception("Replicate timeout")
        else:
            raise Exception(f"Replicate API error: {response.status_code}")

    def _call_ai21(self, api_config: Dict, prompt: str, max_tokens: int) -> str:
        """Call AI21 Labs API"""
        headers = {
            'Authorization': f'Bearer {api_config["key"]}',
            'Content-Type': 'application/json'
        }

        data = {
            'prompt': prompt,
            'maxTokens': max_tokens,
            'temperature': 0.7,
            'topP': 1.0
        }

        response = requests.post(
            f"{api_config['base_url']}/{api_config['models'][0]}/complete",
            headers=headers,
            json=data,
            timeout=60
        )

        if response.status_code == 200:
            return response.json()['completions'][0]['data']['text']
        else:
            raise Exception(f"AI21 API error: {response.status_code}")

    def get_status(self) -> Dict[str, Any]:
        """Get current status of all APIs"""
        return {
            'apis': {
                name: {
                    'status': status.status,
                    'response_time': round(status.response_time, 2),
                    'success_rate': round(status.success_rate * 100, 1),
                    'error_count': status.error_count
                }
                for name, status in self.api_status.items()
            },
            'total_apis': len(self.apis),
            'online_apis': sum(1 for status in self.api_status.values() if status.status == 'online')
        }
