import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True, unique=True)
    username = sa.Column(sa.String, unique=True)
    email = sa.Column(sa.Text, unique=True)
    password_hash = sa.Column(sa.Text)


class Operation(Base):
    __tablename__ = 'operations'

    id = sa.Column(sa.Integer, primary_key=True, unique=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    date = sa.Column(sa.Date)
    type = sa.Column(sa.String(50))
    amount = sa.Column(sa.Numeric(10, 2))
    description = sa.Column(sa.String, nullable=True)
