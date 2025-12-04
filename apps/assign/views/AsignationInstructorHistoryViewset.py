from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.viewsets import ViewSet
from apps.assign.services.AsignationInstructorHistoryService import AsignationInstructorHistoryService
from apps.assign.entity.serializers.AsignationInstructor.AsignationInstructorHistorySerializer import AsignationInstructorHistorySerializer
from apps.assign.entity.serializers.AsignationInstructor.ReasignationInstructorSerializer import ReasignationInstructorSerializer


class AsignationInstructorHistoryViewset(ViewSet):
    
    def get_service(self):
        return AsignationInstructorHistoryService()

    def get_serializer(self, *args, **kwargs):
        return AsignationInstructorHistorySerializer(*args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Reasigna un instructor y guarda el historial automáticamente.",
        request_body=ReasignationInstructorSerializer,
        tags=["AsignationInstructorHistory"],
        responses={
            200: openapi.Response("Reasignación realizada correctamente."),
            400: openapi.Response("Error: {'status': 'error', 'type': 'not_found', 'message': 'No existe la asignación'}")
        }
    )
    @action(detail=False, methods=['post'], url_path='reasignar-instructor')
    def reasignar_instructor(self, request):
        serializer = ReasignationInstructorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        asignation_instructor = serializer.validated_data['asignation_instructor']
        new_instructor_id = serializer.validated_data['new_instructor_id']
        message = serializer.validated_data['message']
        service = self.get_service()
        result = service.reasignar_instructor(
            asignation_instructor,
            new_instructor_id,
            message
        )
        if isinstance(result, dict) and result.get('status') == 'error':
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Reasignación realizada y guardada en historial."}, status=status.HTTP_200_OK)
    

    @swagger_auto_schema(
        operation_description="Obtiene el historial de reasignaciones para una asignación.",
        manual_parameters=[
            openapi.Parameter('asignation_instructor', openapi.IN_QUERY, description="ID de la asignación", type=openapi.TYPE_INTEGER)
        ],
        tags=["AsignationInstructorHistory"],
        responses={
            200: openapi.Response("Historial obtenido correctamente."),
            400: openapi.Response("Error: {'status': 'error', 'type': 'list_by_asignation', 'message': 'No se pudo obtener el historial: ...'}")
        }
    )
    @action(detail=False, methods=['get'], url_path='list-history')
    def list_history(self, request):
        asignation_instructor = request.query_params.get('asignation_instructor')
        service = self.get_service()
        history = service.list_by_asignation(asignation_instructor)
        if isinstance(history, dict) and history.get('status') == 'error':
            return Response(history, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

