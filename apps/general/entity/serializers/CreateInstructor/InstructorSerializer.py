from apps.general.entity.models import Instructor
from apps.security.entity.models import Person
from apps.general.entity.models.TypeContract import TypeContract
from rest_framework import serializers


class InstructorSerializer(serializers.ModelSerializer):
    # Use PrimaryKeyRelatedField for foreign keys so serializer accepts related model instances
    person = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all())
    contract_type = serializers.PrimaryKeyRelatedField(queryset=TypeContract.objects.all())

    class Meta:
        model = Instructor
        fields = [
            'id',
            'person',
            'contract_type',
            'contract_start_date',
            'contract_end_date',
            'knowledge_area',
            'active',
            'assigned_learners',
            'max_assigned_learners',
            'is_followup_instructor'
        ]
        extra_kwargs = {
            'assigned_learners': {'write_only': True},
            'max_assigned_learners': {'write_only': True},
        }
