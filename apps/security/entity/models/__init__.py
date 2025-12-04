# Importar DocumentType para registrar el modelo correctamente
from .DocumentType import DocumentType
from .Form import Form
from .FormModule import FormModule
from .Module import Module
from .Permission import Permission
from .Person import Person
from .Role import Role
from .RoleFormPermission import RoleFormPermission
from .User import User


__all__ = [
    'User', 'Role', 'Person', 'Form', 'Permission',
    'Module', 'FormModule', 'RoleFormPermission', 'DocumentType'
]
