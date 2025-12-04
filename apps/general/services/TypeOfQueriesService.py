from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.TypeOfQueriesRepository import TypeOfQueriesRepository
from apps.general.entity.models.TypeOfQueries import TypeOfQueries


class TypeOfQueriesService(BaseService):
    def create_type_of_queries(self, validated_data):
        name = validated_data.get('name', '').strip()
        if not name:
            return None, "El nombre es requerido."
        from apps.general.entity.models.TypeOfQueries import TypeOfQueries
        exists = TypeOfQueries.objects.filter(name__iexact=name, delete_at__isnull=True).exists()
        if exists:
            return None, "Ya existe un tipo de consulta con ese nombre."
        from apps.general.entity.serializers.TypeOfQueriesSerializer import TypeOfQueriesSerializer
        serializer = TypeOfQueriesSerializer(data=validated_data)
        if serializer.is_valid():
            instance = serializer.save()
            return instance, None
        return None, serializer.errors

    def __init__(self):
        self.repository = TypeOfQueriesRepository()

    def get_filtered_type_of_queries(self, active=None, search=None):
        queryset = TypeOfQueries.objects.all()
        if active is not None:
            if str(active).lower() in ['true', '1', 'yes']:
                queryset = queryset.filter(active=True)
            elif str(active).lower() in ['false', '0', 'no']:
                queryset = queryset.filter(active=False)
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset
