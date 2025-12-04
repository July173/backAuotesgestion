from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.general.services.CenterService import CenterService
from apps.general.entity.serializers.CenterSerializer import CenterSerializer
from apps.general.entity.serializers.CenterSerializer import CenterSerializer



class CenterViewset(BaseViewSet):

    service_class = CenterService
    serializer_class = CenterSerializer

    # ----------- LIST -----------
    @swagger_auto_schema(
        operation_description="Obtiene una lista de todos los centros registrados.",
        tags=["Center"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        operation_description="Crea un nuevo centro con la información proporcionada.",
        tags=["Center"]
    )
    def create(self, request, *args, **kwargs):
        service = self.service_class()
        instance, error = service.create_center(request.data)
        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"detail": error}, status=status.HTTP_400_BAD_REQUEST)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description="Obtiene la información de un centro específico.",
        tags=["Center"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description="Actualiza la información completa de un centro.",
        tags=["Center"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description="Actualiza solo algunos campos de un centro.",
        tags=["Center"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description="Elimina físicamente un centro de la base de datos.",
        tags=["Center"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # ----------- SOFT DELETE (custom) -----------
    @swagger_auto_schema(
        method='delete',
        operation_description="Realiza un borrado lógico (soft delete) del centro especificado.",
        tags=["Center"],
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
        
        

    # ----------- GET CENTER WITH SEDES BY ID-----------
    @swagger_auto_schema(
        operation_description="Obtiene un centro por id con sus sedes anidadas.",
        tags=["Center"],
    responses={200: CenterSerializer()}
    )
    @action(detail=True, methods=['get'], url_path='with-sedes')
    def with_sedes_by_id(self, request, pk=None):
        center = self.service_class().get_center_with_sedes_by_id(pk)
        if not center:
            return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
        serializer = CenterSerializer(center)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    # ----------- GET CENTER WITH SEDES -----------
    @swagger_auto_schema(
        operation_description="Obtiene todos los centros con sus sedes anidadas.",
        tags=["Center"],
    responses={200: CenterSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='with-sedes')
    def with_sedes(self, request):
        queryset = self.service_class().get_all_centers_with_sedes()
        serializer = CenterSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #----------- FILTER CENTERS -----------
    @swagger_auto_schema(
        operation_description="Filtra centros por nombre y estado (activo/inactivo)",
        tags=["Center"],
        manual_parameters=[
            openapi.Parameter('active', openapi.IN_QUERY, description="Estado del centro (true/false)", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('search', openapi.IN_QUERY, description="Nombre del centro", type=openapi.TYPE_STRING)
        ],
        responses={200: openapi.Response("Lista de centros filtrados")}
    )
    @action(detail=False, methods=['get'], url_path='filter')
    def filter_centers(self, request):
        active = request.query_params.get('active')
        search = request.query_params.get('search')
        service = self.service_class()
        queryset = service.get_filtered_centers(active, search)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
