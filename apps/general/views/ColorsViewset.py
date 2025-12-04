from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.general.services.ColorsService import ColorsService
from apps.general.entity.serializers.ColorsSerializer import ColorsSerializer
from rest_framework.response import Response


class ColorsViewset(BaseViewSet):

    service_class = ColorsService
    serializer_class = ColorsSerializer

    @swagger_auto_schema(
        operation_description="Obtiene una lista de todos los colores registrados.",
        tags=["Colors"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        operation_description="Crea un nuevo color.",
        tags=["Colors"]
    )
    def create(self, request, *args, **kwargs):
        service = self.service_class()
        instance, error = service.create_color(request.data)
        if error:
            return Response({"detail": error}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description="Obtiene la información de un color específico.",
        tags=["Colors"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description="Actualiza la información completa de un color.",
        tags=["Colors"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description="Actualiza solo algunos campos de un color.",
        tags=["Colors"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description="Elimina físicamente un color de la base de datos.",
        tags=["Colors"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
     # ----------- SOFT DELETE (custom) -----------

    @swagger_auto_schema(
        method='delete',
        operation_description="Realiza un borrado lógico (soft delete) del color especificado.",
        tags=["Colors"],
        responses={
            204: openapi.Response("Eliminado lógicamente correctamente."),
            404: openapi.Response("No encontrado.")
        }
    )
    @action(detail=True, methods=['delete'], url_path='soft-delete')
    def soft_destroy(self, request, pk=None):
        """
        Realiza un borrado lógico del color especificado.
        """
        return super().soft_destroy(request, pk)

    # ----------- FILTER COLORS (custom) -----------
    @swagger_auto_schema(
        operation_description="Filtra colores por nombre y estado (activo/inactivo)",
        tags=["Colors"],
        manual_parameters=[
            openapi.Parameter('active', openapi.IN_QUERY, description="Estado del color (true/false)", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('search', openapi.IN_QUERY, description="Nombre del color", type=openapi.TYPE_STRING)
        ],
        responses={200: openapi.Response("Lista de colores filtrados")}
    )
    @action(detail=False, methods=['get'], url_path='filter')
    def filter_colors(self, request):
        active = request.query_params.get('active')
        search = request.query_params.get('search')
        service = self.service_class()
        queryset = service.get_filtered_colors(active, search)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)