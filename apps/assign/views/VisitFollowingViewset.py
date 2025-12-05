from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.base.view.implements.BaseViewset import BaseViewSet
from apps.assign.services.VisitFollowingService import VisitFollowingService
from apps.assign.entity.serializers.VisitFollowingSerializer import VisitFollowingSerializer
from apps.assign.entity.serializers.VisitFollowingUpdateSerializer import VisitFollowingUpdateSerializer


from apps.assign.entity.models import VisitFollowing

class VisitFollowingViewset(BaseViewSet):
    service_class = VisitFollowingService
    serializer_class = VisitFollowingSerializer
    queryset = VisitFollowing.objects.all()

    @swagger_auto_schema(
        operation_description="Obtiene una lista de todas las visitas de seguimiento.",
        tags=["VisitFollowing"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Crea una nueva visita de seguimiento.",
        tags=["VisitFollowing"]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Obtiene la información de una visita específica.",
        tags=["VisitFollowing"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Actualiza la información completa de una visita.",
        tags=["VisitFollowing"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Actualiza solo algunos campos de una visita.",
        tags=["VisitFollowing"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    
    @swagger_auto_schema(
        operation_description="Elimina físicamente una visita de la base de datos.",
        tags=["VisitFollowing"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        method='delete',
        operation_description="Realiza un borrado lógico (soft delete) de la visita especificada.",
        tags=["VisitFollowing"],
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

    #---------------------- Custom Patch ---------------------#
    @swagger_auto_schema(
        method='patch',
        operation_description="Actualiza campos de una visita excepto `pdf_report`, `scheduled_date`, `visit_number` y `name_visit`.",
        tags=["VisitFollowing"],
        request_body=VisitFollowingUpdateSerializer,
        responses={200: openapi.Response("OK", VisitFollowingUpdateSerializer)},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID de la visita", type=openapi.TYPE_INTEGER, required=True)
        ]
    )
    @action(detail=True, methods=['patch'], url_path='patch-excluding')
    def patch_excluding(self, request, pk=None):
        # Campos que NO se deben modificar mediante este endpoint
        excluded = ['pdf_report', 'scheduled_date', 'visit_number', 'name_visit']
        service = self.service_class()
        try:
            visit = service.partial_update_excluding(pk, request.data or {}, exclude_fields=excluded)
        except Exception as e:
            return Response({'success': False, 'message': f'Error al actualizar la visita: {e}'}, status=status.HTTP_400_BAD_REQUEST)
        if visit is None:
            return Response({'success': False, 'message': 'Visita no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(visit)
        return Response({'success': True, 'visit': serializer.data}, status=status.HTTP_200_OK)
