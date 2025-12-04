from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.SupportScheduleRepository import SupportScheduleRepository
from apps.general.entity.models.SupportSchedule import SupportSchedule
from apps.general.entity.serializers.SupportScheduleSerializer import SupportScheduleSerializer


class SupportScheduleService(BaseService):
    def create_support_schedule(self, validated_data):
        day_range = validated_data.get('day_range', '').strip()
        if not day_range:
            return None, "El rango de días es requerido."
        exists = SupportSchedule.objects.filter(day_range__iexact=day_range, delete_at__isnull=True).exists()
        if exists:
            return None, "Ya existe un horario de soporte con ese rango de días."        
        serializer = SupportScheduleSerializer(data=validated_data)
        if serializer.is_valid():
            instance = serializer.save()
            return instance, None
        return None, serializer.errors
    def __init__(self):
        self.repository = SupportScheduleRepository()


    def get_filtered_support_schedules(self, active=None, search=None):        
        queryset = SupportSchedule.objects.all()
        if active is not None:
            if str(active).lower() in ['true', '1', 'yes']:
                queryset = queryset.filter(active=True)
            elif str(active).lower() in ['false', '0', 'no']:
                queryset = queryset.filter(active=False)
        if search:
            queryset = queryset.filter(day_range__icontains=search)
        return queryset
