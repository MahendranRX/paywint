from pydantic import BaseModel

class ExpenseCreate(BaseModel):
    name: str
    amount: float
    category: str


class ExpenseSchema(ExpenseCreate):
    id: int

    class Config:
        from_attributes = True