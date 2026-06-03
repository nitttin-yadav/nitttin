from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.utils import get_current_user
from app.database import get_db
from app.fitness.models import SleepLog, WaterLog, WeightLog, Workout
from app.fitness.schemas import (
    SleepLogCreate,
    SleepLogResponse,
    WaterLogCreate,
    WaterLogResponse,
    WeightLogCreate,
    WeightLogResponse,
    WorkoutCreate,
    WorkoutResponse,
)

router = APIRouter(prefix="/api/fitness", tags=["Fitness & Wellness"])


# ── Workouts ───────────────────────────────────────────────────────────

@router.get("/workouts", response_model=list[WorkoutResponse])
def list_workouts(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return (
        db.query(Workout)
        .filter(Workout.user_id == current_user.id)
        .order_by(Workout.completed_at.desc())
        .limit(50)
        .all()
    )


@router.post("/workouts", response_model=WorkoutResponse, status_code=201)
def create_workout(payload: WorkoutCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    w = Workout(user_id=current_user.id, **payload.model_dump())
    db.add(w)
    db.commit()
    db.refresh(w)
    return w


# ── Weight ─────────────────────────────────────────────────────────────

@router.get("/weight", response_model=list[WeightLogResponse])
def list_weight(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return (
        db.query(WeightLog)
        .filter(WeightLog.user_id == current_user.id)
        .order_by(WeightLog.recorded_at.desc())
        .limit(90)
        .all()
    )


@router.post("/weight", response_model=WeightLogResponse, status_code=201)
def log_weight(payload: WeightLogCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    w = WeightLog(user_id=current_user.id, **payload.model_dump())
    db.add(w)
    db.commit()
    db.refresh(w)
    return w


# ── Water ──────────────────────────────────────────────────────────────

@router.get("/water", response_model=list[WaterLogResponse])
def list_water(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    return (
        db.query(WaterLog)
        .filter(WaterLog.user_id == current_user.id, WaterLog.recorded_at >= today)
        .order_by(WaterLog.recorded_at.desc())
        .all()
    )


@router.post("/water", response_model=WaterLogResponse, status_code=201)
def log_water(payload: WaterLogCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    w = WaterLog(user_id=current_user.id, **payload.model_dump())
    db.add(w)
    db.commit()
    db.refresh(w)
    return w


@router.get("/water/today")
def water_today(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    total = (
        db.query(func.coalesce(func.sum(WaterLog.amount_ml), 0))
        .filter(WaterLog.user_id == current_user.id, WaterLog.recorded_at >= today)
        .scalar()
    )
    return {"total_ml": total, "goal_ml": 3000}


# ── Sleep ──────────────────────────────────────────────────────────────

@router.get("/sleep", response_model=list[SleepLogResponse])
def list_sleep(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return (
        db.query(SleepLog)
        .filter(SleepLog.user_id == current_user.id)
        .order_by(SleepLog.sleep_end.desc())
        .limit(30)
        .all()
    )


@router.post("/sleep", response_model=SleepLogResponse, status_code=201)
def log_sleep(payload: SleepLogCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    s = SleepLog(user_id=current_user.id, **payload.model_dump())
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


# ── Dashboard ──────────────────────────────────────────────────────────

@router.get("/dashboard")
def fitness_dashboard(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago = today - timedelta(days=7)

    workouts_this_week = db.query(Workout).filter(
        Workout.user_id == current_user.id, Workout.completed_at >= week_ago
    ).count()
    total_water = (
        db.query(func.coalesce(func.sum(WaterLog.amount_ml), 0))
        .filter(WaterLog.user_id == current_user.id, WaterLog.recorded_at >= today)
        .scalar()
    )
    latest_weight = (
        db.query(WeightLog)
        .filter(WeightLog.user_id == current_user.id)
        .order_by(WeightLog.recorded_at.desc())
        .first()
    )
    latest_sleep = (
        db.query(SleepLog)
        .filter(SleepLog.user_id == current_user.id)
        .order_by(SleepLog.sleep_end.desc())
        .first()
    )

    return {
        "workouts_this_week": workouts_this_week,
        "water_today_ml": total_water,
        "water_goal_ml": 3000,
        "latest_weight_kg": latest_weight.weight_kg if latest_weight else None,
        "latest_sleep_quality": latest_sleep.quality if latest_sleep else None,
    }
