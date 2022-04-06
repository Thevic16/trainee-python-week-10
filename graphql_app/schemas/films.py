import strawberry

from models.films_and_rents import (Category, CategoryCreate, Film, FilmCreate,
                                    CategoryRead, FilmRead, Season,
                                    SeasonCreate, SeasonRead)


# Category
@strawberry.experimental.pydantic.type(model=Category, all_fields=True)
class CategoryType:
    pass


@strawberry.experimental.pydantic.input(model=CategoryCreate, all_fields=True)
class CategoryCreateType:
    pass


@strawberry.experimental.pydantic.type(model=CategoryRead, all_fields=True)
class CategoryReadType:
    pass


# Film
@strawberry.experimental.pydantic.type(model=Film, all_fields=True)
class FilmType:
    pass


@strawberry.experimental.pydantic.input(model=FilmCreate, all_fields=True)
class FilmCreateType:
    pass


@strawberry.experimental.pydantic.type(model=FilmRead, all_fields=True)
class FilmReadType:
    pass


# Season
@strawberry.experimental.pydantic.type(model=Season, all_fields=True)
class SeasonType:
    pass


@strawberry.experimental.pydantic.input(model=SeasonCreate, all_fields=True)
class SeasonCreateType:
    pass


@strawberry.experimental.pydantic.type(model=SeasonRead, all_fields=True)
class SeasonReadType:
    pass
