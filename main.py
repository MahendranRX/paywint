from fastapi import FastAPI, Depends, HTTPException
from database import SessionLocal, Base, engine
from schemas import ExpenseCreate, ExpenseSchema
from sqlalchemy.orm import Session
from models import Expense

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/expense', response_model=ExpenseSchema)
def create(expense: ExpenseCreate, db: Session = Depends(get_db)):
    expense_db = Expense(**expense.dict())
    db.add(expense_db)
    db.commit()
    db.refresh(expense_db)
    return expense_db


@app.get('/expenses', response_model=list[ExpenseSchema])
def expenses(db: Session = Depends(get_db)):
    return db.query(Expense).all()


@app.put('/expense/{pk}', response_model=ExpenseSchema)
def update(pk: int, updated: ExpenseCreate,  db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == pk).first()

    if not expense:
        raise HTTPException(status_code=404, detail='Expense not found.')

    for key, value in updated.dict().items():
        setattr(expense, key, value)

    db.commit()
    db.refresh(expense)
    return expense


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
