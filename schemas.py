from pydantic import BaseModel
from datetime import date
class ExpenseCreate(BaseModel):
    name: str
    amount: float
    category: str
    # date: date


class ExpenseSchema(ExpenseCreate):
    id: int

    class Config:
        from_attributes = True