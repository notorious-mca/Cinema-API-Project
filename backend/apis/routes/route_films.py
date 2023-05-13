from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status

from db.session import get_db
from db.instances.films import Film
from schemas.films import FilmCreate,ShowFilm
from db.instances.films import create_new_film

router = APIRouter()


@router.post("/create-film/",response_model=ShowFilm)
def create_film(film:FilmCreate, db:Session=Depends(get_db)):
    current_user = 1
    film = create_new_film(film=film,db=db,owner_id=current_user)
    return film