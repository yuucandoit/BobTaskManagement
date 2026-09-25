from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from app.models.db_models import CardModel, EvidenceModel, ActivityLogModel
from app.models.schemas import CardCreate, CardUpdate, EvidenceCreate
from app.core.ai.card_generator import generate_card_from_pr
from app.core.scoring.estimation import check_scope_creep

def get_cards(db: Session, status: Optional[str] = None) -> List[CardModel]:
    query = db.query(CardModel)
    if status:
        query = query.filter(CardModel.status == status)
    return query.order_by(CardModel.updated_at.desc()).all()


def get_card_by_id(db: Session, card_id: int) -> Optional[CardModel]:
    return db.query(CardModel).filter(CardModel.id == card_id).first()


def get_card_by_pr(db: Session, repo_name: str, pr_number: int) -> Optional[CardModel]:
    return db.query(CardModel).filter(
        CardModel.repo_name == repo_name,
        CardModel.pr_number == pr_number
    ).first()


def create_card(db: Session, card_in: CardCreate) -> CardModel:
    db_card = CardModel(
        title=card_in.title,
        description=card_in.description,
        status=card_in.status,
        priority=card_in.priority,
        task_type=card_in.task_type,
        assignee_name=card_in.assignee_name,
        assignee_username=card_in.assignee_username,
        assignee_avatar=card_in.assignee_avatar,
        estimation_hours=card_in.estimation_hours,
        story_points=card_in.story_points,
        diff_loc=card_in.diff_loc,
        is_scope_creep=card_in.is_scope_creep,
        scope_creep_ratio=card_in.scope_creep_ratio,
        is_stale_pr=card_in.is_stale_pr,
        days_inactive=card_in.days_inactive,
        repo_name=card_in.repo_name,
        branch_name=card_in.branch_name,
        pr_number=card_in.pr_number,
        pr_url=card_in.pr_url,
        pr_state=card_in.pr_state,
        origin=card_in.origin
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)

    # Initial evidence if provided
    if card_in.initial_evidence:
        add_evidence_to_card(db, db_card.id, card_in.initial_evidence)

    # Activity log
    add_activity_log(
        db,
        card_id=db_card.id,
        action="card_created",
        actor=card_in.origin or "system",
        details=f"Task card initialized in '{db_card.status}' column"
    )

    db.refresh(db_card)
    return db_card


def update_card(db: Session, card_id: int, card_update: CardUpdate) -> Optional[CardModel]:
    card = get_card_by_id(db, card_id)
    if not card:
        return None

    update_data = card_update.model_dump(exclude_unset=True)
    prev_status = card.status

    for field, value in update_data.items():
        setattr(card, field, value)

    card.updated_at = datetime.utcnow()
    if "status" in update_data and update_data["status"] == "Done" and prev_status != "Done":
        card.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(card)

    if "status" in update_data and update_data["status"] != prev_status:
        add_activity_log(
            db,
            card_id=card.id,
            action="status_changed",
            actor="user",
            details=f"Moved from '{prev_status}' to '{card.status}'"
        )

    return card


def delete_card(db: Session, card_id: int) -> bool:
    card = get_card_by_id(db, card_id)
    if not card:
        return False
    db.delete(card)
    db.commit()
    return True


def add_evidence_to_card(db: Session, card_id: int, evidence_in: EvidenceCreate) -> EvidenceModel:
    db_evidence = EvidenceModel(
        card_id=card_id,
        evidence_type=evidence_in.evidence_type,
        title=evidence_in.title,
        description=evidence_in.description,
        url=evidence_in.url,
        reference_id=evidence_in.reference_id,
        author_username=evidence_in.author_username,
        author_avatar=evidence_in.author_avatar,
        meta_json=evidence_in.meta_json
    )
    db.add(db_evidence)
    db.commit()
    db.refresh(db_evidence)
    return db_evidence


def add_activity_log(db: Session, card_id: int, action: str, actor: str = "system", details: Optional[str] = None):
    log = ActivityLogModel(
        card_id=card_id,
        action=action,
        actor=actor,
        details=details
    )
    db.add(log)
    db.commit()


