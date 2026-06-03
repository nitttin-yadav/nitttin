import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.utils import get_current_user
from app.conversations.ai_engine import get_ai_provider
from app.conversations.models import Conversation, Message
from app.conversations.schemas import (
    ConversationCreate,
    ConversationDetail,
    ConversationResponse,
    MessageCreate,
    MessageResponse,
)
from app.database import get_db

router = APIRouter(prefix="/api/conversations", tags=["Conversations"])


@router.get("/", response_model=list[ConversationResponse])
def list_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(Conversation)
        .filter(Conversation.user_id == current_user.id)
        .order_by(Conversation.updated_at.desc())
        .all()
    )


@router.post("/", response_model=ConversationResponse, status_code=201)
def create_conversation(
    payload: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conv = Conversation(user_id=current_user.id, title=payload.title)
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv


@router.get("/{conversation_id}", response_model=ConversationDetail)
def get_conversation(
    conversation_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conv = db.query(Conversation).filter(
        Conversation.id == conversation_id, Conversation.user_id == current_user.id
    ).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conv


@router.post("/{conversation_id}/messages", response_model=MessageResponse, status_code=201)
def send_message(
    conversation_id: uuid.UUID,
    payload: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conv = db.query(Conversation).filter(
        Conversation.id == conversation_id, Conversation.user_id == current_user.id
    ).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    user_msg = Message(conversation_id=conv.id, role="user", content=payload.content)
    db.add(user_msg)
    db.flush()

    history = [{"role": m.role, "content": m.content} for m in conv.messages]
    history.append({"role": "user", "content": payload.content})

    ai = get_ai_provider()
    ai_text = ai.generate_response(history, language=payload.language)

    ai_msg = Message(conversation_id=conv.id, role="assistant", content=ai_text)
    db.add(ai_msg)
    db.commit()
    db.refresh(ai_msg)
    return ai_msg


@router.delete("/{conversation_id}", status_code=204)
def delete_conversation(
    conversation_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conv = db.query(Conversation).filter(
        Conversation.id == conversation_id, Conversation.user_id == current_user.id
    ).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    db.delete(conv)
    db.commit()
