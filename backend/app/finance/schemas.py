import uuid
from datetime import date, datetime

from pydantic import BaseModel


class ExpenseCreate(BaseModel):
    amount: float
    category: str = "other"
    description: str = ""
    expense_date: date


class ExpenseResponse(BaseModel):
    id: uuid.UUID
    amount: float
    category: str
    description: str
    expense_date: date
    created_at: datetime

    model_config = {"from_attributes": True}


class BudgetCreate(BaseModel):
    category: str
    monthly_limit: float


class BudgetResponse(BaseModel):
    id: uuid.UUID
    category: str
    monthly_limit: float
    created_at: datetime

    model_config = {"from_attributes": True}


class SavingsGoalCreate(BaseModel):
    title: str
    target_amount: float
    current_amount: float = 0.0
    target_date: date | None = None


class SavingsGoalUpdate(BaseModel):
    title: str | None = None
    target_amount: float | None = None
    current_amount: float | None = None
    target_date: date | None = None


class SavingsGoalResponse(BaseModel):
    id: uuid.UUID
    title: str
    target_amount: float
    current_amount: float
    target_date: date | None
    created_at: datetime

    model_config = {"from_attributes": True}
