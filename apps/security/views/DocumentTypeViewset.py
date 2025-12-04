from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.security.services.DocumentTypeService import DocumentTypeService
from apps.security.entity.serializers.DocumentTypeSerializer import DocumentTypeSerializer
from apps.security.entity.models.DocumentType import DocumentType


class DocumentTypeViewset(BaseViewSet):

    service_class = DocumentTypeService
    serializer_class = DocumentTypeSerializer

    # ----------- LIST -----------
    @swagger_auto_schema(
        operation_description="Obtiene una lista de todos los tipos de documento registrados.",
        tags=["DocumentType"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        operation_description="Crea un nuevo tipo de documento.",
        tags=["DocumentType"]
    )
    def create(self, request, *args, **kwargs):
        service = self.service_class()
        instance, error = service.create_document_type(request.data)
        if error:
            return Response({"detail": error}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description="Obtiene la información de un tipo de documento específico.",
        tags=["DocumentType"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description="Actualiza la información completa de un tipo de documento.",
        tags=["DocumentType"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description="Actualiza solo algunos campos de un tipo de documento.",
        tags=["DocumentType"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description="Elimina físicamente un tipo de documento de la base de datos.",
        tags=["DocumentType"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # ----------- SOFT DELETE (custom) -----------
    @swagger_auto_schema(
        method='delete',
        operation_description="Realiza un borrado lógico (soft delete) del tipo de documento especificado.",
        tags=["DocumentType"],
        responses={
            204: openapi.Response("Eliminado lógicamente correctamente."),
            404: openapi.Response("No encontrado.")
        }
    )
    @action(detail=True, methods=['delete'], url_path='soft-delete')
    def soft_destroy(self, request, pk=None):
        deleted = self.service_class().soft_delete(pk)
        if deleted:
            return Response(
                {"detail": "Eliminado lógicamente correctamente."},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {"detail": "No encontrado."},
            status=status.HTTP_404_NOT_FOUND
        )

    # ----------- FILTER (custom) -----------
    @swagger_auto_schema(
        operation_description="Filtra tipos de documento por nombre y estado (activo/inactivo)",
        tags=["DocumentType"],
        manual_parameters=[
            openapi.Parameter('active', openapi.IN_QUERY, description="Estado del tipo de documento (true/false)", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('search', openapi.IN_QUERY, description="Nombre del tipo de documento", type=openapi.TYPE_STRING)
        ],
        responses={200: openapi.Response("Lista de tipos de documento filtrados")}
    )
    @action(detail=False, methods=['get'], url_path='filter')
    def filter_document_types(self, request):
        active = request.query_params.get('active')
        search = request.query_params.get('search')
        service = self.service_class()
        queryset = service.get_filtered_document_types(active, search)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)