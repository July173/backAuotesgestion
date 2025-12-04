from apps.security.entity.models import User
from rest_framework import serializers

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'person', 'role', 'is_active', 'registered']
        ref_name = "UserSimpleModelSerializer"
        extra_kwargs = {
            'password': {'write_only': True}
        }
