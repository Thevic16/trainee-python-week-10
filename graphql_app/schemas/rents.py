import strawberry
from models.films_and_rents import Rent, RentRead, RentCreate


# Rent
@strawberry.experimental.pydantic.type(model=Rent, all_fields=True)
class RentType:
    pass


@strawberry.experimental.pydantic.input(model=RentCreate, all_fields=True)
class RentCreateType:
    pass


@strawberry.experimental.pydantic.type(model=RentRead, all_fields=True)
class RentReadType:
    pass
