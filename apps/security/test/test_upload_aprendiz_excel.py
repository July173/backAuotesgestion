import io
import time
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from openpyxl import Workbook

@pytest.mark.django_db
def test_upload_aprendiz_excel_performance():
    """
    Prueba el endpoint de carga masiva de aprendices con datos simulados.
    No almacena datos reales, solo mide el tiempo de procesamiento y la respuesta.
    """
    client = APIClient()
    url = '/api/security/excel-templates/upload-aprendiz-excel/'

    # Crear archivo Excel usando la plantilla oficial del backend
    from apps.security.services.excel.ExcelAprendizTemplateService import ExcelAprendizTemplateService
    template_service = ExcelAprendizTemplateService()
    response = template_service.generate_aprendiz_template()
    # Obtener el archivo generado
    from openpyxl import load_workbook
    wb = load_workbook(io.BytesIO(response.content))
    ws = wb["Aprendices"]
    # Agregar 100 filas simuladas después de los encabezados
    for i in range(100):
        ws.append([
            'CC', f'2000{i}', f'Aprendiz{i}', '', f'Apellido{i}', '', f'aprendiz{i}@soy.sena.edu.co', f'301{i}'
        ])
    excel_bytes = io.BytesIO()
    wb.save(excel_bytes)
    excel_bytes.seek(0)
    from django.core.files.uploadedfile import SimpleUploadedFile
    excel_file = SimpleUploadedFile(
        "test_aprendiz.xlsx",
        excel_bytes.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Mock del envío de correo para evitar emails reales
    from unittest.mock import patch
    with patch('apps.security.services.excel.ExcelAprendizTemplateService.ExcelAprendizTemplateService._send_credentials_email', return_value=True):
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
