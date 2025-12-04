from apps.general.entity.models.PersonSede import PersonSede
from apps.security.services.PersonService import PersonService
from apps.security.services.UserService import UserService
from apps.security.entity.models.DocumentType import DocumentType
from core.base.services.implements.baseService.BaseService import BaseService
from apps.general.repositories.InstructorRepository import InstructorRepository
from django.db import transaction
from apps.general.entity.models import Sede, KnowledgeArea, TypeContract
from apps.security.entity.models import User, Person
from apps.general.entity.models import Instructor
from core.utils.Validation import is_unique_email, validate_document_number, validate_phone_number, format_response
from core.utils.Validation import is_sena_email
from apps.security.emails.CreacionCuentaUsers import send_account_created_email
from django.utils.crypto import get_random_string
from apps.assign.entity.models import AsignationInstructor
from django.db import transaction
from django.db.models import F



class InstructorService(BaseService):
    def get_asignations(self, instructor_id):
        return AsignationInstructor.objects.filter(instructor_id=instructor_id)

    def update_learners_fields(self, instructor_id, assigned_learners=None, max_assigned_learners=None):
        instructor = Instructor.objects.filter(pk=instructor_id).first()
        if not instructor:
            return None
        # Validación: assigned_learners never less than 0 and not exceed max limit
        if assigned_learners is not None:
            if assigned_learners < 0:
                raise ValueError('El número de aprendices asignados no puede ser menor que 0.')
            # Validación: no exceed max limit
            max_limit = max_assigned_learners if max_assigned_learners is not None else instructor.max_assigned_learners or 80
            if assigned_learners > max_limit:
                raise ValueError('El número de aprendices asignados no puede superar el límite máximo.')
            instructor.assigned_learners = assigned_learners
        if max_assigned_learners is not None:
            if max_assigned_learners < 0:
                raise ValueError('El límite máximo no puede ser menor que 0.')
            instructor.max_assigned_learners = max_assigned_learners
            # if assigned_learners exceeds new max, adjust it
            if instructor.assigned_learners is not None and instructor.assigned_learners > max_assigned_learners:
                instructor.assigned_learners = max_assigned_learners
        instructor.save()
        return instructor

    def increment_assigned_learners(self, instructor_id, delta=1):
        """Incrementa assigned_learners de forma atómica y valida límites."""
        with transaction.atomic():
            inst = Instructor.objects.select_for_update().filter(pk=instructor_id).first()
            if not inst:
                return None
            current = inst.assigned_learners or 0
            max_limit = inst.max_assigned_learners or 80
            if current + delta > max_limit:
                raise ValueError('El número de aprendices asignados no puede superar el límite máximo.')
            inst.assigned_learners = current + delta
            inst.save()
            return inst

    def decrement_assigned_learners(self, instructor_id, delta=1):
        """Decrementa assigned_learners de forma atómica y evita valores negativos."""
        with transaction.atomic():
            inst = Instructor.objects.select_for_update().filter(pk=instructor_id).first()
            if not inst:
                return None
            current = inst.assigned_learners or 0
            new_val = max(current - delta, 0)
            inst.assigned_learners = new_val
            inst.save()
            return inst

    def __init__(self):
        self.repository = InstructorRepository()

    def list_instructors(self):
        """
        Devuelve todos los instructores.
        """
        return Instructor.objects.all()


    def create_instructor(self, person_data, user_data, instructor_data, sede_id):
        try:
            # Validations before transaction
            email = user_data.get('email')
            numero_identificacion = person_data.get('number_identification')
            phone_number = person_data.get('phone_number')
            contract_type_id = instructor_data.get('contract_type_id') or instructor_data.get('contract_type')
            knowledge_area_id = instructor_data.get('knowledge_area_id') or instructor_data.get('knowledge_area')

            if not is_sena_email(email):
                return format_response('Solo se permiten correos institucionales (@sena.edu.co) para instructores.', success=False, type='invalid_email', status_code=400)
            if not is_unique_email(email, User):
                return format_response('El correo institucional ya está registrado.', success=False, type='email_exists', status_code=400)
            valid_doc, doc_msg = validate_document_number(numero_identificacion, Person)
            if not valid_doc:
                return format_response(doc_msg, success=False, type='invalid_document', status_code=400)
            if phone_number:
                valid_phone, phone_msg = validate_phone_number(phone_number)
                if not valid_phone:
                    return format_response(phone_msg, success=False, type='invalid_phone', status_code=400)

            if not contract_type_id:
                return format_response('El tipo de contrato es obligatorio.', success=False, type='invalid_contract_type', status_code=400)
            if not knowledge_area_id:
                return format_response('El área de conocimiento es obligatoria.', success=False, type='invalid_knowledge_area', status_code=400)
            try:
                sede = Sede.objects.get(pk=sede_id)
            except Sede.DoesNotExist:
                return format_response('La sede proporcionada no existe.', success=False, type='invalid_sede', status_code=400)
            try:
                contract_type = TypeContract.objects.get(pk=contract_type_id)
            except Exception:
                return format_response('El tipo de contrato proporcionado no existe.', success=False, type='invalid_contract_type', status_code=400)
            try:
                knowledge_area = KnowledgeArea.objects.get(pk=knowledge_area_id)
            except Exception:
                return format_response('El área de conocimiento proporcionada no existe.', success=False, type='invalid_knowledge_area', status_code=400)


            # Validar fechas de contrato
            fecha_inicio = instructor_data.get('contract_start_date')
            fecha_fin = instructor_data.get('contract_end_date')
            if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
                return format_response('La fecha de fin de contrato no puede ser anterior a la fecha de inicio.', success=False, type='invalid_contract_dates', status_code=400)

            # Validate TypeIdentification
            type_id = person_data.get('type_identification')
            if type_id and not isinstance(type_id, DocumentType):
                person_data['type_identification'] = DocumentType.objects.get(pk=type_id)

            #Transactional handling of data creation
            with transaction.atomic():
                # 1. Create person
                person = PersonService().create(person_data)
                if isinstance(person, dict) and person.get('status') == 'error':
                    raise Exception(person.get('message', 'No se pudo crear la persona'))

                user_data['person_id'] = person.id

                # 2. Create user
                # Activate user automatically
                user_data['is_active'] = True
                # Allow dynamic role
                if 'role_id' not in user_data:
                    return format_response('El rol es obligatorio.', success=False, type='invalid_role', status_code=400)
                # Hash the password using the identification number
                identification_number = str(person_data.get('number_identification'))
                temp_suffix = get_random_string(length=2)
                temp_password = identification_number + temp_suffix
                user_data['password'] = temp_password

                user = UserService().create(user_data)
                if isinstance(user, dict) and user.get('status') == 'error':
                    raise Exception(user.get('message', 'No se pudo crear el usuario'))
                # Asegurar que el campo registered quede en False
                user.registered = False
                user.save()

                # 3. Create instructor
                instructor_data['person'] = person
                instructor_data['contract_type'] = contract_type
                instructor_data['knowledge_area'] = knowledge_area
                instructor = Instructor.objects.create(**instructor_data)

                # 4. Create PersonSede association
                PersonSede.objects.create(person=person, sede=sede)

                # 5. Send account creation email to instructor
                full_name = f"{person.first_name} {person.first_last_name}"
                send_account_created_email(user.email, full_name, temp_password)
                # 6. Serialize response
                return format_response(
                    "Instructor registrado correctamente.",
                    success=True,
                    type='register_instructor',
                    status_code=201
                )
        except Exception as e:
            return format_response(str(e), success=False, type='register_instructor', status_code=400)

    def update_instructor(self, instructor_id, person_data, user_data, instructor_data, sede_id):
        try:
            # Validaciones previas 
            instructor = Instructor.objects.select_related('person').get(pk=instructor_id)
            person = instructor.person
            user = User.objects.filter(person=person).first()

            email = user_data.get('email')
            numero_identificacion = person_data.get('number_identification')
            phone_number = person_data.get('phone_number')
            contract_type_id = instructor_data.get('contract_type_id') or instructor_data.get('contract_type')
            knowledge_area_id = instructor_data.get('knowledge_area_id') or instructor_data.get('knowledge_area')

            if not is_sena_email(email):
                return format_response('Solo se permiten correos institucionales (@sena.edu.co) para instructores.', success=False, type='invalid_email', status_code=400)
            if not is_unique_email(email, User, exclude_user_id=user.id if user else None):
                return format_response('El correo institucional ya está registrado.', success=False, type='email_exists', status_code=400)
            valid_doc, doc_msg = validate_document_number(numero_identificacion, Person, exclude_person_id=person.id)
            if not valid_doc:
                return format_response(doc_msg, success=False, type='invalid_document', status_code=400)
            if phone_number:
                valid_phone, phone_msg = validate_phone_number(phone_number)
                if not valid_phone:
                    return format_response(phone_msg, success=False, type='invalid_phone', status_code=400)

            if not contract_type_id:
                return format_response('El tipo de contrato es obligatorio.', success=False, type='invalid_contract_type', status_code=400)
            if not knowledge_area_id:
                return format_response('El área de conocimiento es obligatoria.', success=False, type='invalid_knowledge_area', status_code=400)
            try:
                sede = Sede.objects.get(pk=sede_id)
            except Sede.DoesNotExist:
                return format_response('La sede proporcionada no existe.', success=False, type='invalid_sede', status_code=400)
            try:
                contract_type = TypeContract.objects.get(pk=contract_type_id)
            except Exception:
                return format_response('El tipo de contrato proporcionado no existe.', success=False, type='invalid_contract_type', status_code=400)
            try:
                knowledge_area = KnowledgeArea.objects.get(pk=knowledge_area_id)
            except Exception:
                return format_response('El área de conocimiento proporcionada no existe.', success=False, type='invalid_knowledge_area', status_code=400)

            # Validar y actualizar type_identification
            type_id = person_data.get('type_identification')
            if type_id and not isinstance(type_id, DocumentType):
                person_data['type_identification'] = DocumentType.objects.get(pk=type_id)

            with transaction.atomic():
                # Actualizar campos de Person
                for attr, value in person_data.items():
                    setattr(person, attr, value)
                person.save()

                # Actualizar campos de User
                if user:
                    for attr, value in user_data.items():
                        setattr(user, attr, value)
                    user.save()

                # Actualizar campos de Instructor
                instructor_data['contract_type'] = contract_type
                instructor_data['knowledge_area'] = knowledge_area
                for attr, value in instructor_data.items():
                    setattr(instructor, attr, value)
                instructor.save()

                # Actualizar PersonSede
                from apps.general.entity.models import PersonSede
                person_sede = PersonSede.objects.filter(person=person).first()
                if person_sede:
                    person_sede.sede = sede
                    person_sede.save()

                return format_response(
                    "Instructor actualizado correctamente.",
                    success=True,
                    type='update_instructor',
                    status_code=200
                )
        except Exception as e:
            return format_response(str(e), success=False, type='update_instructor', status_code=400)
