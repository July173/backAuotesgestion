from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.general.services.SupportContactService import SupportContactService
from apps.general.entity.serializers.SupportContactSerializer import SupportContactSerializer
from apps.general.entity.models.SupportContact import SupportContact


class SupportContactViewset(BaseViewSet):

    service_class = SupportContactService
    serializer_class = SupportContactSerializer

    # ----------- LIST -----------
    @swagger_auto_schema(
        operation_description="Obtiene una lista de todos los contactos de soporte registrados.",
        tags=["SupportContact"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        operation_description="Crea un nuevo contacto de soporte.",
        tags=["SupportContact"]
    )
    def create(self, request, *args, **kwargs):
        service = self.service_class()
        instance, error = service.create_support_contact(request.data)
        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"detail": error}, status=status.HTTP_400_BAD_REQUEST)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description="Obtiene la información de un contacto de soporte específico.",
        tags=["SupportContact"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description="Actualiza la información completa de un contacto de soporte.",
        tags=["SupportContact"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description="Actualiza solo algunos campos de un contacto de soporte.",
        tags=["SupportContact"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description="Elimina físicamente un contacto de soporte de la base de datos.",
        tags=["SupportContact"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # ----------- SOFT DELETE (custom) -----------
    @swagger_auto_schema(
        operation_description="Elimina lógicamente (soft delete) un contacto de soporte, marcándolo como inactivo.",
        tags=["SupportContact"]
    )
    @action(detail=True, methods=["delete"], url_path="soft-delete")
    def soft_delete(self, request, pk=None):
        instance = self.service.get(pk)
        if not instance:
            return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
        self.service.soft_delete(pk)
        return Response({"detail": "Eliminado lógicamente correctamente."}, status=status.HTTP_200_OK)

    # ----------- FILTER SUPPORT CONTACTS (custom) -----------
    @swagger_auto_schema(
        operation_description="Filtra contactos de soporte por nombre y estado (activo/inactivo)",
        tags=["SupportContact"],
        manual_parameters=[
            openapi.Parameter('active', openapi.IN_QUERY, description="Estado del contacto de soporte (true/false)", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('search', openapi.IN_QUERY, description="Nombre del contacto de soporte", type=openapi.TYPE_STRING)
        ],
        responses={200: openapi.Response("Lista de contactos de soporte filtrados")}
    )
    @action(detail=False, methods=['get'], url_path='filter')
    def filter_support_contacts(self, request):
        active = request.query_params.get('active')
        search = request.query_params.get('search')
        service = self.service_class()
        queryset = service.get_filtered_support_contacts(active, search)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)