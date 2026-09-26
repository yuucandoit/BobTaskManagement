import json
import logging
import urllib.parse
from fastapi import APIRouter, Request, Header, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.github.webhook_handler import verify_github_signature, parse_pull_request_event
from app.services.card_service import process_github_pr_event

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/webhook", tags=["GitHub Webhook"])

async def handle_webhook_payload(
    request: Request,
    x_github_event: str,
    x_hub_signature_256: str,
    db: Session
):
    body_bytes = await request.body()
    body_str = body_bytes.decode("utf-8", errors="replace").strip()

    # Determine event type (case-insensitive header lookup)
    event_type = (
        x_github_event
        or request.headers.get("X-GitHub-Event")
        or request.headers.get("x-github-event")
        or "unknown"
    ).lower()

    # 1. Verify HMAC Signature if configured
    if not verify_github_signature(body_bytes, x_hub_signature_256):
        logger.warning("Invalid GitHub webhook signature")
        raise HTTPException(status_code=401, detail="Invalid webhook signature")

    # 2. Parse Payload (Support application/json AND application/x-www-form-urlencoded)
    content_type = request.headers.get("content-type", "").lower()
    payload = {}

    try:
        if "application/x-www-form-urlencoded" in content_type or body_str.startswith("payload="):
            if body_str.startswith("payload="):
                raw_json = urllib.parse.unquote_plus(body_str[8:])
            else:
                form_data = urllib.parse.parse_qs(body_str)
                raw_json = form_data.get("payload", ["{}"])[0]
            payload = json.loads(raw_json)
        else:
            payload = json.loads(body_str) if body_str else {}
    except Exception as err:
        logger.error(f"Failed to parse GitHub webhook payload: {err} | Body: {body_str[:200]}")
        raise HTTPException(
            status_code=400,
            detail="Invalid JSON payload. Please ensure Content type in GitHub is set to application/json."
        )

    action = payload.get("action", "")
    repo_name = payload.get("repository", {}).get("full_name", "unknown")
    logger.info(f"GitHub Webhook received: event='{event_type}', action='{action}', repo='{repo_name}'")

    # 3. Handle 'ping' event (initial webhook verification by GitHub)
    if event_type == "ping":
        zen = payload.get("zen", "")
        hook_id = payload.get("hook_id", "")
        return {
            "status": "pong",
            "message": "GitHub Webhook configured successfully! Ready to track cards.",
            "hook_id": hook_id,
            "zen": zen
        }

    # 4. Handle 'pull_request' events (Fitur Wajib #1 & #2)
    elif event_type == "pull_request":
        pr_data = parse_pull_request_event(payload)
        card = process_github_pr_event(db, pr_data)
        return {
            "status": "success",
            "event": event_type,
            "action": pr_data.get("action"),
            "card_id": card.id,
            "card_status": card.status,
            "card_title": card.title,
            "repo_name": pr_data.get("repo_name")
        }

    # 5. Handle any other GitHub events (return 200 OK so GitHub delivery stays green)
    return {
        "status": "received",
        "event": event_type,
        "action": action,
        "message": f"Event '{event_type}' received and acknowledged."
    }


def get_webhook_info_response():
    return {
        "status": "online",
        "service": "Bob Task Management - GitHub Webhook Listener",
        "message": "Listener is active and ready. Send POST requests from GitHub Webhooks (pull_request, push).",
        "supported_events": ["pull_request", "push", "ping"],
        "expected_method": "POST",
        "content_type": "application/json"
    }


# Route handlers supporting GET (browser inspection) and POST (GitHub webhook delivery)
# Also supporting both /github, /github/, and root /webhook endpoints
@router.api_route("/github", methods=["GET", "POST"])
@router.api_route("/github/", methods=["GET", "POST"])
@router.api_route("", methods=["GET", "POST"])
@router.api_route("/", methods=["GET", "POST"])
async def webhook_dispatcher(
    request: Request,
    x_github_event: str = Header(None, alias="X-GitHub-Event"),
    x_hub_signature_256: str = Header(None, alias="X-Hub-Signature-256"),
    db: Session = Depends(get_db)
):
    if request.method == "GET":
        return get_webhook_info_response()

    return await handle_webhook_payload(
        request=request,
        x_github_event=x_github_event,
        x_hub_signature_256=x_hub_signature_256,
        db=db
    )
