from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.base.view.implements.BaseViewset import BaseViewSet
from apps.general.services.InstructorService import InstructorService
from apps.general.entity.serializers.CreateInstructor.InstructorSerializer import InstructorSerializer
from apps.general.entity.models import Instructor
from apps.general.entity.serializers.CreateInstructor.CreateInstructorSerializer import CreateInstructorSerializer
from apps.general.entity.serializers.CreateInstructor.GetInstructorSerializer import GetInstructorSerializer
from apps.general.entity.serializers.CreateInstructor.AsignationInstructorWithMessageSerializer import AsignationInstructorWithMessageSerializer


class InstructorViewset(BaseViewSet):

    

    def get_queryset(self):
        return Instructor.objects.all()
    
    # ----------- LIST -----------
    @swagger_auto_schema(
        operation_description="Obtiene una lista de todos los instructores registrados.",
        tags=["Instructor"]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # ----------- CREATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Crea un nuevo instructor con la información proporcionada."
        ),
        tags=["Instructor"]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    # ----------- RETRIEVE -----------
    @swagger_auto_schema(
        operation_description=(
            "Obtiene la información de un instructor específico."
        ),
        tags=["Instructor"]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # ----------- UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza la información completa de un instructor."
        ),
        tags=["Instructor"]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # ----------- PARTIAL UPDATE -----------
    @swagger_auto_schema(
        operation_description=(
            "Actualiza solo algunos campos de un instructor."
        ),
        tags=["Instructor"]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # ----------- DELETE -----------
    @swagger_auto_schema(
        operation_description=(
            "Elimina físicamente un instructor de la base de datos."
        ),
        tags=["Instructor"]
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # ----------- SOFT DELETE (custom) -----------
    @swagger_auto_schema(
        method='delete',
        operation_description=(
            "Realiza un borrado lógico (soft delete) del instructor especificado."
        ),
        tags=["Instructor"],
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

#-----------------------------------------------------------------------------------

    # ----------- CUSTOM CREATE -----------
    @swagger_auto_schema(
        request_body=CreateInstructorSerializer,
        operation_description="Crea un nuevo instructor (nuevo endpoint avanzado).",
        tags=["Instructor"]
    )
    @action(detail=False, methods=['post'], url_path='Create-Instructor/create')
    def custom_create(self, request, *args, **kwargs):
        serializer = CreateInstructorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        result = self.service.create_instructor(
            {k: data[k] for k in ['first_name', 'second_name', 'first_last_name', 'second_last_name', 'phone_number', 'type_identification', 'number_identification']},
            {k: data[k] for k in ['email', 'role_id', 'password'] if k in data},
            {
                'contract_type_id': data.get('contract_type_id'),
                'contract_start_date': data.get('contract_start_date'),
                'contract_end_date': data.get('contract_end_date'),
                'knowledge_area_id': data.get('knowledge_area_id'),
                'is_followup_instructor': data.get('is_followup_instructor')
            },
            data['sede_id']
        )
        return self.render_message(result)


    # ----------- CUSTOM LIST -----------
    @swagger_auto_schema(
        operation_description="Lista todos los instructores (nuevo endpoint avanzado).",
        responses={200: GetInstructorSerializer(many=True)},
        tags=["Instructor"]
    )
    @action(detail=False, methods=['get'], url_path='custom-list')
    def custom_list(self, request, *args, **kwargs):
        instructors = self.service.list_instructors()
        serializer = GetInstructorSerializer(instructors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    # ----------- LIST ----------- (parámetros de filtrado unificados en el endpoint `filter`)
    

    # ----------- CUSTOM UPDATE -----------
    @swagger_auto_schema(
        request_body=CreateInstructorSerializer,
        operation_description="Actualiza un instructor existente (nuevo endpoint avanzado).",
        tags=["Instructor"]
    )
    @action(detail=True, methods=['put'], url_path='Create-Instructor/update')
    def custom_update(self, request, pk=None):
        serializer = CreateInstructorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            result = self.service.update_instructor(
                pk,
                {k: data[k] for k in ['first_name', 'second_name', 'first_last_name', 'second_last_name', 'phone_number', 'type_identification', 'number_identification']},
                {k: data[k] for k in ['email', 'role_id'] if k in data},
                {
                    'contract_type_id': data.get('contract_type_id'),
                    'contract_start_date': data.get('contract_start_date'),
                    'contract_end_date': data.get('contract_end_date'),
                    'knowledge_area_id': data.get('knowledge_area_id'),
                    'is_followup_instructor': data.get('is_followup_instructor')
                },
                data.get('sede_id')
            )
            return self.render_message(result)
        except Instructor.DoesNotExist:
            return Response({"detail": "Instructor no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

   
    # ----------- CUSTOM UPDATE PARTIAL-----------
    @swagger_auto_schema(
        method='patch',
        operation_description="Actualiza solo los campos assigned_learners y max_assigned_learners de un instructor.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'assigned_learners': openapi.Schema(type=openapi.TYPE_INTEGER, description='Aprendices actualmente asignados', nullable=True),
                'max_assigned_learners': openapi.Schema(type=openapi.TYPE_INTEGER, description='Límite máximo permitido', nullable=True)
            },
            required=[]
        ),
        responses={200: InstructorSerializer},
        tags=["Instructor"]
    )
    @action(detail=True, methods=['patch'], url_path='update-learners')
    def update_learners(self, request, pk=None):
        service = InstructorService()
        assigned_learners = request.data.get('assigned_learners', None)
        max_assigned_learners = request.data.get('max_assigned_learners', None)
        try:
            instructor = service.update_learners_fields(pk, assigned_learners, max_assigned_learners)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        if not instructor:
            return Response({"detail": "Instructor no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        serializer = InstructorSerializer(instructor)
        return Response(serializer.data, status=status.HTTP_200_OK)
    service_class = InstructorService
    serializer_class = GetInstructorSerializer


    # ----------- FILTER INSTRUCTORS -----------
    @swagger_auto_schema(
        operation_description="Filtra instructores por nombre, número de documento y área de conocimiento.",
        manual_parameters=[
                                    openapi.Parameter(
                                        'request_state',
                                        openapi.IN_QUERY,
                                        description="Estado de la solicitud a filtrar (opcional)",
                                        type=openapi.TYPE_STRING,
                                        required=False
                                    ),
                        openapi.Parameter(
                            'program_name',
                            openapi.IN_QUERY,
                            description="Nombre (o parte) del programa a filtrar (opcional)",
                            type=openapi.TYPE_STRING,
                            required=False
                        ),
            openapi.Parameter('search', openapi.IN_QUERY, description="Buscar por nombre o número de documento", type=openapi.TYPE_STRING),
            openapi.Parameter('knowledge_area_id', openapi.IN_QUERY, description="Filtrar por área de conocimiento (ID)", type=openapi.TYPE_INTEGER),
            openapi.Parameter('is_followup_instructor', openapi.IN_QUERY, description="Filtrar instructores: 'all' (todos), 'true' (solo seguimiento), 'false' (solo no seguimiento)", type=openapi.TYPE_STRING, enum=['all','true','false']),
        ],
        responses={200: openapi.Response("Lista de instructores filtrados")},
        tags=["Instructor"]
    )
    @action(detail=False, methods=['get'], url_path='filter')
    def filter_instructors(self, request):
        search = request.query_params.get('search')
        knowledge_area_id = request.query_params.get('knowledge_area_id')
        is_followup = request.query_params.get('is_followup_instructor', 'all')
        if knowledge_area_id:
            try:
                knowledge_area_id = int(knowledge_area_id)
            except ValueError:
                return Response({"detail": "El ID de área de conocimiento debe ser un número."}, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.service_class().repository.get_filtered_instructors(search, knowledge_area_id, is_followup)
        # Paginar resultados si corresponde
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Lista todas las asignaciones de un instructor, incluyendo datos del aprendiz y la solicitud. Si se proporciona 'asignation_id' o 'apprentice_name' como parámetros de query string, filtra por esos valores.",
        tags=["Instructor"],
        manual_parameters=[
            openapi.Parameter(
                'asignation_id',
                openapi.IN_QUERY,
                description="ID de la asignación específica a filtrar (opcional)",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'apprentice_name',
                openapi.IN_QUERY,
                description="Nombre (o parte) del aprendiz a filtrar (opcional)",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'apprentice_id_number',
                openapi.IN_QUERY,
                description="Número de identificación del aprendiz a filtrar (opcional)",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'modality_name',
                openapi.IN_QUERY,
                description="Nombre (o parte) de la modalidad a filtrar (opcional)",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'program_name',
                openapi.IN_QUERY,
                description="Nombre (o parte) del programa a filtrar (opcional)",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'request_state',
                openapi.IN_QUERY,
                description="Estado de la solicitud a filtrar (opcional)",
                type=openapi.TYPE_STRING,
                required=False
            )
        ],
        responses={200: openapi.Response("Lista de asignaciones", 
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_OBJECT)
            )
        )}
    )
    @action(detail=True, methods=['get'], url_path='asignations')
    def asignations(self, request, pk=None):
        program_name = request.query_params.get('program_name')
        request_state = request.query_params.get('request_state')
        """
        Endpoint para obtener todas las asignaciones de un instructor específico.
        Si se proporciona 'asignation_id' como parámetro de query string, filtra por esa asignación.
        """
        service = InstructorService()
        asignation_id = request.query_params.get('asignation_id')
        apprentice_name = request.query_params.get('apprentice_name')
        apprentice_id_number = request.query_params.get('apprentice_id_number')
        modality_name = request.query_params.get('modality_name')
        asignaciones = service.get_asignations(pk)
        if asignation_id:
            asignaciones = asignaciones.filter(id=asignation_id)
        if apprentice_name:
            asignaciones = asignaciones.filter(
                request_asignation__apprentice__person__first_name__icontains=apprentice_name
            )
        if apprentice_id_number:
            asignaciones = asignaciones.filter(
                request_asignation__apprentice__person__number_identification=apprentice_id_number
            )
        if modality_name:
            asignaciones = asignaciones.filter(
                request_asignation__modality_productive_stage__name_modality__icontains=modality_name
            )
        if program_name:
            asignaciones = asignaciones.filter(
                request_asignation__apprentice__ficha__program__name__icontains=program_name
            )
        if request_state:
            asignaciones = asignaciones.filter(
                request_asignation__request_state=request_state
            )
        serializer = AsignationInstructorWithMessageSerializer(asignaciones, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)