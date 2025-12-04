from core.base.services.implements.baseService.BaseService import BaseService
from apps.assign.repositories.BossRepository import BossRepository


class BossService(BaseService):
    def __init__(self):
        self.repository = BossRepository()

    def get_by_enterprise(self, enterprise_id):
        return self.repository.model.objects.filter(enterprise_id=enterprise_id)
