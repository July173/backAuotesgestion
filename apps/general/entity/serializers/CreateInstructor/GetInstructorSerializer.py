from rest_framework import serializers
from apps.general.entity.models import Instructor, PersonSede
from apps.security.entity.models import User


class GetInstructorSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving instructor data.
    All comments and docstrings are in English. User-facing messages remain in Spanish if any.
    """
    first_name = serializers.SerializerMethodField()
    second_name = serializers.SerializerMethodField()
    first_last_name = serializers.SerializerMethodField()
    second_last_name = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    type_identification = serializers.SerializerMethodField()
    number_identification = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    contract_type = serializers.SerializerMethodField()  # Changed to return the ID
    contract_start_date = serializers.DateField()
    contract_end_date = serializers.DateField()
    knowledge_area = serializers.SerializerMethodField()
    sede = serializers.SerializerMethodField()
    active = serializers.SerializerMethodField()
    assigned_learners = serializers.IntegerField(read_only=True)
    max_assigned_learners = serializers.IntegerField(read_only=True)

    class Meta:
        model = Instructor
        fields = [
            'id',
            'first_name',
            'second_name',
            'first_last_name',
            'second_last_name',
            'phone_number',
            'type_identification',
            'number_identification',
            'email',
            'role',
            'contract_type',
            'contract_start_date',
            'contract_end_date',
            'knowledge_area',
            'sede',
            'is_followup_instructor',
            'assigned_learners',
            'max_assigned_learners',
            'active',
        ]

    def get_first_name(self, obj):
        """Get the instructor's first name from the related person object."""
        return obj.person.first_name if obj.person else None

    def get_second_name(self, obj):
        """Get the instructor's second name from the related person object."""
        return obj.person.second_name if obj.person else None

    def get_first_last_name(self, obj):
        """Get the instructor's first last name from the related person object."""
        return obj.person.first_last_name if obj.person else None

    def get_second_last_name(self, obj):
        """Get the instructor's second last name from the related person object."""
        return obj.person.second_last_name if obj.person else None

    def get_phone_number(self, obj):
        """Get the instructor's phone number from the related person object."""
        return obj.person.phone_number if obj.person else None

    def get_type_identification(self, obj):
        """Return the ID of the document type instead of the full object."""
        return obj.person.type_identification_id if obj.person else None

    def get_number_identification(self, obj):
        """Get the instructor's identification number from the related person object."""
        return obj.person.number_identification if obj.person else None

    def get_email(self, obj):
        """Get the instructor's email from the related User object."""
        user = User.objects.filter(person=obj.person).first()
        return user.email if user else None

    def get_role(self, obj):
        """Get the role ID from the related User object."""
        user = User.objects.filter(person=obj.person).first()
        return user.role.id if user and user.role else None

    def get_contract_type(self, obj):
        """Return the ID of the contract type instead of the full object."""
        return obj.contract_type_id if obj.contract_type_id else None

    def get_knowledge_area(self, obj):
        """Get the knowledge area ID from the related object."""
        return obj.knowledge_area.id if obj.knowledge_area else None

    def get_sede(self, obj):
        """Get the site ID from the related PersonSede object."""
        person_sede = PersonSede.objects.filter(person=obj.person).first()
        if person_sede and person_sede.sede:
            return person_sede.sede.id
        return None

    def get_active(self, obj):
        """Get the active status from the related User object."""
        user = User.objects.filter(person=obj.person).first()
        return user.is_active if user else False
