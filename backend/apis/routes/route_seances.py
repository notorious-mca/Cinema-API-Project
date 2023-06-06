from typing import List, Optional

from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status

from db.session import get_db
from db.tables.seances import Seance
from db.tables.users import User
from schemas.seances import SeanceCreate, ShowSeance
from apis.routes.route_login import get_current_user_from_token
from db.instances.seances import *

router = APIRouter()


# =========================== POST : Create a new film ===========================
@router.post("/create-seance/")
def create_seance(seance:SeanceCreate, db: Session = Depends(get_db),current_user:User = Depends(get_current_user_from_token)):
    seance = create_new_seance(seance=seance, db=db, owner_id=current_user.id)
    print(db.query(Seance.id).all())
    if type(seance) == Seance:
        return {"msg":"Seance successfully created !"}
    return {"msg":"Seance not created !"}


# =========================== GET : Get a film by ID ===========================
@router.get("/get/{id}", response_model=ShowSeance)
def get_seance(id: int, db: Session = Depends(get_db)):
    seance = list_seance(id=id, db=db)
    if not seance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Seance with this id \"{id}\" does not exist",
        )
    return seance


# =========================== GET : Get all films ===========================
@router.get("/allSeances/",response_model=List[ShowSeance])
def get_all_seances(db:Session = Depends(get_db)):
    seances = list_all_seances(db=db)
    return seances


# =========================== PUT : Update a film by ID ===========================
@router.put("/update/{id}")
def update_seance(id: int,seance: SeanceCreate,db: Session = Depends(get_db)):
    current_user = 1
    message = update_seance_by_id(id=id,seance=seance,db=db,owner_id=current_user)
    if message==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Seance with id {id} not found !")
    elif message==-1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Film with id={seance.film_id} not found (for film_id field) !")
    return {"msg":"Seance successfully updated !"}


# =========================== DELETE : Delete a film by ID ===========================
@router.delete("/delete/{id}")
def delete_seance(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_token)):
    
    seance = list_seance(id=id, db=db)
    if not seance:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Seance with id={id} does not exist")
    if (seance.owner_id == current_user.id) or (current_user.id == 1):
        delete_seance_by_id(id=id,db=db,owner_id=current_user.id)
        return {"msg":"Seance successfully deleted."}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Accès refusé !")


