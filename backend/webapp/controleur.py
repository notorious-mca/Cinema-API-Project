from webapp.films import route_films
from fastapi import APIRouter


api_router = APIRouter()
api_router.include_router(route_films.router, prefix="", tags=["film-webapp"])