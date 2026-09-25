import json
import logging
import httpx
from typing import Optional
from app.config import settings

logger = logging.getLogger(__name__)

class OpenRouterClient:
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.model_id = settings.OPENROUTER_MODEL or "meta-llama/llama-3.3-70b-instruct:free"
        self.base_url = settings.OPENROUTER_BASE_URL or "https://openrouter.ai/api/v1"

    def is_available(self) -> bool:
        return bool(self.api_key and self.api_key.strip())

    def generate_text(self, prompt: str, system_prompt: Optional[str] = None) -> Optional[str]:
        if not self.is_available():
            return None

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key.strip()}",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "IBM Bob 2.0 - Kanban Evidence Board",
            "Content-Type": "application/json"
        }

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model_id,
            "messages": messages,
            "temperature": 0.2,
        }

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(url, headers=headers, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    choices = data.get("choices", [])
                    if choices and "message" in choices[0]:
                        content = choices[0]["message"].get("content", "")
                        logger.info(f"Successfully generated response using OpenRouter ({self.model_id})")
                        return content
                else:
                    logger.warning(
                        f"OpenRouter API returned status {response.status_code}: {response.text[:200]}"
                    )
        except Exception as e:
            logger.error(f"Error calling OpenRouter API: {e}")

        return None

openrouter_client = OpenRouterClient()
