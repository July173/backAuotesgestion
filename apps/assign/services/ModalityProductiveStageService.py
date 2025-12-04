from core.base.services.implements.baseService.BaseService import BaseService
from apps.assign.repositories.ModalityProductiveStageRepository import ModalityProductiveStageRepository


class ModalityProductiveStageService(BaseService):
    def __init__(self):
        self.repository = ModalityProductiveStageRepository()
