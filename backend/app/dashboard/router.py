from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.utils import get_current_user
from app.database import get_db
from app.devices.models import Device
from app.finance.models import Expense
from app.fitness.models import WaterLog, Workout
from app.memory.models import Note
from app.study.models import StudyPlan, StudySession
from app.tasks.models import CalendarEvent, Goal, Task

router = APIRouter(prefix="/api/dashboard", tags=["Life OS Dashboard"])


@router.get("/")
def get_dashboard(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago = today - timedelta(days=7)

    # Tasks
    pending_tasks = db.query(Task).filter(
        Task.user_id == current_user.id, Task.status == "pending"
    ).count()
    today_tasks = db.query(Task).filter(
        Task.user_id == current_user.id, Task.due_date == today.date()
    ).count()

    # Goals
    active_goals = db.query(Goal).filter(
        Goal.user_id == current_user.id, Goal.status == "active"
    ).count()

    # Study
    study_hours_week = (
        db.query(func.coalesce(func.sum(StudySession.duration_minutes), 0))
        .filter(StudySession.user_id == current_user.id, StudySession.completed_at >= week_ago)
        .scalar()
    ) / 60.0
    active_study_plans = db.query(StudyPlan).filter(
        StudyPlan.user_id == current_user.id, StudyPlan.status == "active"
    ).count()

    # Fitness
    workouts_week = db.query(Workout).filter(
        Workout.user_id == current_user.id, Workout.completed_at >= week_ago
    ).count()
    water_today = (
        db.query(func.coalesce(func.sum(WaterLog.amount_ml), 0))
        .filter(WaterLog.user_id == current_user.id, WaterLog.recorded_at >= today)
        .scalar()
    )

    # Finance
    month_expenses = (
        db.query(func.coalesce(func.sum(Expense.amount), 0.0))
        .filter(
            Expense.user_id == current_user.id,
            extract("month", Expense.expense_date) == now.month,
            extract("year", Expense.expense_date) == now.year,
        )
        .scalar()
    )

    # Notes
    total_notes = db.query(Note).filter(Note.user_id == current_user.id).count()

    # Upcoming events
    upcoming_events = (
        db.query(CalendarEvent)
        .filter(CalendarEvent.user_id == current_user.id, CalendarEvent.start_time >= now)
        .order_by(CalendarEvent.start_time)
        .limit(5)
        .all()
    )

    # Devices
    online_devices = db.query(Device).filter(
        Device.user_id == current_user.id, Device.status == "online"
    ).count()
    total_devices = db.query(Device).filter(Device.user_id == current_user.id).count()

    return {
        "greeting": f"Welcome back, {current_user.full_name or current_user.username}!",
        "tasks": {"pending": pending_tasks, "due_today": today_tasks},
        "goals": {"active": active_goals},
        "study": {
            "hours_this_week": round(study_hours_week, 1),
            "active_plans": active_study_plans,
        },
        "fitness": {"workouts_this_week": workouts_week, "water_today_ml": water_today, "water_goal_ml": 3000},
        "finance": {"month_spent": round(month_expenses, 2)},
        "notes": {"total": total_notes},
        "upcoming_events": [
            {"title": e.title, "start": e.start_time.isoformat(), "location": e.location}
            for e in upcoming_events
        ],
        "devices": {"online": online_devices, "total": total_devices},
    }
