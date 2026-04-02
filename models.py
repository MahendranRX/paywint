from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from datetime import date

class Expense(Base):

    __tablename__ = 'expense'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    date = Column(DateTime)