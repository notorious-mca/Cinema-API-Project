from sqlalchemy.orm import Session

from schemas.seances import SeanceCreate
from db.tables.films import Film
from db.tables.seances import Seance


def create_new_seance(seance:SeanceCreate, db:Session, owner_id:int):
    seance_object = Seance(**seance.dict(), owner_id=owner_id)
    film_ids = db.query(Film.id).filter(Film.owner_id == owner_id).all()
    if seance_object.film_id in [x[0] for x in film_ids]:
        print(type(seance_object))
        db.add(seance_object)
        db.commit()
        db.refresh(seance_object)
        print("Seance added !")
        return seance_object
    else:
        print("Film ID not found !")
        return {"msg":"Film not found !"}

# Get a seance by a specific ID
def list_seance(id: int, db: Session):
    seance = db.query(Seance).filter(Seance.id == id).first()
    return seance


# Get the list of all seances
def list_all_seances(db : Session):
    seances = db.query(Seance).all()
    return seances


# Update seance by ID
def update_seance_by_id(id:int, seance: SeanceCreate,db: Session,owner_id):
    existing_seance = db.query(Seance).filter(Seance.id == id, Seance.owner_id==owner_id)
    print(seance.film_id)
    if not existing_seance.first():
        return 0
    # Vérification de l'identifiant de film
    existing_film = db.query(Film.id).filter(Film.owner_id == owner_id).all()
    if not seance.film_id in [x[0] for x in existing_film]:
        return -1
    existing_seance.update(seance.__dict__)
    db.commit()
    return 1


# Delete seance by ID
def delete_seance_by_id(id: int,db: Session,owner_id):
    existing_seance = db.query(Seance).filter(Seance.id == id)
    if not existing_seance.first():
        return 0
    existing_seance.delete(synchronize_session=False)
    db.commit()
    return 1


# Search a seance
def search_seance(query: str, db: Session):
    seances = db.query(Seance).filter(Seance.ville.contains(query))
    return seances