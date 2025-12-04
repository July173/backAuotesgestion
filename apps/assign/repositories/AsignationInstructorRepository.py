from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.assign.entity.models import AsignationInstructor


class AsignationInstructorRepository(BaseRepository):
    def __init__(self):
        super().__init__(AsignationInstructor)
        
    def create_custom(self, instructor, request_asignation):
        return self.model.objects.create(
            instructor=instructor,
            request_asignation=request_asignation
        )
