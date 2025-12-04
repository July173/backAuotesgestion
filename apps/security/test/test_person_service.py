from django.test import TestCase
from unittest.mock import patch, MagicMock
from apps.security.services.PersonService import PersonService
import time
from apps.security.entity.models.DocumentType import DocumentType


class RegisterApprenticeTest(TestCase):
    
    # Test para registro exitoso de aprendiz (solo pasa con correo válido)
    @patch('apps.general.services.AprendizService.AprendizService')
    @patch('apps.security.services.PersonService.enviar_registro_pendiente')
    @patch('apps.security.services.PersonService.PersonSerializer')
    @patch('apps.security.services.PersonService.UserService')
    @patch('apps.security.services.PersonService.validate_phone_number')
    @patch('apps.security.services.PersonService.validate_document_number')
    @patch('apps.security.services.PersonService.is_unique_email')
    @patch('apps.security.services.PersonService.is_soy_sena_email')
    def test_register_apprentice_success(
        self, mock_soy_sena_email, mock_unique_email, mock_validate_doc, mock_validate_phone,
        mock_user_service, mock_person_serializer, mock_enviar_email, mock_aprendiz_service
    ):
        # Crear tipo de identificación requerido en la base de datos de pruebas
        doc_type = DocumentType.objects.create(id=1, name='Cédula de Ciudadanía', acronyms='CC', active=True)

        # Configura los mocks para validar según el dato de entrada
        mock_soy_sena_email.side_effect = lambda email: email.endswith('@soy.sena.edu.co')
        mock_validate_doc.side_effect = lambda doc, model=None: (str(doc).isdigit() and len(str(doc)) >= 6, '')
        mock_validate_phone.side_effect = lambda phone: (str(phone).isdigit() and len(str(phone)) == 10, '')
        mock_unique_email.side_effect = lambda email, model=None: email != 'repetido@soy.sena.edu.co'
        start = time.time()
        data = {
            'email': 'test@soy.sena.edu.co',      # Correo válido (dominio institucional)
            'number_identification': 12345678,    # Documento válido (entero)
            'phone_number': 3001234567,           # Teléfono válido (entero)
            'type_identification': doc_type.id,   # Tipo de documento válido
            'first_name': 'Juan',
            'first_last_name': 'Pérez'
        }

        # Mock PersonSerializer
        person_instance = MagicMock()
        person_instance.id = 1
        person_instance.first_name = 'Juan'
        person_instance.first_last_name = 'Pérez'
        mock_person_serializer.return_value.is_valid.return_value = True
        mock_person_serializer.return_value.save.return_value = person_instance

        # Mock UserService
        user_instance = MagicMock()
        user_instance.id = 1
        user_instance.email = data['email']
        user_instance.person = person_instance
        mock_user_service.return_value.create.return_value = user_instance

        # Mock AprendizService
        aprendiz_instance = MagicMock()
        mock_aprendiz_service.return_value.create.return_value = aprendiz_instance


        service = PersonService()
        response = service.register_apprentice(data)
        print("RESPUESTA DEL SERVICIO:", response)
        # El servicio usa format_response y devuelve claves: 'detail','type','status','status_code'
        self.assertEqual(response['status'], 'success')
        self.assertEqual(response['status_code'], 201)
        self.assertEqual(response['type'], 'register_apprentice')
        self.assertIn('Usuario registrado correctamente', response['detail'])
        end = time.time()
        print(f"Tiempo de ejecución test_register_apprentice_success: {end - start:.4f} segundos")

    # Test para registro con email inválido
    def test_register_apprentice_invalid_email(self):
        start = time.time()
        # Crear tipo de identificación para que el flujo no dependa de su existencia
        doc_type = DocumentType.objects.create(id=1, name='Cédula de Ciudadanía', acronyms='CC', active=True)
        data = {
            'email': 'test@soy.sena.edu.co',
            'number_identification': 12345678,
            'phone_number': 3001234567,
            'type_identification': doc_type.id,
            'first_name': 'Juan',
            'first_last_name': 'Pérez'
        }
        service = PersonService()
        response = service.register_apprentice(data)

        # Esperamos que la validación real detecte el correo inválido
        self.assertEqual(response['status'], 'error')
        self.assertEqual(response['status_code'], 400)
        self.assertEqual(response['type'], 'invalid_email')
        self.assertIn('Solo se permiten correos institucionales', response['detail'])
        end = time.time()
        print(f"Tiempo de ejecución test_register_apprentice_invalid_email: {end - start:.4f} segundos")




# Se ejecuta el test con 

# para todos los tests de este archivo
# python manage.py test apps.security.test.test_person_service.RegisterApprenticeTest

# para un test específico
# python manage.py test apps.security.test.test_person_service.RegisterApprenticeTest.test_register_apprentice_success
# python manage.py test apps.security.test.test_person_service.RegisterApprenticeTest.test_register_apprentice_invalid_email