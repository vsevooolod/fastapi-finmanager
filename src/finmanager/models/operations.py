from decimal import Decimal
from datetime import date
from typing import Optional
from enum import Enum

from pydantic import BaseModel


class OperationType(str, Enum):
    INCOME = 'income'
    OUTCOME = 'outcome'


class OperationBase(BaseModel):
    date: date
    type: OperationType
    amount: Decimal
    description: Optional[str] = None


class Operation(OperationBase):
    id: int

    class Config:
        orm_mode = True


class OperationCreate(OperationBase):
    pass


class OperationUpdate(OperationBase):
    pass
