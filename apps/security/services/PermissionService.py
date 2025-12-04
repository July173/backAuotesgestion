from core.base.services.implements.baseService.BaseService import BaseService
from apps.security.repositories.PerimissionRepository import PermissionRepository


class PermissionService(BaseService):
    def __init__(self):
        self.repository = PermissionRepository()