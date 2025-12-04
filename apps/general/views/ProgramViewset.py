from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.general.services.ProgramService import ProgramService
from apps.general.entity.serializers.ProgramSerializer import ProgramSerializer
from apps.general.entity.serializers.FichaSerializer import FichaSerializer


class ProgramViewset(BaseViewSet):
    
    service_class = ProgramService
    serializer_class = ProgramSerializer

    # ----------- LIST -----------
    @swagger_auto_schema(
        operation_description=(
            "Obtiene una lista de todos los programas registrados."
        ),
        tags=["Program"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Crea un nuevo programa con la información proporcionada."
        ),
        tags=["Program"]
    )
    def create(self, request, *args, **kwargs):
        service = self.service_class()
        instance, error = service.create_program(request.data)
        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"detail": error}, status=status.HTTP_400_BAD_REQUEST)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description=(
            "Obtiene la información de un programa específico."
        ),
        tags=["Program"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza la información completa de un programa."
        ),
        tags=["Program"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza solo algunos campos de un programa."
        ),
        tags=["Program"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description=(
            "Elimina físicamente un programa de la base de datos."
        ),
        tags=["Program"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    # ----------- SOFT DELETE (custom) -----------
    @swagger_auto_schema(
        method='delete',
        operation_description=(
            "Realiza un borrado lógico (soft delete) del programa especificado."
        ),
        tags=["Program"],
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

    # ----------- GET FICHAS BY PROGRAM (custom) -----------
    @swagger_auto_schema(
        operation_description="Obtiene todas las fichas vinculadas a un programa específico.",
        responses={200: FichaSerializer(many=True)},
        tags=["Program"]
    )
    @action(detail=True, methods=['get'], url_path='fichas')
    def get_fichas_by_program(self, request, pk=None):
        fichas = self.service_class().get_fichas_by_program(pk)
        serializer = FichaSerializer(fichas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ----------- DISABLE PROGRAM WITH FICHAS (custom) -----------
    @swagger_auto_schema(
        method='delete',
        operation_description="Deshabilita o reactiva un programa y todas sus fichas vinculadas.",
        tags=["Program"],
        responses={
            200: "Acción realizada correctamente",
            400: "Error de validación", 
            404: "Programa no encontrado"
        }
    )
    @action(detail=True, methods=['delete'], url_path='disable-with-fichas')
    def disable_program_with_fichas(self, request, pk=None):
        try:
            mensaje = self.service_class().logical_delete_program(pk)
            return Response(
                {"detail": mensaje},
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    # ----------- FILTER PROGRAMS (custom) -----------
    @swagger_auto_schema(
        operation_description="Filtra programas por nombre y estado (activo/inactivo)",
        tags=["Program"],
        manual_parameters=[
            openapi.Parameter('active', openapi.IN_QUERY, description="Estado del programa (true/false)", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('search', openapi.IN_QUERY, description="Nombre del programa", type=openapi.TYPE_STRING)
        ],
        responses={200: openapi.Response("Lista de programas filtrados")}
    )
    @action(detail=False, methods=['get'], url_path='filter')
    def filter_programs(self, request):
        active = request.query_params.get('active')
        search = request.query_params.get('search')
        service = self.service_class()
        queryset = service.get_filtered_programs(active, search)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
