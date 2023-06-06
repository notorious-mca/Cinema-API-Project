from sqlalchemy import Column, Integer, ForeignKey, String, Date
from sqlalchemy.orm import relationship

from db.base_class import Base

class Seance(Base):
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('user.id'))
    film_id = Column(Integer, ForeignKey('film.id'))
    ville = Column(String,nullable=False)
    adresse = Column(String,nullable=False)
    date_debut = Column(Date,nullable=False)
    date_fin = Column(Date,nullable=False)
    heure_debut = Column(String,nullable=False)
    duree = Column(String,nullable=False)

    owner = relationship("User", back_populates="seances")
    film_seances = relationship("Film", back_populates="seances")

    @property
    def film_titre(self):
        return self.film_seances.titre
