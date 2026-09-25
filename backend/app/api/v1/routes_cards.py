from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.schemas import CardResponse, CardCreate, CardUpdate, EvidenceResponse, EvidenceCreate
from app.services import card_service

router = APIRouter(prefix="/cards", tags=["Cards"])

@router.get("", response_model=List[CardResponse])
def list_cards(status: Optional[str] = None, db: Session = Depends(get_db)):
    """List all cards, optionally filtered by status ('To Do', 'In Progress', 'Done')."""
    return card_service.get_cards(db, status=status)


@router.post("", response_model=CardResponse, status_code=status.HTTP_201_CREATED)
def create_new_card(card_in: CardCreate, db: Session = Depends(get_db)):
    """Create a new card manually."""
    return card_service.create_card(db, card_in)


@router.get("/{card_id}", response_model=CardResponse)
def get_card(card_id: int, db: Session = Depends(get_db)):
    """Get card details including attached evidence links and activity logs."""
    card = card_service.get_card_by_id(db, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card


@router.put("/{card_id}", response_model=CardResponse)
def update_existing_card(card_id: int, card_update: CardUpdate, db: Session = Depends(get_db)):
    """Update card status, assignee, priority, or estimations."""
    card = card_service.update_card(db, card_id, card_update)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card


@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_card(card_id: int, db: Session = Depends(get_db)):
    """Delete a card and its cascade dependencies."""
    success = card_service.delete_card(db, card_id)
    if not success:
        raise HTTPException(status_code=404, detail="Card not found")
    return None


@router.post("/{card_id}/evidence", response_model=EvidenceResponse, status_code=status.HTTP_201_CREATED)
def attach_evidence(card_id: int, evidence_in: EvidenceCreate, db: Session = Depends(get_db)):
    """Attach evidence (PR link, commit, CI verification) to a card."""
    card = card_service.get_card_by_id(db, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    evidence = card_service.add_evidence_to_card(db, card_id, evidence_in)
    card_service.add_activity_log(
        db,
        card_id=card_id,
        action="evidence_attached",
        actor=evidence_in.author_username or "user",
        details=f"Evidence '{evidence_in.title}' manually attached."
    )
    return evidence
