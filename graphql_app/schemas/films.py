import strawberry

from models.films_and_rents import Category, CategoryCreate


@strawberry.experimental.pydantic.type(model=Category, all_fields=True)
class CategoryType:
    pass


@strawberry.experimental.pydantic.input(model=CategoryCreate, all_fields=True)
class CategoryCreateType:
    pass
