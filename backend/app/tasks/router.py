import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.utils import get_current_user
from app.database import get_db
from app.tasks.models import CalendarEvent, Goal, Habit, HabitLog, Task
from app.tasks.schemas import (
    CalendarEventCreate,
    CalendarEventResponse,
    GoalCreate,
    GoalResponse,
    GoalUpdate,
    HabitCreate,
    HabitResponse,
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)

router = APIRouter(prefix="/api/tasks", tags=["Task Management"])

# ── Tasks ──────────────────────────────────────────────────────────────

@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    status: str | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = db.query(Task).filter(Task.user_id == current_user.id)
    if status:
        q = q.filter(Task.status == status)
    return q.order_by(Task.created_at.desc()).all()


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(payload: TaskCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = Task(user_id=current_user.id, **payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: uuid.UUID, payload: TaskUpdate,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(404, "Task not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(404, "Task not found")
    db.delete(task)
    db.commit()


# ── Goals ──────────────────────────────────────────────────────────────

@router.get("/goals", response_model=list[GoalResponse])
def list_goals(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Goal).filter(Goal.user_id == current_user.id).order_by(Goal.created_at.desc()).all()


@router.post("/goals", response_model=GoalResponse, status_code=201)
def create_goal(payload: GoalCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    goal = Goal(user_id=current_user.id, **payload.model_dump())
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal


@router.patch("/goals/{goal_id}", response_model=GoalResponse)
def update_goal(
    goal_id: uuid.UUID, payload: GoalUpdate,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    goal = db.query(Goal).filter(Goal.id == goal_id, Goal.user_id == current_user.id).first()
    if not goal:
        raise HTTPException(404, "Goal not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(goal, field, value)
    db.commit()
    db.refresh(goal)
    return goal


# ── Habits ─────────────────────────────────────────────────────────────

@router.get("/habits", response_model=list[HabitResponse])
def list_habits(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Habit).filter(Habit.user_id == current_user.id).all()


@router.post("/habits", response_model=HabitResponse, status_code=201)
def create_habit(payload: HabitCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    habit = Habit(user_id=current_user.id, **payload.model_dump())
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit


@router.post("/habits/{habit_id}/log", status_code=201)
def log_habit(
    habit_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    habit = db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == current_user.id).first()
    if not habit:
        raise HTTPException(404, "Habit not found")
    log = HabitLog(habit_id=habit.id)
    db.add(log)
    habit.streak += 1
    db.commit()
    return {"status": "logged", "streak": habit.streak}


# ── Calendar Events ────────────────────────────────────────────────────

@router.get("/events", response_model=list[CalendarEventResponse])
def list_events(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)
    return (
        db.query(CalendarEvent)
        .filter(CalendarEvent.user_id == current_user.id, CalendarEvent.end_time >= now)
        .order_by(CalendarEvent.start_time)
        .all()
    )


@router.post("/events", response_model=CalendarEventResponse, status_code=201)
def create_event(
    payload: CalendarEventCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    event = CalendarEvent(user_id=current_user.id, **payload.model_dump())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event
