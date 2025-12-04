from rest_framework import serializers

class FormPDFSerializer(serializers.Serializer):
    """
    Serializer for uploading PDF files only.
    """
    pdf_file = serializers.FileField(help_text="Archivo PDF de la solicitud")  # User-facing help text remains in Spanish

