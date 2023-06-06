from fastapi import APIRouter
from apis.routes import route_homepage, route_users, route_films, route_login, route_seances


api_router = APIRouter()
#api_router.include_router(route_homepage.homepage_router,prefix="",tags=["Homepage"])
api_router.include_router(route_users.router,prefix="/users",tags=["Users"])
api_router.include_router(route_films.router,prefix="/films",tags=["Films"])
api_router.include_router(route_login.router,prefix="/login",tags=["Login"])
api_router.include_router(route_seances.router,prefix="/seances",tags=["Séances"])