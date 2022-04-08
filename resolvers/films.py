from typing import List

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from databases.db import get_db_session
from graphql_app.schemas.films import (CategoryCreateType,
                                       CategoryReadType, FilmReadType,
                                       FilmCreateType, SeasonReadType,
                                       SeasonCreateType, ChapterReadType,
                                       ChapterCreateType, PosterReadType)
from models.films_and_rents import (Category, Film, Season, Chapter,
                                    Poster)
from s3_events.s3_utils import S3_SERVICE

# S3 related imports
import os
from dotenv import load_dotenv
from fastapi.param_functions import File
from fastapi.datastructures import UploadFile
import datetime

from utilities.logger import Logger

load_dotenv()

router = APIRouter()

session = get_db_session()

# S3 service environment variables and service
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.environ.get("AWS_REGION")
S3_Bucket = os.environ.get("S3_Bucket")
S3_Key = os.environ.get("S3_Key")

# Object of S3_SERVICE Class
s3_client = S3_SERVICE(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)


# Film Related Resolvers
def get_all_categories() -> List[CategoryReadType]:
    session.rollback()
    statement = select(Category)
    results = session.exec(statement).all()

    results_strawberry = [CategoryReadType.from_pydantic(category)
                          for category in results]

    return results_strawberry


def get_by_id_a_category(category_id: int) -> CategoryReadType:
    session.rollback()
    statement = select(Category).where(Category.id == category_id)
    result = session.exec(statement).first()

    if result is None:
        raise Exception("Resource Not Found")

    return CategoryReadType.from_pydantic(result)


def create_a_category(category_create_type: CategoryCreateType) \
        -> CategoryReadType:
    session.rollback()
    category = category_create_type.to_pydantic()
    new_category = Category(name=category.name,
                            description=category.description)
    session.add(new_category)

    session.commit()

    return CategoryReadType.from_pydantic(new_category)


def update_a_category(category_id: int, category_create_type:
                      CategoryCreateType) -> CategoryReadType:
    session.rollback()
    category = category_create_type.to_pydantic()

    statement = select(Category).where(Category.id == category_id)

    result = session.exec(statement).first()

    if result is None:
        raise Exception("Resource Not Found")

    result.name = category.name
    result.description = category.description

    session.commit()

    return CategoryReadType.from_pydantic(result)


def delete_a_category(category_id: int) -> CategoryReadType:
    session.rollback()
    statement = select(Category).where(Category.id == category_id)

    result = session.exec(statement).one_or_none()

    if result is None:
        raise Exception("Resource Not Found")

    session.delete(result)
    session.commit()

    return CategoryReadType.from_pydantic(result)


def get_all_films() -> List[FilmReadType]:
    session.rollback()
    statement = select(Film)
    results = session.exec(statement).all()

    for film in results:
        if film:
            film.availability = Film.get_availability(film.id)
            session.commit()

    results_strawberry = [FilmReadType.from_pydantic(film)
                          for film in results]

    return results_strawberry


def get_by_id_a_film(film_id: int) -> FilmReadType:
    session.rollback()
    statement = select(Film).where(Film.id == film_id)
    result = session.exec(statement).first()

    if result:
        result.availability = Film.get_availability(film_id)
        session.commit()
    else:
        raise Exception("Resource Not Found")

    return FilmReadType.from_pydantic(result)


def create_a_film(film_create_type: FilmCreateType) -> FilmReadType:
    session.rollback()
    film = film_create_type.to_pydantic()
    new_film = Film(title=film.title,
                    description=film.description,
                    release_date=film.release_date,
                    category_id=film.category_id,
                    price_by_day=film.price_by_day,
                    stock=film.stock,
                    film_type=film.film_type,
                    film_prequel_id=film.film_prequel_id,
                    availability=film.stock)

    session.add(new_film)

    session.commit()

    return FilmReadType.from_pydantic(new_film)


def update_a_film(film_id: int,
                  film_create_type: FilmCreateType) -> FilmReadType:
    session.rollback()
    film = film_create_type.to_pydantic()
    statement = select(Film).where(Film.id == film_id)

    result = session.exec(statement).first()

    if result is None:
        raise Exception("Resource Not Found")

    result.title = film.title
    result.description = film.description
    result.release_date = film.release_date
    result.category_id = film.category_id
    result.price_by_day = film.price_by_day
    result.stock = film.stock
    result.film_type = film.film_type
    result.film_prequel_id = film.film_prequel_id
    if result:
        result.availability = Film.get_availability(film_id)

    session.commit()

    return FilmReadType.from_pydantic(result)


def delete_a_film(film_id: int) -> FilmReadType:
    session.rollback()
    statement = select(Film).where(Film.id == film_id)

    result = session.exec(statement).one_or_none()

    if result is None:
        raise Exception("Resource Not Found")

    session.delete(result)
    session.commit()

    return FilmReadType.from_pydantic(result)


async def get_all_posters() -> List[PosterReadType]:
    session.rollback()
    statement = select(Poster)
    results = session.exec(statement).all()

    results_strawberry = [PosterReadType.from_pydantic(poster)
                          for poster in results]

    return results_strawberry


def get_by_id_a_poster(poster_id: int) -> PosterReadType:
    session.rollback()
    statement = select(Poster).where(Poster.id == poster_id)
    result = session.exec(statement).first()

    if result is None:
        raise Exception("Resource Not Found")

    return PosterReadType.from_pydantic(result)


