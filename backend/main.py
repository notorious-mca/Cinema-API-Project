#main.py 

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from core.config import settings
from apis.contoleur import api_router
from db.session import engine   
from db.models import Base
from fastapi.staticfiles import StaticFiles
from webapp.controleur import api_router as web_app_router


def include_router(app):
	app.include_router(api_router)
	app.include_router(web_app_router)


def create_tables():
	print("create_tables")
	Base.metadata.create_all(bind=engine)

def configure_static(app):
    app.mount("/static", StaticFiles(directory="static"), name="static")

	
def start_application():
	app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
	include_router(app)
	configure_static(app)
	create_tables()
	return app

app = start_application()