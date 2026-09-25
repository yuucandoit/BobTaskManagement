import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.db.database import Base, engine
from app.api.v1 import api_v1_router
from app.core.ai.watsonx_client import watsonx_client

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("kanban-evidence-backend")

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IBM Bob 2.0 — Auto Kanban Evidence Board",
    description="Automated real-time Kanban board powered by GitHub webhooks & IBM watsonx.ai with PR/commit evidence tracking.",
    version="1.0.0"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.CORS_ORIGINS == ["*"] else settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API v1
app.include_router(api_v1_router)

@app.get("/")
def root():
    return {
        "project": "IBM Bob 2.0 Kanban Evidence Board",
        "status": "online",
        "version": "1.0.0",
        "watsonx_active": watsonx_client.is_available(),
        "docs_url": "/docs"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "environment": settings.APP_ENV,
        "watsonx_configured": watsonx_client.is_available()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True)
