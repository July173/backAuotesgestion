from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.AprendizRepository import AprendizRepository
from apps.security.entity.models import User, Role, Person
from apps.general.entity.models import Apprentice, Ficha
from apps.security.emails.CreacionCuentaUsers import send_account_created_email
from django.db import transaction
from django.db import models
from core.utils.Validation import format_response, is_unique_email, validate_document_number, validate_phone_number
from apps.security.entity.models.DocumentType import DocumentType
from django.utils.crypto import get_random_string
from core.utils.Validation import is_soy_sena_email
from apps.security.services.UserService import UserService
from apps.general.services.NotificationService import NotificationService


class AprendizService(BaseService):

    def __init__(self):
        self.repository = AprendizRepository()

    def create_apprentice(self, validated_data):
        try:
            from apps.security.services.PersonService import PersonService
            email = validated_data.get('email')
            numero_identificacion = validated_data.get('number_identification')
            phone_number = validated_data.get('phone_number')
            ficha_id = validated_data.get('ficha_id')
            first_name = validated_data.get('first_name')
            first_last_name = validated_data.get('first_last_name')
            second_name = validated_data.get('second_name', '')
            second_last_name = validated_data.get('second_last_name', '')
            type_identification = validated_data.get('type_identification')

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

            with transaction.atomic():
                # 1. Create person
                person_data = {
                    'type_identification_id': type_identification,
                    'number_identification': numero_identificacion,
                    'first_name': first_name,
                    'second_name': second_name,
                    'first_last_name': first_last_name,
                    'second_last_name': second_last_name,
                    'phone_number': phone_number,
                }
                person = PersonService().create(person_data)

                # 2. Create user
                password_temporal = str(numero_identificacion) + get_random_string(length=2)
                user_data = {
                    'email': email,
                    'password': password_temporal,
                    'person_id': person.id,
                    'is_active': True,
                    'registered': False,
                    'role_id': 2
                }
                user = UserService().create(user_data)

                # 3. Create apprentice
                ficha = Ficha.objects.get(pk=ficha_id)
                aprendiz = Apprentice.objects.create(person=person, ficha=ficha, active=True)

                # 4. Send welcome email
                try:
                    full_name = f"{first_name} {first_last_name}"
                    send_account_created_email(email, full_name, password_temporal)
                except Exception as e:
                    print(f"[AprendizService] No se pudo enviar el correo de registro al aprendiz: {str(e)}")



                return format_response(
                    f"Aprendiz registrado exitosamente. Email: {user.email}",
                    success=True,
                    type='register_apprentice',
                    status_code=201
                )
        except Exception as e:
            return format_response(str(e), success=False, type='register_apprentice', status_code=400)


    def update_aprendiz(self, aprendiz_id, validated_data):
        """
        Actualiza los datos de aprendiz, usuario y persona. Valida datos y roles.
        """
        
        # Validar y obtener el ID del tipo de documento
        type_identification = validated_data.get('type_identification')
        if type_identification:
            if isinstance(type_identification, int):
                # Si viene como ID, verificar que exista
                if not DocumentType.objects.filter(pk=type_identification, active=True).exists():
                    raise ValueError('Tipo de identificación inválido')
            else:
                # Si viene como string (acronym o name), buscar el ID
                doc_type = DocumentType.objects.filter(
                    models.Q(acronyms=type_identification) | models.Q(name=type_identification),
                    active=True
                ).first()
                if not doc_type:
                    raise ValueError('Tipo de identificación inválido')
                type_identification = doc_type.id
        
        # Construcción de datos de persona
        person_data = {
            'type_identification_id': type_identification,  # Usar _id para el campo ForeignKey
            'number_identification': validated_data['number_identification'],
            'first_name': validated_data['first_name'],
            'second_name': validated_data.get('second_name', ''),
            'first_last_name': validated_data['first_last_name'],
            'second_last_name': validated_data.get('second_last_name', ''),
            'phone_number': validated_data.get('phone_number', ''),
        }
        # Construcción de datos de usuario
        user_data = {
            'email': validated_data['email'],
        }
        ficha_id = validated_data.get('ficha_id', validated_data.get('ficha'))
        role_id = validated_data.get('role_id', validated_data.get('role'))

        aprendiz = Apprentice.objects.get(pk=aprendiz_id)
        # Validación de correo institucional
        if not user_data['email'] or not is_soy_sena_email(user_data['email']):
            raise ValueError('Solo se permiten correos institucionales (@soy.sena.edu.co) para aprendices.')
        # Obtener el usuario usando la relación con la persona
        user = User.objects.filter(person=aprendiz.person).first()
        # Validaciones de unicidad y formato
        if not is_unique_email(user_data['email'], User, exclude_user_id=user.id if user else None):
            raise ValueError('El correo ya está registrado.')
        if not validate_document_number(person_data['number_identification'], Person, exclude_person_id=aprendiz.person.id):
            raise ValueError('El número de documento ya está registrado.')
        if person_data['phone_number'] and not validate_phone_number(person_data['phone_number']):
            raise ValueError('El número de teléfono debe tener exactamente 10 dígitos.')

        with transaction.atomic():
            # Actualiza ficha y rol
            aprendiz = Apprentice.objects.get(pk=aprendiz_id)
            ficha = Ficha.objects.get(pk=ficha_id)
            if not role_id:
                role_id = 2
            try:
                role = Role.objects.get(pk=role_id)
                user_data['role_id'] = role.id
            except Role.DoesNotExist:
                user_data['role_id'] = 2
            self.repository.update_all_dates_apprentice(aprendiz, person_data, user_data, ficha)
            return aprendiz
    
    def list_aprendices(self):
        """
        Lista todos los aprendices.
        """
        return Apprentice.objects.all()
