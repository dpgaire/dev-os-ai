import requests
from config import config
from typing import Optional, Dict, Any

class AIClient:
    BASE_URL = "https://openrouter.ai/api/v1"
    
    def __init__(self):
        if not config.api_key:
            raise ValueError("OpenRouter API key not configured. Set OPENROUTER_API_KEY in .env")
        
        self.headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/devos-ai",
            "X-Title": "DevOS AI"
        }
    
    def send_prompt(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Send prompt to AI model with optional system prompt and parameters."""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": model or config.model,
            "messages": messages,
            "max_tokens": kwargs.get("max_tokens", config.max_tokens),
            "temperature": kwargs.get("temperature", config.temperature),
        }
        
        try:
            response = requests.post(
                f"{self.BASE_URL}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}