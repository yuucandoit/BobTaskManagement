import os
import json
import logging
from typing import Optional, Dict, Any
from app.config import settings

logger = logging.getLogger(__name__)

class WatsonxClient:
    def __init__(self):
        self.api_key = settings.WATSONX_API_KEY
        self.project_id = settings.WATSONX_PROJECT_ID
        self.url = settings.WATSONX_URL or "https://us-south.ml.cloud.ibm.com"
        self.model_id = settings.WATSONX_MODEL_ID or "ibm/granite-13b-chat-v2"
        self.use_fallback = settings.WATSONX_USE_FALLBACK_ON_ERROR
        self._model = None
        self._init_client()

    def _init_client(self):
        if not self.api_key or not self.project_id:
            logger.info("Watsonx credentials not fully configured. Safe fallback engine enabled.")
            return

        try:
            from ibm_watsonx_ai.foundation_models import ModelInference
            from ibm_watsonx_ai import Credentials

            credentials = Credentials(
                url=self.url,
                api_key=self.api_key
            )
            self._model = ModelInference(
                model_id=self.model_id,
                credentials=credentials,
                project_id=self.project_id,
                params={
                    "decoding_method": "greedy",
                    "max_new_tokens": 512,
                    "repetition_penalty": 1.1,
                    "temperature": 0.2
                }
            )
            logger.info(f"Watsonx ModelInference initialized with model: {self.model_id}")
        except Exception as e:
            logger.warning(f"Failed to initialize watsonx client: {e}. Fallback enabled.")
            self._model = None

    def is_available(self) -> bool:
        return self._model is not None

    def generate_text(self, prompt: str) -> Optional[str]:
        if self._model:
            try:
                response = self._model.generate_text(prompt=prompt)
                return response
            except Exception as e:
                logger.error(f"watsonx.ai generate_text error: {e}")
                if not self.use_fallback:
                    raise e
        return None

watsonx_client = WatsonxClient()
