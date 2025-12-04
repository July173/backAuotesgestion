from apps.security.entity.models import User
from rest_framework import serializers
from apps.security.entity.serializers.person.PersonSerializer import PersonSerializer
from apps.security.entity.serializers.RoleSerializer import RoleSerializer
from apps.general.entity.serializers.CreateAprendiz.ApprenticeSerializer import ApprenticeSerializer
from apps.general.entity.serializers.CreateInstructor.InstructorSerializer import InstructorSerializer
from apps.general.entity.models import Apprentice, Instructor, Instructor, PersonSede



class UserSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)
    role = RoleSerializer(read_only=True)

    # Dynamic fields for apprentice and instructor
    apprentice = serializers.SerializerMethodField()
    instructor = serializers.SerializerMethodField()

    def get_apprentice(self, obj):
        apprentice = Apprentice.objects.filter(person=obj.person).select_related('ficha__program').first()
        if apprentice:
            data = ApprenticeSerializer(apprentice).data
            ficha = apprentice.ficha  # Esto es un objeto Ficha o None
            if ficha and ficha.program:
                data['programa'] = {
                    'id': ficha.program.id,
                    'name': ficha.program.name
                }
            else:
                data['programa'] = None
            return data
        return None

    def get_instructor(self, obj):
        # Buscar si la persona está vinculada como Instructor
        instructor = Instructor.objects.filter(person=obj.person).first()
        if instructor:
            data = InstructorSerializer(instructor).data
            # Buscar la sede vinculada usando nombres de campo del modelo
            # PersonSede model fields: person (FK to Person), sede (FK to Sede)
            person_sede = PersonSede.objects.filter(person=instructor.person).select_related('sede__center__regional').first()
            if person_sede and person_sede.sede:
                sede = person_sede.sede
                centro = getattr(sede, 'center', None)
                regional = getattr(centro, 'regional', None) if centro else None
                data['sede'] = {'id': sede.id, 'name': getattr(sede, 'name', None)} if sede else None
                data['centro'] = {'id': centro.id, 'name': getattr(centro, 'name', None)} if centro else None
                data['regional'] = {'id': regional.id, 'name': getattr(regional, 'name', None)} if regional else None
            else:
                data['sede'] = None
                data['centro'] = None
                data['regional'] = None
            return data
        return None

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'person', 'role', 'is_active', 'registered', 'apprentice', 'instructor']
        ref_name = "UserModelSerializer"
        extra_kwargs = {
            'password': {'write_only': True}
        }