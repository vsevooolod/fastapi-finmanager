import csv
from io import StringIO
from typing import Any

from fastapi import Depends

from ..models.operations import OperationCreate, Operation
from ..services.operations import OperationsService


class ReportsService:
    FIELDNAMES = ['date', 'type', 'amount', 'description']

    def __init__(self, operations_service: OperationsService = Depends()):
        self.operations_service = operations_service

    def import_csv(self, user_id: int, file: Any):
        reader = csv.DictReader(
            f=(row.decode() for row in file),
            fieldnames=self.FIELDNAMES,
        )
        operations = []
        next(reader)
        for row in reader:
            operation_dt = OperationCreate.parse_obj(row)
            if not operation_dt.description:
                operation_dt.description = None
            operations.append(operation_dt)
        self.operations_service.create_many(
            user_id=user_id,
            operations_in=operations
        )

    def export_csv(self, user_id: int) -> Any:
        output = StringIO()
        writer = csv.DictWriter(
            f=output,
            fieldnames=self.FIELDNAMES,
            extrasaction='ignore',
        )
        operations = self.operations_service.get_list(user_id=user_id)

        writer.writeheader()
        for operation in operations:
            operation_dt = Operation.from_orm(operation)
            writer.writerow(operation_dt.dict())
        output.seek(0)
        return output
