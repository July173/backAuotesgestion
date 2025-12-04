from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.SupportContactRepository import SupportContactRepository
from apps.general.entity.models.SupportContact import SupportContact
from apps.general.entity.serializers.SupportContactSerializer import SupportContactSerializer


class SupportContactService(BaseService):
    def create_support_contact(self, validated_data):
        type_value = validated_data.get('type', '').strip()
        if not type_value:
            return None, "El tipo de contacto es requerido."
        exists = SupportContact.objects.filter(type__iexact=type_value, delete_at__isnull=True).exists()
        if exists:
            return None, "Ya existe un contacto de soporte con ese tipo."        
        serializer = SupportContactSerializer(data=validated_data)
        if serializer.is_valid():
            instance = serializer.save()
            return instance, None
        return None, serializer.errors
    def __init__(self):
        self.repository = SupportContactRepository()


    def get_filtered_support_contacts(self, active=None, search=None):        
        queryset = SupportContact.objects.all()
        if active is not None:
            if str(active).lower() in ['true', '1', 'yes']:
                queryset = queryset.filter(active=True)
            elif str(active).lower() in ['false', '0', 'no']:
                queryset = queryset.filter(active=False)
        if search:
            queryset = queryset.filter(type__icontains=search)
        return queryset
