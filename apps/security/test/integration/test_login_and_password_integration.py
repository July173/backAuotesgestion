from rest_framework.test import APITestCase
from unittest.mock import patch
from apps.security.entity.models import User, Person, Role
from apps.security.entity.models.DocumentType import DocumentType
from django.utils import timezone


class BaseIntegrationSetup(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.doc_type = DocumentType.objects.create(name='Cédula', acronyms='CC', active=True)
        cls.role = Role.objects.create(type_role='apprentice', description='Aprendiz')
        cls.person = Person.objects.create(
            type_identification=cls.doc_type,
            first_name='Juan',
            first_last_name='Pérez',
            phone_number=3001234567,
            number_identification=12345678
        )
        cls.user = User.objects.create_user(
            email='test@soy.sena.edu.co',
            password='password123',
            person=cls.person,
            role=cls.role
        )


class PasswordResetRequestNonInstitutionalTest(BaseIntegrationSetup):
    def test_password_reset_request_non_institutional(self):
        url = '/api/security/users/request-password-reset/'
        data = {'email': 'someone@gmail.com'}
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('Solo se permiten correos institucionales', resp.data.get('error', ''))
        # Run this single test (PowerShell):
        # python manage.py test apps.security.test.integration.test_login_and_password_integration.PasswordResetRequestNonInstitutionalTest.test_password_reset_request_non_institutional -v 2


class PasswordResetFullFlowTest(BaseIntegrationSetup):
    @patch('django.core.mail.EmailMultiAlternatives.send')
    def test_password_reset_flow_and_login_with_new_password(self, mock_send):
        # Request reset code (send is mocked)
        req_url = '/api/security/users/request-password-reset/'
        data = {'email': 'test@soy.sena.edu.co'}
        resp = self.client.post(req_url, data, format='json')
        self.assertEqual(resp.status_code, 200)
        user = User.objects.get(email='test@soy.sena.edu.co')
        self.assertIsNotNone(user.reset_code)

        # Reset password using the endpoint
        reset_url = '/api/security/users/reset-password/'
        new_password = 'NewPassword123'
        resp2 = self.client.post(reset_url, {'email': user.email, 'new_password': new_password}, format='json')
        self.assertEqual(resp2.status_code, 200)

        # Now login with the new password (mock 2FA send to avoid email)
        with patch('apps.security.services.UserService.enviar_codigo_verificacion_2fa') as mock_2fa:
            login_url = '/api/security/users/validate-institutional-login/'
            resp3 = self.client.post(login_url, {'email': user.email, 'password': new_password}, format='json')
            self.assertEqual(resp3.status_code, 200)
            user.refresh_from_db()
            self.assertIsNotNone(user.login_code)
            mock_2fa.assert_called()
        # Run this single test (PowerShell):
        # python manage.py test apps.security.test.integration.test_login_and_password_integration.PasswordResetFullFlowTest.test_password_reset_flow_and_login_with_new_password -v 2
