from typing import List

from fastapi import APIRouter
from sqlmodel import select

from databases.db import get_db_session
from graphql_app.schemas.persons import (PersonReadType, PersonCreateType,
                                         RoleReadType, RoleCreateType,
                                         FilmPersonRoleReadType,
                                         FilmPersonRoleCreateType,
                                         ClientReadType, ClientCreateType)
from models.persons import (Person, Role, FilmPersonRole, Client)

router = APIRouter()

session = get_db_session()


# Person Related Routes
def get_all_persons() -> List[PersonReadType]:
    session.rollback()
    statement = select(Person)
    results = session.exec(statement).all()

    results_strawberry = [PersonReadType.from_pydantic(person)
                          for person in results]

    return results_strawberry


def get_by_id_a_person(person_id: int) -> PersonReadType:
    session.rollback()
    statement = select(Person).where(Person.id == person_id)
    result = session.exec(statement).first()

    if result is None:
        raise Exception("Resource Not Found")

    return PersonReadType.from_pydantic(result)


def create_a_person(person_create_type: PersonCreateType) -> PersonReadType:
    session.rollback()
    person = person_create_type.to_pydantic()
    new_person = Person(name=person.name,
                        lastname=person.lastname,
                        gender=person.gender,
                        date_of_birth=person.date_of_birth,
                        person_type=person.person_type,
                        age=Person.get_age(person.date_of_birth))

    session.add(new_person)

    session.commit()

    return PersonReadType.from_pydantic(new_person)


def update_a_person(person_id: int,
                    person_create_type: PersonCreateType) -> PersonReadType:
    session.rollback()
    person = person_create_type.to_pydantic()
    statement = select(Person).where(Person.id == person_id)

    result = session.exec(statement).first()

    if result is None:
        raise Exception("Resource Not Found")

    result.name = person.name
    result.lastname = person.lastname
    result.gender = person.gender
    result.date_of_birth = person.date_of_birth
    result.person_type = person.person_type
    result.age = Person.get_age(result.date_of_birth)

    session.commit()

    return PersonReadType.from_pydantic(result)


def delete_a_person(person_id: int) -> PersonReadType:
    session.rollback()
    statement = select(Person).where(Person.id == person_id)

    result = session.exec(statement).one_or_none()

    if result is None:
        raise Exception("Resource Not Found")

    session.delete(result)
    session.commit()

    return PersonReadType.from_pydantic(result)


def get_all_roles() -> List[RoleReadType]:
    session.rollback()
    statement = select(Role)
    results = session.exec(statement).all()

    results_strawberry = [RoleReadType.from_pydantic(role)
                          for role in results]

    return results_strawberry


def get_by_id_a_role(role_id: int) -> RoleReadType:
    session.rollback()
    statement = select(Role).where(Role.id == role_id)
    result = session.exec(statement).first()

    if result is None:
        raise Exception("Resource Not Found")

    return RoleReadType.from_pydantic(result)


def create_a_role(role_create_type: RoleCreateType) -> RoleReadType:
    session.rollback()
    role = role_create_type.to_pydantic()
    new_role = Role(name=role.name,
                    description=role.description)

    session.add(new_role)

    session.commit()

    return RoleReadType.from_pydantic(new_role)


def update_a_role(role_id: int,
                  role_create_type: RoleCreateType) -> RoleReadType:
    session.rollback()
    role = role_create_type.to_pydantic()

    statement = select(Role).where(Role.id == role_id)

    result = session.exec(statement).first()

    if result is None:
        raise Exception("Resource Not Found")

    result.name = role.name
    result.description = role.description

    session.commit()

    return RoleReadType.from_pydantic(result)


def delete_a_role(role_id: int) -> RoleReadType:
    session.rollback()
    statement = select(Role).where(Role.id == role_id)

    result = session.exec(statement).one_or_none()

    if result is None:
        raise Exception("Resource Not Found")

    session.delete(result)
    session.commit()

    return RoleReadType.from_pydantic(result)


