from typing import Optional
from pydantic import BaseModel
from datetime import date,datetime, timedelta


#shared properties
class SeanceBase(BaseModel):
    ville : Optional[str] = None
    adresse : Optional[str] = None
    date_debut : Optional[date] = datetime.now().date()
    date_fin : Optional[date] = datetime.now().date() + timedelta(days=10)
    heure_debut : Optional[str] = None
    duree : Optional[str] = None


class SeanceCreate(SeanceBase):
    film_id : int
    ville : str
    adresse : str
    heure_debut : str
    duree : str
    

    
#this will be used to format the response to not to have id,owner_id etc
class ShowSeance(SeanceBase):
    ville : str
    adresse : str
    heure_debut : str
    duree : str
    date_debut : Optional[date]
    date_fin : Optional[date]

    class Config():  #to convert non dict obj to json
        orm_mode = True


class ShowSeanceForUser(SeanceBase):
    id : int
    ville : str
    adresse : str
    heure_debut : str
    duree : str
    date_debut : Optional[date]
    date_fin : Optional[date]
    film_titre : Optional[str]

    class Config():  #to convert non dict obj to json
        orm_mode = True