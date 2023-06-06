from typing import List, Optional
from datetime import date
from fastapi import Request
from datetime import date, datetime, timedelta

class SeanceCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.film_id: Optional[int] = None
        self.ville: Optional[str] = None
        self.adresse: Optional[str] = None
        self.date_debut: Optional[date] = datetime.now().date()
        self.date_fin: Optional[date] = datetime.now().date() + timedelta(days=10)
        self.heure_debut: Optional[str] = None
        self.duree: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.film_id = int(form.get("film_id"))
        self.ville = form.get("ville")
        self.adresse = form.get("adresse")
        self.date_debut = form.get("date_debut") if form.get("date_debut") else datetime.now().date()
        self.date_fin = form.get("date_fin") if form.get("date_fin") else datetime.now().date() + timedelta(days=10)
        self.heure_debut = form.get("heure_debut")
        self.duree = form.get("duree")

    def is_valid(self):
        if not self.ville :
            self.errors.append("Entrez la ville de la séance")
        if not self.adresse :
            self.errors.append("Entrez l'adresse de la séance")
        if not self.heure_debut:
            self.errors.append("Entrez l'heure de début de la séance")
        if not self.duree:
            self.errors.append("Entrez la durée de la séance")
        if not self.film_id:
            self.errors.append("Le film n'a pas été sélectionné")
        if not self.errors:
            return True
        return False