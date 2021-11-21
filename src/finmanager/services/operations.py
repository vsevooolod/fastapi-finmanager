from typing import List, Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import tables
from ..db import get_session
from ..models import operations


class OperationsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get(self, id: int, user_id: int) -> tables.Operation:
        operation = self.session.query(tables.Operation).filter_by(
            id=id,
            user_id=user_id,
        ).first()
        if not operation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return operation

    def get_list(self, user_id: int, type: Optional[operations.OperationType] = None) -> List[tables.Operation]:
        query = self.session.query(tables.Operation).filter_by(user_id=user_id)
        if type:
            query = query.filter_by(type=type)
        return query.all()

    def get(self, id: int, user_id: int) -> tables.Operation:
        return self._get(id=id, user_id=user_id)

    def create(self, user_id: int, operation_in: operations.OperationCreate) -> tables.Operation:
        created_operation = tables.Operation(
            **operation_in.dict(),
            user_id=user_id,
        )
        self.session.add(created_operation)
        self.session.commit()
        return created_operation

    def create_many(self, user_id: int, operations_in: List[operations.OperationCreate]) -> List[tables.Operation]:
        created_operations = [tables.Operation(
            **operation_in.dict(),
            user_id=user_id,
        ) for operation_in in operations_in]
        self.session.add_all(created_operations)
        self.session.commit()
        return created_operations

    def update(self, id: int, user_id: int, operation_in: operations.OperationUpdate) -> tables.Operation:
        operation = self._get(id=id, user_id=user_id)
        [setattr(operation, key, value) for key, value in operation_in]
        self.session.commit()
        return operation

    def delete(self, id: int, user_id: int):
        operation = self._get(id=id, user_id=user_id)
        self.session.delete(operation)
        self.session.commit()
