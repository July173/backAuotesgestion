from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.security.entity.models import FormModule


class FormModuleRepository(BaseRepository):
    def __init__(self):
        super().__init__(FormModule)
