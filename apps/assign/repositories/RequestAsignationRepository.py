from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.assign.entity.models import RequestAsignation
from apps.assign.entity.enums.request_state_enum import RequestState
from django.db.models import Q
from apps.general.entity.models import PersonSede
from apps.general.entity.models import Apprentice, Sede
from apps.assign.entity.models import Enterprise, Boss, HumanTalent, ModalityProductiveStage, RequestAsignation
from django.db import transaction
from django.utils import timezone
from apps.general.entity.models import Ficha
from dateutil.relativedelta import relativedelta
import logging

logger = logging.getLogger(__name__)


class RequestAsignationRepository(BaseRepository):

    def __init__(self):
        super().__init__(RequestAsignation)

    def filter_form_requests(self, search=None, request_state=None, program_id=None, modality_id=None):
        queryset = RequestAsignation.objects.select_related(
            'apprentice__person',
            'apprentice__ficha__program',
            'enterprise',
            'modality_productive_stage'
        ).all()

        #  Filtro por texto (nombre o número de documento)
        if search:
            queryset = queryset.filter(
                Q(apprentice__person__first_name__icontains=search) |
                Q(apprentice__person__first_last_name__icontains=search) |
                Q(apprentice__person__second_last_name__icontains=search) |
                Q(apprentice__person__number_identification__icontains=search)
            )

        #  Filtro por estado
        if request_state:
            queryset = queryset.filter(request_state=request_state)

        #  Filtro por programa
        if program_id:
            queryset = queryset.filter(apprentice__ficha__program_id=program_id)

        #  Filtro por modalidad de etapa práctica
        if modality_id:
            try:
                modality_id = int(modality_id)
                queryset = queryset.filter(modality_productive_stage_id=modality_id)
            except ValueError:
                # invalid modality id, no filter applied (or could raise)
                pass

        return queryset

    
    def get_form_request_by_id(self, request_id):
        """
        Obtener una solicitud de formulario por su ID con todas sus relaciones (usando las nuevas foráneas directas).
        """
        try:
            request_asignation = RequestAsignation.objects.select_related(
                'apprentice__person',
                'apprentice__ficha',
                'enterprise',
                'modality_productive_stage',
                'boss',
                'human_talent'
            ).get(pk=request_id)
            # Verificar que tenga boss y human_talent asociados directamente
            if request_asignation.boss and request_asignation.human_talent:
                modality = request_asignation.modality_productive_stage
                regional = getattr(modality, 'regional', None)
                center = getattr(modality, 'center', None)
                sede = getattr(modality, 'sede', None)
                person = request_asignation.apprentice.person
                person_sede = PersonSede.objects.filter(person=person).first()
                sede = person_sede.sede if person_sede and person_sede.sede else sede
                return (
                    person,
                    request_asignation.apprentice,
                    request_asignation.enterprise,
                    request_asignation.boss,
                    request_asignation.human_talent,
                    modality,
                    request_asignation,
                    regional,
                    center,
                    sede
                )
            else:
                return None
        except RequestAsignation.DoesNotExist:
            return None


    def create_all_dates_form_request(self, data):
        """
        Crea las entidades relacionadas con la solicitud de formulario en una sola transacción.
        Vincula el aprendiz existente y actualiza su ficha.
        """
        
        with transaction.atomic():
            logger.info(f"Iniciando creación de solicitud para {data.get('person_first_name')} {data.get('person_first_last_name')} {data.get('person_second_last_name', '')}")
            
            # OBTENER ENTIDADES DE REFERENCIA (solo comunicación BD)
            sede = Sede.objects.get(pk=data['sede'])
            modality = ModalityProductiveStage.objects.get(pk=data['modality_productive_stage'])
            
            # Buscar aprendiz existente
            aprendiz = Apprentice.objects.get(pk=data['apprentice'])

            # Buscar ficha y vincularla al aprendiz
            ficha = Ficha.objects.get(pk=data['ficha'])
            aprendiz.ficha = ficha
            aprendiz.save()
            
            # CREACIÓN DE ENTIDADES (solo operaciones BD)
            

            # 3. Crear Enterprise primero (antes boss era OneToOne en Enterprise)
            enterprise_data = {
                'name_enterprise': data['enterprise_name'],
                'nit_enterprise': data['enterprise_nit'],
                'locate': data['enterprise_location'],
                'email_enterprise': data['enterprise_email'],
            }
            enterprise = Enterprise.objects.create(**enterprise_data)
            logger.info(f"Empresa creada con ID: {enterprise.id}")

            # 4. Crear Boss y relacionarlo con la enterprise (FK en Boss)
            boss_data = {
                'enterprise': enterprise,
                'name_boss': data['boss_name'],
                'phone_number': data['boss_phone'],
                'email_boss': data['boss_email'],
                'position': data['boss_position'],
            }
            boss = Boss.objects.create(**boss_data)
            logger.info(f"Jefe creado con ID: {boss.id} (enterprise_id={enterprise.id})")

            # 5. Crear HumanTalent
            human_talent_data = {
                'enterprise': enterprise,
                'name': data['human_talent_name'],
                'email': data['human_talent_email'],
                'phone_number': data['human_talent_phone'],
            }
            human_talent = HumanTalent.objects.create(**human_talent_data)
            logger.info(f"Talento humano creado con ID: {human_talent.id}")
            
            # 6. Crear RequestAsignation con PDF
            # Manejar fechas opcionales: request_date no puede ser NULL, usar hoy si no se provee
            fecha_inicio = data.get('fecha_inicio_contrato')
            fecha_fin = data.get('fecha_fin_contrato')
            request_date_value = fecha_inicio if fecha_inicio else timezone.now().date()

            # Determinar fecha de fin por defecto (6 meses desde la fecha de inicio o request_date)
            if fecha_fin:
                fecha_fin_value = fecha_fin
            else:
                base_for_end = fecha_inicio if fecha_inicio else request_date_value
                fecha_fin_value = base_for_end + relativedelta(months=6)

            request_asignation_data = {
                'apprentice': aprendiz,
                'enterprise': enterprise,
                'modality_productive_stage': modality,
                'request_date': request_date_value,
                # Si no se proporciona fecha de inicio, usar request_date_value
                # para evitar insertar NULL cuando la columna en la BD no lo permita.
                'date_start_production_stage': fecha_inicio if fecha_inicio else request_date_value,
                # Si no se proporciona fecha fin, usar fecha_fin_value (por ejemplo +6 meses)
                'date_end_production_stage': fecha_fin_value,
                'pdf_request': data.get('pdf_request'),  # El archivo PDF
                'request_state': RequestState.SIN_ASIGNAR,  # Estado inicial correcto del enum
            }
            request_asignation = RequestAsignation.objects.create(**request_asignation_data)
            logger.info(f"RequestAsignation creado con ID: {request_asignation.id}, PDF: {request_asignation.pdf_request}")
            
            logger.info("Solicitud de formulario creada exitosamente")
            
            # Retornar instancias directamente (incluyendo request_asignation)
            return aprendiz, ficha, enterprise, boss, human_talent, sede, modality, request_asignation


    def get_all_form_requests(self):
        """
        Obtener todas las solicitudes de formulario con sus relaciones.
        Usa RequestAsignation como tabla principal que conecta todo.
        """
        logger.info("Obteniendo todas las solicitudes de formulario")

        # Obtener todas las RequestAsignation con sus relaciones optimizadas
        request_asignations = RequestAsignation.objects.select_related(
            'apprentice__person',           # Person a través de Apprentice
            'apprentice__ficha',            # Ficha del aprendiz
            'enterprise',                   # Enterprise
            'modality_productive_stage',    # ModalityProductiveStage
            'boss',                         # Boss directo
            'human_talent'                  # HumanTalent directo
        ).all()

        form_requests = []

        for request_asignation in request_asignations:
            # Verificar que tenga boss y human_talent asociados directamente
            if request_asignation.boss and request_asignation.human_talent:
                modality = request_asignation.modality_productive_stage
                regional = getattr(modality, 'regional', None)
                center = getattr(modality, 'center', None)
                sede = getattr(modality, 'sede', None)
                person = request_asignation.apprentice.person
                person_sede = PersonSede.objects.filter(person=person).first()
                sede = person_sede.sede if person_sede and person_sede.sede else None
                form_request = (
                    person,
                    request_asignation.apprentice,
                    request_asignation.enterprise,
                    request_asignation.boss,
                    request_asignation.human_talent,
                    sede,
                    modality,
                    request_asignation
                )
                form_requests.append(form_request)

        logger.info(f"Se encontraron {len(form_requests)} solicitudes")
        return form_requests
    
    
    
    




