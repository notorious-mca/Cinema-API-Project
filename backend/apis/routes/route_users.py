from fastapi import APIRouter, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi import Depends
from apis.routes.route_login import get_current_user_from_token
from schemas.users import UserCreate, ShowUser
from db.session import get_db
from db.instances.users import *
from db.tables.users import User
from fastapi.security.utils import get_authorization_scheme_param

router = APIRouter()


@router.post("/", response_model = ShowUser)
def create_user(user : UserCreate,db: Session = Depends(get_db)):
    user = create_new_user(user=user,db=db)
    return user

@router.delete("/delete-user/{id}")
def delete_user(id: int, request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_token)):
    token = request.cookies.get("access_token")
    scheme, param = get_authorization_scheme_param(token)  # scheme will hold "Bearer" and param will hold actual token value
    current_user: User = get_current_user_from_token(token=param, db=db)
    user = list_user(id=id, db=db)
    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Aucun utilisateur enrégistré")
    elif (current_user.id == 1) and id != 1:
        delete_user_by_id(id=id,db=db)
        return {"detail":"User successfully deleted."}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Accès refusé !")