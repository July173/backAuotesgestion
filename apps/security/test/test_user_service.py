import time
from django.test import TestCase
from unittest.mock import patch, MagicMock
from apps.security.services.UserService import UserService
from rest_framework import status
import datetime
from apps.security.entity.models import User


class SendLogin2FACodeTest(TestCase):
    
    # Test para x
    @patch('apps.security.services.UserService.enviar_codigo_verificacion_2fa')
    @patch('apps.security.services.UserService.timezone')
    @patch('apps.security.services.UserService.get_random_string', return_value='123456')
    def test_send_login_2fa_code_success(self, mock_get_random_string, mock_timezone, mock_enviar_2fa):
        start = time.time()
        # Preparar mocks
        fake_now = datetime.datetime(2025, 1, 1, 12, 0)
        mock_timezone.now.return_value = fake_now
        # Instanciar usuario simulado
        user = MagicMock()
        user.person = MagicMock()
        user.person.first_name = 'Juan'
        user.email = 'juan@soy.sena.edu.co'
        # Instanciar servicio
        service = UserService()
        # Ejecutar método
        response = service.send_login_2fa_code(user)
        # Verificar que se asignó el código y expiración
        self.assertEqual(user.login_code, '123456')
        self.assertTrue(user.login_code_expiration is not None)
        self.assertFalse(user.login_code_used)
        user.save.assert_called_once()
        # Verificar que se llamó a enviar_codigo_verificacion_2fa
        mock_enviar_2fa.assert_called_once()
        args, kwargs = mock_enviar_2fa.call_args
        self.assertEqual(args[0], user.email)
        self.assertEqual(args[1], 'Juan')
        self.assertEqual(args[2], '123456')
        self.assertIsInstance(args[3], str)
        # Verificar respuesta
        self.assertEqual(response['status'], status.HTTP_200_OK)
        self.assertIn('Código de verificación enviado', response['data']['success'])
        end = time.time()
        print(f"Tiempo de ejecución test_send_login_2fa_code_success: {end - start:.4f} segundos")

# Se ejecuta el test con

# para todos los tests de este archivo
# python manage.py test apps.security.test.User.test_user_service.SendLogin2FACodeTest

# para un test específico
# python manage.py test apps.security.test.User.test_user_service.SendLogin2FACodeTest.test_send_login_2fa_code_success

class ValidateInstitutionalLoginTest(TestCase):
    
    # Test para login con correo no institucional
    @patch('apps.security.services.UserService.is_soy_sena_email', return_value=False)
    @patch('apps.security.services.UserService.is_sena_email', return_value=False)
    def test_login_non_institutional_email(self, mock_sena_email, mock_soy_sena_email):
        start = time.time()
        service = UserService()
        response = service.validate_institutional_login('test@gmail.com', 'password123')
        self.assertEqual(response['status'], 400)
        self.assertIn('Solo se permiten correos institucionales', response['data']['error'])
        end = time.time()
        print(f"Tiempo de ejecución test_login_non_institutional_email: {end - start:.4f} segundos")

    # Test para login con contraseña corta
    def test_login_short_password(self):
        start = time.time()
        service = UserService()
        with patch('apps.security.services.UserService.is_soy_sena_email', return_value=True), \
             patch('apps.security.services.UserService.is_sena_email', return_value=True):
            response = service.validate_institutional_login('test@soy.sena.edu.co', 'short')
            self.assertEqual(response['status'], 400)
            self.assertIn('La contraseña debe tener al menos 8 caracteres', response['data']['error'])
        end = time.time()
        print(f"Tiempo de ejecución test_login_short_password: {end - start:.4f} segundos")

    # Test para login con credenciales inválidas
    @patch('apps.security.services.UserService.authenticate', return_value=None)
    @patch('apps.security.services.UserService.is_soy_sena_email', return_value=True)
    @patch('apps.security.services.UserService.is_sena_email', return_value=True)
    def test_login_invalid_credentials(self, mock_sena_email, mock_soy_sena_email, mock_auth):
        start = time.time()
        service = UserService()
        response = service.validate_institutional_login('test@soy.sena.edu.co', 'password123')
        self.assertEqual(response['status'], 401)
        self.assertIn('Credenciales inválidas', response['data']['error'])
        end = time.time()
        print(f"Tiempo de ejecución test_login_invalid_credentials: {end - start:.4f} segundos")

    # Test para login exitoso
    @patch.object(UserService, 'send_login_2fa_code')
    @patch('apps.security.services.UserService.authenticate')
    @patch('apps.security.services.UserService.is_soy_sena_email', return_value=True)
    @patch('apps.security.services.UserService.is_sena_email', return_value=True)
    def test_login_success(self, mock_sena_email, mock_soy_sena_email, mock_auth, mock_send_2fa):
        start = time.time()
        service = UserService()
        user_mock = MagicMock()
        mock_auth.return_value = user_mock
        mock_send_2fa.return_value = {
            'data': {'success': 'Código de verificación enviado al correo institucional.'},
            'status': 200
        }
        response = service.validate_institutional_login('test@soy.sena.edu.co', 'password123')
        self.assertEqual(response['status'], 200)
        self.assertIn('Código de verificación enviado', response['data']['success'])
        mock_send_2fa.assert_called_once_with(user_mock)
        end = time.time()
        print(f"Tiempo de ejecución test_login_success: {end - start:.4f} segundos")

# Se ejecuta el test con

# para todos los tests de este archivo
# python manage.py test apps.security.test.User.test_user_service.ValidateInstitutionalLoginTest

