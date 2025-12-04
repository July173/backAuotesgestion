from apps.general.entity.models.Notification import Notification


class NotificationRepository:
        
    def __init__(self):
        self.model = Notification


    #---- Create Notification ----#
    def create(self, validated_data):
        return self.model.objects.create(**validated_data)

    #----- Get Methods -----#
    #---- List All Notifications ----#
    def list_all(self):
        """Devuelve todas las notificaciones activas ordenadas por fecha descendente."""
        return self.model.objects.filter(active=True).order_by('-created_at')

    #---- GetById Notification Apprentice----#
    def get_by_apprentice_id(self, apprentice_id):
        """Devuelve notificaciones del usuario con rol 'Aprendiz'."""
        return self.model.objects.filter(
            id_user__id=apprentice_id,
            id_user__role__type_role__iexact='Aprendiz'
        ).order_by('-created_at')

    #---- GetById Notification Instructor----#
    def get_by_instructor_id(self, instructor_id):
        """Devuelve notificaciones del usuario con rol 'Instructor'."""
        return self.model.objects.filter(
            id_user__id=instructor_id,
            id_user__role__type_role__iexact='Instructor'
        ).order_by('-created_at')

    #---- GetById Notification Coordinator----#
    def get_by_coordinator_id(self, coordinator_id):
        """Devuelve notificaciones del usuario con rol 'Coordinador'."""
        return self.model.objects.filter(
            id_user__id=coordinator_id,
            id_user__role__type_role__iexact='Coordinador'
        ).order_by('-created_at')

    #---- GetById Notification Admin----#
    def get_by_admin_id(self, admin_id):
        """Devuelve notificaciones del usuario con rol 'Administrador'."""
        return self.model.objects.filter(
            id_user__id=admin_id,
            id_user__role__type_role__iexact='Administrador'
        ).order_by('-created_at')

    #---- GetById Notification Sofia Operator----#
    def get_by_sofia_operator_id(self, sofia_operator_id):
        """Devuelve notificaciones del usuario con rol 'Operador Sofia Plus'."""
        return self.model.objects.filter(
            id_user__id=sofia_operator_id,
            id_user__role__type_role__iexact='Operador Sofia Plus'
        ).order_by('-created_at')

    #---- GetById Notification ----#
    def get_by_id(self, notification_id):
        """Devuelve una notificación activa por su id o None si no existe o está inactiva."""
        return self.model.objects.filter(id=notification_id, active=True).first()
    
    
    #--- Delete Methods ----#
    
    #---- DeleteById Notification Apprentice----#
    def delete_by_apprentice_id(self, apprentice_id):
        """Desactiva (active=False) todas las notificaciones del usuario con rol 'Aprendiz'."""
        qs = self.model.objects.filter(
            id_user__id=apprentice_id,
            id_user__role__type_role__iexact='Aprendiz',
            active=True
        )
        updated = qs.update(active=False)
        return updated

    #---- DeleteById Notification Instructor----#
    def delete_by_instructor_id(self, instructor_id):
        """Desactiva (active=False) todas las notificaciones del usuario con rol 'Instructor'."""
        qs = self.model.objects.filter(
            id_user__id=instructor_id,
            id_user__role__type_role__iexact='Instructor',
            active=True
        )
        updated = qs.update(active=False)
        return updated

    #---- DeleteById Notification Coordinator----#
    def delete_by_coordinator_id(self, coordinator_id):
        """Desactiva (active=False) todas las notificaciones del usuario con rol 'Coordinador'."""
        qs = self.model.objects.filter(
            id_user__id=coordinator_id,
            id_user__role__type_role__iexact='Coordinador',
            active=True
        )
        updated = qs.update(active=False)
        return updated

    #---- DeleteById Notification Admin----#
    def delete_by_admin_id(self, admin_id):
        """Desactiva (active=False) todas las notificaciones del usuario con rol 'Administrador'."""
        qs = self.model.objects.filter(
            id_user__id=admin_id,
            id_user__role__type_role__iexact='Administrador',
            active=True
        )
        updated = qs.update(active=False)
        return updated

    #---- DeleteById Notification Sofia Operator----#
    def delete_by_sofia_operator_id(self, sofia_operator_id):
        """Desactiva (active=False) todas las notificaciones del usuario con rol 'Operador Sofia Plus'."""
        qs = self.model.objects.filter(
            id_user__id=sofia_operator_id,
            id_user__role__type_role__iexact='Operador Sofia Plus',
            active=True
        )
        updated = qs.update(active=False)
        return updated

    #---- DeleteById Notification ----#
    def delete_by_id(self, notification_id):
        """Desactiva (active=False) la notificación por su id y la retorna, o None si no existe."""
        notification = self.model.objects.filter(id=notification_id, active=True).first()
        if notification:
            notification.active = False
            notification.save(update_fields=["active"])
            return notification
        return None