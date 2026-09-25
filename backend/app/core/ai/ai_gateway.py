import logging
from typing import Optional
from app.core.ai.watsonx_client import watsonx_client
from app.core.ai.openrouter_client import openrouter_client

logger = logging.getLogger(__name__)

def ai_generate_text(prompt: str, system_prompt: Optional[str] = None) -> Optional[str]:
    """
    Multi-Tier AI Text Generation:
    1. Tier 1: IBM watsonx.ai (Main Sponsor Tech)
    2. Tier 2: OpenRouter (Fallback with free models like Llama 3.3 70B Free)
    3. Tier 3: Returns None -> Triggers deterministic regex/semantic fallback
    """
    # 1. Try IBM watsonx.ai first
    if watsonx_client.is_available():
        try:
            logger.info("Attempting AI generation via Tier 1: IBM watsonx.ai...")
            text = watsonx_client.generate_text(prompt)
            if text and text.strip():
                return text
            logger.info("watsonx.ai returned empty response, checking fallback...")
        except Exception as e:
            logger.warning(f"IBM watsonx.ai error: {e}. Falling back to OpenRouter...")

    # 2. Try OpenRouter (Free model fallback)
    if openrouter_client.is_available():
        try:
            logger.info(f"Attempting AI generation via Tier 2: OpenRouter ({openrouter_client.model_id})...")
            text = openrouter_client.generate_text(prompt, system_prompt)
            if text and text.strip():
                return text
            logger.info("OpenRouter returned empty response, falling back to deterministic engine...")
        except Exception as e:
            logger.warning(f"OpenRouter error: {e}. Falling back to deterministic engine...")

    # 3. None returned -> callers handle Tier 3 deterministic fallback
    logger.info("Using Tier 3: Deterministic Rule-Based Fallback Engine.")
    return None


def get_active_ai_provider() -> str:
    if watsonx_client.is_available():
        return f"IBM watsonx.ai ({watsonx_client.model_id})"
    elif openrouter_client.is_available():
        return f"OpenRouter Free ({openrouter_client.model_id})"
    return "Deterministic Offline Rule Engine"