def process_github_pr_event(db: Session, pr_data: Dict[str, Any]) -> CardModel:
    """
    Core engine handling PR opened, synchronized (commit push), or closed (merged).
    Fulfills Fitur Wajib #1, #2, #3 and Bonus #8.
    """
    action = pr_data.get("action")
    pr_number = pr_data.get("pr_number")
    repo_name = pr_data.get("repo_name")
    pr_url = pr_data.get("pr_url")
    merged = pr_data.get("merged", False)
    author_username = pr_data.get("author_username")
    author_avatar = pr_data.get("author_avatar")
    diff_loc = pr_data.get("diff_loc", 0)

    card = get_card_by_pr(db, repo_name, pr_number)

    # 1. PR MERGED -> AUTO UPDATE TO DONE (Fitur Wajib #2)
    if action == "closed" and merged:
        if not card:
            # Create completed card if somehow missed
            ai_data = generate_card_from_pr(
                pr_title=pr_data.get("pr_title", f"PR #{pr_number}"),
                pr_body=pr_data.get("pr_body"),
                branch_name=pr_data.get("branch_name"),
                author_username=author_username,
                diff_loc=diff_loc
            )
            card = CardModel(
                title=ai_data["title"],
                description=ai_data["description"],
                status="Done",
                priority=ai_data["priority"],
                task_type=ai_data["task_type"],
                assignee_name=ai_data["assignee_name"],
                assignee_username=author_username,
                assignee_avatar=author_avatar,
                estimation_hours=ai_data["estimation_hours"],
                story_points=ai_data["story_points"],
                diff_loc=diff_loc,
                repo_name=repo_name,
                branch_name=pr_data.get("branch_name"),
                pr_number=pr_number,
                pr_url=pr_url,
                pr_state="merged",
                origin="github_pr",
                completed_at=datetime.utcnow()
            )
            db.add(card)
            db.commit()
            db.refresh(card)
        else:
            card.status = "Done"
            card.pr_state = "merged"
            card.completed_at = datetime.utcnow()
            card.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(card)

        # Attach merge evidence
        add_evidence_to_card(db, card.id, EvidenceCreate(
            evidence_type="pr",
            title=f"Merged PR #{pr_number} into main",
            description=f"Pull request merged by {author_username}",
            url=pr_url,
            reference_id=str(pr_number),
            author_username=author_username,
            author_avatar=author_avatar
        ))

        add_activity_log(
            db,
            card_id=card.id,
            action="pr_merged",
            actor=author_username,
            details=f"Pull Request #{pr_number} merged successfully. Card moved to 'Done'."
        )
        return card

    # 2. PR OPENED -> AUTO CREATE CARD IN PROGRESS (Fitur Wajib #1 & #2)
    if not card:
        ai_data = generate_card_from_pr(
            pr_title=pr_data.get("pr_title", f"PR #{pr_number}"),
            pr_body=pr_data.get("pr_body"),
            branch_name=pr_data.get("branch_name"),
            author_username=author_username,
            diff_loc=diff_loc
        )

        is_creep, ratio = check_scope_creep(diff_loc, ai_data["estimation_hours"])

        card = CardModel(
            title=ai_data["title"],
            description=ai_data["description"],
            status="In Progress", # PR is actively being worked on
            priority=ai_data["priority"],
            task_type=ai_data["task_type"],
            assignee_name=ai_data["assignee_name"],
            assignee_username=author_username,
            assignee_avatar=author_avatar,
            estimation_hours=ai_data["estimation_hours"],
            story_points=ai_data["story_points"],
            diff_loc=diff_loc,
            is_scope_creep=is_creep,
            scope_creep_ratio=ratio,
            is_stale_pr=False,
            repo_name=repo_name,
            branch_name=pr_data.get("branch_name"),
            pr_number=pr_number,
            pr_url=pr_url,
            pr_state="open",
            origin="github_pr"
        )
        db.add(card)
        db.commit()
        db.refresh(card)

        # Evidence: PR link (Fitur Wajib #3)
        add_evidence_to_card(db, card.id, EvidenceCreate(
            evidence_type="pr",
            title=f"PR #{pr_number}: {pr_data.get('pr_title')}",
            description=f"Branch: {pr_data.get('branch_name')} (+{pr_data.get('additions', 0)} / -{pr_data.get('deletions', 0)})",
            url=pr_url,
            reference_id=str(pr_number),
            author_username=author_username,
            author_avatar=author_avatar
        ))

        add_activity_log(
            db,
            card_id=card.id,
            action="created",
            actor=author_username,
            details=f"Auto-created card from PR #{pr_number} in 'In Progress' column"
        )

        if is_creep:
            add_activity_log(
                db,
                card_id=card.id,
                action="alarm_raised",
                actor="scope_guard",
                details=f"Scope-creep warning! Diff size ({diff_loc} LOC) is {ratio}x baseline estimation."
            )

        return card

    # 3. EXISTING PR REOPENED OR OPENED AGAIN
    if action in ["opened", "reopened"]:
        card.status = "In Progress"
        card.pr_state = "open"
        card.completed_at = None
        card.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(card)
        add_activity_log(
            db,
            card_id=card.id,
            action="status_changed",
            actor=author_username,
            details=f"PR #{pr_number} reopened/active. Moved to 'In Progress'."
        )
        return card

    # 3. EXISTING PR UPDATED (e.g. new commits pushed / synchronize)
    card.diff_loc = diff_loc
    is_creep, ratio = check_scope_creep(diff_loc, card.estimation_hours or 2.0)
    card.is_scope_creep = is_creep
    card.scope_creep_ratio = ratio
    card.updated_at = datetime.utcnow()
    card.is_stale_pr = False # Activity resets stale timer!
    card.days_inactive = 0.0
    db.commit()
    db.refresh(card)

    commit_sha = pr_data.get("commit_sha")
    if commit_sha:
        short_sha = commit_sha[:7]
        commit_url = f"{pr_url}/commits/{commit_sha}" if pr_url else None
        add_evidence_to_card(db, card.id, EvidenceCreate(
            evidence_type="commit",
            title=f"Commit {short_sha} pushed",
            description=f"Updated branch {pr_data.get('branch_name')}",
            url=commit_url,
            reference_id=short_sha,
            author_username=author_username,
            author_avatar=author_avatar
        ))

    add_activity_log(
        db,
        card_id=card.id,
        action="evidence_attached",
        actor=author_username,
        details=f"Code push updated PR #{pr_number}. Total diff: {diff_loc} LOC."
    )

    return card
