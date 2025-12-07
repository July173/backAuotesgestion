from rest_framework import serializers

class VisitFollowingPDFOnlySerializer(serializers.Serializer):
    pdf_report = serializers.FileField(help_text="Archivo PDF del reporte de visita")
