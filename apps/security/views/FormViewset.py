from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.base.view.implements.BaseViewset import BaseViewSet
from apps.security.services.FormService import FormService
from apps.security.entity.serializers.FormSerializer import FormSerializer



class FormViewSet(BaseViewSet):
    

    service_class = FormService
    serializer_class = FormSerializer

    # ----------- LIST -----------
    @swagger_auto_schema(
        operation_description=(
            "Obtiene una lista de todos los formularios registrados."
        ),
        tags=["Form"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Crea un nuevo formulario con la información proporcionada."
        ),
        tags=["Form"]
    )
    def create(self, request, *args, **kwargs):
        service = self.service_class()
        instance, error = service.create_form(request.data)
        if error:
            return Response({"detail": error}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description=(
            "Obtiene la información de un formulario específico."
        ),
        tags=["Form"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza la información completa de un formulario."
        ),
        tags=["Form"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza solo algunos campos de un formulario."
        ),
        tags=["Form"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description=(
            "Elimina físicamente un formulario de la base de datos."
        ),
        tags=["Form"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # ----------- SOFT DELETE (custom) -----------
    @swagger_auto_schema(
        method='delete',
        operation_description=(
            "Realiza un borrado lógico (soft delete) del formulario especificado."
        ),
        tags=["Form"],
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

    # ----------- FILTER FORMS (custom) -----------
    @swagger_auto_schema(
        operation_description="Filtra formularios por nombre y estado (activo/inactivo)",
        tags=["Form"],
        manual_parameters=[
            openapi.Parameter('active', openapi.IN_QUERY, description="Estado del formulario (true/false)", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('search', openapi.IN_QUERY, description="Nombre del formulario", type=openapi.TYPE_STRING)
        ],
        responses={200: openapi.Response("Lista de formularios filtrados")}
    )
    @action(detail=False, methods=['get'], url_path='filter')
    def filter_forms(self, request):
        active = request.query_params.get('active')
        search = request.query_params.get('search')
        service = self.service_class()
        queryset = service.get_filtered_forms(active, search)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)