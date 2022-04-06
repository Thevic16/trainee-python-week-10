import typing

import strawberry
from strawberry.asgi import GraphQL

from graphql_app.schemas.films import CategoryType, CategoryCreateType
from resolvers.films import get_all_categories, get_by_id_a_category, \
    create_a_category, update_a_category, delete_a_category


@strawberry.type
class Query:
    categories: typing.List[CategoryType] = strawberry.field(
        resolver=get_all_categories)
    category: CategoryType = strawberry.field(
        resolver=get_by_id_a_category)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_category(self, category: CategoryCreateType) -> CategoryType:
        return create_a_category(category)

    @strawberry.mutation
    def update_category(self, category_id: int,
                        category: CategoryCreateType) -> CategoryType:
        return update_a_category(category_id, category)

    @strawberry.mutation
    def delete_category(self, category_id: int) -> CategoryType:
        return delete_a_category(category_id)


schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQL(schema)
