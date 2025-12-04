from rest_framework import serializers
from apps.assign.entity.models import RequestAsignation


from apps.security.entity.models import User

class RequestAsignationDashboardSerializer(serializers.ModelSerializer):


    instructor_id = serializers.SerializerMethodField()
    instructor_first_name = serializers.SerializerMethodField()
    instructor_second_name = serializers.SerializerMethodField()
    instructor_first_last_name = serializers.SerializerMethodField()
    instructor_second_last_name = serializers.SerializerMethodField()
    instructor_number_identification = serializers.SerializerMethodField()
    instructor_phone_number = serializers.SerializerMethodField()
    instructor_type_identification = serializers.SerializerMethodField()
    instructor_knowledge_area = serializers.SerializerMethodField()
    instructor_email = serializers.SerializerMethodField()

    class Meta:
        model = RequestAsignation
        fields = [
            'id',
            'enterprise',
            'modality_productive_stage',
            'start_date',
            'end_date',
            'request_date',
            'request_state',
            'pdf_url',
            'instructor_id',
            'instructor_first_name',
            'instructor_second_name',
            'instructor_first_last_name',
            'instructor_second_last_name',
            'instructor_number_identification',
            'instructor_phone_number',
            'instructor_type_identification',
            'instructor_knowledge_area',
            'instructor_email',
        ]

    def get_instructor_email(self, obj):
        instructor = self._get_instructor(obj)
        if instructor:
            user = User.objects.filter(person=instructor.person).first()
            return user.email if user else None
        return None

    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()
    request_date = serializers.SerializerMethodField()
    pdf_url = serializers.SerializerMethodField()

    def get_start_date(self, obj):
        return str(obj.date_start_production_stage) if obj.date_start_production_stage else None

    def get_end_date(self, obj):
        return str(obj.date_end_production_stage) if obj.date_end_production_stage else None

    def get_request_date(self, obj):
        return str(obj.request_date) if obj.request_date else None

    def get_pdf_url(self, obj):
        return obj.pdf_request.url if obj.pdf_request else None

    def _get_instructor(self, obj):
        asignation = getattr(obj, 'asignation_instructor', None)
        if asignation and asignation.instructor:
            return asignation.instructor
        return None

    def get_instructor_id(self, obj):
        instructor = self._get_instructor(obj)
        return instructor.id if instructor else None

    def get_instructor_first_name(self, obj):
        instructor = self._get_instructor(obj)
        return instructor.person.first_name if instructor else None

    def get_instructor_second_name(self, obj):
        instructor = self._get_instructor(obj)
        return instructor.person.second_name if instructor else None

    def get_instructor_first_last_name(self, obj):
        instructor = self._get_instructor(obj)
        return instructor.person.first_last_name if instructor else None

    def get_instructor_second_last_name(self, obj):
        instructor = self._get_instructor(obj)
        return instructor.person.second_last_name if instructor else None

    def get_instructor_number_identification(self, obj):
        instructor = self._get_instructor(obj)
        return instructor.person.number_identification if instructor else None

    def get_instructor_phone_number(self, obj):
        instructor = self._get_instructor(obj)
        return instructor.person.phone_number if instructor else None

    def get_instructor_type_identification(self, obj):
        instructor = self._get_instructor(obj)
        return getattr(instructor.person.type_identification, 'name', None) if instructor else None

    def get_instructor_knowledge_area(self, obj):
        instructor = self._get_instructor(obj)
        return getattr(instructor.knowledge_area, 'name', None) if instructor else None
