from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.security.services.PersonService import PersonService
from apps.security.entity.serializers.person.PatchPersonSerializer import PatchPersonSerializer
from apps.security.entity.serializers.person.PersonSerializer import PersonSerializer
from apps.security.entity.serializers.person.RegisterAprendizSerializer import RegisterAprendizSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class PersonViewSet(BaseViewSet):

    service_class = PersonService
    serializer_class = PersonSerializer
    
    # ----------- LIST -----------
    @swagger_auto_schema(
        operation_description=(
            "Obtiene una lista de todas las personas registradas."
        ),
        tags=["Person"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Crea una nueva persona con la información proporcionada."
        ),
        tags=["Person"]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description=(
            "Obtiene la información de una persona específica."
        ),
        tags=["Person"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza la información completa de una persona."
        ),
        tags=["Person"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza solo algunos campos de una persona."
        ),
        tags=["Person"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description=(
            "Elimina físicamente una persona de la base de datos."
        ),
        tags=["Person"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # ----------- SOFT DELETE (custom) -----------
    @swagger_auto_schema(
        method='delete',
        operation_description=(
            "Realiza un borrado lógico (soft delete) de la persona especificada."
        ),
        tags=["Person"],
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




    #--- REGISTRO APRENDIZ ---
    @swagger_auto_schema(
        operation_description=(
            "Registra un nuevo aprendiz en el sistema.\n\n"
            "• **Correo**: Debe ser proporcionado por el usuario (formato: usuario@soy.sena.edu.co)\n"
            "• **Contraseña**: Se establecerá cuando un administrador active la cuenta\n\n"
            "El aprendiz queda registrado pero inactivo hasta que un administrador active su cuenta."
        ),
        operation_summary="Registro de Aprendiz con activación pendiente",
        tags=["Person - Registro"],
        request_body=RegisterAprendizSerializer,
        responses={}
    )
    @action(detail=False, methods=['post'], url_path='register-apprentice')
    def register_apprentice(self, request):
        """
        Controller: Solo orquesta la llamada al servicio.
        No contiene validaciones ni lógica de negocio.
        """
        result = self.service.register_apprentice(request.data)
        return self.render_message(result)
    