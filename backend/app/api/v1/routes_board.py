from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.schemas import BoardResponse
from app.services.board_service import get_board_state

router = APIRouter(prefix="/board", tags=["Board"])

@router.get("", response_model=BoardResponse)
def get_board(
    repo: Optional[str] = Query(None, description="Filter cards by GitHub repo full name or 'all'"),
    db: Session = Depends(get_db)
):
    """
    Get full Kanban board state grouped into To Do, In Progress, and Done,
    along with team stats and evidence summary, with optional multi-repo filtering.
    """
    return get_board_state(db, repo_name=repo)
