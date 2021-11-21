from typing import List, Optional

from fastapi import APIRouter, Depends, Response, status

from ..models import operations, auth
from ..services.operations import OperationsService
from ..services.auth import get_current_user


router = APIRouter(
    prefix='/operations',
    tags=['Operations'],
)


@router.get('/', response_model=List[operations.Operation])
def get_operations(
        type: Optional[operations.OperationType] = None,
        user: auth.User = Depends(get_current_user),
        service: OperationsService = Depends(),
):
    return service.get_list(type=type, user_id=user.id)


@router.get('/{id}', response_model=operations.Operation)
def get_operation(
        id: int,
        user: auth.User = Depends(get_current_user),
        service: OperationsService = Depends()
):
    return service.get(id=id, user_id=user.id)


@router.post('/', response_model=operations.Operation)
def create_operation(
        operation_in: operations.OperationCreate,
        user: auth.User = Depends(get_current_user),
        service: OperationsService = Depends(),
):
    return service.create(operation_in=operation_in, user_id=user.id)


@router.put('/{id}', response_model=operations.Operation)
def update_operation(
        id: int,
        operation_in: operations.OperationUpdate,
        user: auth.User = Depends(get_current_user),
        service: OperationsService = Depends(),
):
    return service.update(id=id, operation_in=operation_in, user_id=user.id)


@router.delete('/{id}')
def delete_operation(
        id: int,
        user: auth.User = Depends(get_current_user),
        service: OperationsService = Depends(),
):
    service.delete(id=id, user_id=user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
