from datetime import datetime
from sqlalchemy.orm import Session
from app.models.db_models import CardModel, ActivityLogModel

def check_and_update_stale_cards(db: Session, threshold_days: float = 2.0) -> int:
    """
    Scans In Progress cards with active PRs and marks cards stale if inactive for > threshold_days.
    Returns number of newly flagged stale cards.
    """
    now = datetime.utcnow()
    in_progress_cards = db.query(CardModel).filter(
        CardModel.status == "In Progress"
    ).all()

    stale_count = 0
    for card in in_progress_cards:
        ref_time = card.updated_at or card.created_at
        diff_days = (now - ref_time).total_seconds() / 86400.0

        if diff_days >= threshold_days:
            if not card.is_stale_pr:
                card.is_stale_pr = True
                card.days_inactive = round(diff_days, 1)
                stale_count += 1
                
                # Log activity
                log = ActivityLogModel(
                    card_id=card.id,
                    action="alarm_raised",
                    actor="stale_checker",
                    details=f"PR inactive for {round(diff_days, 1)} days (> {threshold_days} days threshold)"
                )
                db.add(log)
        else:
            if card.is_stale_pr:
                card.is_stale_pr = False
                card.days_inactive = 0.0

    db.commit()
    return stale_count
