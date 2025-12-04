from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.TypeContractRepository import TypeContractRepository
from apps.general.entity.models.TypeContract import TypeContract
from apps.general.entity.serializers.TypeContractSerializer import TypeContractSerializer



class TypeContractService(BaseService):
    def __init__(self):
        super().__init__(TypeContractRepository())

    def get_filtered_type_contracts(self, active=None, search=None):        
        queryset = TypeContract.objects.all()
        if active is not None:
            if str(active).lower() in ['true', '1', 'yes']:
                queryset = queryset.filter(active=True)
            elif str(active).lower() in ['false', '0', 'no']:
                queryset = queryset.filter(active=False)
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset

    def create_type_contract(self, validated_data):
        name = validated_data.get('name', '').strip()
        if not name:
            return None, "El nombre es requerido."
        exists = TypeContract.objects.filter(name__iexact=name, delete_at__isnull=True).exists()
        if exists:
            return None, "Ya existe un tipo de contrato con ese nombre."
        serializer = TypeContractSerializer(data=validated_data)
        if serializer.is_valid():
            instance = serializer.save()
            return instance, None
        return None, serializer.errors
