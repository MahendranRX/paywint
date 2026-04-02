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
