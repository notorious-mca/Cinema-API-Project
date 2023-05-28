from sqlalchemy import Column, Integer, String, Boolean,Date, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base


class Film(Base):
    id = Column(Integer,primary_key=True, index=True)
    titre = Column(String,nullable=False)
    realisateur = Column(String,nullable=False)
    acteurs_principaux = Column(String,nullable=False)
    duree = Column(String,nullable=False)
    age_min = Column(Integer,nullable=False)
    langue = Column(String,nullable=False)

    # Maybe, à voir
    description = Column(String)
    date_debut = Column(Date)
    date_fin = Column(Date)
    #cover = Column(String)

    owner_id =  Column(Integer,ForeignKey("user.id"))
    owner = relationship("User",back_populates="films")
    
    
    