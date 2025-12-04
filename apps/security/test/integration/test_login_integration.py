from rest_framework.test import APITestCase
from unittest.mock import patch
from apps.security.entity.models import User, Person, Role
from apps.security.entity.models.DocumentType import DocumentType
from django.utils import timezone
import datetime


class LoginIntegrationTest(APITestCase):
    def setUp(self):
        # Crear datos necesarios: DocumentType, Role, Person y User
        self.doc_type = DocumentType.objects.create(name='Cédula', acronyms='CC', active=True)
        self.role = Role.objects.create(type_role='apprentice', description='Aprendiz')
        self.person = Person.objects.create(
            type_identification=self.doc_type,
            first_name='Juan',
            first_last_name='Pérez',
            phone_number=3001234567,
            number_identification=12345678
        )
        # Usuario institucional válido
        self.user = User.objects.create_user(
            email='test@soy.sena.edu.co',
            password='password123',
            person=self.person,
            role=self.role
        )

    def test_non_institutional_email_rejected(self):
        url = '/api/security/users/validate-institutional-login/'
        data = {'email': 'user@gmail.com', 'password': 'password123'}
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('Solo se permiten correos institucionales', resp.data.get('error', ''))
        # Run this single test (PowerShell):
        # python manage.py test apps.security.test.integration.test_login_integration.LoginIntegrationTest.test_non_institutional_email_rejected -v 2

    

    def test_invalid_credentials(self):
        url = '/api/security/users/validate-institutional-login/'
        data = {'email': 'test@soy.sena.edu.co', 'password': 'wrongpassword'}
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, 401)
        self.assertIn('Credenciales inválidas', resp.data.get('error', ''))
        # Run this single test (PowerShell):
        # python manage.py test apps.security.test.integration.test_login_integration.LoginIntegrationTest.test_invalid_credentials -v 2

    @patch('apps.security.services.UserService.enviar_codigo_verificacion_2fa')
    def test_full_login_flow_2fa(self, mock_send_email):
        """End-to-end: login -> server saves 2FA code -> validate 2FA returns tokens."""
        login_url = '/api/security/users/validate-institutional-login/'
        data = {'email': 'test@soy.sena.edu.co', 'password': 'password123'}
        resp = self.client.post(login_url, data, format='json')
        # Should succeed and trigger 2FA send (mocked)
        self.assertEqual(resp.status_code, 200)
        # Refresh user from DB to get login_code
        user = User.objects.get(email='test@soy.sena.edu.co')
        self.assertIsNotNone(user.login_code)

        # Now validate the 2FA code
        validate_url = '/api/security/users/validate-2fa-code/'
        data2 = {'email': user.email, 'code': user.login_code}
        resp2 = self.client.post(validate_url, data2, format='json')
        self.assertEqual(resp2.status_code, 200)
        self.assertIn('access', resp2.data)
        self.assertIn('refresh', resp2.data)
        # Run this single test (PowerShell):
        # python manage.py test apps.security.test.integration.test_login_integration.LoginIntegrationTest.test_full_login_flow_2fa -v 2


