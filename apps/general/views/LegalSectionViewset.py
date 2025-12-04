from rest_framework import status
from core.base.view.implements.BaseViewset import BaseViewSet
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from apps.general.entity.serializers.LegalSectionSerializer import LegalSectionSerializer
from apps.general.services.LegalSectionService import LegalSectionService
from rest_framework.decorators import action
from drf_yasg import openapi


class LegalSectionViewset(BaseViewSet):
    
    service_class = LegalSectionService
    serializer_class = LegalSectionSerializer

    # ----------- LIST -----------
    @swagger_auto_schema(
        operation_description="Obtiene una lista de todas las secciones legales registradas.",
        tags=["LegalSection"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        operation_description="Crea una nueva sección legal.",
        tags=["LegalSection"]
    )
    def create(self, request, *args, **kwargs):
        service = self.service_class()
        instance, error = service.create_legal_section(request.data)
        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"detail": error}, status=status.HTTP_400_BAD_REQUEST)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description="Obtiene la información de una sección legal específica.",
        tags=["LegalSection"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description="Actualiza la información completa de una sección legal.",
        tags=["LegalSection"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description="Actualiza solo algunos campos de una sección legal.",
        tags=["LegalSection"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description="Elimina físicamente una sección legal de la base de datos.",
        tags=["LegalSection"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # ----------- SOFT DELETE -----------
    @swagger_auto_schema(
        operation_description="Realiza un borrado lógico de la sección legal especificada.",
        tags=["LegalSection"]
    )
    @action(detail=True, methods=['delete'], url_path='soft-delete')
    def soft_destroy(self, request, pk=None):
        """
        Realiza un borrado lógico de la sección legal especificada.
        """
        return super().soft_destroy(request, pk)
    
    # ----------- FILTER LEGAL SECTIONS (custom) -----------
    @swagger_auto_schema(
        operation_description="Filtra secciones legales por nombre y estado (activo/inactivo)",
        tags=["LegalSection"],
        manual_parameters=[
            openapi.Parameter('active', openapi.IN_QUERY, description="Estado de la sección legal (true/false)", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('search', openapi.IN_QUERY, description="Nombre de la sección legal", type=openapi.TYPE_STRING)
        ],
        responses={200: openapi.Response("Lista de secciones legales filtradas")}
    )
    @action(detail=False, methods=['get'], url_path='filter')
    def filter_legal_sections(self, request):
        active = request.query_params.get('active')
        search = request.query_params.get('search')
        service = self.service_class()
        queryset = service.get_filtered_legal_sections(active, search)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

