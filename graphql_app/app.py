import typing

import strawberry
from strawberry.asgi import GraphQL

from graphql_app.schemas.films import (CategoryType, CategoryCreateType,
                                       CategoryReadType, FilmType,
                                       FilmCreateType, FilmReadType,
                                       SeasonType, SeasonCreateType,
                                       SeasonReadType, ChapterType,
                                       ChapterCreateType, ChapterReadType)
from resolvers.films import (get_all_categories, get_by_id_a_category,
                             create_a_category, update_a_category,
                             delete_a_category, get_all_films,
                             get_by_id_a_film, create_a_film, update_a_film,
                             delete_a_film, get_all_seasons, get_by_a_season,
                             create_a_season, update_a_season, delete_a_season,
                             get_all_chapters, get_by_id_a_chapter,
                             create_a_chapter, update_a_chapter,
                             delete_a_chapter)


@strawberry.type
class Query:
    # Category
    categories: typing.List[CategoryType] = strawberry.field(
        resolver=get_all_categories)
    category: CategoryType = strawberry.field(
        resolver=get_by_id_a_category)

    # Film
    films: typing.List[FilmType] = strawberry.field(
        resolver=get_all_films)
    film: FilmType = strawberry.field(
        resolver=get_by_id_a_film)

    # Season
    seasons: typing.List[SeasonType] = strawberry.field(
        resolver=get_all_seasons)
    season: SeasonType = strawberry.field(
        resolver=get_by_a_season)

    # Chapter
    chapters: typing.List[ChapterType] = strawberry.field(
        resolver=get_all_chapters)
    chapter: ChapterType = strawberry.field(
        resolver=get_by_id_a_chapter)


@strawberry.type
class Mutation:
    # Category
    @strawberry.mutation
    def create_category(self, category: CategoryCreateType) \
            -> CategoryReadType:
        return create_a_category(category)

    @strawberry.mutation
    def update_category(self, category_id: int,
                        category: CategoryCreateType) -> CategoryReadType:
        return update_a_category(category_id, category)

    @strawberry.mutation
    def delete_category(self, category_id: int) -> CategoryReadType:
        return delete_a_category(category_id)

    # Film
    @strawberry.mutation
    def create_film(self, film: FilmCreateType) \
            -> FilmReadType:
        return create_a_film(film)

    @strawberry.mutation
    def update_film(self, film_id: int,
                    film: FilmCreateType) -> FilmReadType:
        return update_a_film(film_id, film)

    @strawberry.mutation
    def delete_film(self, film_id: int) -> FilmReadType:
        return delete_a_film(film_id)

    # Season
    @strawberry.mutation
    def create_season(self, season: SeasonCreateType) \
            -> SeasonReadType:
        return create_a_season(season)

    @strawberry.mutation
    def update_season(self, season_id: int,
                      season: SeasonCreateType) -> SeasonReadType:
        return update_a_season(season_id, season)

    @strawberry.mutation
    def delete_season(self, season_id: int) -> SeasonReadType:
        return delete_a_season(season_id)

    # Chapter
    @strawberry.mutation
    def create_chapter(self, chapter: ChapterCreateType) \
            -> ChapterReadType:
        return create_a_chapter(chapter)

    @strawberry.mutation
    def update_chapter(self, chapter_id: int,
                       chapter: ChapterCreateType) -> ChapterReadType:
        return update_a_chapter(chapter_id, chapter)

    @strawberry.mutation
    def delete_chapter(self, chapter_id: int) -> ChapterReadType:
        return delete_a_chapter(chapter_id)


schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQL(schema)
