from typing import List

from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status

from db.session import get_db
from db.instances.films import Film
from schemas.films import FilmCreate,ShowFilm
from db.instances.films import *

router = APIRouter()


# =========================== POST : Create a new film ===========================
@router.post("/create-film/")
def create_film(film:FilmCreate, db:Session=Depends(get_db)):
    current_user = 1
    film = create_new_film(film=film,db=db,owner_id=current_user)
    if type(film) != Film:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Film not created !")
    return {"msg":"Film successfully created !"}


# =========================== GET : Get a film by ID ===========================
@router.get("/get/{id}", response_model=ShowFilm)
def get_film(id: int, db: Session = Depends(get_db)):
    film = list_film(id=id, db=db)
    if not film:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Film with this id \"{id}\" does not exist",
        )
    return film


# =========================== GET : Get all films ===========================
@router.get("/allFilms",response_model=List[ShowFilm])
def get_all_films(db:Session = Depends(get_db)):
    films = list_all_films(db=db)
    return films


# =========================== PUT : Update a film by ID ===========================
@router.put("/update/{id}")
def update_film(id: int,film: FilmCreate,db: Session = Depends(get_db)):
    current_user = 1
    message = update_film_by_id(id=id,film=film,db=db,owner_id=current_user)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Film with id {id} not found !")
    return {"msg":"Film successfully updated !"}


# =========================== DELETE : Delete a film by ID ===========================
@router.delete("/delete/{id}")
def delete_film(id: int,db: Session = Depends(get_db)):
    current_user_id = 1
    message = delete_film_by_id(id=id,db=db,owner_id=current_user_id)
    if not message:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Film with id {id} not found")
    return {"msg":"Film successfully deleted !"}