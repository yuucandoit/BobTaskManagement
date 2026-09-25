from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.db_models import CardModel, EvidenceModel, ActivityLogModel
from app.models.schemas import DemoSimulatePRRequest, CardResponse
from app.services.card_service import process_github_pr_event, add_activity_log, add_evidence_to_card
from app.models.schemas import EvidenceCreate
from app.core.scheduler.stale_pr_checker import check_and_update_stale_cards

router = APIRouter(prefix="/demo", tags=["Pitch Demo Simulator"])

@router.post("/simulate-pr-opened", response_model=CardResponse)
def simulate_pr_opened(req: Optional[DemoSimulatePRRequest] = None, db: Session = Depends(get_db)):
    """
    Pitch Demo Trigger: Simulates developer opening a new Pull Request.
    Card is auto-created and placed in 'In Progress' with PR Evidence link.
    """
    if req is None:
        # Check if PR 42 is already Done; if so, dynamically create next PR
        existing_42 = db.query(CardModel).filter(
            CardModel.repo_name == "ibm-bob/smart-tracker",
            CardModel.pr_number == 42
        ).first()

        if existing_42 and existing_42.status == "Done":
            from sqlalchemy import func
            max_pr = db.query(func.max(CardModel.pr_number)).filter(
                CardModel.repo_name == "ibm-bob/smart-tracker"
            ).scalar() or 42
            next_num = max_pr + 1
            demo_variants = [
                ("feat(ai): watsonx.ai auto-tagging and risk analysis engine", "Implements automated risk estimation and tag generation using IBM Granite LLM.", "feat/watsonx-tagging"),
                ("fix(cache): resolve race condition in distributed session lock", "Replaces optimistic token lock with Redis redlock consensus.", "fix/redis-lock"),
                ("feat(metrics): add real-time sprint velocity charts", "Exposes telemetry endpoint for team sprint progress and burndown metrics.", "feat/metrics-chart"),
            ]
            picked = demo_variants[(next_num - 43) % len(demo_variants)]
            req = DemoSimulatePRRequest(
                pr_number=next_num,
                title=picked[0],
                description=picked[1],
                branch_name=picked[2]
            )
        else:
            req = DemoSimulatePRRequest()

    pr_data = {
        "action": "opened",
        "pr_number": req.pr_number,
        "pr_title": req.title,
        "pr_body": req.description,
        "pr_url": f"https://github.com/{req.repo_name}/pull/{req.pr_number}",
        "merged": False,
        "state": "open",
        "branch_name": req.branch_name,
        "commit_sha": "a8f3d1b94c8e721",
        "author_username": req.author_username,
        "author_avatar": f"https://api.dicebear.com/7.x/bottts/svg?seed={req.author_username}",
        "repo_name": req.repo_name,
        "diff_loc": req.additions + req.deletions,
        "additions": req.additions,
        "deletions": req.deletions
    }

    card = process_github_pr_event(db, pr_data)
    return card


@router.post("/simulate-commit-push", response_model=CardResponse)
def simulate_commit_push(
    pr_number: int = 42,
    repo_name: str = "ibm-bob/smart-tracker",
    additional_loc: int = 280,
    db: Session = Depends(get_db)
):
    """
    Pitch Demo Trigger: Simulates developer pushing more commits.
    Demonstrates evidence log update and scope-creep alarm detection.
    """
    pr_data = {
        "action": "synchronize",
        "pr_number": pr_number,
        "pr_title": "feat(auth): Add IBM Cloud SSO & OAuth2 session verification",
        "pr_body": "Updated with extensive migration scripts and token storage",
        "pr_url": f"https://github.com/{repo_name}/pull/{pr_number}",
        "merged": False,
        "state": "open",
        "branch_name": "feat/ibm-sso-auth",
        "commit_sha": "c4d7e9f12345678",
        "author_username": "firza-dev",
        "author_avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=firza-dev",
        "repo_name": repo_name,
        "diff_loc": 209 + additional_loc, # Exceeds baseline to trigger scope creep
        "additions": 185 + additional_loc,
        "deletions": 24
    }

    card = process_github_pr_event(db, pr_data)
    return card


