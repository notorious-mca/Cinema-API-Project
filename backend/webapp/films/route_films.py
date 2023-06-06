from typing import Optional

from db.tables.users import User
from fastapi import APIRouter, Request, Depends, status, responses
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.instances.films import list_all_films, list_film, search_film
from apis.routes.route_login import get_current_user_from_token
from db.session import get_db
from webapp.films.forms import FilmCreateForm
from schemas.films import FilmCreate
from db.instances.films import create_new_film



templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/")
async def home(request: Request, db: Session = Depends(get_db), msg:str = None):
    films = list_all_films(db=db)
    return templates.TemplateResponse("general_pages/homepage.html", {"request": request, "films":films, "msg":msg})


@router.get("/film-webapp/details/{id}")
def film_detail(id:int,request: Request,db:Session = Depends(get_db)):    
    film = list_film(id=id, db=db)
    return templates.TemplateResponse("films/detail.html", {"request": request, "film":film})


@router.get("/search/")
def search(request: Request, db: Session = Depends(get_db), query: Optional[str] = None):
    films = search_film(query, db=db)
    return templates.TemplateResponse("general_pages/homepage.html", {"request": request, "films": films})


@router.get("/film-webapp/create-film/") 
def create_film(request: Request, db: Session = Depends(get_db), msg:str = None):
    return templates.TemplateResponse("films/create_film.html", {"request": request, "msg":msg})


@router.post("/film-webapp/create-film/")
async def create_film(request: Request, db: Session = Depends(get_db)):
    form = FilmCreateForm(request)
    await form.load_data()
    if form.is_valid():
        try:
            token = request.cookies.get("access_token")
            scheme, param = get_authorization_scheme_param(
                token
            )  # scheme will hold "Bearer" and param will hold actual token value
            current_user: User = get_current_user_from_token(token=param, db=db)
            film = FilmCreate(**form.__dict__)
            film = create_new_film(film=film, db=db, owner_id=current_user.id)
            return responses.RedirectResponse(
                f"/film-webapp/details/{film.id}", status_code=status.HTTP_302_FOUND
            )
        except Exception as e:
            print(e)
            form.__dict__.get("errors").append("Authentifiez-vous avant de poster un film !")
            return templates.TemplateResponse("films/create_film.html", form.__dict__)
    return templates.TemplateResponse("films/create_film.html", form.__dict__)