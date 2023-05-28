from typing import Optional
from pydantic import BaseModel
from datetime import date,datetime, timedelta


#shared properties
class FilmBase(BaseModel):
    titre : Optional[str] = None
    realisateur : Optional[str] = None
    acteurs_principaux : Optional[str] = None
    duree : Optional[str] = None
    age_min : Optional[int] = None
    langue : Optional[str] = "Français"
    #cover : Optional[str] = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTiFzTA1xqPC1yUhWY0WYtE2Gx2lkAMmVztuQ&usqp=CAU"

    description : Optional[str] = None
    date_debut : Optional[date] = datetime.now().date()
    date_fin : Optional[date] = datetime.now().date() + timedelta(days=10)
    


class FilmCreate(FilmBase):
    titre : str
    realisateur : str
    acteurs_principaux : str
    duree : str
    age_min : int
    

    
#this will be used to format the response to not to have id,owner_id etc
class ShowFilm(FilmBase):
    titre : str
    realisateur : str
    acteurs_principaux : str
    duree : str
    age_min : int
    langue : Optional[str]
    #cover : Optional[str]

    description : Optional[str]
    date_debut : Optional[date]
    date_fin : Optional[date]

    class Config():  #to convert non dict obj to json
        orm_mode = True