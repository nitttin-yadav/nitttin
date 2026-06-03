import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.utils import get_current_user
from app.database import get_db
from app.devices.models import Automation, Device, DeviceReading
from app.devices.schemas import (
    AutomationCreate,
    AutomationResponse,
    DeviceCreate,
    DeviceReadingCreate,
    DeviceReadingResponse,
    DeviceResponse,
)

router = APIRouter(prefix="/api/devices", tags=["Arduino & IoT"])


# ── Devices ────────────────────────────────────────────────────────────

@router.get("/", response_model=list[DeviceResponse])
def list_devices(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Device).filter(Device.user_id == current_user.id).all()


@router.post("/", response_model=DeviceResponse, status_code=201)
def register_device(payload: DeviceCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    dev = Device(user_id=current_user.id, **payload.model_dump())
    db.add(dev)
    db.commit()
    db.refresh(dev)
    return dev


@router.post("/{device_id}/readings", response_model=DeviceReadingResponse, status_code=201)
def post_reading(
    device_id: uuid.UUID,
    payload: DeviceReadingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    dev = db.query(Device).filter(Device.id == device_id, Device.user_id == current_user.id).first()
    if not dev:
        raise HTTPException(404, "Device not found")
    reading = DeviceReading(device_id=dev.id, **payload.model_dump())
    dev.status = "online"
    dev.last_seen = datetime.now(timezone.utc)
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return reading


@router.get("/{device_id}/readings", response_model=list[DeviceReadingResponse])
def get_readings(
    device_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    dev = db.query(Device).filter(Device.id == device_id, Device.user_id == current_user.id).first()
    if not dev:
        raise HTTPException(404, "Device not found")
    return (
        db.query(DeviceReading)
        .filter(DeviceReading.device_id == dev.id)
        .order_by(DeviceReading.recorded_at.desc())
        .limit(100)
        .all()
    )


@router.delete("/{device_id}", status_code=204)
def delete_device(device_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    dev = db.query(Device).filter(Device.id == device_id, Device.user_id == current_user.id).first()
    if not dev:
        raise HTTPException(404, "Device not found")
    db.delete(dev)
    db.commit()


# ── Automations ────────────────────────────────────────────────────────

@router.get("/automations", response_model=list[AutomationResponse])
def list_automations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Automation).filter(Automation.user_id == current_user.id).all()


@router.post("/automations", response_model=AutomationResponse, status_code=201)
def create_automation(
    payload: AutomationCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    auto = Automation(user_id=current_user.id, **payload.model_dump())
    db.add(auto)
    db.commit()
    db.refresh(auto)
    return auto


@router.patch("/automations/{automation_id}/toggle")
def toggle_automation(
    automation_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    auto = db.query(Automation).filter(Automation.id == automation_id, Automation.user_id == current_user.id).first()
    if not auto:
        raise HTTPException(404, "Automation not found")
    auto.is_active = not auto.is_active
    db.commit()
    return {"is_active": auto.is_active}
