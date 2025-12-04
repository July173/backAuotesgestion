from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.general.entity.serializers.CreateAprendiz.ApprenticeSerializer import ApprenticeSerializer
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.assign.services.AsignationInstructorService import AsignationInstructorService
from apps.assign.entity.serializers.AsignationInstructor.AsignationInstructorSerializer import AsignationInstructorSerializer
from apps.assign.entity.serializers.AsignationInstructor.AsignationInstructorAllDatesSerializer import AsignationInstructorSerializer as AsignationInstructorAllDatesSerializer
from apps.assign.entity.serializers.AsignationInstructor.AsignationInstructorWithNamesSerializer import AsignationInstructorWithNamesSerializer, PersonBasicSerializer
from apps.general.entity.models import Instructor
from apps.general.entity.serializers.CreateInstructor.InstructorSerializer import InstructorSerializer
from apps.assign.entity.serializers.AsignationInstructor.AsignationInstructorFullDataSerializer import AsignationInstructorFullDataSerializer



class AsignationInstructorViewset(BaseViewSet):

    service_class = AsignationInstructorService
    serializer_class = AsignationInstructorSerializer

    #-- Get --
    @swagger_auto_schema(
        operation_description="Obtiene una lista de todas las asignaciones de instructor.",
        tags=["AsignationInstructor"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    #-- Post --
    @swagger_auto_schema(
        operation_description="Crea una nueva asignación de instructor.",
        tags=["AsignationInstructor"]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    #-- Get by ID --
    @swagger_auto_schema(
        operation_description="Obtiene la información de una asignación específica.",
        tags=["AsignationInstructor"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    #-- Put --
    @swagger_auto_schema(
        operation_description="Actualiza la información completa de una asignación.",
        tags=["AsignationInstructor"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    #-- Patch --
    @swagger_auto_schema(
        operation_description="Actualiza solo algunos campos de una asignación.",
        tags=["AsignationInstructor"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    #-- Delete --
    @swagger_auto_schema(
        operation_description="Elimina físicamente una asignación de la base de datos.",
        tags=["AsignationInstructor"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    #-- Soft Delete --
    @swagger_auto_schema(
        method='delete',
        operation_description="Realiza un borrado lógico (soft delete) de la asignación especificada.",
        tags=["AsignationInstructor"],
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

    #-- Custom Create --
    @swagger_auto_schema(
        method='post',
        operation_description="Crea una asignación de instructor personalizada (fecha automática) y permite enviar mensaje y estado manualmente",
        request_body=AsignationInstructorAllDatesSerializer,
        responses={
            201: openapi.Response("Asignación creada correctamente", AsignationInstructorSerializer),
            400: openapi.Response("Error: {'status': 'error', 'type': 'not_found', 'message': 'El instructor no existe.'}")
        },
        tags=["AsignationInstructor"]
    )
    @action(detail=False, methods=['post'], url_path='custom-create')
    def custom_create(self, request):
        instructor_id = request.data.get('instructor')
        request_asignation_id = request.data.get('request_asignation')
        content = request.data.get('content')
        type_message = request.data.get('type_message')
        whose_message = request.data.get('whose_message')
        request_state = request.data.get('request_state')
        if not instructor_id or not request_asignation_id:
            return Response({"status": "error", "type": "missing_data", "message": "Faltan datos obligatorios."}, status=status.HTTP_400_BAD_REQUEST)
        service = self.service_class()
        result = service.create_custom(instructor_id, request_asignation_id, content=content, type_message=type_message, whose_message=whose_message, request_state=request_state)
        if isinstance(result, dict) and result.get('status') == 'error':
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        instructor = Instructor.objects.get(pk=instructor_id)
        instructor_data = InstructorSerializer(instructor).data
        serializer = self.serializer_class(result)
        return Response({
            'asignation': serializer.data,
            'instructor': instructor_data
        }, status=status.HTTP_201_CREATED)

    #-- Get with Apprentice and Instructor Data --
    @swagger_auto_schema(
        method='get',
        operation_description="Obtiene el id, datos de aprendiz y de instructor para una asignación específica.",
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY, description="ID de la asignación", type=openapi.TYPE_INTEGER, required=True)
        ],
        responses={200: openapi.Response("OK")},
        tags=["AsignationInstructor"]
    )
    @action(detail=False, methods=['get'], url_path='with-apprentice-instructor')
    def with_apprentice_instructor(self, request):
        asignation_id = request.query_params.get('id')
        if not asignation_id:
            return Response({'detail': 'El parámetro id es requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            asignation = self.service_class().get_with_apprentice_instructor().get(id=asignation_id)
        except self.service_class().repository.model.DoesNotExist:
            return Response({'detail': 'No se encontró la asignación.'}, status=status.HTTP_404_NOT_FOUND)
        apprentice = asignation.request_asignation.apprentice
        instructor = asignation.instructor
        data = {
            'asignation_id': asignation.id,
            'apprentice': {
                'id': apprentice.id,
                'first_name': apprentice.person.first_name,
                'second_name': apprentice.person.second_name,
                'first_last_name': apprentice.person.first_last_name,
                'second_last_name': apprentice.person.second_last_name,
                'number_identification': apprentice.person.number_identification,
                'phone_number': apprentice.person.phone_number,
                'type_identification': getattr(apprentice.person.type_identification, 'name', None),
                'active': apprentice.active
            },
            'instructor': {
                'id': instructor.id,
                'first_name': instructor.person.first_name,
                'second_name': instructor.person.second_name,
                'first_last_name': instructor.person.first_last_name,
                'second_last_name': instructor.person.second_last_name,
                'number_identification': instructor.person.number_identification,
                'phone_number': instructor.person.phone_number,
                'type_identification': getattr(instructor.person.type_identification, 'name', None),
                'active': instructor.active
            }
        }
        serializer = AsignationInstructorWithNamesSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

#-- Get full data for asignation (apprentice, instructor, asignation) --
    @swagger_auto_schema(
        method='get',
        operation_description="Obtiene los datos del aprendiz, instructor y la asignación para una asignación específica.",
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY, description="ID de la asignación", type=openapi.TYPE_INTEGER, required=True)
        ],
        responses={200: openapi.Response("OK")},
        tags=["AsignationInstructor"]
    )
    @action(detail=False, methods=['get'], url_path='full-data')
    def full_data(self, request):
        asignation_id = request.query_params.get('id')
        if not asignation_id:
            return Response({'detail': 'El parámetro id es requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        service = self.service_class()
        data = service.get_full_data(asignation_id)
        if not data:
            return Response({'success': False, 'message': 'No se encontró la asignación activa.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AsignationInstructorFullDataSerializer(data)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)