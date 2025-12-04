from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.base.view.implements.BaseViewset import BaseViewSet
from apps.security.services.ModuleService import ModuleService
from apps.security.entity.serializers.ModuleSerializer import ModuleSerializer


class ModuleViewSet(BaseViewSet):
    @swagger_auto_schema(
        operation_description="Filtra módulos por estado y búsqueda en nombre.",
        tags=["Module"],
        manual_parameters=[
            openapi.Parameter('active', openapi.IN_QUERY, description="Estado del módulo (true/false)", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('search', openapi.IN_QUERY, description="Texto de búsqueda (nombre de módulo)", type=openapi.TYPE_STRING)
        ],
        responses={200: openapi.Response("Lista de módulos filtrados")}
    )
    @action(detail=False, methods=['get'], url_path='filter')
    def filter_modules(self, request):
        active = request.query_params.get('active')
        search = request.query_params.get('search')
        if active is not None:
            active = active.lower() in ['true', '1', 'yes']
        service = self.service_class()
        modules = service.get_filtered_modules(active, search)
        serializer = self.get_serializer(modules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    service_class = ModuleService
    serializer_class = ModuleSerializer

    # ----------- LIST -----------
    @swagger_auto_schema(
        operation_description=(
            "Obtiene una lista de todos los módulos registrados."
        ),
        tags=["Module"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Crea un nuevo módulo con la información proporcionada."
        ),
        tags=["Module"]
    )
    def create(self, request, *args, **kwargs):
        service = self.service_class()
        instance, error = service.create_module(request.data)
        if error:
            return Response({"detail": error}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description=(
            "Obtiene la información de un módulo específico."
        ),
        tags=["Module"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza la información completa de un módulo."
        ),
        tags=["Module"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza solo algunos campos de un módulo."
        ),
        tags=["Module"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description=(
            "Elimina físicamente un módulo de la base de datos."
        ),
        tags=["Module"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # ----------- SOFT DELETE (custom) -----------
    @swagger_auto_schema(
        method='delete',
        operation_description=(
            "Realiza un borrado lógico (soft delete) del módulo especificado."
        ),
        tags=["Module"],
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
