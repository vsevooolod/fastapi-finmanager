from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..models.auth import UserCreate, Token, User
from ..services.auth import AuthService, get_current_user


router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)


@router.post('/sign-up', response_model=Token)
def sign_up(
        user_dt: UserCreate,
        service: AuthService = Depends(),
):
    return service.register_user(user_dt)


@router.post('/sign-in', response_model=Token)
def sign_in(
        form_data: OAuth2PasswordRequestForm = Depends(),
        service: AuthService = Depends(),
):
    return service.authenticate_user(
        username=form_data.username,
        password=form_data.password,
    )


@router.get('/user', response_model=User)
def get_user(user: User = Depends(get_current_user)) -> User:
    return user
