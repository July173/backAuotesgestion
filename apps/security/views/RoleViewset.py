from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.security.services.RoleService import RoleService
from apps.security.entity.serializers.RoleSerializer import RoleSerializer
from apps.security.entity.models import Role, User  # Asegúrate de importar User y Role


class RoleViewSet(BaseViewSet):
    @swagger_auto_schema(
        operation_description="Filtra roles por estado y búsqueda en nombre de rol.",
        tags=["Role"],
        manual_parameters=[
            openapi.Parameter('active', openapi.IN_QUERY, description="Estado del rol (true/false)", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('search', openapi.IN_QUERY, description="Texto de búsqueda (nombre de rol)", type=openapi.TYPE_STRING)
        ],
        responses={200: openapi.Response("Lista de roles filtrados")}
    )
    @action(detail=False, methods=['get'], url_path='filter')
    def filter_roles(self, request):
        active = request.query_params.get('active')
        search = request.query_params.get('search')
        # Convertir active a boolean si viene como string
        if active is not None:
            active = active.lower() in ['true', '1', 'yes']
        service = self.service_class()
        roles = service.get_filtered_roles(active, search)
        serializer = self.get_serializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    service_class = RoleService
    serializer_class = RoleSerializer
   
    # ----------- LIST -----------
    @swagger_auto_schema(
        operation_description=(
            "Obtiene una lista de todos los roles registrados."
        ),
        tags=["Role"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Crea un nuevo rol con la información proporcionada."
        ),
        tags=["Role"]
    )
    def create(self, request, *args, **kwargs):
        service = self.service_class()
        instance, error = service.create_role(request.data)
        if error:
            return Response({"detail": error}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description=(
            "Obtiene la información de un rol específico."
        ),
        tags=["Role"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza la información completa de un rol."
        ),
        tags=["Role"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza solo algunos campos de un rol."
        ),
        tags=["Role"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description=(
            "Elimina físicamente un rol de la base de datos."
        ),
        tags=["Role"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # ----------- SOFT DELETE (custom) -----------
    @swagger_auto_schema(
        method='delete',
        operation_description=(
            "Realiza un borrado lógico (soft delete) del rol especificado."
        ),
        tags=["Role"],
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
        operation_description="Lista roles con cantidad de usuarios asignados.",
        tags=["Role"],
        responses={200: openapi.Response("Lista de roles con cantidad de usuarios")}
    )
    @action(detail=False, methods=['get'], url_path='roles-with-user-count')
    def roles_with_user_count(self, request):
        roles = Role.objects.all()
        data = []
        for role in roles:
            user_count = User.objects.filter(role=role, is_active=True).count()
            data.append({
                "id": role.id,
                "nombre": role.type_role,
                "descripcion": role.description,
                "active": role.active,
                "cantidad_usuarios": user_count
            })
        return Response(data, status=status.HTTP_200_OK)


    
    @swagger_auto_schema(
        method='delete',
        operation_description="Activa si está desactivado y desactiva si está activo el rol y todos los usuarios vinculados. Solo se requiere el id en la URL.",
        responses={200: openapi.Response('Resultado de la operación')},
        tags=["Role"]
    )
    @action(detail=True, methods=['delete'], url_path='logical-delete-with-users')
    def logical_delete_with_users(self, request, pk=None):
        """
        Activa si está desactivado y desactiva si está activo el rol y todos los usuarios vinculados. Solo se requiere el id en la URL.
        """
        # Obtener el estado actual del rol
        try:
            role = Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            return Response({'detail': 'Rol no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        nuevo_estado = not role.active
        result = self.service_class().set_active_role_and_users(pk, nuevo_estado)
        return Response(result)
    
    