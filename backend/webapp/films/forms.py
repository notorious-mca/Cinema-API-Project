from typing import List, Optional

from fastapi import Request


class FilmCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.titre: Optional[str] = None
        self.realisateur: Optional[str] = None
        self.acteurs_principaux: Optional[str] = None
        self.duree: Optional[str] = None
        self.age_min: Optional[int] = None
        self.description: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.titre = form.get("titre")
        self.realisateur = form.get("realisateur")
        self.acteurs_principaux = form.get("acteurs_principaux")
        self.duree = form.get("duree")
        self.age_min = int(form.get("age_min"))
        self.description = form.get("description")

    def is_valid(self):
        if not self.titre :
            self.errors.append("Veuillez entrer un titre")
        if not self.realisateur :
            self.errors.append("Veuillez entrer un/des réalisateur(s)")
        if not self.acteurs_principaux:
            self.errors.append("Veuillez entrer un/des acteur(s) principal(aux)")
        if not self.duree :
            self.errors.append("Veuillez entrer la durée")
        if not self.age_min or type(self.age_min) != int:
            self.errors.append("Veuillez entrer l'âge minimum requis")
        if not self.description or not len(self.description) >= 20:
            self.errors.append("Description trop courte.")
        if not self.errors:
            return True
        return False