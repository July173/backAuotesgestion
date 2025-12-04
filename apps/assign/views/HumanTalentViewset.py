from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.assign.services.HumanTalentService import HumanTalentService
from apps.assign.entity.serializers.HumanTalentSerializer import HumanTalentSerializer


class HumanTalentViewset(BaseViewSet):
    service_class = HumanTalentService
    serializer_class = HumanTalentSerializer

    @swagger_auto_schema(
        operation_description="Obtiene una lista de todo el talento humano registrado.",
        tags=["HumanTalent"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Crea un nuevo talento humano con la información proporcionada.",
        tags=["HumanTalent"]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Obtiene la información de un talento humano específico.",
        tags=["HumanTalent"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Actualiza la información completa de un talento humano.",
        tags=["HumanTalent"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Actualiza solo algunos campos de un talento humano.",
        tags=["HumanTalent"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Elimina físicamente un talento humano de la base de datos.",
        tags=["HumanTalent"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        method='delete',
        operation_description="Realiza un borrado lógico (soft delete) del talento humano especificado.",
        tags=["HumanTalent"],
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
        operation_description="Obtiene el talento humano filtrado por empresa (enterprise_id).",
        manual_parameters=[
            openapi.Parameter(
                'enterprise_id', openapi.IN_QUERY, description="ID de la empresa", type=openapi.TYPE_INTEGER, required=True
            )
        ],
        responses={200: HumanTalentSerializer(many=True)},
        tags=["HumanTalent"]
    )
    @action(detail=False, methods=['get'], url_path='by-enterprise')
    def by_enterprise(self, request):
        enterprise_id = request.query_params.get('enterprise_id')
        if not enterprise_id:
            return Response({'detail': 'enterprise_id es requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        human_talents = self.service_class().get_by_enterprise(enterprise_id)
        serializer = self.serializer_class(human_talents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
