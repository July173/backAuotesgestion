from core.base.services.implements.baseService.BaseService import BaseService
from apps.assign.repositories.VisitFollowingRepository import VisitFollowingRepository
from apps.assign.entity.serializers.VisitFollowingUpdateSerializer import VisitFollowingUpdateSerializer


class VisitFollowingService(BaseService):
    def __init__(self):
        self.repository = VisitFollowingRepository()
    
    def partial_update_excluding(self, visit_id, data, exclude_fields=None):
        """
        Actualiza parcialmente un VisitFollowing excluyendo los campos indicados en exclude_fields.
        Retorna la instancia actualizada o None si no existe.
        """
        if exclude_fields is None:
            exclude_fields = []
        visit = self.repository.get_by_id(visit_id)
        if not visit:
            return None
        # Build payload excluding protected fields
        allowed_payload = {k: v for k, v in (data or {}).items() if k not in exclude_fields}
        # Validate with serializer to ensure proper types/limits
        serializer = VisitFollowingUpdateSerializer(instance=visit, data=allowed_payload, partial=True)
        if not serializer.is_valid():
            # raise value error with serializer errors so caller can return 400
            raise ValueError(serializer.errors)
        serializer.save()
        return serializer.instance
