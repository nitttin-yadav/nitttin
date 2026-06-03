import uuid
from datetime import date, datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.utils import get_current_user
from app.database import get_db
from app.finance.models import Budget, Expense, SavingsGoal
from app.finance.schemas import (
    BudgetCreate,
    BudgetResponse,
    ExpenseCreate,
    ExpenseResponse,
    SavingsGoalCreate,
    SavingsGoalResponse,
    SavingsGoalUpdate,
)

router = APIRouter(prefix="/api/finance", tags=["Finance Dashboard"])


# ── Expenses ───────────────────────────────────────────────────────────

@router.get("/expenses", response_model=list[ExpenseResponse])
def list_expenses(
    month: int | None = None,
    year: int | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = db.query(Expense).filter(Expense.user_id == current_user.id)
    now = datetime.now(timezone.utc)
    m = month or now.month
    y = year or now.year
    q = q.filter(extract("month", Expense.expense_date) == m, extract("year", Expense.expense_date) == y)
    return q.order_by(Expense.expense_date.desc()).all()


@router.post("/expenses", response_model=ExpenseResponse, status_code=201)
def create_expense(payload: ExpenseCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    exp = Expense(user_id=current_user.id, **payload.model_dump())
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp


@router.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    exp = db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == current_user.id).first()
    if not exp:
        raise HTTPException(404, "Expense not found")
    db.delete(exp)
    db.commit()


# ── Budgets ────────────────────────────────────────────────────────────

@router.get("/budgets", response_model=list[BudgetResponse])
def list_budgets(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Budget).filter(Budget.user_id == current_user.id).all()


@router.post("/budgets", response_model=BudgetResponse, status_code=201)
def create_budget(payload: BudgetCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    b = Budget(user_id=current_user.id, **payload.model_dump())
    db.add(b)
    db.commit()
    db.refresh(b)
    return b


# ── Savings Goals ──────────────────────────────────────────────────────

@router.get("/savings", response_model=list[SavingsGoalResponse])
def list_savings(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(SavingsGoal).filter(SavingsGoal.user_id == current_user.id).all()


@router.post("/savings", response_model=SavingsGoalResponse, status_code=201)
def create_savings_goal(payload: SavingsGoalCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    sg = SavingsGoal(user_id=current_user.id, **payload.model_dump())
    db.add(sg)
    db.commit()
    db.refresh(sg)
    return sg


@router.patch("/savings/{goal_id}", response_model=SavingsGoalResponse)
def update_savings_goal(
    goal_id: uuid.UUID, payload: SavingsGoalUpdate,
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db),
):
    sg = db.query(SavingsGoal).filter(SavingsGoal.id == goal_id, SavingsGoal.user_id == current_user.id).first()
    if not sg:
        raise HTTPException(404, "Savings goal not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(sg, field, value)
    db.commit()
    db.refresh(sg)
    return sg


# ── Monthly Report ─────────────────────────────────────────────────────

@router.get("/report")
def monthly_report(
    month: int | None = None,
    year: int | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    now = datetime.now(timezone.utc)
    m = month or now.month
    y = year or now.year

    expenses = (
        db.query(Expense.category, func.sum(Expense.amount))
        .filter(
            Expense.user_id == current_user.id,
            extract("month", Expense.expense_date) == m,
            extract("year", Expense.expense_date) == y,
        )
        .group_by(Expense.category)
        .all()
    )

    total = sum(amt for _, amt in expenses)
    breakdown = {cat: amt for cat, amt in expenses}

    budgets = db.query(Budget).filter(Budget.user_id == current_user.id).all()
    budget_status = []
    for b in budgets:
        spent = breakdown.get(b.category, 0.0)
        budget_status.append({
            "category": b.category,
            "limit": b.monthly_limit,
            "spent": spent,
            "remaining": b.monthly_limit - spent,
        })

    return {
        "month": m,
        "year": y,
        "total_spent": total,
        "breakdown": breakdown,
        "budget_status": budget_status,
    }
