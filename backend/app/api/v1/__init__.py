from fastapi import APIRouter
from app.api.v1.routes_board import router as board_router
from app.api.v1.routes_cards import router as cards_router
from app.api.v1.routes_chat import router as chat_router
from app.api.v1.routes_webhook import router as webhook_router
from app.api.v1.routes_demo import router as demo_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(board_router)
api_v1_router.include_router(cards_router)
api_v1_router.include_router(chat_router)
api_v1_router.include_router(webhook_router)
api_v1_router.include_router(demo_router)

__all__ = ["api_v1_router"]
