from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.assign.services.BossService import BossService
from apps.assign.entity.serializers.BossSerializer import BossSerializer


class BossViewset(BaseViewSet):
    service_class = BossService
    serializer_class = BossSerializer

    @swagger_auto_schema(
        operation_description="Obtiene una lista de todos los jefes registrados.",
        tags=["Boss"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Crea un nuevo jefe con la información proporcionada.",
        tags=["Boss"]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Obtiene la información de un jefe específico.",
        tags=["Boss"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Actualiza la información completa de un jefe.",
        tags=["Boss"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Actualiza solo algunos campos de un jefe.",
        tags=["Boss"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Elimina físicamente un jefe de la base de datos.",
        tags=["Boss"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        method='delete',
        operation_description="Realiza un borrado lógico (soft delete) del jefe especificado.",
        tags=["Boss"],
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

    @swagger_auto_schema(
        method='get',
        operation_description="Obtiene los jefes filtrados por empresa (enterprise_id).",
        manual_parameters=[
            openapi.Parameter(
                'enterprise_id', openapi.IN_QUERY, description="ID de la empresa", type=openapi.TYPE_INTEGER, required=True
            )
        ],
        responses={200: BossSerializer(many=True)},
        tags=["Boss"]
    )
    @action(detail=False, methods=['get'], url_path='by-enterprise')
    def by_enterprise(self, request):
        enterprise_id = request.query_params.get('enterprise_id')
        if not enterprise_id:
            return Response({'detail': 'enterprise_id es requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        bosses = self.service_class().get_by_enterprise(enterprise_id)
        serializer = self.serializer_class(bosses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