@router.post("/api/poster/upload/{film_id}", status_code=200,
             description="Upload png poster asset to S3 ")
async def upload_poster(
        film_id: int, fileobject: UploadFile = File(...)):
    filename = fileobject.filename
    current_time = datetime.datetime.now()
    # split the file name into two different path (string +  extention)
    split_file_name = os.path.splitext(
        filename)

    # for realtime application you must have genertae unique name for the file
    file_name_unique = str(current_time.timestamp()).replace('.', '')

    file_extension = split_file_name[1]  # file extention
    # Converting tempfile.SpooledTemporaryFile to io.BytesIO
    data = fileobject.file._file
    uploads3 = await s3_client.upload_fileobj(
        bucket=S3_Bucket,
        key=S3_Key + file_name_unique + file_extension,
        fileobject=data)

    if uploads3:
        s3_url = f"https://" \
                 f"{S3_Bucket}.s3.{AWS_REGION}.amazonaws.com/" \
                 f"{S3_Key}{file_name_unique + file_extension}"
        Logger.info(f"s3_url:{s3_url}")

        session.rollback()
        new_poster = Poster(film_id=film_id,
                            link=s3_url)
        session.add(new_poster)
        session.commit()

        return {"status": "success", "image_url": s3_url}  # response added
    else:
        raise HTTPException(status_code=400, detail="Failed to upload in S3")


def delete_a_poster(poster_id: int) -> PosterReadType:
    session.rollback()
    statement = select(Poster).where(Poster.id == poster_id)

    result = session.exec(statement).one_or_none()

    if result is None:
        raise Exception("Resource Not Found")

    session.delete(result)
    session.commit()

    return PosterReadType.from_pydantic(result)


def get_all_seasons() -> List[SeasonReadType]:
    session.rollback()
    statement = select(Season)
    results = session.exec(statement).all()

    results_strawberry = [SeasonReadType.from_pydantic(season)
                          for season in results]

    return results_strawberry


def get_by_a_season(season_id: int) -> SeasonReadType:
    session.rollback()
    statement = select(Season).where(Season.id == season_id)
    result = session.exec(statement).first()

    if result is None:
        raise Exception("Resource Not Found")

    return SeasonReadType.from_pydantic(result)


def create_a_season(season_create_type: SeasonCreateType) -> SeasonReadType:
    session.rollback()
    season = season_create_type.to_pydantic()
    new_season = Season(film_id=season.film_id,
                        title=season.title,
                        season_prequel_id=season.season_prequel_id)

    session.add(new_season)
    session.commit()

    return SeasonReadType.from_pydantic(new_season)


def update_a_season(season_id: int,
                    season_create_type: SeasonCreateType) -> SeasonReadType:
    session.rollback()
    season = season_create_type.to_pydantic()

    statement = select(Season).where(Season.id == season_id)

    result = session.exec(statement).first()

    if result is None:
        raise Exception("Resource Not Found")

    result.film_id = season.film_id
    result.title = season.title
    result.season_prequel_id = season.season_prequel_id

    session.commit()

    return SeasonReadType.from_pydantic(result)


def delete_a_season(season_id: int) -> SeasonReadType:
    session.rollback()
    statement = select(Season).where(Season.id == season_id)

    result = session.exec(statement).one_or_none()

    if result is None:
        raise Exception("Resource Not Found")

    session.delete(result)
    session.commit()

    return SeasonReadType.from_pydantic(result)


def get_all_chapters() -> List[ChapterReadType]:
    session.rollback()
    statement = select(Chapter)
    results = session.exec(statement).all()

    results_strawberry = [ChapterReadType.from_pydantic(chapter)
                          for chapter in results]

    return results_strawberry


def get_by_id_a_chapter(chapter_id: int) -> ChapterReadType:
    session.rollback()
    statement = select(Chapter).where(Chapter.id == chapter_id)
    result = session.exec(statement).first()

    if result is None:
        raise Exception("Resource Not Found")

    return ChapterReadType.from_pydantic(result)


def create_a_chapter(
        chapter_create_type: ChapterCreateType) -> ChapterReadType:
    session.rollback()
    chapter = chapter_create_type.to_pydantic()
    new_chapter = Chapter(season_id=chapter.season_id,
                          title=chapter.title,
                          chapter_prequel_id=chapter.chapter_prequel_id)

    session.add(new_chapter)

    session.commit()

    return ChapterReadType.from_pydantic(new_chapter)


def update_a_chapter(chapter_id: int,
                     chapter_create_type: ChapterCreateType) \
        -> ChapterReadType:
    session.rollback()
    chapter = chapter_create_type.to_pydantic()

    statement = select(Chapter).where(Chapter.id == chapter_id)

    result = session.exec(statement).first()

    if result is None:
        raise Exception("Resource Not Found")

    result.season_id = chapter.season_id
    result.title = chapter.title
    result.chapter_prequel_id = chapter.chapter_prequel_id

    session.commit()

    return ChapterReadType.from_pydantic(result)


def delete_a_chapter(chapter_id: int) -> ChapterReadType:
    session.rollback()
    statement = select(Chapter).where(Chapter.id == chapter_id)

    result = session.exec(statement).one_or_none()

    if result is None:
        raise Exception("Resource Not Found")

    session.delete(result)
    session.commit()

    return ChapterReadType.from_pydantic(result)
