from typing import List

from fastapi import APIRouter
from sqlmodel import select

from databases.db import get_db_session
from graphql_app.schemas.users import UserReadType, UserCreateType
from models.users import User
from security.security import get_password_hash

router = APIRouter()

session = get_db_session()


# User Related Resolvers
def get_all_users() -> List[UserReadType]:
    session.rollback()
    statement = select(User)
    results = session.exec(statement).all()

    results_strawberry = [UserReadType.from_pydantic(user)
                          for user in results]

    return results_strawberry


def get_by_id_a_user(user_id: int) -> UserReadType:
    session.rollback()
    statement = select(User).where(User.id == user_id)
    result = session.exec(statement).first()

    if result is None:
        raise Exception("Resource Not Found")

    return UserReadType.from_pydantic(result)


def create_a_user(user_create_type: UserCreateType) -> UserReadType:
    session.rollback()
    user = user_create_type.to_pydantic()
    new_user = User(username=user.username,
                    password=get_password_hash(user.password),
                    is_admin=user.is_admin,
                    is_employee=user.is_employee)

    session.add(new_user)

    session.commit()

    return UserReadType.from_pydantic(new_user)


def update_a_user(user_id: int,
                  user_create_type: UserCreateType) -> UserReadType:
    session.rollback()
    user = user_create_type.to_pydantic()

    statement = select(User).where(User.id == user_id)

    result = session.exec(statement).first()

    if result is None:
        raise Exception("Resource Not Found")

    result.username = user.username
    result.password = get_password_hash(user.password)
    result.is_admin = user.is_admin
    result.is_employee = user.is_employee

    session.commit()

    return UserReadType.from_pydantic(result)


def delete_a_user(user_id: int) -> UserReadType:
    session.rollback()
    statement = select(User).where(User.id == user_id)
    result = session.exec(statement).one_or_none()

    if result is None:
        raise Exception("Resource Not Found")

    session.delete(result)
    session.commit()

    return UserReadType.from_pydantic(result)
