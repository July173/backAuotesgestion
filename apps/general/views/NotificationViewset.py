from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.general.entity.serializers.NotificationSerializer import NotificationSerializer
from apps.general.services.NotificationService import NotificationService


class NotificationViewset(viewsets.ViewSet):


    #---- Get Methods ----#
    #---- Retrieve Notification by ID ----#
    @swagger_auto_schema(
        responses={200: NotificationSerializer()},
        tags=['Notificaciones']
    )
    def retrieve(self, request, pk=None):
        service = NotificationService()
        notification = service.get_notification_by_id(pk)
        if not notification:
            return Response({'detail': 'Notificación no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)

    #---- List Notifications ----#
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('apprentice_id', openapi.IN_QUERY, description="ID del aprendiz", type=openapi.TYPE_INTEGER, required=False),
            openapi.Parameter('instructor_id', openapi.IN_QUERY, description="ID del instructor", type=openapi.TYPE_INTEGER, required=False),
            openapi.Parameter('coordinator_id', openapi.IN_QUERY, description="ID del coordinador", type=openapi.TYPE_INTEGER, required=False),
            openapi.Parameter('sofia_operator_id', openapi.IN_QUERY, description="ID del operador de Sofia Plus", type=openapi.TYPE_INTEGER, required=False),
            openapi.Parameter('admin_id', openapi.IN_QUERY, description="ID del administrador", type=openapi.TYPE_INTEGER, required=False),
        ],
        responses={200: NotificationSerializer(many=True)},
        tags=['Notificaciones']
    )
    def list(self, request):
        apprentice_id = request.query_params.get('apprentice_id')
        instructor_id = request.query_params.get('instructor_id')
        coordinator_id = request.query_params.get('coordinator_id')
        sofia_operator_id = request.query_params.get('sofia_operator_id')
        admin_id = request.query_params.get('admin_id')
        service = NotificationService()
        try:
            if apprentice_id:
                qs = service.get_notifications(apprentice_id=apprentice_id)
            elif instructor_id:
                qs = service.get_notifications(instructor_id=instructor_id)
            elif coordinator_id:
                qs = service.get_notifications(coordinator_id=coordinator_id)
            elif sofia_operator_id:
                qs = service.get_notifications(sofia_operator_id=sofia_operator_id)
            elif admin_id:
                qs = service.get_notifications(admin_id=admin_id)
            else:
                qs = service.list_all()
            if qs is None:
                return Response({'detail': 'No hay notificaciones para este usuario.'}, status=status.HTTP_204_NO_CONTENT)
            serializer = NotificationSerializer(qs, many=True)
            return Response(serializer.data)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)

    
    #---- Delete Notification by ID ----#
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY, description="ID de la notificación", type=openapi.TYPE_INTEGER, required=True),
        ],
        responses={200: NotificationSerializer()},
        tags=['Notificaciones']
    )
    @action(detail=False, methods=['delete'], url_path='delete-by-id')
    def delete_notification(self, request):
        notification_id = request.query_params.get('id')
        service = NotificationService()
        notification = service.repository.delete_by_id(notification_id)
        if not notification:
            return Response({'detail': 'Notificación no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'detail': 'Notificación eliminada correctamente.'}, status=status.HTTP_200_OK)

    #---- Delete Notifications by User/Role ----#
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('apprentice_id', openapi.IN_QUERY, description="ID del aprendiz", type=openapi.TYPE_INTEGER, required=False),
            openapi.Parameter('instructor_id', openapi.IN_QUERY, description="ID del instructor", type=openapi.TYPE_INTEGER, required=False),
            openapi.Parameter('coordinator_id', openapi.IN_QUERY, description="ID del coordinador", type=openapi.TYPE_INTEGER, required=False),
            openapi.Parameter('sofia_operator_id', openapi.IN_QUERY, description="ID del operador de Sofia Plus", type=openapi.TYPE_INTEGER, required=False),
            openapi.Parameter('admin_id', openapi.IN_QUERY, description="ID del administrador", type=openapi.TYPE_INTEGER, required=False),
        ],
        responses={200: NotificationSerializer(many=True)},
        tags=['Notificaciones']
    )
    @action(detail=False, methods=['delete'], url_path='delete-by-user')
    def delete_notifications(self, request):
        apprentice_id = request.query_params.get('apprentice_id')
        instructor_id = request.query_params.get('instructor_id')
        coordinator_id = request.query_params.get('coordinator_id')
        sofia_operator_id = request.query_params.get('sofia_operator_id')
        admin_id = request.query_params.get('admin_id')
        service = NotificationService()
        try:
            qs = service.delete_notifications(
                apprentice_id=apprentice_id,
                instructor_id=instructor_id,
                coordinator_id=coordinator_id,
                sofia_operator_id=sofia_operator_id,
                admin_id=admin_id
            )
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)

        # Si el repositorio retorna un entero (cantidad de eliminados), devolver respuesta vacía o mensaje
        if isinstance(qs, int):
            if qs == 0:
                return Response({'detail': 'No hay notificaciones para este usuario.'}, status=status.HTTP_204_NO_CONTENT)
            return Response({'detail': f'Se eliminaron {qs} notificaciones.'}, status=status.HTTP_200_OK)
        # Si es un queryset
        if hasattr(qs, 'exists'):
            if qs is None or not qs.exists():
                return Response({'detail': 'No hay notificaciones para este usuario.'}, status=status.HTTP_204_NO_CONTENT)
            serializer = NotificationSerializer(qs, many=True)
            return Response(serializer.data)
        # Si no es ninguno de los anteriores
        return Response({'detail': 'No hay notificaciones para este usuario.'}, status=status.HTTP_204_NO_CONTENT)

