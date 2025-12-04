from rest_framework.test import APITestCase
from django.urls import reverse


class CreateFormRequestInvalidPayloadTest(APITestCase):
    def test_create_form_request_invalid_payload_returns_400(self):
        url = '/api/assign/request_asignation/form-request/'
        # Send an empty payload which should fail serializer validation
        resp = self.client.post(url, {}, format='json')
        self.assertEqual(resp.status_code, 400)
        # Run this single test (PowerShell):
        # python manage.py test apps.assign.test.integration.test_request_asignation_integration.CreateFormRequestInvalidPayloadTest.test_create_form_request_invalid_payload_returns_400 -v 2



class GetPdfUrlNotFoundTest(APITestCase):
    def test_get_pdf_url_nonexistent_returns_404(self):
        url = '/api/assign/request_asignation/9999/form-request-pdf-url/'
        resp = self.client.get(url, format='json')
        self.assertEqual(resp.status_code, 404)
        # Run this single test (PowerShell):
        # python manage.py test apps.assign.test.integration.test_request_asignation_integration.GetPdfUrlNotFoundTest.test_get_pdf_url_nonexistent_returns_404 -v 2


class AprendizDashboardMissingParamTest(APITestCase):
    def test_aprendiz_dashboard_missing_param_returns_400(self):
        url = '/api/assign/request_asignation/aprendiz-dashboard/'
        resp = self.client.get(url, format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('Se requiere el ID del aprendiz', resp.data.get('message', ''))
        # Run this single test (PowerShell):
        # python manage.py test apps.assign.test.integration.test_request_asignation_integration.AprendizDashboardMissingParamTest.test_aprendiz_dashboard_missing_param_returns_400 -v 2
