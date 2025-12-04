from rest_framework import serializers
from apps.general.entity.models import Apprentice
from apps.security.entity.models import User

class GetApprenticeSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving apprentice data.
    All comments and docstrings are in English. User-facing messages remain in Spanish if any.
    """
    # Use type_identification_id to get the ID instead of the full object
    type_identification = serializers.IntegerField(source='person.type_identification_id')
    number_identification = serializers.CharField(source='person.number_identification')
    first_name = serializers.CharField(source='person.first_name')
    second_name = serializers.CharField(source='person.second_name')
    first_last_name = serializers.CharField(source='person.first_last_name')
    second_last_name = serializers.CharField(source='person.second_last_name')
    phone_number = serializers.CharField(source='person.phone_number')
    email = serializers.SerializerMethodField()
    program = serializers.IntegerField(source='ficha.program_id', required=False)
    ficha = serializers.IntegerField(source='ficha_id', required=False)
    role = serializers.SerializerMethodField()

    class Meta:
        model = Apprentice
        fields = [
            'id',
            'type_identification',
            'number_identification',
            'first_name',
            'second_name',
            'first_last_name',
            'second_last_name',
            'phone_number',
            'email',
            'program',
            'ficha',
            'role'
        ]

    def get_email(self, obj):
        """Get the apprentice's email from the related User object."""
        user = User.objects.filter(person=obj.person).first()
        return user.email if user else None

    def get_role(self, obj):
        """Get the role ID from the related User object."""
        user = User.objects.filter(person=obj.person).first()
        return user.role.id if user and user.role else None