from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.ColorsRepository import ColorsRepository
from apps.general.entity.serializers.ColorsSerializer import ColorsSerializer



class ColorsService(BaseService):
    def get_filtered_colors(self, active=None, search=None):
        from apps.general.entity.models.Colors import Colors
        queryset = Colors.objects.all()
        if active is not None:
            if str(active).lower() in ['true', '1', 'yes']:
                queryset = queryset.filter(active=True)
            elif str(active).lower() in ['false', '0', 'no']:
                queryset = queryset.filter(active=False)
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset

    def __init__(self):
        super().__init__(ColorsRepository())

    def create_color(self, validated_data):
        name = validated_data.get('name', '').strip()
        if not name:
            return None, "El nombre es requerido."
        from apps.general.entity.models.Colors import Colors
        exists = Colors.objects.filter(name__iexact=name, delete_at__isnull=True).exists()
        if exists:
            return None, "Ya existe un color con ese nombre."
        serializer = ColorsSerializer(data=validated_data)
        if serializer.is_valid():
            instance = serializer.save()
            return instance, None
        return None, serializer.errors
