import uuid
from datetime import datetime

from pydantic import BaseModel


class DeviceCreate(BaseModel):
    name: str
    device_type: str = "arduino"
    ip_address: str = ""


class DeviceResponse(BaseModel):
    id: uuid.UUID
    name: str
    device_type: str
    ip_address: str
    status: str
    last_seen: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class DeviceReadingCreate(BaseModel):
    sensor_type: str
    value: float


class DeviceReadingResponse(BaseModel):
    id: uuid.UUID
    device_id: uuid.UUID
    sensor_type: str
    value: float
    recorded_at: datetime

    model_config = {"from_attributes": True}


class AutomationCreate(BaseModel):
    name: str
    trigger_type: str
    trigger_value: str = ""
    action_type: str
    action_value: str = ""


class AutomationResponse(BaseModel):
    id: uuid.UUID
    name: str
    trigger_type: str
    trigger_value: str
    action_type: str
    action_value: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
