from sqlalchemy.orm import Session

from schemas.films import FilmCreate
from db.tables.films import Film


def create_new_film(film:FilmCreate, db:Session, owner_id:int):
    film_object = Film(**film.dict(), owner_id=owner_id)
    db.add(film_object)
    db.commit()
    db.refresh(film_object)

    return film_object