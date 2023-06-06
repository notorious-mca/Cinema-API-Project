from typing import Optional

from db.tables.users import User
from fastapi import APIRouter, Request, Depends, status, responses
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.instances.seances import list_all_seances, list_seance
from apis.routes.route_login import get_current_user_from_token
from db.session import get_db
from webapp.seances.forms import SeanceCreateForm
from schemas.seances import SeanceCreate
from db.tables.films import Film
from db.instances.seances import create_new_seance



templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/allSeances")
async def home_seances(request: Request, db: Session = Depends(get_db), msg:str = None):
    seances = list_all_seances(db=db)
    return templates.TemplateResponse("seances/seances.html", {"request": request, "seances":seances})


@router.get("/details/{id}")             #new
def seance_detail(id:int,request: Request,db:Session = Depends(get_db)):    
    seance = list_seance(id=id, db=db)
    return templates.TemplateResponse("seances/detail.html", {"request": request, "seance":seance})



@router.get("/create-seance/")
def create_seance(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    scheme, param = get_authorization_scheme_param(token)  # scheme will hold "Bearer" and param will hold actual token value
    current_user: User = get_current_user_from_token(token=param, db=db)
    films = db.query(Film).filter(Film.owner_id == current_user.id).all()
    return templates.TemplateResponse("seances/create_seance.html", {"request": request, "films":films})


@router.post("/create-seance/")    #new
async def create_seance(request: Request, db: Session = Depends(get_db)):
    form = SeanceCreateForm(request)
    await form.load_data()
    if form.is_valid():
        try:
            token = request.cookies.get("access_token")
            scheme, param = get_authorization_scheme_param(
                token
            )  # scheme will hold "Bearer" and param will hold actual token value
            current_user: User = get_current_user_from_token(token=param, db=db)
            seance = SeanceCreate(**form.__dict__)
            seance = create_new_seance(seance=seance, db=db, owner_id=current_user.id)
            return responses.RedirectResponse(
                f"/seances-webapp/details/{seance.id}", status_code=status.HTTP_302_FOUND
            )
        except Exception as e:
            print(e)
            form.__dict__.get("errors").append("Authentifiez-vous avant de poster un film !")
            return templates.TemplateResponse("seances/create_seance.html", form.__dict__)
    return templates.TemplateResponse("films/create_film.html", form.__dict__)