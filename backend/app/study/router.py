import uuid
from datetime import timedelta, datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.utils import get_current_user
from app.database import get_db
from app.study.models import StudyPlan, StudySession
from app.study.schemas import (
    StudyPlanCreate,
    StudyPlanResponse,
    StudySessionCreate,
    StudySessionResponse,
)

router = APIRouter(prefix="/api/study", tags=["Study & Career"])


@router.get("/plans", response_model=list[StudyPlanResponse])
def list_plans(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(StudyPlan).filter(StudyPlan.user_id == current_user.id).order_by(StudyPlan.created_at.desc()).all()


@router.post("/plans", response_model=StudyPlanResponse, status_code=201)
def create_plan(payload: StudyPlanCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    plan = StudyPlan(user_id=current_user.id, **payload.model_dump())
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


@router.get("/plans/{plan_id}", response_model=StudyPlanResponse)
def get_plan(plan_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    plan = db.query(StudyPlan).filter(StudyPlan.id == plan_id, StudyPlan.user_id == current_user.id).first()
    if not plan:
        raise HTTPException(404, "Plan not found")
    return plan


@router.post("/sessions", response_model=StudySessionResponse, status_code=201)
def log_session(payload: StudySessionCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    plan = db.query(StudyPlan).filter(StudyPlan.id == payload.plan_id, StudyPlan.user_id == current_user.id).first()
    if not plan:
        raise HTTPException(404, "Plan not found")
    sess = StudySession(user_id=current_user.id, **payload.model_dump())
    db.add(sess)
    db.commit()
    db.refresh(sess)
    return sess


@router.get("/sessions", response_model=list[StudySessionResponse])
def list_sessions(
    plan_id: uuid.UUID | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = db.query(StudySession).filter(StudySession.user_id == current_user.id)
    if plan_id:
        q = q.filter(StudySession.plan_id == plan_id)
    return q.order_by(StudySession.completed_at.desc()).limit(50).all()


@router.get("/dashboard")
def study_dashboard(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    active_plans = db.query(StudyPlan).filter(
        StudyPlan.user_id == current_user.id, StudyPlan.status == "active"
    ).count()
    total_hours_week = (
        db.query(func.coalesce(func.sum(StudySession.duration_minutes), 0))
        .filter(StudySession.user_id == current_user.id, StudySession.completed_at >= week_ago)
        .scalar()
    ) / 60.0
    sessions_week = db.query(StudySession).filter(
        StudySession.user_id == current_user.id, StudySession.completed_at >= week_ago
    ).count()

    return {
        "active_plans": active_plans,
        "study_hours_this_week": round(total_hours_week, 1),
        "sessions_this_week": sessions_week,
    }
