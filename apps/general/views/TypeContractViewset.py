from urllib import request
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.general.services.TypeContractService import TypeContractService
from apps.general.entity.serializers.TypeContractSerializer import TypeContractSerializer
from apps.general.entity.models.TypeContract import TypeContract


class TypeContractViewset(BaseViewSet):

    service_class = TypeContractService
    serializer_class = TypeContractSerializer

    # ----------- LIST -----------
    @swagger_auto_schema(
        operation_description="Obtiene una lista de todos los tipos de contrato registrados.",
        tags=["TypeContract"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        operation_description="Crea un nuevo tipo de contrato.",
        tags=["TypeContract"]
    )
    def create(self, request, *args, **kwargs):
        service = self.service_class()
        instance, error = service.create_type_contract(request.data)
        if error:
            return Response({"detail": error}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description="Obtiene la información de un tipo de contrato específico.",
        tags=["TypeContract"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description="Actualiza la información completa de un tipo de contrato.",
        tags=["TypeContract"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description="Actualiza solo algunos campos de un tipo de contrato.",
        tags=["TypeContract"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description="Elimina físicamente un tipo de contrato de la base de datos.",
        tags=["TypeContract"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # ----------- SOFT DELETE -----------
    @swagger_auto_schema(
    method='delete',
    operation_description="Realiza un borrado lógico (soft delete) del tipo de contrato especificado.",
    tags=["TypeContract"],
    responses={
        204: openapi.Response("Eliminado lógicamente correctamente."),
        404: openapi.Response("No encontrado.")
    }
    )
    @action(detail=True, methods=['delete'], url_path='soft-delete')
    def soft_destroy(self, request, pk=None):
        """
            Realiza un borrado lógico del tipo de contrato especificado.
        """
        return super().soft_destroy(request, pk)
    
    # ----------- FILTER TYPE CONTRACTS (custom) -----------
    @swagger_auto_schema(
        operation_description="Filtra tipos de contrato por nombre y estado (activo/inactivo)",
        tags=["TypeContract"],
        manual_parameters=[
            openapi.Parameter('active', openapi.IN_QUERY, description="Estado del tipo de contrato (true/false)", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('search', openapi.IN_QUERY, description="Nombre del tipo de contrato", type=openapi.TYPE_STRING)
        ],
        responses={200: openapi.Response("Lista de tipos de contrato filtrados")}
    )
    @action(detail=False, methods=['get'], url_path='filter')
    def filter_type_contracts(self, request):
        active = request.query_params.get('active')
        search = request.query_params.get('search')
        service = self.service_class()
        queryset = service.get_filtered_type_contracts(active, search)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