# para un test específico
# python manage.py test apps.security.test.User.test_user_service.ValidateInstitutionalLoginTest.test_login_non_institutional_email
# python manage.py test apps.security.test.User.test_user_service.ValidateInstitutionalLoginTest.test_login_short_password
# python manage.py test apps.security.test.User.test_user_service.ValidateInstitutionalLoginTest.test_login_invalid_credentials
# python manage.py test apps.security.test.User.test_user_service.ValidateInstitutionalLoginTest.test_login_success




class Validate2FACodeTest(TestCase):
    
    # Test para usuario no encontrado
    def test_user_not_found(self):
        start = time.time()
        with patch.object(User.objects, 'get', side_effect=User.DoesNotExist):
            service = UserService()
            response = service.validate_2fa_code('no@correo.com', '123456')
            self.assertEqual(response['status'], status.HTTP_404_NOT_FOUND)
            self.assertIn('No existe un usuario', response['data']['error'])
        end = time.time()
        print(f"Tiempo de ejecución test_user_not_found: {end - start:.4f} segundos")

    # Test para código incorrecto
    @patch('apps.security.services.UserService.User')
    @patch('apps.security.services.UserService.timezone')
    def test_code_incorrect(self, mock_timezone, mock_user_model):
        start = time.time()
        user = MagicMock()
        user.login_code = '654321'
        user.login_code_expiration = mock_timezone.now.return_value + datetime.timedelta(minutes=5)
        user.login_code_used = False
        mock_user_model.objects.get.return_value = user
        service = UserService()
        response = service.validate_2fa_code('test@correo.com', '123456')
        self.assertEqual(response['status'], status.HTTP_400_BAD_REQUEST)
        self.assertIn('incorrecto', response['data']['error'])
        end = time.time()
        print(f"Tiempo de ejecución test_code_incorrect: {end - start:.4f} segundos")

    # Test para código expirado
    @patch('apps.security.services.UserService.User')
    @patch('apps.security.services.UserService.timezone')
    def test_code_expired(self, mock_timezone, mock_user_model):
        start = time.time()
        now = datetime.datetime(2025, 1, 1, 12, 0)
        mock_timezone.now.return_value = now
        user = MagicMock()
        user.login_code = '123456'
        user.login_code_expiration = now - datetime.timedelta(minutes=1)
        user.login_code_used = False
        mock_user_model.objects.get.return_value = user
        service = UserService()
        response = service.validate_2fa_code('test@correo.com', '123456')
        self.assertEqual(response['status'], status.HTTP_400_BAD_REQUEST)
        self.assertIn('ha expirado', response['data']['error'])
        end = time.time()
        print(f"Tiempo de ejecución test_code_expired: {end - start:.4f} segundos")

    # Test para código ya usado
    @patch('apps.security.services.UserService.User')
    @patch('apps.security.services.UserService.timezone')
    def test_code_already_used(self, mock_timezone, mock_user_model):
        start = time.time()
        now = datetime.datetime(2025, 1, 1, 12, 0)
        mock_timezone.now.return_value = now
        user = MagicMock()
        user.login_code = '123456'
        user.login_code_expiration = now + datetime.timedelta(minutes=5)
        user.login_code_used = True
        mock_user_model.objects.get.return_value = user
        service = UserService()
        response = service.validate_2fa_code('test@correo.com', '123456')
        self.assertEqual(response['status'], status.HTTP_400_BAD_REQUEST)
        self.assertIn('ya fue usado', response['data']['error'])
        end = time.time()
        print(f"Tiempo de ejecución test_code_already_used: {end - start:.4f} segundos")

    # Test para código correcto
    @patch('apps.security.services.UserService.RefreshToken')
    @patch('apps.security.services.UserService.User')
    @patch('apps.security.services.UserService.timezone')
    def test_code_success(self, mock_timezone, mock_user_model, mock_refresh_token):
        start = time.time()
        now = datetime.datetime(2025, 1, 1, 12, 0)
        mock_timezone.now.return_value = now
        user = MagicMock()
        user.login_code = '123456'
        user.login_code_expiration = now + datetime.timedelta(minutes=5)
        user.login_code_used = False
        user.email = 'test@correo.com'
        user.id = 1
        user.role = MagicMock()
        user.role.id = 2
        user.person = MagicMock()
        user.person.id = 3
        user.registered = True
        mock_user_model.objects.get.return_value = user
        mock_refresh = MagicMock()
        mock_refresh.access_token = 'access'
        mock_refresh.__str__.return_value = 'refresh'
        mock_refresh_token.for_user.return_value = mock_refresh
        service = UserService()
        response = service.validate_2fa_code('test@correo.com', '123456')
        self.assertEqual(response['status'], status.HTTP_200_OK)
        self.assertIn('Autenticación 2FA exitosa', response['data']['success'])
        self.assertEqual(response['data']['user']['email'], 'test@correo.com')
        self.assertEqual(response['data']['user']['id'], 1)
        self.assertEqual(response['data']['user']['role'], 2)
        self.assertEqual(response['data']['user']['person'], 3)
        self.assertTrue(response['data']['user']['registered'])
        end = time.time()
        print(f"Tiempo de ejecución test_code_success: {end - start:.4f} segundos")

# Se ejecuta el test con

# para todos los tests de este archivo
# python manage.py test apps.security.test.User.test_user_service.Validate2FACodeTest

# para un test específico
# python manage.py test apps.security.test.User.test_user_service.Validate2FACodeTest.test_user_not_found
# python manage.py test apps.security.test.User.test_user_service.Validate2FACodeTest.test_code_incorrect
# python manage.py test apps.security.test.User.test_user_service.Validate2FACodeTest.test_code_expired
# python manage.py test apps.security.test.User.test_user_service.Validate2FACodeTest.test_code_already_used
# python manage.py test apps.security.test.User.test_user_service.Validate2FACodeTest.test_code_success