from sqlalchemy.orm import Session

from schemas.films import FilmCreate
from db.tables.films import Film


def create_new_film(film:FilmCreate, db:Session, owner_id:int):
    try:
        film_object = Film(**film.dict(), owner_id=owner_id)
        db.add(film_object)
        db.commit()
        db.refresh(film_object)
        return film_object
    except Exception as e:
        return e

# Get a film by a specific ID
def list_film(id: int, db: Session):
    film = db.query(Film).filter(Film.id == id).first()
    return film


# Get the list of all films
def list_all_films(db : Session):
    films = db.query(Film).all()
    return films


# Update film by ID
def update_film_by_id(id:int, film: FilmCreate,db: Session,owner_id):
    existing_film = db.query(Film).filter(Film.id == id)
    if not existing_film.first():
        return 0
    film.__dict__.update(owner_id=owner_id)  #update dictionary with new key value of owner_id
    existing_film.update(film.__dict__)
    db.commit()
    return 1


# Delete film by ID
def delete_film_by_id(id: int,db: Session,owner_id):
    existing_film = db.query(Film).filter(Film.id == id)
    if not existing_film.first():
        return 0
    existing_film.delete(synchronize_session=False)
    db.commit()
    return 1