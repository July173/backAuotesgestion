# EnterpriseService.py
from core.base.services.implements.baseService.BaseService import BaseService
from apps.assign.repositories.EnterpriseRepository import EnterpriseRepository


class EnterpriseService(BaseService):
    def __init__(self):
        self.repository = EnterpriseRepository()
