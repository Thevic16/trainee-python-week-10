import strawberry

from models.persons import (PersonCreate, Person, PersonRead, Role, RoleCreate,
                            RoleRead, FilmPersonRole, FilmPersonRoleCreate,
                            FilmPersonRoleRead, Client, ClientCreate,
                            ClientRead)


# Person
@strawberry.experimental.pydantic.type(model=Person, all_fields=True)
class PersonType:
    pass


@strawberry.experimental.pydantic.input(model=PersonCreate, all_fields=True)
class PersonCreateType:
    pass


@strawberry.experimental.pydantic.type(model=PersonRead, all_fields=True)
class PersonReadType:
    pass


# Role
@strawberry.experimental.pydantic.type(model=Role, all_fields=True)
class RoleType:
    pass


@strawberry.experimental.pydantic.input(model=RoleCreate, all_fields=True)
class RoleCreateType:
    pass


@strawberry.experimental.pydantic.type(model=RoleRead, all_fields=True)
class RoleReadType:
    pass


# FilmPersonRole
@strawberry.experimental.pydantic.type(model=FilmPersonRole,
                                       all_fields=True)
class FilmPersonRoleType:
    pass


@strawberry.experimental.pydantic.input(model=FilmPersonRoleCreate,
                                        all_fields=True)
class FilmPersonRoleCreateType:
    pass


@strawberry.experimental.pydantic.type(model=FilmPersonRoleRead,
                                       all_fields=True)
class FilmPersonRoleReadType:
    pass


# Client
@strawberry.experimental.pydantic.type(model=Client,
                                       all_fields=True)
class ClientType:
    pass


@strawberry.experimental.pydantic.input(model=ClientCreate,
                                        all_fields=True)
class ClientCreateType:
    pass


@strawberry.experimental.pydantic.type(model=ClientRead,
                                       all_fields=True)
class ClientReadType:
    pass
