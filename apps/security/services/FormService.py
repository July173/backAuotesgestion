from core.base.services.implements.baseService.BaseService import BaseService
from apps.security.repositories.FormRepository import FormRepository
from apps.security.entity.models import Form
from apps.security.entity.serializers.FormSerializer import FormSerializer


class FormService(BaseService):
    def __init__(self):
        super().__init__(FormRepository())
    
    def get_filtered_forms(self, active=None, search=None):
        
        queryset = Form.objects.all()
        if active is not None:
            if str(active).lower() in ['true', '1', 'yes']:
                queryset = queryset.filter(active=True)
            elif str(active).lower() in ['false', '0', 'no']:
                queryset = queryset.filter(active=False)
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset

    def create_form(self, validated_data):
        name = validated_data.get('name', '').strip()
        if not name:
            return None, "El nombre es requerido."
        exists = Form.objects.filter(name__iexact=name, delete_at__isnull=True).exists()
        if exists:
            return None, "Ya existe un formulario con ese nombre."
        serializer = FormSerializer(data=validated_data)
        if serializer.is_valid():
            instance = serializer.save()
            return instance, None
        return None, serializer.errors

    