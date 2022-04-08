import typing

import strawberry
from strawberry.asgi import GraphQL
from strawberry.extensions import ParserCache, ValidationCache

from graphql_app.schemas.films import (CategoryType, CategoryCreateType,
                                       CategoryReadType, FilmType,
                                       FilmCreateType, FilmReadType,
                                       SeasonType, SeasonCreateType,
                                       SeasonReadType, ChapterType,
                                       ChapterCreateType, ChapterReadType,
                                       PosterType, PosterReadType)
from graphql_app.schemas.persons import PersonReadType, PersonCreateType, \
    PersonType, RoleType, FilmPersonRoleType, ClientType, RoleReadType, \
    RoleCreateType, FilmPersonRoleCreateType, FilmPersonRoleReadType, \
    ClientCreateType, ClientReadType
from graphql_app.schemas.rents import RentType, RentCreateType, RentReadType
from graphql_app.schemas.tokens import TokenType
from graphql_app.schemas.users import UserType, UserCreateType, UserReadType
from resolvers.films import (get_all_categories, get_by_id_a_category,
                             create_a_category, update_a_category,
                             delete_a_category, get_all_films,
                             get_by_id_a_film, create_a_film, update_a_film,
                             delete_a_film, get_all_seasons, get_by_a_season,
                             create_a_season, update_a_season, delete_a_season,
                             get_all_chapters, get_by_id_a_chapter,
                             create_a_chapter, update_a_chapter,
                             delete_a_chapter, get_all_posters,
                             get_by_id_a_poster, delete_a_poster)
from resolvers.persons import create_a_person, update_a_person, \
    delete_a_person, get_all_persons, get_by_id_a_person, get_all_roles, \
    get_by_id_a_role, get_all_clients, get_by_id_a_client, create_a_role, \
    update_a_role, delete_a_role, create_a_film_person_role, \
    update_a_film_person_role, delete_a_film_person_role, create_a_client, \
    update_a_client, delete_a_client
from resolvers.rents import get_by_id_a_rent, get_all_rents, create_a_rent, \
    update_a_rent, delete_a_rent
from resolvers.security import login_for_access_token
from resolvers.users import get_all_users, get_by_id_a_user, create_a_user, \
    update_a_user, delete_a_user
from security.security import get_current_user, verify_admin_user, \
    verify_admin_or_employee_user


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

    # Person
    persons: typing.List[PersonType] = strawberry.field(
        resolver=get_all_persons)
    person: PersonType = strawberry.field(
        resolver=get_by_id_a_person)

    # Role
    roles: typing.List[RoleType] = strawberry.field(
        resolver=get_all_roles)
    role: RoleType = strawberry.field(
        resolver=get_by_id_a_role)

    # FilmPersonRole
    films_persons_roles: typing.List[FilmPersonRoleType] = strawberry.field(
        resolver=get_all_roles)
    film_person_role: FilmPersonRoleType = strawberry.field(
        resolver=get_by_id_a_role)

    # Client
    clients: typing.List[ClientType] = strawberry.field(
        resolver=get_all_clients)
    client: ClientType = strawberry.field(
        resolver=get_by_id_a_client)

    # Rent
    rents: typing.List[RentType] = strawberry.field(
        resolver=get_all_rents)
    rent: RentType = strawberry.field(
        resolver=get_by_id_a_rent)

    # User
    users: typing.List[UserType] = strawberry.field(
        resolver=get_all_users)
    user: RentType = strawberry.field(
        resolver=get_by_id_a_user)

    # Poster
    posters: typing.List[PosterType] = strawberry.field(
        resolver=get_all_posters)
    poster: PosterType = strawberry.field(
        resolver=get_by_id_a_poster)


