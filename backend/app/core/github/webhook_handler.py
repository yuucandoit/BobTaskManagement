import hmac
import hashlib
import json
import logging
from typing import Dict, Any, Optional, Tuple
from app.config import settings

logger = logging.getLogger(__name__)

def verify_github_signature(payload_body: bytes, signature_header: Optional[str]) -> bool:
    """
    Verifies that the webhook payload came from GitHub using the configured secret.
    If no secret is set (e.g. dev/hackathon testing), returns True.
    """
    secret = settings.GITHUB_WEBHOOK_SECRET
    if not secret:
        return True

    if not signature_header:
        return False

    hash_type, signature = signature_header.split("=")
    if hash_type != "sha256":
        return False

    mac = hmac.new(secret.encode("utf-8"), msg=payload_body, digestmod=hashlib.sha256)
    return hmac.compare_digest(mac.hexdigest(), signature)


def parse_pull_request_event(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extracts key fields from GitHub pull_request event payload.
    """
    action = payload.get("action", "")
    pr = payload.get("pull_request", {})
    repo = payload.get("repository", {})
    sender = payload.get("sender", {})

    pr_number = pr.get("number")
    pr_title = pr.get("title", "")
    pr_body = pr.get("body", "")
    html_url = pr.get("html_url", "")
    merged = pr.get("merged", False)
    state = pr.get("state", "open") # "open", "closed"

    head = pr.get("head", {})
    branch_name = head.get("ref", "")
    head_sha = head.get("sha", "")

    user = pr.get("user", {})
    author_username = user.get("login", sender.get("login", "unknown"))
    author_avatar = user.get("avatar_url", sender.get("avatar_url", ""))

    additions = pr.get("additions", 0)
    deletions = pr.get("deletions", 0)
    diff_loc = additions + deletions

    repo_full_name = repo.get("full_name", "")

    return {
        "action": action,
        "pr_number": pr_number,
        "pr_title": pr_title,
        "pr_body": pr_body,
        "pr_url": html_url,
        "merged": merged,
        "state": state,
        "branch_name": branch_name,
        "commit_sha": head_sha,
        "author_username": author_username,
        "author_avatar": author_avatar,
        "repo_name": repo_full_name,
        "diff_loc": diff_loc,
        "additions": additions,
        "deletions": deletions
    }
