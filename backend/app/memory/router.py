import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.utils import get_current_user
from app.database import get_db
from app.memory.models import Memory, Note
from app.memory.schemas import (
    MemoryCreate,
    MemoryResponse,
    MemoryUpdate,
    NoteCreate,
    NoteResponse,
    NoteUpdate,
)

router = APIRouter(prefix="/api/memory", tags=["Memory System"])

# ── Memories ───────────────────────────────────────────────────────────

@router.get("/", response_model=list[MemoryResponse])
def list_memories(
    search: str | None = None,
    category: str | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = db.query(Memory).filter(Memory.user_id == current_user.id)
    if category:
        q = q.filter(Memory.category == category)
    if search:
        pattern = f"%{search}%"
        q = q.filter(or_(Memory.title.ilike(pattern), Memory.content.ilike(pattern)))
    return q.order_by(Memory.importance.desc(), Memory.updated_at.desc()).all()


@router.post("/", response_model=MemoryResponse, status_code=201)
def create_memory(payload: MemoryCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    mem = Memory(user_id=current_user.id, **payload.model_dump())
    db.add(mem)
    db.commit()
    db.refresh(mem)
    return mem


@router.patch("/{memory_id}", response_model=MemoryResponse)
def update_memory(
    memory_id: uuid.UUID, payload: MemoryUpdate,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    mem = db.query(Memory).filter(Memory.id == memory_id, Memory.user_id == current_user.id).first()
    if not mem:
        raise HTTPException(404, "Memory not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(mem, field, value)
    db.commit()
    db.refresh(mem)
    return mem


@router.delete("/{memory_id}", status_code=204)
def delete_memory(memory_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    mem = db.query(Memory).filter(Memory.id == memory_id, Memory.user_id == current_user.id).first()
    if not mem:
        raise HTTPException(404, "Memory not found")
    db.delete(mem)
    db.commit()


# ── Notes ──────────────────────────────────────────────────────────────

@router.get("/notes", response_model=list[NoteResponse])
def list_notes(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Note).filter(Note.user_id == current_user.id).order_by(Note.updated_at.desc()).all()


@router.post("/notes", response_model=NoteResponse, status_code=201)
def create_note(payload: NoteCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    note = Note(user_id=current_user.id, **payload.model_dump())
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.patch("/notes/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: uuid.UUID, payload: NoteUpdate,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    if not note:
        raise HTTPException(404, "Note not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(note, field, value)
    db.commit()
    db.refresh(note)
    return note
