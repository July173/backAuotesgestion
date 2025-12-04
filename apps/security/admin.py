from django.contrib import admin
from .entity.models import User, Role, Person, Form, Permission, Module, FormModule, RoleFormPermission

admin.site.register(Form)
admin.site.register(FormModule)
admin.site.register(Module)
admin.site.register(Permission)
admin.site.register(Person)
admin.site.register(RoleFormPermission)
admin.site.register(Role)
admin.site.register(User)
