from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.schemas import BoardResponse
from app.services.board_service import get_board_state

router = APIRouter(prefix="/board", tags=["Board"])

@router.get("", response_model=BoardResponse)
def get_board(db: Session = Depends(get_db)):
    """
    Get full Kanban board state grouped into To Do, In Progress, and Done,
    along with team stats and evidence summary.
    """
    return get_board_state(db)
