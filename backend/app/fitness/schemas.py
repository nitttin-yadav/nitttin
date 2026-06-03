import uuid
from datetime import datetime

from pydantic import BaseModel


class WorkoutCreate(BaseModel):
    workout_type: str
    duration_minutes: int = 0
    calories_burned: int = 0
    notes: str = ""


class WorkoutResponse(BaseModel):
    id: uuid.UUID
    workout_type: str
    duration_minutes: int
    calories_burned: int
    notes: str
    completed_at: datetime

    model_config = {"from_attributes": True}


class WeightLogCreate(BaseModel):
    weight_kg: float


class WeightLogResponse(BaseModel):
    id: uuid.UUID
    weight_kg: float
    recorded_at: datetime

    model_config = {"from_attributes": True}


class WaterLogCreate(BaseModel):
    amount_ml: int


class WaterLogResponse(BaseModel):
    id: uuid.UUID
    amount_ml: int
    recorded_at: datetime

    model_config = {"from_attributes": True}


class SleepLogCreate(BaseModel):
    sleep_start: datetime
    sleep_end: datetime
    quality: int = 5
    notes: str = ""


class SleepLogResponse(BaseModel):
    id: uuid.UUID
    sleep_start: datetime
    sleep_end: datetime
    quality: int
    notes: str

    model_config = {"from_attributes": True}
