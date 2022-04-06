import typing

import strawberry
from strawberry.asgi import GraphQL

from graphql_app.schemas.films import (CategoryType, CategoryCreateType,
                                       CategoryReadType, FilmType,
                                       FilmCreateType, FilmReadType)
from resolvers.films import (get_all_categories, get_by_id_a_category,
                             create_a_category, update_a_category,
                             delete_a_category, get_all_films,
                             get_by_id_a_film, create_a_film, update_a_film,
                             delete_a_film)


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


schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQL(schema)
