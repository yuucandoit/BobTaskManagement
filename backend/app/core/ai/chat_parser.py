import re
import json
import logging
from typing import Dict, Any, Optional
from app.core.ai.ai_gateway import ai_generate_text
from app.models.schemas import ChatCardExtraction

logger = logging.getLogger(__name__)

def parse_chat_to_card(message: str, context_repo: Optional[str] = None) -> ChatCardExtraction:
    """
    Parses natural language chat request into a structured task card representation.
    """
    prompt = f"""You are an intelligent project management AI assistant.
The Project Manager says:
"{message}"

Context Repo: {context_repo or 'general'}

Extract the task details and respond strictly with a valid JSON object matching this structure:
{{
  "title": "Short title of the task",
  "description": "Clear description of the work requested",
  "assignee_name": "Name of the person assigned or null if none mentioned",
  "task_type": "feature" or "bugfix" or "refactor" or "chore" or "docs",
  "priority": "Low" or "Medium" or "High" or "Critical",
  "estimation_hours": 2.0,
  "target_column": "To Do" or "In Progress" or "Done",
  "matched_branch_or_pr": null
}}
"""

    llm_output = ai_generate_text(prompt)
    if llm_output:
        try:
            match = re.search(r'\{.*\}', llm_output, re.DOTALL)
            if match:
                data = json.loads(match.group(0))
                return ChatCardExtraction(
                    title=data.get("title", message[:60]),
                    description=data.get("description", message),
                    assignee_name=data.get("assignee_name"),
                    task_type=data.get("task_type", "feature"),
                    priority=data.get("priority", "Medium"),
                    estimation_hours=float(data.get("estimation_hours", 2.0)),
                    target_column=data.get("target_column", "To Do"),
                    matched_branch_or_pr=data.get("matched_branch_or_pr")
                )
        except Exception as e:
            logger.warning(f"Error parsing watsonx response in chat_parser: {e}")

    # Fallback Rule/Regex Parser
    return _fallback_chat_parser(message)


def _fallback_chat_parser(message: str) -> ChatCardExtraction:
    msg_lower = message.lower()
    
    # 1. Extract assignee (e.g. "assign ke Firza", "untuk Budi", "assigned to Sarah")
    assignee = None
    assignee_match = re.search(r'(?:assign(?:ed)?\s+(?:ke|to)|untuk|kepada)\s+([A-Za-z0-9_-]+)', message, re.IGNORECASE)
    if assignee_match:
        assignee = assignee_match.group(1).capitalize()

    # 2. Extract priority
    priority = "Medium"
    if any(k in msg_lower for k in ["urgent", "darurat", "critical", "p0", "secepatnya"]):
        priority = "Critical"
    elif any(k in msg_lower for k in ["penting", "high", "p1"]):
        priority = "High"
    elif any(k in msg_lower for k in ["santai", "low", "minor", "p3"]):
        priority = "Low"

    # 3. Extract task type
    task_type = "feature"
    if any(k in msg_lower for k in ["bug", "fix", "error", "rusak", "perbaiki"]):
        task_type = "bugfix"
    elif any(k in msg_lower for k in ["refactor", "cleanup", "rapikan", "reorganize"]):
        task_type = "refactor"
    elif any(k in msg_lower for k in ["doc", "dokumentasi", "readme"]):
        task_type = "docs"

    # 4. Extract clean title
    cleaned = re.sub(r'^(buat|bikin|create|tambah)\s+(kartu|task|tiket)?[:\s-]*', '', message, flags=re.IGNORECASE)
    cleaned = re.sub(r'(?:,\s*)?(?:assign(?:ed)?\s+(?:ke|to)|untuk|kepada)\s+[A-Za-z0-9_-]+', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'(?:,\s*)?(?:deadline|batas|target)\s+[^\.,;]+', '', cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.strip(" ,.-:")

    title = cleaned.capitalize() if cleaned else message[:50]
    if len(title) > 80:
        title = title[:80] + "..."

    return ChatCardExtraction(
        title=title,
        description=f"Created via AI Chat: {message}",
        assignee_name=assignee or "Unassigned",
        task_type=task_type,
        priority=priority,
        estimation_hours=3.0 if task_type == "refactor" else 2.0,
        target_column="To Do",
        matched_branch_or_pr=None
    )
