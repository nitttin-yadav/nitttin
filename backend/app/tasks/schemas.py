import uuid
from datetime import date, datetime

from pydantic import BaseModel


# --- Tasks ---
class TaskCreate(BaseModel):
    title: str
    description: str = ""
    priority: str = "medium"
    due_date: date | None = None
    category: str = "general"


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    due_date: date | None = None
    category: str | None = None


class TaskResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    status: str
    priority: str
    due_date: date | None
    category: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# --- Goals ---
class GoalCreate(BaseModel):
    title: str
    description: str = ""
    target_date: date | None = None


class GoalUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    target_date: date | None = None
    progress: float | None = None
    status: str | None = None


class GoalResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    target_date: date | None
    progress: float
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


# --- Habits ---
class HabitCreate(BaseModel):
    title: str
    frequency: str = "daily"


class HabitResponse(BaseModel):
    id: uuid.UUID
    title: str
    frequency: str
    streak: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# --- Calendar Events ---
class CalendarEventCreate(BaseModel):
    title: str
    description: str = ""
    start_time: datetime
    end_time: datetime
    location: str = ""


class CalendarEventResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    location: str
    created_at: datetime

    model_config = {"from_attributes": True}
