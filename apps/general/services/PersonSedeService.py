from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.PersonSedeRepository import PersonSedeRepository


class PersonSedeService(BaseService):
    def __init__(self):
        self.repository = PersonSedeRepository()
