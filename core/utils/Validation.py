import random
import string


def validate_document_number(value, person_model, exclude_person_id=None):
	"""Valida el número de identificación. Retorna True si es válido, False si no, y un string con el mensaje de error."""
	if not isinstance(value, int):
		return False, "El número de identificación debe ser un número entero."
	length = len(str(abs(value)))
	if not (8 <= length <= 10):
		return False, "El número de identificación debe tener entre 8 y 10 dígitos numéricos."
	queryset = person_model.objects.filter(number_identification=value)
	if exclude_person_id:
		queryset = queryset.exclude(id=exclude_person_id)
	if queryset.exists():
		return False, "El número de documento ya está registrado."
	return True, None

def is_soy_sena_email(email):
	"""Checks if the email ends with @soy.sena.edu.co."""
	if not email:
		return False
	return email.endswith('@soy.sena.edu.co')

def is_sena_email(email):
	"""Checks if the email ends with @sena.edu.co."""
	if not email:
		return False
	return email.endswith('@sena.edu.co')

def is_unique_email(email, user_model, exclude_user_id=None):
	"""Checks that the email is unique in the given model. Can exclude a user by id (for updates)."""
	if not email:
		return False
	queryset = user_model.objects.filter(email=email)
	if exclude_user_id:
		queryset = queryset.exclude(id=exclude_user_id)
	return not queryset.exists()

def validate_phone_number(value):
	"""Valida el número de teléfono. Retorna True si es válido, False si no, y un string con el mensaje de error."""
	if not isinstance(value, int):
		return False, "El número de teléfono debe ser un número entero."
	length = len(str(abs(value)))
	if length != 10:
		return False, "El número de teléfono debe tener exactamente 10 dígitos numéricos."
	return True, None


def format_response(message, success=True, type="info", status_code=200):
	"""
	Returns a standardized response dict for both success and error cases.
	- message: The main message (string, exception, dict, etc.)
	- success: True for success, False for error
	- type: Custom type or code for the response
	- status_code: HTTP status code (default 200 for success, 400 for error)
	"""
	# Clean up message if it's an exception or complex object
	msg = message
	if isinstance(message, dict) and 'detail' in message:
		msg = message['detail']
	elif hasattr(message, 'detail'):
		msg = message.detail
	elif hasattr(message, 'args') and len(message.args) > 0:
		msg = message.args[0]
	if isinstance(msg, (list, tuple)) and len(msg) > 0:
		msg = msg[0]
	# Si es ErrorDetail o similar, conviértelo a string plano
	try:
		from rest_framework.exceptions import ErrorDetail
		if isinstance(msg, ErrorDetail):
			msg = str(msg)
	except ImportError:
		pass
	if hasattr(msg, 'code'):
		msg = str(msg)
	return {
		"detail": str(msg),
		"type": type,
		"status": "success" if success else "error",
		"status_code": status_code
	}