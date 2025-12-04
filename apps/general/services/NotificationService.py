from apps.security.entity.models import User, Role
from apps.general.repositories.NotificationRepository import NotificationRepository
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from apps.general.entity.serializers.NotificationSerializer import NotificationSerializer
import logging


logger = logging.getLogger(__name__)

class NotificationService:

    def __init__(self):
        self.repository = NotificationRepository()

    #--- Create Notification ---#
    def create_notification(self, validated_data):
        # repository.create expects a single dict argument (see BaseRepository.create)
        if not isinstance(validated_data, dict):
            # try to coerce dataclass-like objects
            try:
                validated_data = dict(validated_data)
            except Exception:
                raise ValueError('validated_data debe ser un dict')
        # Log the payload to help debugging when notifications are not created
        try:
            log_preview = {k: (type(v).__name__ if not isinstance(v, (int, str, bool)) else v) for k, v in validated_data.items()}
        except Exception:
            log_preview = str(validated_data)
        logger.debug(f"Creando notificación con payload: {log_preview}")
        try:
            notification = self.repository.create(validated_data)
        except Exception as e:
            logger.exception(f"Error al crear Notification en repositorio: {e} | payload={log_preview}")
            raise
        # Send real-time notification via Channels
        channel_layer = get_channel_layer()
        if channel_layer is not None:
            group_name = f"notifications_{notification.id_user.id}"
            serializer = NotificationSerializer(notification)
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'send_notification',
                    'notification': serializer.data
                }
            )
        return notification

    #--- Notify Methods ---#
    def notify_request_created(self, apprentice, ficha, sede):
        # Notify coordinators of the apprentice's location
        
        try:
            coordinador_role = Role.objects.filter(type_role="Coordinador").first()
            # Log incoming values for debugging (types and reprs)
            logger.debug(f"notify_request_created called with apprentice={repr(apprentice)} ficha={repr(ficha)} sede={repr(sede)}")
            # Normalize sede to id if possible to avoid passing model instances or strings directly
            sede_id = None
            if sede is None:
                sede_id = None
            else:
                sede_id = getattr(sede, 'id', None) or sede

            if not coordinador_role:
                logger.debug("No hay role 'Coordinador' definido en la base de datos")
                return

            # Send to all accounts with the 'Coordinador' role
            coordinadores = User.objects.filter(role=coordinador_role).distinct()
            logger.debug(f"Enviando notificación de solicitud a {coordinadores.count()} coordinadores")
            for coordinador in coordinadores:
                try:
                    self.create_notification({
                        'id_user': coordinador,
                        'title': 'Nueva solicitud de asignación',
                        'message': f'Se ha creado una nueva solicitud de asignación para la ficha {ficha.file_number if ficha else ""}.',
                        'type': 'solicitud',
                        'link': '',
                    })
                except Exception:
                    logger.exception(f"Error creando notificación para coordinador id={getattr(coordinador, 'id', None)}")
            else:
                logger.debug(f"No se notificó: coordinador_role={coordinador_role} sede_id={sede_id}")
        except Exception as e:
            logger.exception(f"Error en notify_request_created: {e} | apprentice={repr(apprentice)} ficha={repr(ficha)} sede={repr(sede)}")

    #--- Notify Assignment ---#
    def notify_assignment(self, apprentice, instructor, ficha=None):
        # Notify the apprentice and the assigned instructor
        # Notify the apprentice
        user_apprentice = User.objects.filter(person_id=getattr(apprentice.person, 'id', None)).first()
        if user_apprentice:
            self.create_notification({
                'id_user': user_apprentice,
                'title': 'Asignación de instructor',
                'message': f'Se te ha asignado un instructor para la ficha {ficha.file_number if ficha else ""}.',
                'type': 'asignacion',
                'link': '',
            })
        # Notify the instructor
        user_instructor = User.objects.filter(person_id=getattr(instructor.person, 'id', None)).first()
        if user_instructor:
            self.create_notification({
                'id_user': user_instructor,
                'title': 'Nueva asignación de seguimiento',
                'message': f'Se te ha asignado un aprendiz para seguimiento en la ficha {ficha.file_number if ficha else ""}.',
                'type': 'asignacion',
                'link': '',
            })

    #--- Notify Rejection ---#
    def notify_rejection(self, apprentice, motivo):
        # Notify the apprentice about the rejection
        user_apprentice = User.objects.filter(person_id=getattr(apprentice.person, 'id', None)).first()
        if user_apprentice:
            self.create_notification({
                'id_user': user_apprentice,
                'title': 'Solicitud rechazada',
                'message': f'Tu solicitud ha sido rechazada. Motivo: {motivo}',
                'type': 'rechazo',
                'link': '',
            })

    #--- Notify Registration ---#
    def notify_registration(self, apprentice):
        # Notify all administrators when an apprentice registers
        admin_role = Role.objects.filter(type_role="Administrador").first()
        if admin_role:
            admins = User.objects.filter(role=admin_role)
            for admin in admins:
                self.create_notification({
                    'id_user': admin,
                    'title': 'Nuevo registro de aprendiz',
                    'message': f'Se ha registrado un nuevo aprendiz: {apprentice.person.first_name} {apprentice.person.first_last_name}',
                    'type': 'registro',
                    'link': '',
                })

    #--- Notify Reassignment ---#
    def notify_reassignment(self, apprentice, instructor_old, instructor_new, ficha=None):
        # Notify the apprentice and the two instructors
        # Apprentice
        user_apprentice = User.objects.filter(person_id=getattr(apprentice.person, 'id', None)).first()
        if user_apprentice:
            self.create_notification({
                'id_user': user_apprentice,
                'title': 'Reasignación de instructor',
                'message': f'Se ha reasignado tu instructor para la ficha {ficha.file_number if ficha else ""}.',
                'type': 'reasignacion',
                'link': '',
            })
        # Previous instructor
        user_old = User.objects.filter(person_id=getattr(instructor_old.person, 'id', None)).first()
        if user_old:
            self.create_notification({
                'id_user': user_old,
                'title': 'Reasignación de aprendiz',
                'message': f'El aprendiz ha sido reasignado a otro instructor en la ficha {ficha.file_number if ficha else ""}.',
                'type': 'reasignacion',
                'link': '',
            })
        # New instructor
        user_new = User.objects.filter(person_id=getattr(instructor_new.person, 'id', None)).first()
        if user_new:
            self.create_notification({
                'id_user': user_new,
                'title': 'Nueva asignación de aprendiz',
                'message': f'Se te ha asignado un nuevo aprendiz en la ficha {ficha.file_number if ficha else ""}.',
                'type': 'reasignacion',
                'link': '',
            })


    #----- Get Methods -----#
    #--- Get Notifications ---#
    def get_notifications(self, apprentice_id=None, instructor_id=None, coordinator_id=None, sofia_operator_id=None, admin_id=None):
        user = None
        role_map = {
            'apprentice_id': 'Aprendiz',
            'instructor_id': 'Instructor',
            'coordinator_id': 'Coordinador',
            'sofia_operator_id': 'Operador de Sofia Plus',
            'admin_id': 'Administrador',
        }
        if apprentice_id:
            user = User.objects.filter(id=apprentice_id, role__type_role__iexact=role_map['apprentice_id']).first()
            if not user:
                raise ValueError('El usuario no es un aprendiz o no existe.')
            qs = self.repository.get_by_apprentice_id(apprentice_id)
        elif instructor_id:
            user = User.objects.filter(id=instructor_id, role__type_role__iexact=role_map['instructor_id']).first()
            if not user:
                raise ValueError('El usuario no es un instructor o no existe.')
            qs = self.repository.get_by_instructor_id(instructor_id)
        elif coordinator_id:
            user = User.objects.filter(id=coordinator_id, role__type_role__iexact=role_map['coordinator_id']).first()
            if not user:
                raise ValueError('El usuario no es un coordinador o no existe.')
            qs = self.repository.get_by_coordinator_id(coordinator_id)
        elif sofia_operator_id:
            user = User.objects.filter(id=sofia_operator_id, role__type_role__iexact=role_map['sofia_operator_id']).first()
            if not user:
                raise ValueError('El usuario no es un operador Sofia Plus o no existe.')
            qs = self.repository.get_by_sofia_operator_id(sofia_operator_id)
        elif admin_id:
            user = User.objects.filter(id=admin_id, role__type_role__iexact=role_map['admin_id']).first()
            if not user:
                raise ValueError('El usuario no es un administrador o no existe.')
            qs = self.repository.get_by_admin_id(admin_id)
        else:
            qs = self.repository.list_all()
        if qs is None or not qs.exists():
            raise ValueError('No hay notificaciones para este usuario.')
        return qs
        
    #--- List All Notifications ---#
    def list_all(self):
        """Devuelve todas las notificaciones ordenadas por fecha descendente."""
        return self.repository.list_all()
    
    #--- Get Notification by ID ---#
    def get_notification_by_id(self, notification_id):
        notification = self.repository.get_by_id(notification_id)
        if notification and not notification.is_read:
            notification.is_read = True
            notification.save(update_fields=["is_read"])
        return notification
    
    
    #--- Delete Methods ---#
    #--- Delete Notifications ---#
    def delete_notifications(self, apprentice_id=None, instructor_id=None, coordinator_id=None, sofia_operator_id=None, admin_id=None):
        user = None
        role_map = {
            'apprentice_id': 'Aprendiz',
            'instructor_id': 'Instructor',
            'coordinator_id': 'Coordinador',
            'sofia_operator_id': 'Operador de Sofia Plus',
            'admin_id': 'Administrador',
        }
        if apprentice_id:
            user = User.objects.filter(id=apprentice_id, role__type_role__iexact=role_map['apprentice_id']).first()
            if not user:
                raise ValueError('El usuario no es un aprendiz o no existe.')
            qs = self.repository.delete_by_apprentice_id(apprentice_id)
        elif instructor_id:
            user = User.objects.filter(id=instructor_id, role__type_role__iexact=role_map['instructor_id']).first()
            if not user:
                raise ValueError('El usuario no es un instructor o no existe.')
            qs = self.repository.delete_by_instructor_id(instructor_id)
        elif coordinator_id:
            user = User.objects.filter(id=coordinator_id, role__type_role__iexact=role_map['coordinator_id']).first()
            if not user:
                raise ValueError('El usuario no es un coordinador o no existe.')
            qs = self.repository.delete_by_coordinator_id(coordinator_id)
        elif sofia_operator_id:
            user = User.objects.filter(id=sofia_operator_id, role__type_role__iexact=role_map['sofia_operator_id']).first()
            if not user:
                raise ValueError('El usuario no es un operador Sofia Plus o no existe.')
            qs = self.repository.delete_by_sofia_operator_id(sofia_operator_id)
        elif admin_id:
            user = User.objects.filter(id=admin_id, role__type_role__iexact=role_map['admin_id']).first()
            if not user:
                raise ValueError('El usuario no es un administrador o no existe.')
            qs = self.repository.delete_by_admin_id(admin_id)
        else:
            qs = self.repository.list_all()
        # Los métodos delete_by_* devuelven la cantidad de notificaciones desactivadas (int)
        if isinstance(qs, int):
            if qs == 0:
                raise ValueError('No hay notificaciones para este usuario.')
            return qs
        if qs is None:
            raise ValueError('No hay notificaciones para este usuario.')
        return qs
    
    #--- Delete Notification by ID ---#
    def delete_notification_by_id(self, notification_id):
        notification = self.repository.get_by_id(notification_id)
        if notification and not notification.is_read:
            notification.is_read = True
            notification.save(update_fields=["is_read"])
        return notification