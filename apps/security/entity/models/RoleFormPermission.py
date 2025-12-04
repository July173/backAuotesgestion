from .Role import Role
from .Form import Form
from .Permission import Permission
from django.db import models


class RoleFormPermission(models.Model):

    class Meta:
        db_table = 'role_form_permission'

    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    delete_at = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
