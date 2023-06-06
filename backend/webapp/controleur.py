from webapp.films import route_films
from fastapi import APIRouter
from webapp.users import route_users
from webapp.auth import route_login
from webapp.seances import route_seances

api_router = APIRouter()
api_router.include_router(route_films.router, prefix="", tags=["films-webapp"])
api_router.include_router(route_users.router, prefix="/users-webapp", tags=["users-webapp"])
api_router.include_router(route_login.router, prefix="/auth-webapp", tags=["auth-webapp"])
api_router.include_router(route_seances.router, prefix="/seances-webapp", tags=["seances-webapp"])