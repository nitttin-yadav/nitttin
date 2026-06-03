import uuid
from datetime import datetime

from pydantic import BaseModel


class MemoryCreate(BaseModel):
    category: str = "general"
    title: str
    content: str
    tags: list[str] = []
    importance: int = 5


class MemoryUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    category: str | None = None
    tags: list[str] | None = None
    importance: int | None = None


class MemoryResponse(BaseModel):
    id: uuid.UUID
    category: str
    title: str
    content: str
    tags: list[str] | None
    importance: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class NoteCreate(BaseModel):
    title: str
    content: str = ""
    tags: list[str] = []


class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    tags: list[str] | None = None


class NoteResponse(BaseModel):
    id: uuid.UUID
    title: str
    content: str
    tags: list[str] | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
