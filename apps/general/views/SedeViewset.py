from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.general.services.SedeService import SedeService
from apps.general.entity.serializers.SedeSerializer import SedeSerializer



class SedeViewset(BaseViewSet):
    
    service_class = SedeService
    serializer_class = SedeSerializer

    # ----------- LIST -----------
    @swagger_auto_schema(
        operation_description=(
            "Obtiene una lista de todas las sedes registradas."
        ),
        tags=["Sede"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Crea una nueva sede con la información proporcionada."
        ),
        tags=["Sede"]
    )
    def create(self, request, *args, **kwargs):
        service = self.service_class()
        instance, error = service.create_sede(request.data)
        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"detail": error}, status=status.HTTP_400_BAD_REQUEST)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description=(
            "Obtiene la información de una sede específica."
        ),
        tags=["Sede"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza la información completa de una sede."
        ),
        tags=["Sede"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza solo algunos campos de una sede."
        ),
        tags=["Sede"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description=(
            "Elimina físicamente una sede de la base de datos."
        ),
        tags=["Sede"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # ----------- SOFT DELETE (custom) -----------
    @swagger_auto_schema(
        method='delete',
        operation_description=(
            "Realiza un borrado lógico (soft delete) de la sede especificada."
        ),
        tags=["Sede"],
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
        operation_description="Filtra sedes por nombre y estado (activo/inactivo)",
        tags=["Sede"],
        manual_parameters=[
            openapi.Parameter('active', openapi.IN_QUERY, description="Estado de la sede (true/false)", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('search', openapi.IN_QUERY, description="Nombre de la sede", type=openapi.TYPE_STRING)
        ],
        responses={200: openapi.Response("Lista de sedes filtradas")}
    )
    @action(detail=False, methods=['get'], url_path='filter')
    def filter_sedes(self, request):
        active = request.query_params.get('active')
        search = request.query_params.get('search')
        service = self.service_class()
        queryset = service.get_filtered_sedes(active, search)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
