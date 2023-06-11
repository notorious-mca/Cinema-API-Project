from typing import List, Optional

from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status, Request

from db.session import get_db
from db.tables.seances import Seance
from db.tables.users import User
from schemas.seances import SeanceCreate, ShowSeance, ShowSeanceForUser
from apis.routes.route_login import get_current_user_from_token
from fastapi.security.utils import get_authorization_scheme_param
from db.instances.seances import *

router = APIRouter()


# =========================== POST : Create a new seance ===========================
@router.post("/create-seance/")
def create_seance(seance:SeanceCreate, db: Session = Depends(get_db),current_user:User = Depends(get_current_user_from_token)):
    seance = create_new_seance(seance=seance, db=db, owner_id=current_user.id)
    print(db.query(Seance.id).all())
    if type(seance) == Seance:
        return {"msg":"Seance successfully created !"}
    return {"msg":"Seance not created (Film ID maybe not found or not available)!"}


# =========================== GET : Get a seance by ID ===========================
@router.get("/get/{id}", response_model=ShowSeance)
def get_seance(id: int, db: Session = Depends(get_db)):
    seance = list_seance(id=id, db=db)
    if not seance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Seance with this id \"{id}\" does not exist",
        )
    return seance


# =========================== GET : Get all seances ===========================
@router.get("/allSeances/",response_model=List[ShowSeance])
def get_all_seances(db:Session = Depends(get_db)):
    seances = list_all_seances(db=db)
    return seances

# =========================== GET : Get my seances ===========================
@router.get("/my-seances/",response_model=List[ShowSeanceForUser])
def get_my_seances(request: Request, db:Session = Depends(get_db), current_user: User = Depends(get_current_user_from_token)):
    token = request.cookies.get("access_token")
    scheme, param = get_authorization_scheme_param(token)  # scheme will hold "Bearer" and param will hold actual token value
    current_user: User = get_current_user_from_token(token=param, db=db)
    seances = db.query(Seance).filter(Seance.owner_id == current_user.id).all()
    return seances

# =========================== GET : Get seances in a specific city ===========================
@router.get('/seance-by-city/{selected_ville}', response_model=List[ShowSeance]) 
def show_seances_by_city(selected_ville, db: Session = Depends(get_db)):
    seances = db.query(Seance).filter(Seance.ville == selected_ville).all()
    return seances

# =========================== GET : Get seances for a specific film ===========================
@router.get("/seance-by-film/{selected_film}") 
def show_Seance_By_Film(selected_film, db: Session = Depends(get_db)):
    film = db.query(Film).filter(Film.titre == selected_film).first()
    seances = db.query(Seance).filter(Seance.film_id == film.id).all()
    return seances


# =========================== PUT : Update a seance by ID ===========================
@router.put("/update/{id}")
def update_seance(request: Request, id: int,seance: SeanceCreate,db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_token)):
    token = request.cookies.get("access_token")
    scheme, param = get_authorization_scheme_param(token)  # scheme will hold "Bearer" and param will hold actual token value
    current_user: User = get_current_user_from_token(token=param, db=db)
    message = update_seance_by_id(id=id,seance=seance,db=db,owner_id=current_user.id)
    if message==0:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Accès refusé ou séance non disponible !")
    elif message==-1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Film with id={seance.film_id} not available (for film_id field) !")
    return {"msg":"Seance successfully updated !"}


# =========================== DELETE : Delete a seance by ID ===========================
@router.delete("/delete/{id}")
def delete_seance(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_token)):
    
    seance = list_seance(id=id, db=db)
    if not seance:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Seance with id={id} does not exist")
    if (seance.owner_id == current_user.id) or (current_user.id == 1):
        delete_seance_by_id(id=id,db=db,owner_id=current_user.id)
        return {"detail":"Seance successfully deleted."}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Accès refusé !")


