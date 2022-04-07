import strawberry

from models.films_and_rents import (Category, CategoryCreate, Film, FilmCreate,
                                    CategoryRead, FilmRead, Season,
                                    SeasonCreate, SeasonRead, Chapter,
                                    ChapterCreate, ChapterRead, Poster,
                                    PosterCreate, PosterRead)


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


# Poster
@strawberry.experimental.pydantic.type(model=Poster, all_fields=True)
class PosterType:
    pass


@strawberry.experimental.pydantic.input(model=PosterCreate, all_fields=True)
class PosterCreateType:
    pass


@strawberry.experimental.pydantic.type(model=PosterRead, all_fields=True)
class PosterReadType:
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


# Chapter
@strawberry.experimental.pydantic.type(model=Chapter, all_fields=True)
class ChapterType:
    pass


@strawberry.experimental.pydantic.input(model=ChapterCreate, all_fields=True)
class ChapterCreateType:
    pass


@strawberry.experimental.pydantic.type(model=ChapterRead, all_fields=True)
class ChapterReadType:
    pass
