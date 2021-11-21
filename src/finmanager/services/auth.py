from datetime import datetime, timedelta

from jose import jwt
from pydantic import ValidationError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.hash import bcrypt
from sqlalchemy.orm import Session

from .. import tables
from ..db import get_session
from ..settings import settings
from ..models.auth import User, UserCreate, Token


oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/sign-in')


def get_current_user(token: str = Depends(oauth2_schema)) -> User:
    return AuthService.validate_token(token)


class AuthService:
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, plain_password: str) -> str:
        return bcrypt.hash(plain_password)

    @classmethod
    def validate_token(cls, token: str) -> User:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        try:
            payload = jwt.decode(token=token, key=settings.jwt_secret,
                                 algorithms=[settings.jwt_algorithm])
        except jwt.JWTError:
            raise exception from None

        user_dt = payload.get('user')

        try:
            user = User.parse_obj(user_dt)
        except ValidationError:
            raise exception from None
        return user

    @classmethod
    def create_token(cls, user: tables.User) -> Token:
        user_dt = User.from_orm(user)

        now = datetime.utcnow()

        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=settings.jwt_expiration),
            'sub': str(user_dt.id),
            'user': user_dt.dict(),
        }
        token = jwt.encode(
            claims=payload,
            key=settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )
        return Token(access_token=token)

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_user(self, user_dt: UserCreate) -> Token:
        user = tables.User(
            email=user_dt.email,
            username=user_dt.username,
            password_hash=self.hash_password(user_dt.password),
        )
        self.session.add(user)
        self.session.commit()
        return self.create_token(user)

    def authenticate_user(self, username: str, password: str) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        user = self.session.query(tables.User).filter(tables.User.username == username).first()
        if not user or not self.verify_password(password, user.password_hash):
            raise exception

        return self.create_token(user)

