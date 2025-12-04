from core.base.services.implements.baseService.BaseService import BaseService
from apps.assign.repositories.VisitFollowingRepository import VisitFollowingRepository


class VisitFollowingService(BaseService):
    def __init__(self):
        self.repository = VisitFollowingRepository()
