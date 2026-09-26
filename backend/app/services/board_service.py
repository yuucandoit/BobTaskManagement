from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.models.db_models import CardModel, EvidenceModel
from app.models.schemas import BoardResponse, BoardColumn, CardResponse

def get_board_state(db: Session, repo_name: Optional[str] = None) -> BoardResponse:
    """
    Aggregates cards into the Kanban 3-column view (To Do, In Progress, Done)
    along with team stats, evidence summary, and multi-repo filtering.
    """
    # Discover all distinct connected repositories
    distinct_repos = [
        r[0] for r in db.query(CardModel.repo_name).distinct().all() if r[0]
    ]

    query = db.query(CardModel)
    if repo_name and repo_name.strip() and repo_name != "all":
        query = query.filter(CardModel.repo_name == repo_name.strip())

    all_cards = query.order_by(CardModel.updated_at.desc()).all()

    to_do_cards: List[CardResponse] = []
    in_progress_cards: List[CardResponse] = []
    done_cards: List[CardResponse] = []

    stale_count = 0
    scope_creep_count = 0
    assignees_set = set()

    for card in all_cards:
        card_dto = CardResponse.model_validate(card)
        if card.status == "To Do":
            to_do_cards.append(card_dto)
        elif card.status == "In Progress":
            in_progress_cards.append(card_dto)
            if card.is_stale_pr:
                stale_count += 1
            if card.is_scope_creep:
                scope_creep_count += 1
        elif card.status == "Done":
            done_cards.append(card_dto)

        if card.assignee_name:
            assignees_set.add(card.assignee_name)

    total_evidences = db.query(EvidenceModel).count()

    columns: Dict[str, BoardColumn] = {
        "to_do": BoardColumn(
            id="to_do",
            title="To Do",
            count=len(to_do_cards),
            cards=to_do_cards
        ),
        "in_progress": BoardColumn(
            id="in_progress",
            title="In Progress",
            count=len(in_progress_cards),
            cards=in_progress_cards
        ),
        "done": BoardColumn(
            id="done",
            title="Done",
            count=len(done_cards),
            cards=done_cards
        )
    }

    return BoardResponse(
        total_cards=len(all_cards),
        columns=columns,
        stats={
            "stale_pr_alerts": stale_count,
            "scope_creep_alerts": scope_creep_count,
            "active_devs": len(assignees_set),
            "total_evidences": total_evidences,
            "completion_rate": round((len(done_cards) / len(all_cards) * 100), 1) if all_cards else 0.0,
            "available_repos": distinct_repos,
            "selected_repo": repo_name or "all"
        }
    )
