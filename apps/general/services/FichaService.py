from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.FichaRepository import FichaRepository
from apps.general.entity.models import Ficha
from apps.general.entity.serializers.FichaSerializer import FichaSerializer


class FichaService(BaseService):
    def get_filtered_fichas(self, active=None, search=None):
        queryset = Ficha.objects.all()
        if active is not None:
            if str(active).lower() in ['true', '1', 'yes']:
                queryset = queryset.filter(active=True)
            elif str(active).lower() in ['false', '0', 'no']:
                queryset = queryset.filter(active=False)
        if search:
            queryset = queryset.filter(file_number__icontains=search)
        return queryset

    def __init__(self):
        self.repository = FichaRepository()

    def create_ficha(self, validated_data):
        file_number = validated_data.get('file_number', '')
        file_number_str = str(file_number).strip()
        if not file_number_str:
            return None, "El número de ficha es requerido."
        exists = Ficha.objects.filter(file_number__iexact=file_number_str, delete_at__isnull=True).exists()
        if exists:
            return None, "Ya existe una ficha con ese número."
        # Actualiza el valor en validated_data para que el serializer reciba el string limpio
        validated_data['file_number'] = file_number_str
        serializer = FichaSerializer(data=validated_data)
        if serializer.is_valid():
            instance = serializer.save()
            return instance, None
        return None, serializer.errors
