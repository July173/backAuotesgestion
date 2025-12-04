from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.security.services.RoleFormPermissionService import RoleFormPermissionService
from apps.security.entity.serializers.RolFormPermission.RoleFormPermissionSerializer import RoleFormPermissionSerializer
from apps.security.entity.serializers.RolFormPermission.CreateRoleWithPermissionsSerializer import CreateRoleWithPermissionsSerializer
from apps.security.entity.models import Role, RoleFormPermission


class RoleFormPermissionViewSet(BaseViewSet):
    service_class = RoleFormPermissionService
    serializer_class = RoleFormPermissionSerializer

    @swagger_auto_schema(
        operation_description="Obtiene la matriz de permisos por rol, formulario y tipo de permiso.",
        tags=["RoleFormPermission"],
        responses={200: openapi.Response("Matriz de permisos por rol")}
    )
    @action(detail=False, methods=['get'], url_path='permission-matrix')
    def permission_matrix(self, request):
        matrix = self.service.get_permission_matrix()
        return Response(matrix, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method='get',
        operation_description="Obtiene un rol con sus formularios y permisos asignados por ID.",
        tags=["RoleFormPermission"],
        responses={200: CreateRoleWithPermissionsSerializer}
    )
    @action(detail=True, methods=['get'], url_path='get-role-with-permissions')
    def get_role_with_permissions(self, request, pk=None):
        try:
            role = Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            return Response({'detail': 'Role not found.'}, status=status.HTTP_404_NOT_FOUND)
        # Obtener todos los RoleFormPermission de ese rol
        rfp_qs = RoleFormPermission.objects.filter(role=role)
        # Agrupar por formulario
        form_map = {}
        for rfp in rfp_qs:
            form_id = rfp.form.id
            if form_id not in form_map:
                form_map[form_id] = {'form_id': form_id, 'permission_ids': []}
            form_map[form_id]['permission_ids'].append(rfp.permission.id)
        data = {
            'type_role': role.type_role,
            'description': role.description,
            'active': role.active,
            'forms': list(form_map.values())
        }
        serializer = CreateRoleWithPermissionsSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method='put',
        request_body=CreateRoleWithPermissionsSerializer,
        operation_description="Actualiza un rol y sus permisos por formulario.",
        tags=["RoleFormPermission"],
        responses={200: openapi.Response("Rol y permisos actualizados correctamente.")}
    )
    @action(detail=True, methods=['put'], url_path='update-role-with-permissions')
    def update_role_with_permissions(self, request, pk=None):
        serializer = CreateRoleWithPermissionsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.service.update_role_with_permissions(pk, serializer.validated_data)
        return Response(result, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method='post',
        request_body=CreateRoleWithPermissionsSerializer,
        operation_description="Crea un nuevo rol y asigna uno o varios permisos a uno o varios formularios.",
        tags=["RoleFormPermission"],
        responses={201: openapi.Response("Rol y permisos creados correctamente.")}
    )
    @action(detail=False, methods=['post'], url_path='create-role-with-permissions')
    def create_role_with_permissions(self, request):
        serializer = CreateRoleWithPermissionsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result, error = self.service.create_role_with_permissions(serializer.validated_data)
        if error:
            return Response({"detail": error}, status=status.HTTP_400_BAD_REQUEST)
        return Response(result, status=status.HTTP_201_CREATED)
    
    

    # ----------- LIST -----------
    @swagger_auto_schema(
        operation_description=(
            "Obtiene una lista de todos los permisos de formulario por rol registrados."
        ),
        tags=["RoleFormPermission"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        request_body=RoleFormPermissionSerializer,
        operation_description="Crea un nuevo permiso de formulario para un rol.",
        tags=["RoleFormPermission"]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description=(
            "Obtiene la información de un permiso de formulario por rol específico."
        ),
        tags=["RoleFormPermission"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza la información completa de un permiso de formulario por rol."
        ),
        tags=["RoleFormPermission"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza solo algunos campos de un permiso de formulario por rol."
        ),
        tags=["RoleFormPermission"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description=(
            "Elimina físicamente un permiso de formulario por rol de la base de datos."
        ),
        tags=["RoleFormPermission"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # ----------- SOFT DELETE (custom) -----------
    @swagger_auto_schema(
        method='delete',
        operation_description=(
                "Realiza un borrado lógico (soft delete) del permiso de formulario por rol especificado."
            ),
            tags=["RoleFormPermission"],
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
        operation_description="Obtiene el menú para el usuario especificado.",
        tags=["RoleFormPermission"],
        responses={
            200: openapi.Response("Menú obtenido correctamente."),
            404: openapi.Response("No se encontró menú para este usuario.")
        }
    )
    @action(detail=True, methods=['get'], url_path='get-menu')
    def get_menu(self, request, pk=None):
        menu = self.service.get_menu(pk)

        if not menu:
            return Response(
                {"detail": "No menu found for this user."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(menu, status=status.HTTP_200_OK)
