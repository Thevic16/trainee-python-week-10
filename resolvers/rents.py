from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_redis_cache import cache_one_month
from sqlmodel import select
from starlette import status

from databases.db import get_db_session
from graphql_app.schemas.rents import RentReadType, RentCreateType
from models.films_and_rents import RentRead, Rent, RentCreate

router = APIRouter()

session = get_db_session()


# Rent Related Routes
@cache_one_month()
def get_all_rents() -> List[RentReadType]:
    session.rollback()
    statement = select(Rent)
    results = session.exec(statement).all()

    results_strawberry = [RentReadType.from_pydantic(rent)
                          for rent in results]

    return results_strawberry


@cache_one_month()
def get_by_id_a_rent(rent_id: int) -> RentReadType:
    session.rollback()
    statement = select(Rent).where(Rent.id == rent_id)
    result = session.exec(statement).first()

    if result is None:
        raise Exception("Resource Not Found")

    return RentReadType.from_pydantic(result)


def create_a_rent(rent_create_type: RentCreateType) -> RentReadType:
    session.rollback()
    rent = rent_create_type.to_pydantic()
    new_rent = Rent(film_id=rent.film_id,
                    client_id=rent.client_id,
                    amount=rent.amount,
                    start_date=rent.start_date,
                    return_date=rent.return_date,
                    actual_return_date=rent.actual_return_date,
                    state=rent.state,
                    cost=Rent.get_cost(rent))

    session.add(new_rent)

    session.commit()

    return RentReadType.from_pydantic(new_rent)


def update_a_rent(
        rent_id: int, rent_create_type: RentCreateType) -> RentReadType:
    session.rollback()
    rent = rent_create_type.to_pydantic()

    statement = select(Rent).where(Rent.id == rent_id)

    result = session.exec(statement).first()

    if result is None:
        raise Exception("Resource Not Found")

    result.film_id = rent.film_id
    result.client_id = rent.client_id
    result.amount = rent.amount
    result.start_date = rent.start_date
    result.return_date = rent.return_date
    result.actual_return_date = rent.actual_return_date
    result.state = rent.state
    result.cost = Rent.get_cost(rent)

    session.commit()

    return RentReadType.from_pydantic(result)


def delete_a_rent(rent_id: int) -> RentReadType:
    session.rollback()
    statement = select(Rent).where(Rent.id == rent_id)

    result = session.exec(statement).one_or_none()

    if result is None:
        raise Exception("Resource Not Found")

    session.delete(result)
    session.commit()

    return RentReadType.from_pydantic(result)
