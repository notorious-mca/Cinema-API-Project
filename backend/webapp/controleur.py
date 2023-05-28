from webapp.films import route_films
from fastapi import APIRouter
from webapp.users import route_users
from webapp.auth import route_login

api_router = APIRouter()
api_router.include_router(route_films.router, prefix="", tags=["film-webapp"])
api_router.include_router(route_users.router, prefix="", tags=["users-webapp"])
api_router.include_router(route_login.router, prefix="", tags=["auth-webapp"])