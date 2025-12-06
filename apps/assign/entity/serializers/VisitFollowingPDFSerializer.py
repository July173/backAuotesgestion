from rest_framework import serializers

class VisitFollowingPDFSerializer(serializers.Serializer):
    """
    Serializer for uploading PDF report files to VisitFollowing.
    """
    pdf_file = serializers.FileField(help_text="Archivo PDF del reporte de visita")

