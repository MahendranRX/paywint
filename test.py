from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
import uvicorn

app = FastAPI()

# --- Mock Data Structure ---


class Expense(BaseModel):
    id: int
    title: str
    amount: float
    category: str
    date: date


# Simulated database
expenses_db = [
    Expense(id=1, title="Rent", amount=1000.0,
            category="Housing", date=date(2026, 4, 1)),
    Expense(id=2, title="Groceries", amount=150.0,
            category="Food", date=date(2026, 4, 2)),
    Expense(id=3, title="Internet", amount=60.0,
            category="Utilities", date=date(2026, 3, 15)),
]

TOTAL_SALARY = 5000.0

# 1.4 Filter Expenses by Month


@app.get("/expenses/month/{year}/{month}/", response_model=List[Expense])
def get_expenses_by_month(year: int, month: int):
    """Retrieves expenses for a specific month/year."""
    if not 1 <= month <= 12:
        raise HTTPException(
            status_code=400, detail="Month must be between 1 and 12")

    filtered_expenses = [
        exp for exp in expenses_db
        if exp.date.year == year and exp.date.month == month
    ]
    return filtered_expenses

# 1.5 Total Expense, Total Salary, and Remaining Amount API


@app.get("/totals/")
def get_totals():
    """Calculates total expense, total salary, and remaining amount."""
    total_expense = sum(exp.amount for exp in expenses_db)
    remaining_amount = TOTAL_SALARY - total_expense

    return {
        "total_salary": TOTAL_SALARY,
        "total_expense": total_expense,
        "remaining_amount": remaining_amount
    }

# Run with: uvicorn main:app --reload
