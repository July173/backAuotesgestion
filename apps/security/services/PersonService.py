from core.base.services.implements.baseService.BaseService import BaseService
from apps.security.repositories.PersonRepository import PersonRepository
from apps.security.entity.serializers.User.UserSerializer import UserSerializer
from datetime import datetime
from apps.security.entity.models import Person, User
from django.db import transaction
from apps.security.services.UserService import UserService
from core.utils.Validation import is_soy_sena_email, is_unique_email, validate_document_number, validate_phone_number
from apps.security.emails.SendEmails import enviar_registro_pendiente
from apps.security.entity.serializers.person.PersonSerializer import PersonSerializer
from core.utils.Validation import format_response
from apps.general.services.NotificationService import NotificationService


class PersonService(BaseService):
    def __init__(self):
        super().__init__(PersonRepository())


    def register_apprentice(self, data):
        try:
            from apps.general.services.AprendizService import AprendizService
            email = data.get('email')
            numero_identificacion = data.get('number_identification')
            phone_number = data.get('phone_number')
            if not is_soy_sena_email(email):
                return format_response('Solo se permiten correos institucionales (@soy.sena.edu.co)', success=False, type='invalid_email', status_code=400)
            if not is_unique_email(email, User):
                return format_response('El correo institucional ya está registrado.', success=False, type='email_exists', status_code=400)
            valid_doc, doc_msg = validate_document_number(numero_identificacion, Person)
            if not valid_doc:
                return format_response(doc_msg, success=False, type='invalid_document', status_code=400)
            if phone_number:
                valid_phone, phone_msg = validate_phone_number(phone_number)
                if not valid_phone:
                    return format_response(phone_msg, success=False, type='invalid_phone', status_code=400)

            # Transactional handling of data creation
            with transaction.atomic():
                # 1. Create person
                serializer = PersonSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                person = serializer.save()

                # 2. Create user using the create method of UserService
                user_data = {
                    'email': data['email'],
                    'password': 'temporal_placeholder',
                    'person_id': person.id,
                    'is_active': False,
                    'role_id': 2
                }
                user_result = UserService().create(user_data)
                if isinstance(user_result, dict) and user_result.get('status') == 'error':
                    raise Exception('No se pudo crear el usuario')
                user = user_result

                # 3. Create apprentice
                aprendiz_data = {
                    'person_id': person.id,
                    'ficha': None  # It will be assigned later
                }

                aprendiz_result = AprendizService().create(aprendiz_data)
                if isinstance(aprendiz_result, dict) and aprendiz_result.get('status') == 'error':
                    raise Exception('No se pudo crear el aprendiz')
                aprendiz = aprendiz_result

                # Notificar a los administradores del registro del aprendiz
                try:
                    
                    NotificationService().notify_registration(aprendiz)
                except Exception as e:
                    print(f"[PersonService] No se pudo notificar a los administradores: {str(e)}")

                # 4. Send pending registration email
                fecha_registro = datetime.now().strftime('%d/%m/%Y')
                enviar_registro_pendiente(data['email'], person.first_name + ' ' + person.first_last_name, fecha_registro)

                # 5. Serialize user for the response
                user_serializer = UserSerializer(user)

                return format_response(
                    'Usuario registrado correctamente. Tu cuenta está pendiente de activación por un administrador.',
                    success=True,
                    type='register_apprentice',
                    status_code=201
                )
        except Exception as e:
            return format_response(str(e), success=False, type='register_apprentice', status_code=400)