@router.post("/simulate-pr-merged", response_model=CardResponse)
def simulate_pr_merged(
    pr_number: int = 42,
    repo_name: str = "ibm-bob/smart-tracker",
    db: Session = Depends(get_db)
):
    """
    Pitch Demo Trigger: Simulates developer merging PR to main.
    The card dynamically moves from 'In Progress' to 'Done'.
    """
    # Smart merge: find active in-progress PR card if 42 already done
    target_card = db.query(CardModel).filter(
        CardModel.repo_name == repo_name,
        CardModel.pr_number == pr_number
    ).first()

    if not target_card or target_card.status != "In Progress":
        active_pr_card = db.query(CardModel).filter(
            CardModel.status == "In Progress",
            CardModel.pr_number.isnot(None)
        ).order_by(CardModel.updated_at.desc()).first()
        if active_pr_card and active_pr_card.pr_number:
            pr_number = active_pr_card.pr_number
            target_card = active_pr_card

    pr_title = target_card.title if target_card else "Add IBM Cloud SSO & OAuth2 session verification"
    branch_name = target_card.branch_name if target_card else "feat/ibm-sso-auth"

    pr_data = {
        "action": "closed",
        "pr_number": pr_number,
        "pr_title": pr_title,
        "pr_body": "All reviews passed, merging to main branch.",
        "pr_url": f"https://github.com/{repo_name}/pull/{pr_number}",
        "merged": True,
        "state": "closed",
        "branch_name": branch_name,
        "commit_sha": "f9e8d7c6b5a4321",
        "author_username": "firza-dev",
        "author_avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=firza-dev",
        "repo_name": repo_name,
        "diff_loc": 209,
        "additions": 185,
        "deletions": 24
    }

    card = process_github_pr_event(db, pr_data)
    return card


@router.post("/simulate-stale-alarm")
def simulate_stale_alarm(
    card_id: Optional[int] = None,
    days_back: float = 3.5,
    db: Session = Depends(get_db)
):
    """
    Pitch Demo Trigger: Backdates an In Progress card to trigger the >2 days Stale PR Alarm (Bonus #6).
    """
    query = db.query(CardModel).filter(CardModel.status == "In Progress")
    if card_id:
        target_card = query.filter(CardModel.id == card_id).first()
    else:
        target_card = query.first()

    if not target_card:
        return {"status": "error", "message": "No 'In Progress' card available to simulate stale PR. Open a PR first."}

    past_date = datetime.utcnow() - timedelta(days=days_back)
    target_card.updated_at = past_date
    target_card.created_at = past_date - timedelta(hours=4)
    db.commit()

    flagged_count = check_and_update_stale_cards(db, threshold_days=2.0)
    db.refresh(target_card)

    return {
        "status": "success",
        "message": f"Card #{target_card.id} backdated by {days_back} days. Stale alarm active!",
        "card_id": target_card.id,
        "is_stale_pr": target_card.is_stale_pr,
        "days_inactive": target_card.days_inactive
    }


