from django.db.models import Q
from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.general.entity.models import Instructor

class InstructorRepository(BaseRepository):
    def __init__(self):
        super().__init__(Instructor)
    
    def get_filtered_instructors(self, search=None, knowledge_area_id=None, is_followup=None):
        queryset = self.model.objects.select_related('person', 'knowledge_area').all()
        if search:
            queryset = queryset.filter(
                Q(person__first_name__icontains=search) |
                Q(person__second_name__icontains=search) |
                Q(person__first_last_name__icontains=search) |
                Q(person__second_last_name__icontains=search) |
                Q(person__number_identification__icontains=search)
            )
        if knowledge_area_id:
            queryset = queryset.filter(knowledge_area__id=knowledge_area_id)
        # Filtrar por instructores de seguimiento si se solicita
        if is_followup is not None and is_followup != 'all':
            if is_followup == 'true':
                queryset = queryset.filter(is_followup_instructor=True)
            elif is_followup == 'false':
                queryset = queryset.filter(is_followup_instructor=False)
        return queryset
