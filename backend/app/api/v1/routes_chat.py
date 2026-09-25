from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.schemas import ChatRequest, ChatResponse, CardCreate
from app.core.ai.chat_parser import parse_chat_to_card
from app.services import card_service

router = APIRouter(prefix="/chat", tags=["AI Chat Assistant"])

@router.post("", response_model=ChatResponse)
def handle_chat_instruction(req: ChatRequest, db: Session = Depends(get_db)):
    """
    Fitur Wajib #4: Chat-based manual card creation.
    Processes natural language commands from PM, extracts task metadata using watsonx.ai,
    creates the card in the board, and returns a friendly confirmation.
    """
    message = req.message.strip()
    extracted = parse_chat_to_card(message, req.context_repo)

    # Create the card in the board (default to "To Do")
    card_in = CardCreate(
        title=extracted.title,
        description=extracted.description,
        status=extracted.target_column or "To Do",
        priority=extracted.priority,
        task_type=extracted.task_type,
        assignee_name=extracted.assignee_name if extracted.assignee_name != "Unassigned" else None,
        estimation_hours=extracted.estimation_hours,
        story_points=2 if extracted.estimation_hours <= 2 else 3,
        origin="chat"
    )

    created_card = card_service.create_card(db, card_in)

    # Construct user-friendly conversational reply
    assignee_str = f" to **{extracted.assignee_name}**" if extracted.assignee_name else ""
    reply = (
        f"✅ Kartu **\"{extracted.title}\"** berhasil dibuat dan ditaruh di kolom **{created_card.status}**!\n"
        f"- Tipe: `{extracted.task_type}`\n"
        f"- Prioritas: `{extracted.priority}`\n"
        f"- Estimasi: `{extracted.estimation_hours} jam`\n"
        f"- Assignee: `{extracted.assignee_name or 'Belum di-assign'}`"
    )

    return ChatResponse(
        reply=reply,
        card_created=created_card,
        extracted_data=extracted
    )
