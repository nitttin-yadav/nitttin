import uuid
from datetime import date, datetime

from pydantic import BaseModel


class StudyPlanCreate(BaseModel):
    subject: str
    goal: str = ""
    start_date: date
    end_date: date | None = None


class StudyPlanResponse(BaseModel):
    id: uuid.UUID
    subject: str
    goal: str
    start_date: date
    end_date: date | None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class StudySessionCreate(BaseModel):
    plan_id: uuid.UUID
    topic: str
    duration_minutes: int = 0
    notes: str = ""


class StudySessionResponse(BaseModel):
    id: uuid.UUID
    plan_id: uuid.UUID
    topic: str
    duration_minutes: int
    notes: str
    completed_at: datetime

    model_config = {"from_attributes": True}
