from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.security.services.FormModuleService import FormModuleService
from apps.security.entity.serializers.FormModule.FormModuleSerializer import FormModuleSerializer
from apps.security.entity.serializers.FormModule.CreateModuleWithFormsSerializer import CreateModuleWithFormsSerializer


class FormModuleViewSet(BaseViewSet):
    service_class = FormModuleService
    serializer_class = FormModuleSerializer
    
    @swagger_auto_schema(
        method='get',
        operation_description="Obtiene un módulo y sus formularios asociados por ID.",
        tags=["FormModule"],
        responses={200: CreateModuleWithFormsSerializer}
    )
    @action(detail=True, methods=['get'], url_path='get-module-with-forms')
    def get_module_with_forms(self, request, pk=None):
        from apps.security.entity.models import Module, FormModule
        try:
            module = Module.objects.get(pk=pk)
        except Module.DoesNotExist:
            return Response({'detail': 'Módulo no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        # Obtener todos los formularios asociados a ese módulo
        form_ids = list(FormModule.objects.filter(module=module).values_list('form_id', flat=True))
        data = {
            'name': module.name,
            'description': module.description,
            'form_ids': form_ids
        }
        serializer = CreateModuleWithFormsSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method='put',
        request_body=CreateModuleWithFormsSerializer,
        operation_description="Actualiza un módulo y sus formularios asociados.",
        tags=["FormModule"],
        responses={200: openapi.Response("Módulo y formularios actualizados correctamente.")}
    )
    @action(detail=True, methods=['put'], url_path='update-module-with-forms')
    def update_module_with_forms(self, request, pk=None):
        serializer = CreateModuleWithFormsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.service_class().update_module_with_forms(pk, serializer.validated_data)
        return Response(result, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method='post',
        request_body=CreateModuleWithFormsSerializer,
        operation_description="Crea un nuevo módulo y le asigna uno o varios formularios.",
        tags=["FormModule"],
        responses={201: openapi.Response("Módulo y formularios creados correctamente.")}
    )
    @action(detail=False, methods=['post'], url_path='create-module-with-forms')
    def create_module_with_forms(self, request):
        serializer = CreateModuleWithFormsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.service_class().create_module_with_forms(serializer.validated_data)
        return Response(result, status=status.HTTP_201_CREATED)
   

    # ----------- LIST -----------
    @swagger_auto_schema(
        operation_description=(
            "Obtiene una lista de todos los módulos de formulario registrados."
        ),
        tags=["FormModule"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Crea un nuevo módulo de formulario con la información proporcionada."
        ),
        tags=["FormModule"]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description=(
            "Obtiene la información de un módulo de formulario específico."
        ),
        tags=["FormModule"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza la información completa de un módulo de formulario."
        ),
        tags=["FormModule"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza solo algunos campos de un módulo de formulario."
        ),
        tags=["FormModule"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description=(
            "Elimina físicamente un módulo de formulario de la base de datos."
        ),
        tags=["FormModule"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # ----------- SOFT DELETE (custom) -----------
    @swagger_auto_schema(
        method='delete',
        operation_description=(
            "Realiza un borrado lógico (soft delete) del módulo de formulario especificado."
        ),
        tags=["FormModule"],
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
