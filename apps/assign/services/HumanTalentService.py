from core.base.services.implements.baseService.BaseService import BaseService
from apps.assign.repositories.HumanTalentRepository import HumanTalentRepository


class HumanTalentService(BaseService):
    def __init__(self):
        self.repository = HumanTalentRepository()

    def get_by_enterprise(self, enterprise_id):
        return self.repository.model.objects.filter(enterprise_id=enterprise_id)
