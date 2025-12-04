import io
import time
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from openpyxl import Workbook

@pytest.mark.django_db
def test_upload_instructor_excel_performance():
    """
    Prueba el endpoint de carga masiva de instructores con datos simulados.
    No almacena datos reales, solo mide el tiempo de procesamiento y la respuesta.
    """
    client = APIClient()
    url = '/api/security/excel-templates/upload-instructor-excel/'

    # Crear archivo Excel usando la plantilla oficial del backend
    from apps.security.services.excel.ExcelInstructorTemplateService import ExcelInstructorTemplateService
    template_service = ExcelInstructorTemplateService()
    response = template_service.generate_instructor_template()
    # Obtener el archivo generado
    from openpyxl import load_workbook
    wb = load_workbook(io.BytesIO(response.content))
    ws = wb["Instructores"]
    # Agregar 100 filas simuladas después de los encabezados
    for i in range(100):
        ws.append([
            'CC', f'1000{i}', f'Nombre{i}', '', f'Apellido{i}', '', f'instructor{i}@sena.edu.co', f'300{i}',
            'Tecnologías de la Información', 'Planta', '2025-01-01', '2025-12-31', 'Huila', 'Centro', 'Sede'
        ])
    excel_bytes = io.BytesIO()
    wb.save(excel_bytes)
    excel_bytes.seek(0)
    from django.core.files.uploadedfile import SimpleUploadedFile
    excel_file = SimpleUploadedFile(
        "test_instructor.xlsx",
        excel_bytes.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Mock del envío de correo para evitar emails reales
    from unittest.mock import patch
    with patch('apps.security.services.excel.ExcelInstructorTemplateService.ExcelInstructorTemplateService._send_credentials_email', return_value=True):
        start = time.time()
        response = client.post(
            url,
            {'file': excel_file},
            format='multipart'
        )
        end = time.time()

    # Verificar respuesta y tiempo
    assert response.status_code in [201, 207]
    print(f"Procesamiento de 1000 filas demoró: {end - start:.2f} segundos")
    print("Resumen de respuesta:", response.json())