@strawberry.type
class Mutation:
    # Category
    @strawberry.mutation
    async def create_category(
            self, category: CategoryCreateType,
            token: str) -> CategoryReadType:
        user = await get_current_user(token)
        await verify_admin_user(user)

        return create_a_category(category)

    @strawberry.mutation
    async def update_category(self, category_id: int,
                              category: CategoryCreateType,
                              token: str) -> CategoryReadType:
        user = await get_current_user(token)
        await verify_admin_user(user)

        return update_a_category(category_id, category)

    @strawberry.mutation
    async def delete_category(self, category_id: int,
                              token: str) -> CategoryReadType:
        user = await get_current_user(token)
        await verify_admin_user(user)

        return delete_a_category(category_id)

    # Film
    @strawberry.mutation
    async def create_film(self, film: FilmCreateType,
                          token: str) -> FilmReadType:
        user = await get_current_user(token)
        await verify_admin_user(user)

        return create_a_film(film)

    @strawberry.mutation
    async def update_film(self, film_id: int,
                          film: FilmCreateType, token: str) -> FilmReadType:
        user = await get_current_user(token)
        await verify_admin_user(user)

        return update_a_film(film_id, film)

    @strawberry.mutation
    async def delete_film(self, film_id: int, token: str) -> FilmReadType:
        user = await get_current_user(token)
        await verify_admin_user(user)

        return delete_a_film(film_id)

    # Season
    @strawberry.mutation
    async def create_season(self,
                            season: SeasonCreateType,
                            token: str) -> SeasonReadType:
        user = await get_current_user(token)
        await verify_admin_user(user)

        return create_a_season(season)

    @strawberry.mutation
    async def update_season(self, season_id: int,
                            season: SeasonCreateType,
                            token: str) -> SeasonReadType:
        user = await get_current_user(token)
        await verify_admin_user(user)

        return update_a_season(season_id, season)

    @strawberry.mutation
    async def delete_season(self, season_id: int,
                            token: str) -> SeasonReadType:
        user = await get_current_user(token)
        await verify_admin_user(user)

        return delete_a_season(season_id)

    # Chapter
    @strawberry.mutation
    async def create_chapter(self,
                             chapter: ChapterCreateType,
                             token: str) -> ChapterReadType:
        user = await get_current_user(token)
        await verify_admin_user(user)

        return create_a_chapter(chapter)

    @strawberry.mutation
    async def update_chapter(self, chapter_id: int,
                             chapter: ChapterCreateType,
                             token: str) -> ChapterReadType:
        user = await get_current_user(token)
        await verify_admin_user(user)

        return update_a_chapter(chapter_id, chapter)

    @strawberry.mutation
    async def delete_chapter(self, chapter_id: int,
                             token: str) -> ChapterReadType:
        user = await get_current_user(token)
        await verify_admin_user(user)

        return delete_a_chapter(chapter_id)

    # Person
    @strawberry.mutation
    async def create_person(self,
                            person: PersonCreateType,
                            token: str) -> PersonReadType:
        user = await get_current_user(token)
        await verify_admin_user(user)

        return create_a_person(person)

    @strawberry.mutation
    async def update_person(self, person_id: int,
                            person: PersonCreateType,
                            token: str) -> PersonReadType:
        user = await get_current_user(token)
        await verify_admin_user(user)

        return update_a_person(person_id, person)

    @strawberry.mutation
    async def delete_person(self, person_id: int,
                            token: str) -> PersonReadType:
        user = await get_current_user(token)
        await verify_admin_user(user)

        return delete_a_person(person_id)

    # Role
    @strawberry.mutation
    async def create_role(self, role: RoleCreateType,
                          token: str) -> RoleReadType:
        user = await get_current_user(token)
        await verify_admin_user(user)

        return create_a_role(role)

    @strawberry.mutation
    async def update_role(self, role_id: int,
                          role: RoleCreateType, token: str) -> RoleReadType:
        user = await get_current_user(token)
        await verify_admin_user(user)

        return update_a_role(role_id, role)

    @strawberry.mutation
    async def delete_role(self, role_id: int, token: str) -> RoleReadType:
        user = await get_current_user(token)
        await verify_admin_user(user)

        return delete_a_role(role_id)

    # Film Person Role
    @strawberry.mutation
    async def create_film_person_role(
            self, film_person_role_create_type: FilmPersonRoleCreateType,
            token: str) -> FilmPersonRoleReadType:
        user = await get_current_user(token)
        await verify_admin_user(user)

        return create_a_film_person_role(film_person_role_create_type)

    @strawberry.mutation
    async def update_film_person_role(
            self, film_person_role_id: int,
            film_person_role_create_type: FilmPersonRoleCreateType,
            token: str) -> FilmPersonRoleReadType:
        user = await get_current_user(token)
        await verify_admin_user(user)

        return update_a_film_person_role(film_person_role_id,
                                         film_person_role_create_type)

    @strawberry.mutation
    async def delete_film_person_role(self, film_person_role_id: int,
                                      token: str) -> FilmPersonRoleReadType:
        user = await get_current_user(token)
        await verify_admin_user(user)

        return delete_a_film_person_role(film_person_role_id)

    # Client
    @strawberry.mutation
    async def create_client(self, client_create_type: ClientCreateType,
                            token: str) -> ClientReadType:
        user = await get_current_user(token)
        await verify_admin_user(user)

        return create_a_client(client_create_type)

    @strawberry.mutation
    async def update_client(self, client_id: int,
                            client_create_type: ClientCreateType,
                            token: str) -> ClientReadType:
        user = await get_current_user(token)
        await verify_admin_user(user)

        return update_a_client(client_id, client_create_type)

    @strawberry.mutation
    async def delete_client(self, client_id: int,
                            token: str) -> ClientReadType:
        user = await get_current_user(token)
        await verify_admin_user(user)

        return delete_a_client(client_id)

    # Rent
    @strawberry.mutation
    async def create_rent(self, rent_create_type: RentCreateType,
                          token: str) -> RentReadType:
        user = await get_current_user(token)
        await verify_admin_or_employee_user(user)

        return create_a_rent(rent_create_type)

    @strawberry.mutation
    async def update_rent(self, rent_id: int,
                          rent_create_type: RentCreateType,
                          token: str) -> RentReadType:
        user = await get_current_user(token)
        await verify_admin_or_employee_user(user)

        return update_a_rent(rent_id, rent_create_type)

    @strawberry.mutation
    async def delete_rent(self, rent_id: int, token: str) -> RentReadType:
        user = await get_current_user(token)
        await verify_admin_or_employee_user(user)

        return delete_a_rent(rent_id)

    # User
    @strawberry.mutation
    async def create_user(self,
                          user_create_type: UserCreateType) -> UserReadType:
        return create_a_user(user_create_type)

    @strawberry.mutation
    async def update_user(self, user_id: int,
                          user_create_type: UserCreateType,
                          token: str) -> UserReadType:
        user = await get_current_user(token)
        await verify_admin_user(user)

        return update_a_user(user_id, user_create_type)

    @strawberry.mutation
    async def delete_user(self, user_id: int, token: str) -> UserReadType:
        user = await get_current_user(token)
        await verify_admin_user(user)

        return delete_a_user(user_id)

    # Poster
    @strawberry.mutation
    async def delete_poster(self, poster_id: int,
                            token: str) -> PosterReadType:
        user = await get_current_user(token)
        await verify_admin_user(user)

        return delete_a_poster(poster_id)

    # Token
    @strawberry.mutation
    def token(self, username: str, password: str) -> TokenType:
        return login_for_access_token(username, password)


schema = strawberry.Schema(query=Query, mutation=Mutation,
                           extensions=[
                               ParserCache(maxsize=128),
                               ValidationCache(maxsize=128)
                           ]
                           )

graphql_app = GraphQL(schema)
