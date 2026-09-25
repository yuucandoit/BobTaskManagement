import re
import json
import logging
from typing import List, Dict, Any
from app.core.ai.ai_gateway import ai_generate_text

logger = logging.getLogger(__name__)

def parse_spec_document_to_cards(doc_text: str) -> List[Dict[str, Any]]:
    """
    Parses a specification document into an actionable list of task cards.
    """
    prompt = f"""You are a Technical Product Manager. Break down the following software requirements specification into concrete, modular development task cards for a Kanban sprint board.

Specification:
{doc_text[:2500]}

Respond ONLY with a JSON array of task objects matching this schema:
[
  {{
    "title": "Clear task title",
    "description": "Implementation checklist or technical detail",
    "task_type": "feature" or "chore" or "bugfix" or "refactor" or "docs",
    "priority": "High" or "Medium" or "Low",
    "estimation_hours": 3.0,
    "story_points": 2
  }}
]
"""

    llm_output = ai_generate_text(prompt)
    if llm_output:
        try:
            match = re.search(r'\[.*\]', llm_output, re.DOTALL)
            if match:
                cards = json.loads(match.group(0))
                if isinstance(cards, list) and len(cards) > 0:
                    return cards
        except Exception as e:
            logger.warning(f"Error parsing watsonx doc output: {e}")

    # Fallback: Extract bullet points or numbered lists
    lines = [l.strip() for l in doc_text.splitlines() if l.strip()]
    cards = []
    for line in lines:
        if line.startswith(("-", "*", "1.", "2.", "3.", "4.", "5.", "#")):
            clean_item = re.sub(r'^[-*#\d\.\s]+', '', line).strip()
            if len(clean_item) > 8:
                cards.append({
                    "title": clean_item[:70],
                    "description": f"Extracted from specification document: {clean_item}",
                    "task_type": "feature",
                    "priority": "Medium",
                    "estimation_hours": 2.5,
                    "story_points": 2
                })
        if len(cards) >= 6:
            break

    if not cards:
        cards.append({
            "title": "Review & Scaffold System Spec",
            "description": doc_text[:200],
            "task_type": "chore",
            "priority": "High",
            "estimation_hours": 2.0,
            "story_points": 2
        })

    return cards