def get_all_films_persons_roles() -> List[FilmPersonRoleReadType]:
    session.rollback()
    statement = select(FilmPersonRole)
    results = session.exec(statement).all()

    results_strawberry = \
        [FilmPersonRoleReadType.from_pydantic(film_person_role)
         for film_person_role in results]

    return results_strawberry


def get_by_id_a_film_person_role(film_person_role_id: int) \
        -> FilmPersonRoleReadType:
    session.rollback()
    statement = select(FilmPersonRole).where(
        FilmPersonRole.id == film_person_role_id)

    result = session.exec(statement).first()

    if result is None:
        raise Exception("Resource Not Found")

    return FilmPersonRoleReadType.from_pydantic(result)


def create_a_film_person_role(
        film_person_role_create_type: FilmPersonRoleCreateType) \
        -> FilmPersonRoleReadType:
    session.rollback()
    film_person_role = film_person_role_create_type.to_pydantic()
    new_film_person_role = FilmPersonRole(film_id=film_person_role.film_id,
                                          person_id=film_person_role.person_id,
                                          role_id=film_person_role.role_id)

    session.add(new_film_person_role)

    session.commit()

    return FilmPersonRoleReadType.from_pydantic(new_film_person_role)


def update_a_film_person_role(film_person_role_id: int,
                              film_person_role_create_type:
                              FilmPersonRoleCreateType) \
        -> FilmPersonRoleReadType:
    session.rollback()
    film_person_role = film_person_role_create_type.to_pydantic()
    statement = select(FilmPersonRole).where(
        FilmPersonRole.id == film_person_role_id)

    result = session.exec(statement).first()

    if result is None:
        raise Exception("Resource Not Found")

    result.film_id = film_person_role.film_id
    result.person_id = film_person_role.person_id
    result.role_id = film_person_role.role_id

    session.commit()

    return FilmPersonRoleReadType.from_pydantic(result)


def delete_a_film_person_role(film_person_role_id: int) \
        -> FilmPersonRoleReadType:
    session.rollback()
    statement = select(FilmPersonRole).where(
        FilmPersonRole.id == film_person_role_id)

    result = session.exec(statement).one_or_none()

    if result is None:
        raise Exception("Resource Not Found")

    session.delete(result)
    session.commit()

    return FilmPersonRoleReadType.from_pydantic(result)


def get_all_clients() -> List[ClientReadType]:
    session.rollback()
    statement = select(Client)
    results = session.exec(statement).all()

    results_strawberry = [ClientReadType.from_pydantic(client)
                          for client in results]

    return results_strawberry


def get_by_id_a_client(client_id: int) -> ClientReadType:
    session.rollback()
    statement = select(Client).where(Client.id == client_id)
    result = session.exec(statement).first()

    if result is None:
        raise Exception("Resource Not Found")

    return ClientReadType.from_pydantic(result)


def create_a_client(client_create_type: ClientCreateType) -> ClientReadType:
    session.rollback()
    client = client_create_type.to_pydantic()
    new_client = Client(person_id=client.person_id,
                        direction=client.direction,
                        phone=client.phone,
                        email=client.email)

    session.add(new_client)

    session.commit()

    return ClientReadType.from_pydantic(new_client)


def update_a_client(client_id: int, client_create_type: ClientCreateType) \
        -> ClientReadType:
    session.rollback()
    client = client_create_type.to_pydantic()
    statement = select(Client).where(Client.id == client_id)

    result = session.exec(statement).first()

    if result is None:
        raise Exception("Resource Not Found")

    result.person_id = client.person_id
    result.direction = client.direction
    result.phone = client.phone
    result.email = client.email

    session.commit()

    return ClientReadType.from_pydantic(result)


def delete_a_client(client_id: int) -> ClientReadType:
    session.rollback()
    statement = select(Client).where(Client.id == client_id)

    result = session.exec(statement).one_or_none()

    if result is None:
        raise Exception("Resource Not Found")

    session.delete(result)
    session.commit()

    return ClientReadType.from_pydantic(result)
