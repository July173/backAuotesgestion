from core.base.services.implements.baseService.BaseService import BaseService
from apps.assign.repositories.RequestAsignationRepository import RequestAsignationRepository
from django.db import transaction
import logging
from apps.general.entity.models import Apprentice, Ficha, Sede
from apps.security.entity.models import Person
from apps.assign.entity.models import ModalityProductiveStage
from apps.assign.entity.enums.request_state_enum import RequestState
from apps.assign.entity.models import RequestAsignation
from apps.security.emails.SolicitudRechazada import send_rejection_email
from apps.security.entity.models import User
from apps.assign.entity.models import RequestAsignation
from apps.general.entity.models import PersonSede
from dateutil.relativedelta import relativedelta
from django.utils.dateparse import parse_date
from apps.assign.entity.models import Enterprise, Boss, HumanTalent
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.assign.entity.serializers.form.RequestAsignationDashboardSerializer import RequestAsignationDashboardSerializer
from apps.general.services.NotificationService import NotificationService
from apps.assign.repositories.MessageRepository import MessageRepository
from apps.assign.entity.models import AsignationInstructor
from apps.assign.entity.models import VisitFollowing


logger = logging.getLogger(__name__)


class RequestAsignationService(BaseService):
 

    

    def __init__(self):
        self.repository = RequestAsignationRepository()

    def error_response(self, message, error_type="error"):
        return {"success": False, "error_type": error_type, "message": str(message), "data": None}

    def get_pdf_url(self, request_id):
        try:
            solicitud = RequestAsignation.objects.get(pk=request_id)
            if solicitud.pdf_request:
                return {
                    'success': True,
                    'pdf_url': solicitud.pdf_request.url
                }
            else:
                return self.error_response('La solicitud no tiene PDF adjunto.', "no_pdf")
        except RequestAsignation.DoesNotExist:
            return self.error_response('Solicitud no encontrada.', "not_found")
        except Exception as e:
            return self.error_response(f"Error al obtener PDF: {e}", "get_pdf_url")

    def reject_request(self, request_id, rejection_message):
        try:
            request = RequestAsignation.objects.get(pk=request_id)
            
            # Disable the learner assignment to the instructor if it exists and update assigned_learners
            asignation = AsignationInstructor.objects.filter(request_asignation=request, active=True).first()
            if asignation:
                asignation.active = False
                asignation.delete_at = timezone.now()
                asignation.save()
                # Disminuir el contador de aprendices asignados al instructor
                instructor = asignation.instructor
                if hasattr(instructor, 'assigned_learners') and instructor.assigned_learners and instructor.assigned_learners > 0:
                    instructor.assigned_learners -= 1
                    instructor.save()
            
            request.request_state = RequestState.RECHAZADO
            request.rejectionMessage = rejection_message
            request.save()
            apprentice = request.apprentice
            person = apprentice.person
            nombre_aprendiz = f"{person.first_name} {person.first_last_name}"
            user = User.objects.filter(person_id=getattr(person, 'id', None)).first()
            email = user.email if user else None
            if email:
                send_rejection_email(email, nombre_aprendiz, rejection_message)
            # Notificación al aprendiz
            NotificationService().notify_rejection(apprentice, rejection_message)
            return {
                'success': True,
                'message': 'Solicitud rechazada correctamente',
                'data': {
                    'id': request.id,
                    'request_state': request.request_state,
                    'rejectionMessage': request.rejectionMessage
                }
            }
        except RequestAsignation.DoesNotExist:
            return self.error_response('Solicitud no encontrada', "not_found")
        except Exception as e:
            return self.error_response(f"Error al rechazar solicitud: {e}", "reject_request")

    def get_form_request_by_id(self, request_id):
        try:
            result = self.repository.get_form_request_by_id(request_id)
            if not result:
                return self.error_response('Solicitud no encontrada', "not_found")
            person, aprendiz, enterprise, boss, human_talent, modality, request_asignation, regional, center, sede = result
            request_item = {
                'aprendiz_id': aprendiz.id,
                'ficha_id': aprendiz.ficha_id if aprendiz.ficha else None,
                'fecha_inicio_contrato': request_asignation.date_start_production_stage,
                'fecha_fin_contrato': getattr(request_asignation, 'date_end_production_stage', None),
                'enterprise_name': enterprise.name_enterprise,
                'enterprise_nit': enterprise.nit_enterprise,
                'enterprise_location': enterprise.locate,
                'enterprise_email': enterprise.email_enterprise,
                'boss_name': boss.name_boss if boss else None,
                'boss_phone': boss.phone_number if boss else None,
                'boss_email': boss.email_boss if boss else None,
                'boss_position': boss.position if boss else None,
                'human_talent_name': human_talent.name if human_talent else None,
                'human_talent_email': human_talent.email if human_talent else None,
                'human_talent_phone': human_talent.phone_number if human_talent else None,
                'regional': regional.id if regional else None,
                'center': center.id if center else None,
                'sede': sede.id if sede else None,
                'modality_productive_stage': modality.id,
                'request_state': request_asignation.request_state
            }
            person, aprendiz, enterprise, boss, human_talent, modality, request_asignation, regional, center, sede = result
            # Get apprentice email
            user = User.objects.filter(person_id=getattr(person, 'id', None)).first()
            correo_aprendiz = user.email if user else None
            # Get sede, center and regional from PersonSede
            personsede = PersonSede.objects.filter(person_id=getattr(person, 'id', None)).first()
            sede_obj = personsede.sede if personsede else sede
            center_obj = sede_obj.center if sede_obj and hasattr(sede_obj, 'center') else center
            regional_obj = center_obj.regional if center_obj and hasattr(center_obj, 'regional') else regional
            # Human talent data
            talento_humano = {
                'nombre': getattr(human_talent, 'name', None),
                'correo': getattr(human_talent, 'email', None),
                'telefono': getattr(human_talent, 'phone_number', None)
            } if human_talent else None
            # Get apprentice file number and program name
            ficha = aprendiz.ficha if hasattr(aprendiz, 'ficha') and aprendiz.ficha else None
            numero_ficha = ficha.file_number if ficha and hasattr(ficha, 'file_number') else None
            programa = ficha.program if ficha and hasattr(ficha, 'program') else None
            nombre_programa = programa.name if programa and hasattr(programa, 'name') else None
            request_item = {
                'aprendiz_id': aprendiz.id,
                'nombre_aprendiz': f"{getattr(person, 'first_name', '')} {getattr(person, 'first_last_name', '')} {getattr(person, 'second_last_name', '')}",
                'tipo_identificacion': getattr(person, 'type_identification_id', None),
                'numero_identificacion': getattr(person, 'number_identification', None),
                'telefono_aprendiz': getattr(person, 'phone_number', None),
                'correo_aprendiz': correo_aprendiz,
                'ficha_id': ficha.id if ficha else None,
                'numero_ficha': numero_ficha,
                'programa': nombre_programa,
                'empresa_nombre': enterprise.name_enterprise,
                'empresa_nit': enterprise.nit_enterprise,
                'empresa_ubicacion': enterprise.locate,
                'empresa_correo': enterprise.email_enterprise,
                'jefe_nombre': boss.name_boss,
                'jefe_telefono': boss.phone_number,
                'jefe_correo': boss.email_boss,
                'jefe_cargo': boss.position,
                'regional': regional_obj.name if regional_obj else None,
                'center': center_obj.name if center_obj else None,
                'sede': sede_obj.name if sede_obj else None,
                'fecha_solicitud': request_asignation.request_date,
                'fecha_inicio_etapa_practica': request_asignation.date_start_production_stage,
                'fecha_fin_etapa_practica': getattr(request_asignation, 'date_end_production_stage', None),
                'modality_productive_stage': modality.name_modality if hasattr(modality, 'name_modality') else None,
                'request_state': request_asignation.request_state,
                'pdf_url': request_asignation.pdf_request.url if request_asignation.pdf_request else None,
                'talento_humano': talento_humano
            }
            return {
                'success': True,
                'message': 'Solicitud encontrada',
                'data': request_item
            }
        except RequestAsignation.DoesNotExist:
            return self.error_response('Solicitud no encontrada', "not_found")
        except Exception as e:
            return self.error_response(f"Error al obtener la solicitud: {e}", "get_form_request_by_id")

   
    def list_form_requests(self):
        """
        Listar solicitudes mostrando solo Nombre, Tipo de identificación, Número y Fecha Solicitud.
        """
        try:
            logger.info("Obteniendo lista de solicitudes (solo datos personales básicos)")
            form_requests = self.repository.get_all_form_requests()
            requests_data = []
            for person, aprendiz, enterprise, boss, human_talent, sede, modality, request_asignation in form_requests:
                # Buscar instructor asignado a la solicitud (si existe)
                instructor_name = None
                instructor_id = None
                asignation = getattr(request_asignation, 'asignation_instructor', None)
                if asignation:
                    instructor = getattr(asignation, 'instructor', None)
                    if instructor and hasattr(instructor, 'person'):
                        instructor_id = instructor.id
                        p = instructor.person
                        instructor_name = f"{getattr(p, 'first_name', '')} {getattr(p, 'first_last_name', '')} {getattr(p, 'second_last_name', '')}".strip()
                request_item = {
                    'id': request_asignation.id,  
                    'aprendiz_id': aprendiz.id,   
                    'nombre': f"{getattr(person, 'first_name', '')} {getattr(person, 'first_last_name', '')} {getattr(person, 'second_last_name', '')}",
                    'tipo_identificacion': getattr(person, 'type_identification_id', None),
                    'numero_identificacion': getattr(person, 'number_identification', None),
                    'fecha_solicitud': request_asignation.request_date,
                    'request_state': request_asignation.request_state,
                    'nombre_modalidad': getattr(modality, 'name_modality', None) if modality else None,
                    'boss': boss.name_boss if boss else None,
                    'human_talent': human_talent.name if human_talent else None,
                    'instructor': instructor_name,
                    'instructor_id': instructor_id
                }
                requests_data.append(request_item)
            logger.info(f"Se encontraron {len(requests_data)} solicitudes")
            return {
                'success': True,
                'message': f'Se encontraron {len(requests_data)} solicitudes',
                'count': len(requests_data),
                'data': requests_data
            }
        except Exception as e:
            logger.error(f"Error al listar solicitudes: {str(e)}")
            return self.error_response(f"Error al obtener las solicitudes: {str(e)}", "list_form_requests")

    def get_aprendiz_dashboard(self, aprendiz_id):
        """
        Obtiene la información del dashboard del aprendiz:
        - Estado de la solicitud activa
        - Instructor asignado (si existe)
        - Detalles de la solicitud
        """
        try:
            
            
            aprendiz = Apprentice.objects.select_related('person', 'ficha').get(pk=aprendiz_id)
            latest_request = RequestAsignation.objects.filter(
                apprentice=aprendiz
            ).select_related(
                'enterprise',
                'modality_productive_stage'
            ).prefetch_related('enterprise__bosses').order_by('-request_date').first()
            
            if latest_request:
                return RequestAsignationDashboardSerializer(latest_request).data
            else:
                return None
            
        except Apprentice.DoesNotExist:
            return self.error_response('Aprendiz no encontrado', 'not_found')
        except Exception as e:
            logger.error(f"Error al obtener dashboard del aprendiz: {str(e)}")
            return self.error_response(f"Error al obtener información del dashboard: {str(e)}", "dashboard_error")


    def filter_form_requests(self, search=None, request_state=None, program_id=None, modality_id=None):
        try:
            requests = self.repository.filter_form_requests(search, request_state, program_id, modality_id)
            data = []

            for req in requests:
                person = req.apprentice.person
                ficha = req.apprentice.ficha
                programa = ficha.program.name if ficha and hasattr(ficha, 'program') and ficha.program else None
                data.append({
                    "id": req.id,
                    "apprentice_id": req.apprentice.id,
                    "nombre": f"{person.first_name} {person.first_last_name} {person.second_last_name}",
                    "tipo_identificacion": getattr(person, 'type_identification_id', None),
                    "numero_identificacion": str(person.number_identification),
                    "fecha_solicitud": str(req.request_date),
                    "request_state": req.request_state,
                    "programa": programa,
                    "modalidad": getattr(req.modality_productive_stage, 'name_modality', None) if hasattr(req, 'modality_productive_stage') else None,
                    "modalidad_id": req.modality_productive_stage.id if getattr(req, 'modality_productive_stage', None) else None
                })

            return {
                "success": True,
                "count": len(data),
                "data": data
            }

        except Exception as e:
            return self.error_response(f"Error al filtrar solicitudes: {e}", "filter_form_requests")


    def update_request_state(self, request_id, request_state=None, fecha_inicio=None, fecha_fin=None, content=None, type_message=None, whose_message=None):
        """
        Update the request_asignation state and optionally the start/end dates.
        If content, type_message and whose_message are provided from frontend, use them.
        Otherwise, generate automatic message for backward compatibility.
        Returns a dict with the same structure as other service methods.
        """
        try:
            req = RequestAsignation.objects.get(pk=request_id)

            # Parse date strings if provided
            if isinstance(fecha_inicio, str):
                fecha_inicio_parsed = parse_date(fecha_inicio)
            else:
                fecha_inicio_parsed = fecha_inicio

            if isinstance(fecha_fin, str):
                fecha_fin_parsed = parse_date(fecha_fin)
            else:
                fecha_fin_parsed = fecha_fin

            if fecha_inicio_parsed is not None and fecha_fin_parsed is not None:
                if fecha_inicio_parsed > fecha_fin_parsed:
                    return self.error_response("La fecha de inicio no puede ser mayor que la fecha de fin de contrato.", "invalid_dates")
                diferencia = relativedelta(fecha_fin_parsed, fecha_inicio_parsed)
                meses = diferencia.years * 12 + diferencia.months
                if meses > 7 or (meses == 7 and diferencia.days > 0):
                    return self.error_response("No debe haber más de 7 meses de diferencia entre la fecha de inicio y fin de contrato.", "invalid_dates")

            # Apply updates
            updated = False
            auto_message_parts = []
            
            if request_state is not None:
                req.request_state = request_state
                updated = True
                auto_message_parts.append(f"Estado actualizado a: {request_state}")

            if fecha_inicio_parsed is not None:
                req.date_start_production_stage = fecha_inicio_parsed
                updated = True
                auto_message_parts.append(f"Fecha de inicio actualizada a: {fecha_inicio_parsed}")

            if fecha_fin_parsed is not None:
                req.date_end_production_stage = fecha_fin_parsed
                updated = True
                auto_message_parts.append(f"Fecha de fin actualizada a: {fecha_fin_parsed}")

            if updated:
                req.save()
                
                # Create message: prioritize frontend-provided message, fallback to auto-generated
                if content and type_message:
                    # Use message data from frontend (instructor valuation message)
                    message_type = type_message if type_message else "ACTUALIZACION"
                    message_whose = whose_message if whose_message else "INSTRUCTOR"
                    MessageRepository().create(req, content, message_type, message_whose)
                elif auto_message_parts:
                    # Fallback: generate automatic message (for backward compatibility)
                    MessageRepository().create(req, " | ".join(auto_message_parts), "ACTUALIZACION")

                # Crear visitas automáticas si el estado cambió a ASIGNADO
                if request_state == RequestState.ASIGNADO:
                    # Verificar si existe una asignación de instructor activa
                    asignation = AsignationInstructor.objects.filter(
                        request_asignation=req, 
                        active=True
                    ).first()
                    
                    if asignation:
                        start_date = req.date_start_production_stage
                        end_date = req.date_end_production_stage
                        
                        if start_date and end_date:
                            # Verificar si ya existen visitas para esta asignación
                            existing_visits = VisitFollowing.objects.filter(
                                asignation_instructor=asignation
                            ).count()
                            
                            # Solo crear visitas si no existen previamente
                            if existing_visits == 0:
                                visitas = []
                                total_days = (end_date - start_date).days
                                if total_days < 1:
                                    total_days = 1
                                periodo = total_days / 3
                                nombres = ['Concertación', 'Visita parcial', 'Visita final']
                                
                                for i, nombre in enumerate(nombres, start=1):
                                    fecha = start_date + relativedelta(days=round(periodo * (i-1)))
                                    visitas.append(VisitFollowing(
                                        asignation_instructor=asignation,
                                        visit_number=i,
                                        name_visit=nombre,
                                        scheduled_date=fecha,
                                        state_visit='por hacer',
                                        observations=None,
                                        date_visit_made=None,
                                        observation_state_visit=None,
                                        pdf_report=None
                                    ))
                                VisitFollowing.objects.bulk_create(visitas)
                                logger.info(f"Se crearon {len(visitas)} visitas para la asignación {asignation.id}")

            return {
                'success': True,
                'message': 'Solicitud actualizada correctamente',
                'data': {
                    'id': req.id,
                    'request_state': req.request_state,
                    'date_start_production_stage': req.date_start_production_stage,
                    'date_end_production_stage': getattr(req, 'date_end_production_stage', None)
                }
            }

        except RequestAsignation.DoesNotExist:
            return self.error_response('Solicitud no encontrada', 'not_found')
        except Exception as e:
            return self.error_response(f"Error al actualizar la solicitud: {e}", 'update_request_state')


    def create_complete_request_package(self, package_data):
        """Recibe un paquete con estructura:
        {
          'empresa': {...}, 'jefe': {...}, 'talentoHumano': {...}, 'solicitud': {...}
        }
        Crea o usa entidades según 'id' y crea la solicitud en una transacción.
        """
        try:
            # --- Extract and validate data before creating any object ---
            empresa_payload = package_data.get('empresa') or package_data.get('enterprise') or package_data.get('company') or {}
            jefe_payload = package_data.get('jefe') or package_data.get('boss') or {}
            talento_payload = package_data.get('talentoHumano') or package_data.get('human_talent') or {}
            solicitud_payload = package_data.get('solicitud') or package_data.get('request') or {}

            # Map fields from Spanish and English payloads
            apprentice_id = solicitud_payload.get('apprentice') or solicitud_payload.get('aprendiz')
            ficha_id = solicitud_payload.get('ficha') or solicitud_payload.get('cohort')
            fecha_inicio = solicitud_payload.get('fecha_inicio_contrato') or solicitud_payload.get('contract_start_date')
            fecha_fin = solicitud_payload.get('fecha_fin_contrato') or solicitud_payload.get('contract_end_date')
            sede_id = solicitud_payload.get('sede') or solicitud_payload.get('site')
            modality_id = solicitud_payload.get('modality_productive_stage') or solicitud_payload.get('modality')

            logger.debug(f"create_complete_request_package payload apprentice_id={apprentice_id} tipo={type(apprentice_id)} sede_id={sede_id} tipo_sede_id={type(sede_id)}")
            if not apprentice_id:
                return self.error_response('El campo solicitud.apprentice es requerido', 'missing_apprentice')

            # Validate existence of related entities before creating anything
            apprentice = Apprentice.objects.get(pk=apprentice_id)

            ficha = None
            if ficha_id:
                ficha = Ficha.objects.get(pk=ficha_id)

            # Normalize 'sede_id': accept pk (int/str) or partial name
            sede = None
            if sede_id is not None:
                try:
                    # first try as PK
                    sede = Sede.objects.get(pk=int(sede_id))
                except Exception:
                    # try to find by partial name
                    sede = Sede.objects.filter(name__icontains=str(sede_id).split('(')[0].strip()).first()
                    if not sede:
                        logger.debug(f"No se encontró sede por nombre: {sede_id}")
                        return self.error_response(f"No se encontró la sede: {sede_id}", 'not_found')
                logger.debug(f"sede resuelta: {getattr(sede, 'id', None)} tipo={type(sede)} nombre={getattr(sede,'name',None)}")
            # Strict validation: ensure `sede` is an instance of Sede if resolved
            if sede is not None and not isinstance(sede, Sede):
                logger.error(f"Valor de 'sede' no es instancia de Sede tras normalizar: valor={sede} tipo={type(sede)}")
                return self.error_response(f"Sede inválida: {sede}", 'invalid_sede')

            modality = None
            if modality_id:
                modality = ModalityProductiveStage.objects.get(pk=modality_id)

            # Validate modality and duration
            duration_months = 6
            if fecha_inicio and fecha_fin:
                difference = relativedelta(fecha_fin, fecha_inicio)
                duration_months = difference.years * 12 + difference.months
                if duration_months < 0:
                    return self.error_response("La fecha de fin debe ser posterior a la de inicio.", "invalid_dates")

            try:
                self._validar_solicitud(apprentice_id, ficha_id, modality_id, duration_months)
            except Exception as e:
                return self.error_response(str(e), 'validation')

            # --- If everything is valid, create objects within the transaction ---
            with transaction.atomic():
                # enterprise
                if empresa_payload.get('id'):
                    enterprise = Enterprise.objects.get(pk=empresa_payload.get('id'))
                else:
                    name = empresa_payload.get('nombre') or empresa_payload.get('name')
                    nit = empresa_payload.get('nit') or empresa_payload.get('tax_id') or empresa_payload.get('nit_enterprise')
                    locate = empresa_payload.get('direccion') or empresa_payload.get('locate') or empresa_payload.get('address')
                    email = empresa_payload.get('correo') or empresa_payload.get('email') or empresa_payload.get('enterprise_email')
                    enterprise = Enterprise.objects.create(
                        name_enterprise=name or '',
                        nit_enterprise=nit or '',
                        locate=locate or '',
                        email_enterprise=email or ''
                    )

                # Boss
                if jefe_payload.get('id'):
                    boss = Boss.objects.get(pk=jefe_payload.get('id'))
                else:
                    boss = Boss.objects.create(
                        enterprise=enterprise,
                        name_boss=jefe_payload.get('nombre') or jefe_payload.get('name') or '',
                        phone_number=jefe_payload.get('telefono') or jefe_payload.get('phone') or 0,
                        email_boss=jefe_payload.get('correo') or jefe_payload.get('email') or '',
                        position=jefe_payload.get('cargo') or jefe_payload.get('position') or ''
                    )

                # Human Talent
                if talento_payload.get('id'):
                    human_talent = HumanTalent.objects.get(pk=talento_payload.get('id'))
                else:
                    human_talent = HumanTalent.objects.create(
                        enterprise=enterprise,
                        name=talento_payload.get('nombre') or talento_payload.get('name') or '',
                        email=talento_payload.get('correo') or talento_payload.get('email') or '',
                        phone_number=talento_payload.get('telefono') or talento_payload.get('phone') or 0
                    )

                # Update apprentice record if provided
                if ficha_id:
                    apprentice.ficha = ficha
                    apprentice.save()

                request_date_value = fecha_inicio if fecha_inicio else timezone.now().date()

                # Determine default end date (6 months from start date or request_date)
                if fecha_fin:
                    fecha_fin_value = fecha_fin
                else:
                    base_for_end = fecha_inicio if fecha_inicio else request_date_value
                    fecha_fin_value = base_for_end + relativedelta(months=6)

                request_asignation = RequestAsignation.objects.create(
                    apprentice=apprentice,
                    enterprise=enterprise,
                    modality_productive_stage=modality if modality else ModalityProductiveStage.objects.first(),
                    human_talent=human_talent,
                    boss=boss,
                    request_date=request_date_value,
                    date_start_production_stage=fecha_inicio if fecha_inicio else request_date_value,
                    date_end_production_stage=fecha_fin_value,
                    request_state=RequestState.SIN_ASIGNAR
                )

                
                if sede:
                    try:
                        person = apprentice.person
                        logger.debug(f"apprentice.person valor={person} tipo={type(person)}")
                        # Ensure 'person' is an instance of Person
                        if not isinstance(person, Person):
                            person = Person.objects.get(pk=getattr(apprentice, 'person_id', None))
                            logger.debug(f"person resuelto por id: {person} tipo={type(person)}")

                        # Use getattr para evitar errores si person_id no existe
                        # Use update_or_create para manejar ambos casos
                        PersonSede.objects.update_or_create(
                            person_id=getattr(apprentice, 'person_id', None),
                            defaults={"sede_id": sede.id if sede else None}
                        )
                    except Exception as e:
                        logger.exception("Error actualizando PersonSede")
                        return self.error_response(f"Error al actualizar PersonSede: {e}", 'person_sede_error')

                # Notificate the apprentice about the created request
                notification_service = NotificationService()
                ficha_obj = apprentice.ficha
                sede_obj = sede if sede else None
                if not sede_obj:
                    person_sede = PersonSede.objects.filter(person_id=getattr(apprentice, 'person_id', None)).first()
                    if person_sede:
                        sede_obj = person_sede.sede
                notification_service.notify_request_created(apprentice, ficha_obj, sede_obj)
                return {
                    'success': True,
                    'message': 'Solicitud creada exitosamente',
                    'data': {
                        'enterprise': {'id': enterprise.id},
                        'boss': {'id': boss.id if boss else None},
                        'human_talent': {'id': human_talent.id if human_talent else None},
                        'request_asignation': {'id': request_asignation.id}
                    }
                }

        except Enterprise.DoesNotExist:
            return self.error_response('Empresa no encontrada', 'not_found')
        except Boss.DoesNotExist:
            return self.error_response('Jefe no encontrado', 'not_found')
        except HumanTalent.DoesNotExist:
            return self.error_response('Talento humano no encontrado', 'not_found')
        except Apprentice.DoesNotExist:
            return self.error_response('Aprendiz no encontrado', 'not_found')
        except Ficha.DoesNotExist:
            return self.error_response('Ficha no encontrada', 'not_found')
        except ModalityProductiveStage.DoesNotExist:
            return self.error_response('Modalidad no encontrada', 'not_found')
        except Exception as e:
            try:
                # Try to capture relevant local variables for debugging
                debug_info = {
                    'apprentice_id': locals().get('apprentice_id'),
                    'apprentice_person': str(type(locals().get('apprentice').person)) if locals().get('apprentice', None) and hasattr(locals().get('apprentice'), 'person') else str(type(locals().get('apprentice', None))),
                    'sede_id': locals().get('sede_id'),
                    'sede': str(type(locals().get('sede', None)))
                }
            except Exception:
                debug_info = {'locals_error': 'error obteniendo locals()'}
            logger.exception(f"Error al crear solicitud completa: {e} | debug: {debug_info}")
            return self.error_response(f"Error al crear solicitud completa: {e}", 'create_complete_request')



    def _validar_solicitud(self, aprendiz_id, ficha_id, modalidad_id, duracion_meses):
        """
        Valida las reglas de negocio para la creación de una solicitud de asignación.
        Lanza ValidationError (o retorna error_response) si alguna regla no se cumple.
        """
        
        solicitudes = RequestAsignation.objects.filter(apprentice_id=aprendiz_id)
        # States that do NOT count as active
        inactivos = [RequestState.RECHAZADO, 'FINALIZADA']
        activas = solicitudes.exclude(request_state__in=inactivos)

        # A. Maximum 2 active requests
        if activas.count() >= 2:
            raise ValidationError("Solo puedes tener máximo dos solicitudes activas.")

        # B. Same ficha
        if ficha_id and activas.filter(apprentice__ficha_id=ficha_id).exists():
            raise ValidationError("Ya tienes una solicitud activa con esta ficha.")

        # C. Modality Contract 
        contrato_nombre = "CONTRATO_APRENDIZAJE"
        modalidad_obj = ModalityProductiveStage.objects.get(pk=modalidad_id) if modalidad_id else None
        if modalidad_obj and modalidad_obj.name_modality.upper().replace(' ', '_') == contrato_nombre:
            if activas.filter(modality_productive_stage__name_modality__iexact=modalidad_obj.name_modality).exists():
                raise ValidationError("Solo puedes tener un contrato de aprendizaje activo.")
        return True
    
    
    
    def get_request_messages_by_request_id(self, request_id):
        """
        Devuelve todos los mensajes asociados a una solicitud de asignación por su ID.
        """
        try:
            messages = MessageRepository().get().filter(request_asignation_id=request_id)
            from apps.assign.entity.serializers.MessageSerializer import MessageSerializer
            serializer = MessageSerializer(messages, many=True)
            return {
                'success': True,
                'count': len(serializer.data),
                'data': serializer.data
            }
        except Exception as e:
            return self.error_response(f"Error al obtener los mensajes: {e}", "get_request_messages_by_request_id")
    
    
    def get_operator_sofia_dashboard(self):
        """
        Obtiene estadísticas del dashboard para el operador de SOFÍA Plus.
        Retorna la evolución mensual de solicitudes registradas y pendientes.
        
        Filtra solicitudes:
        - Estado: ASIGNADO
        - Modalidad: diferente a "Contrato de Aprendizaje"
        
        Cuenta:
        - Registradas: tienen mensaje con whose_message = 'OPERADOR'
        - Pendientes: NO tienen mensaje con whose_message = 'OPERADOR'
        """
        try:
            from datetime import datetime
            from django.db.models import Count, Q
            from apps.assign.entity.models import Message
            
            current_year = datetime.now().year
            
            # Obtener todas las solicitudes ASIGNADAS del año actual
            requests = RequestAsignation.objects.filter(
                request_state=RequestState.ASIGNADO,
                request_date__year=current_year
            ).select_related('modality_productive_stage')
            
            # Excluir "Contrato de Aprendizaje"
            requests = requests.exclude(
                Q(modality_productive_stage__name_modality__icontains='contrato') &
                (Q(modality_productive_stage__name_modality__icontains='aprendizaje') |
                 Q(modality_productive_stage__name_modality__icontains='aprendiz'))
            )
            
            # Inicializar datos por mes (enero a diciembre)
            monthly_data = []
            month_names = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
            
            for month_num in range(1, 13):
                # Filtrar solicitudes del mes
                month_requests = requests.filter(request_date__month=month_num)
                
                # Contar registradas (tienen mensaje de OPERADOR)
                registered_count = 0
                pending_count = 0
                
                for req in month_requests:
                    # Verificar si tiene mensaje de OPERADOR
                    has_operator_msg = Message.objects.filter(
                        request_asignation=req,
                        whose_message='OPERADOR'
                    ).exists()
                    
                    if has_operator_msg:
                        registered_count += 1
                    else:
                        pending_count += 1
                
                monthly_data.append({
                    'month': month_names[month_num - 1],
                    'month_number': month_num,
                    'registered': registered_count,
                    'pending': pending_count,
                    'total': registered_count + pending_count
                })
            
            # Calcular totales
            total_registered = sum(m['registered'] for m in monthly_data)
            total_pending = sum(m['pending'] for m in monthly_data)
            
            return {
                'success': True,
                'message': 'Dashboard del operador obtenido correctamente',
                'data': {
                    'year': current_year,
                    'monthly_data': monthly_data,
                    'totals': {
                        'registered': total_registered,
                        'pending': total_pending,
                        'total': total_registered + total_pending
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"Error al obtener dashboard del operador: {str(e)}")
            return self.error_response(f"Error al obtener dashboard del operador: {str(e)}", "operator_dashboard_error")