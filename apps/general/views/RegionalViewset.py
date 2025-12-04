from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.general.services.RegionalService import RegionalService
from apps.general.entity.serializers.Regional.RegionalSerializer import RegionalSerializer
from apps.general.entity.serializers.Regional.RegionalNestedSerializer import RegionalNestedSerializer



class RegionalViewset(BaseViewSet):

    service_class = RegionalService
    serializer_class = RegionalSerializer

    # ----------- LIST -----------
    @swagger_auto_schema(
        operation_description=(
            "Obtiene una lista de todas las regionales registradas."
        ),
        tags=["Regional"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Crea una nueva regional con la información proporcionada."
        ),
        tags=["Regional"]
    )
    def create(self, request, *args, **kwargs):
        service = self.service_class()
        instance, error = service.create_regional(request.data)
        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"detail": error}, status=status.HTTP_400_BAD_REQUEST)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description=(
            "Obtiene la información de una regional específica."
        ),
        tags=["Regional"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza la información completa de una regional."
        ),
        tags=["Regional"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza solo algunos campos de una regional."
        ),
        tags=["Regional"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description=(
            "Elimina físicamente una regional de la base de datos."
        ),
        tags=["Regional"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # ----------- SOFT DELETE (custom) -----------
    @swagger_auto_schema(
        method='delete',
        operation_description=(
            "Realiza un borrado lógico (soft delete) de la regional especificada."
        ),
        tags=["Regional"],
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
        
        
    # ----------- WITH CENTERS BY ID (custom) -----------
    @swagger_auto_schema(
        operation_description="Obtiene una regional por id con sus centros anidados.",
        tags=["Regional"],
        responses={200: RegionalNestedSerializer()}
    )
    @action(detail=True, methods=['get'], url_path='with-centers')
    def with_centers_by_id(self, request, pk=None):
        regional = self.service_class().get_regional_with_centers_by_id(pk)
        if not regional:
            return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
        serializer = RegionalNestedSerializer(regional)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # ----------- WITH CENTERS (custom) -----------
    @swagger_auto_schema(
        operation_description="Obtiene todas las regionales con sus centros anidados.",
        tags=["Regional"],
        responses={200: RegionalNestedSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='with-centers')
    def with_centers(self, request):
        queryset = self.service_class().get_all_regionals_with_centers()
        serializer = RegionalNestedSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # ----------- FILTER REGIONALS (custom) -----------
    @swagger_auto_schema(
        operation_description="Filtra regionales por nombre y estado (activo/inactivo)",
        tags=["Regional"],
        manual_parameters=[
            openapi.Parameter('active', openapi.IN_QUERY, description="Estado de la regional (true/false)", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('search', openapi.IN_QUERY, description="Nombre de la regional", type=openapi.TYPE_STRING)
        ],
        responses={200: openapi.Response("Lista de regionales filtradas")}
    )
    @action(detail=False, methods=['get'], url_path='filter')
    def filter_regionals(self, request):
        active = request.query_params.get('active')
        search = request.query_params.get('search')
        service = self.service_class()
        queryset = service.get_filtered_regionals(active, search)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
