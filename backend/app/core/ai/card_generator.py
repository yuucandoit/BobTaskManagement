import re
import json
import logging
from typing import Dict, Any, Optional
from app.core.ai.ai_gateway import ai_generate_text
from app.core.scoring.estimation import calculate_estimation_from_diff

logger = logging.getLogger(__name__)

def generate_card_from_pr(
    pr_title: str,
    pr_body: Optional[str] = "",
    branch_name: Optional[str] = "",
    author_username: Optional[str] = "",
    author_name: Optional[str] = "",
    diff_loc: int = 0
) -> Dict[str, Any]:
    """
    Uses IBM watsonx.ai (with OpenRouter & deterministic fallbacks) to transform a PR into a structured Kanban card.
    """
    body_clean = (pr_body or "").strip()
    prompt = f"""You are an expert AI Agile Scrum Master and Tech Lead.
Given the following GitHub Pull Request details, analyze the technical scope and return a JSON object.

PR Title: {pr_title}
Branch: {branch_name}
Author: {author_name or author_username}
Diff Lines Changed: {diff_loc}
PR Description:
{body_clean[:1000]}

Respond ONLY with a valid JSON object matching this schema:
{{
  "title": "Clear, concise card title (max 80 chars)",
  "description": "Executive summary of what this code changes and why (max 200 words)",
  "task_type": "feature" or "bugfix" or "refactor" or "chore" or "docs",
  "priority": "Low" or "Medium" or "High" or "Critical",
  "story_points": 1, 2, 3, 5, or 8,
  "estimation_hours": estimated hours as float
}}
"""

    llm_output = ai_generate_text(prompt)
    if llm_output:
        try:
            match = re.search(r'\{.*\}', llm_output, re.DOTALL)
            if match:
                data = json.loads(match.group(0))
                # Validate and ensure types
                return {
                    "title": data.get("title", pr_title),
                    "description": data.get("description", body_clean or "Automated card created from PR."),
                    "task_type": data.get("task_type", _infer_task_type(pr_title, branch_name)),
                    "priority": data.get("priority", "Medium"),
                    "story_points": int(data.get("story_points", 2)),
                    "estimation_hours": float(data.get("estimation_hours", 2.0)),
                    "assignee_name": author_name or author_username or "Developer",
                    "assignee_username": author_username,
                }
        except Exception as e:
            logger.warning(f"Error parsing watsonx output for PR card: {e}")

    # Resilient Deterministic Fallback
    return _fallback_generate_card(pr_title, body_clean, branch_name, author_username, author_name, diff_loc)


def _infer_task_type(title: str, branch: Optional[str] = "") -> str:
    combined = f"{title} {branch or ''}".lower()
    if any(k in combined for k in ["fix", "bug", "patch", "error", "issue", "hotfix"]):
        return "bugfix"
    elif any(k in combined for k in ["refactor", "cleanup", "reorganize", "perf"]):
        return "refactor"
    elif any(k in combined for k in ["doc", "readme", "spec"]):
        return "docs"
    elif any(k in combined for k in ["chore", "build", "ci", "deps", "test"]):
        return "chore"
    return "feature"


def _infer_priority(title: str, body: str) -> str:
    combined = f"{title} {body}".lower()
    if any(k in combined for k in ["critical", "p0", "blocker", "urgent", "security"]):
        return "Critical"
    elif any(k in combined for k in ["high", "p1", "important", "auth", "payment"]):
        return "High"
    elif any(k in combined for k in ["minor", "low", "typo", "tweak"]):
        return "Low"
    return "Medium"


def _fallback_generate_card(
    pr_title: str,
    pr_body: str,
    branch_name: Optional[str],
    author_username: Optional[str],
    author_name: Optional[str],
    diff_loc: int
) -> Dict[str, Any]:
    task_type = _infer_task_type(pr_title, branch_name)
    priority = _infer_priority(pr_title, pr_body)
    est_hours, story_points = calculate_estimation_from_diff(diff_loc, task_type)

    # Clean conventional commit prefixes like "feat: " or "fix(auth): "
    clean_title = re.sub(r'^(feat|fix|refactor|chore|docs|test)(\([^\)]+\))?:\s*', '', pr_title, flags=re.IGNORECASE).strip()
    if not clean_title:
        clean_title = pr_title

    desc = pr_body.strip() if pr_body.strip() else f"Automated task generated from branch `{branch_name or 'main'}` with {diff_loc} LOC diff."

    return {
        "title": clean_title[:100],
        "description": desc,
        "task_type": task_type,
        "priority": priority,
        "story_points": story_points,
        "estimation_hours": est_hours,
        "assignee_name": author_name or author_username or "Developer",
        "assignee_username": author_username or "developer",
    }
