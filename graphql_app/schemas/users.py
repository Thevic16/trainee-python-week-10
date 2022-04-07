import strawberry
from models.users import User, UserCreate, UserRead


# Rent
@strawberry.experimental.pydantic.type(model=User, all_fields=True)
class UserType:
    pass


@strawberry.experimental.pydantic.input(model=UserCreate, all_fields=True)
class UserCreateType:
    pass


@strawberry.experimental.pydantic.type(model=UserRead, all_fields=True)
class UserReadType:
    pass
