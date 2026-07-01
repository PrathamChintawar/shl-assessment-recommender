"""
api.py

FastAPI routes.
"""

from fastapi import APIRouter

from app.models import (
    ChatRequest,
    ChatResponse,
)

from app.chatbot import chatbot


router = APIRouter()


# -----------------------------------------------------
# Health Check
# -----------------------------------------------------

@router.get("/health")
def health():

    return {
        "status": "ok"
    }


# -----------------------------------------------------
# Chat Endpoint
# -----------------------------------------------------

@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):

    messages = [
        {
            "role": msg.role,
            "content": msg.content,
        }
        for msg in request.messages
    ]

    response = chatbot.chat(messages)

    return response