@router.post("/seed-sample-data")
def seed_sample_data(db: Session = Depends(get_db)):
    """
    Populates sample demo data covering To Do, In Progress (with evidence & alarms), and Done.
    """
    db.query(ActivityLogModel).delete()
    db.query(EvidenceModel).delete()
    db.query(CardModel).delete()
    db.commit()

    # 1. To Do Card (Created via chat)
    c1 = CardModel(
        title="Refactor Session Cache for Redis Cluster",
        description="Migrate in-memory token cache to distributed Redis to handle multi-region failover.",
        status="To Do",
        priority="Medium",
        task_type="refactor",
        assignee_name="Ahmad Rizky",
        assignee_username="ahmadrizky",
        assignee_avatar="https://api.dicebear.com/7.x/bottts/svg?seed=ahmadrizky",
        estimation_hours=3.5,
        story_points=3,
        origin="chat"
    )
    db.add(c1)
    db.commit()
    db.refresh(c1)
    add_activity_log(db, c1.id, "created", "pm_chat", "Card created from PM chat instruction")

    # 2. In Progress Card (Normal PR with evidence)
    c2 = CardModel(
        title="Integrate watsonx.ai Granite 13B Model Engine",
        description="Connect backend services to IBM watsonx.ai REST endpoints for automatic card synthesis.",
        status="In Progress",
        priority="High",
        task_type="feature",
        assignee_name="Firza Pratama",
        assignee_username="firza-dev",
        assignee_avatar="https://api.dicebear.com/7.x/bottts/svg?seed=firza-dev",
        estimation_hours=4.0,
        story_points=5,
        diff_loc=240,
        repo_name="ibm-bob/smart-tracker",
        branch_name="feat/watsonx-engine",
        pr_number=88,
        pr_url="https://github.com/ibm-bob/smart-tracker/pull/88",
        pr_state="open",
        origin="github_pr"
    )
    db.add(c2)
    db.commit()
    db.refresh(c2)

    add_evidence_to_card(db, c2.id, EvidenceCreate(
        evidence_type="pr",
        title="PR #88: Integrate watsonx.ai Granite 13B Model Engine",
        description="Branch feat/watsonx-engine (+195 / -45)",
        url="https://github.com/ibm-bob/smart-tracker/pull/88",
        reference_id="88",
        author_username="firza-dev",
        author_avatar="https://api.dicebear.com/7.x/bottts/svg?seed=firza-dev"
    ))
    add_activity_log(db, c2.id, "created", "firza-dev", "Auto-created from PR #88")

    # 3. In Progress Card with Stale Alarm (Bonus #6)
    c3 = CardModel(
        title="Fix Null Pointer in Payment Webhook Callback",
        description="Edge-case null check when payment gateway transmits empty metadata array.",
        status="In Progress",
        priority="Critical",
        task_type="bugfix",
        assignee_name="Budi Santoso",
        assignee_username="budisantoso",
        assignee_avatar="https://api.dicebear.com/7.x/bottts/svg?seed=budisantoso",
        estimation_hours=1.5,
        story_points=2,
        diff_loc=48,
        is_stale_pr=True,
        days_inactive=2.8,
        repo_name="ibm-bob/smart-tracker",
        branch_name="fix/payment-null-check",
        pr_number=74,
        pr_url="https://github.com/ibm-bob/smart-tracker/pull/74",
        pr_state="open",
        origin="github_pr",
        updated_at=datetime.utcnow() - timedelta(days=2.8)
    )
    db.add(c3)
    db.commit()
    db.refresh(c3)

    add_evidence_to_card(db, c3.id, EvidenceCreate(
        evidence_type="pr",
        title="PR #74: Fix Null Pointer in Payment Webhook",
        description="No commit updates for 2.8 days",
        url="https://github.com/ibm-bob/smart-tracker/pull/74",
        reference_id="74",
        author_username="budisantoso",
        author_avatar="https://api.dicebear.com/7.x/bottts/svg?seed=budisantoso"
    ))
    add_activity_log(db, c3.id, "alarm_raised", "stale_checker", "PR idle for >2 days alert")

    # 4. Done Card (Auto-moved on PR merge)
    c4 = CardModel(
        title="Setup React Kanban Dashboard & Tailwind Layout",
        description="Construct responsive Kanban board with 3 status columns, dark mode, and evidence badges.",
        status="Done",
        priority="High",
        task_type="feature",
        assignee_name="Siti Nurhaliza",
        assignee_username="siti-ui",
        assignee_avatar="https://api.dicebear.com/7.x/bottts/svg?seed=siti-ui",
        estimation_hours=3.0,
        story_points=3,
        diff_loc=310,
        repo_name="ibm-bob/smart-tracker",
        branch_name="feat/kanban-dashboard-ui",
        pr_number=61,
        pr_url="https://github.com/ibm-bob/smart-tracker/pull/61",
        pr_state="merged",
        origin="github_pr",
        completed_at=datetime.utcnow() - timedelta(hours=6)
    )
    db.add(c4)
    db.commit()
    db.refresh(c4)

    add_evidence_to_card(db, c4.id, EvidenceCreate(
        evidence_type="pr",
        title="PR #61: Setup React Kanban Dashboard Layout (Merged)",
        description="Merged into main branch by siti-ui",
        url="https://github.com/ibm-bob/smart-tracker/pull/61",
        reference_id="61",
        author_username="siti-ui",
        author_avatar="https://api.dicebear.com/7.x/bottts/svg?seed=siti-ui"
    ))
    add_activity_log(db, c4.id, "pr_merged", "siti-ui", "PR #61 merged! Moved to Done.")

    return {"status": "success", "message": "Sample seed data successfully loaded!"}


@router.post("/reset")
def reset_board(db: Session = Depends(get_db)):
    """Wipes board database to clean state for fresh demo."""
    db.query(ActivityLogModel).delete()
    db.query(EvidenceModel).delete()
    db.query(CardModel).delete()
    db.commit()
    return {"status": "success", "message": "Board successfully reset."}
