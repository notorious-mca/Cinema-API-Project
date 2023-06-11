from typing import List, Optional

from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status, Request

from db.session import get_db
from db.tables.films import Film
from db.tables.users import User
from schemas.films import FilmCreate, ShowFilm, ShowFilmForUser
from apis.routes.route_login import get_current_user_from_token
from fastapi.security.utils import get_authorization_scheme_param
from db.instances.films import *

router = APIRouter()


# =========================== POST : Create a new film ===========================
@router.post("/create-film/")
def create_film(film:FilmCreate, db: Session = Depends(get_db),current_user:User = Depends(get_current_user_from_token)):
    film = create_new_film(film=film, db=db, owner_id=current_user.id)
    if type(film) == Film:
        return {"msg":"Film successfully created !"}
    return {"msg":"Film not created !"}


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


@router.get("/my-films/",response_model=List[ShowFilmForUser])
def get_my_films(request: Request, db:Session = Depends(get_db), current_user: User = Depends(get_current_user_from_token)):
    token = request.cookies.get("access_token")
    scheme, param = get_authorization_scheme_param(token)  # scheme will hold "Bearer" and param will hold actual token value
    current_user: User = get_current_user_from_token(token=param, db=db)
    films = db.query(Film).filter(Film.owner_id == current_user.id).all()
    return films


# =========================== GET : Autocompletion ===========================
@router.get("/autocomplete")
def autocomplete(term: Optional[str] = None, db: Session = Depends(get_db)):
    """
+    Returns a list of film titles that match a given search term. 
+
+    :param term: (Optional[str]) The search term to use. Defaults to None.
+    :param db: (Session) The database session to use.
+    :return: (List[str]) A list of film titles that match the search term.
    """
    films = search_film(term, db=db)
    films_titres = [film.titre for film in films]
    return films_titres



# =========================== PUT : Update a film by ID ===========================
@router.put("/update/{id}")
def update_film(request: Request, id: int,film: FilmCreate,db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_token)):
    token = request.cookies.get("access_token")
    scheme, param = get_authorization_scheme_param(token)  # scheme will hold "Bearer" and param will hold actual token value
    current_user: User = get_current_user_from_token(token=param, db=db)
    message = update_film_by_id(id=id,film=film,db=db,owner_id=current_user.id)
    if not message:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Accès refusé ou film non disponible !")
    return {"msg":"Film successfully updated !"}


# =========================== DELETE : Delete a film by ID ===========================
@router.delete("/delete/{id}")
def delete_film(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_token)):
    film = list_film(id=id, db=db)
    if not film:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Film with id={id} does not exist")
    print(f"Film Owner ID = {film.owner_id}, Cuurent user ID = {current_user.id}, Current user Admin = {current_user.is_admin}")
    if (film.owner_id == current_user.id) or (current_user.id == 1):
        delete_film_by_id(id=id,db=db,owner_id=current_user.id)
        return {"detail":"Film successfully deleted."}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Accès refusé !")



