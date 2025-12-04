from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.general.entity.models import Apprentice
from apps.security.entity.models import Person, User
from django.utils import timezone
from django.db import transaction

class AprendizRepository(BaseRepository):
    
    def __init__(self):
        super().__init__(Apprentice)


    def update_all_dates_apprentice(self, apprentice, person_data, user_data, file):
        """
        Actualiza persona, usuario y aprendiz en una sola transacción.
        """

        with transaction.atomic():
            # Persona
            for attr, value in person_data.items():
                setattr(apprentice.person, attr, value)
            apprentice.person.save()
            # Usuario
            user = User.objects.filter(person=apprentice.person).first()
            if user:
                for attr, value in user_data.items():
                    setattr(user, attr, value)
                user.save()
            # Aprendiz
            apprentice.ficha = file
            apprentice.save()
            return apprentice

