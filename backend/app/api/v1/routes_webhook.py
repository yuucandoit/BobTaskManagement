import json
import logging
from fastapi import APIRouter, Request, Header, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.github.webhook_handler import verify_github_signature, parse_pull_request_event
from app.services.card_service import process_github_pr_event

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/webhook", tags=["GitHub Webhook"])

@router.post("/github")
async def github_webhook_endpoint(
    request: Request,
    x_github_event: str = Header(None, alias="X-GitHub-Event"),
    x_hub_signature_256: str = Header(None, alias="X-Hub-Signature-256"),
    db: Session = Depends(get_db)
):
    """
    Receives and processes GitHub webhook events (PR opened, synchronize, closed/merged).
    Fulfills Fitur Wajib #1 & #2.
    """
    body_bytes = await request.body()

    # Verify signature
    if not verify_github_signature(body_bytes, x_hub_signature_256):
        logger.warning("Invalid GitHub webhook signature")
        raise HTTPException(status_code=401, detail="Invalid signature")

    try:
        payload = json.loads(body_bytes.decode("utf-8"))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    logger.info(f"Received GitHub webhook event: {x_github_event}, action: {payload.get('action')}")

    if x_github_event == "pull_request":
        pr_data = parse_pull_request_event(payload)
        card = process_github_pr_event(db, pr_data)
        return {
            "status": "success",
            "event": x_github_event,
            "action": pr_data.get("action"),
            "card_id": card.id,
            "card_status": card.status,
            "card_title": card.title
        }

    elif x_github_event == "ping":
        return {"status": "pong", "message": "GitHub Webhook configured successfully"}

    return {"status": "ignored", "event": x_github_event, "reason": "Event not tracked"}
