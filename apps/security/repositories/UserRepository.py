from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.security.entity.models import User
from apps.security.entity.serializers.User.UserSimpleSerializer import UserSimpleSerializer


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def get_queryset(self):
        # Incluye relaciones para optimizar las consultas
        return User.objects.select_related('person', 'role')
  

    def create_user(self, data):
        serializer = UserSimpleSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return user, serializer.data, None
        return None, None, serializer.errors

    def delete_user(self, user):
        user.delete()
    
