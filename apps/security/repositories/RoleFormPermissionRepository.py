from core.base.repositories.implements.baseRepository.BaseRepository import BaseRepository
from apps.security.entity.models import RoleFormPermission

class RoleFormPermissionRepository(BaseRepository):
    def __init__(self):
        super().__init__(RoleFormPermission)

    def get_menu(self, user_id: int):
            
            """
            Retorna la estructura de menú para un usuario dado.
            Usamos directamente la relación User -> Role -> RoleFormPermission.
            """
            datos = (
                RoleFormPermission.objects
                .filter(role__user__id=user_id, form__formmodule__module__active=True)  # Filtrar por usuario y módulos activos
                .select_related("role", "form__formmodule__module", "form")
                .values(
                    "role__type_role",                       # nombre del rol
                    "form__formmodule__module__name",        # nombre del módulo
                    "form__name",                            # nombre del form
                    "form__path"                             # ruta del form
                )
            )

            resultado = {}
            for d in datos:
                rol = d["role__type_role"]
                module = d["form__formmodule__module__name"]
                form_name = d["form__name"]
                form_path = d["form__path"]

                if rol not in resultado:
                    resultado[rol] = {}

                if module not in resultado[rol]:
                    resultado[rol][module] = []

                # evitar duplicados
                if not any(f["name"] == form_name for f in resultado[rol][module]):
                    resultado[rol][module].append({
                        "name": form_name,
                        "path": form_path
                    })

            # transformar a lista de diccionarios como espera el serializer
            menu = []
            for rol, modules in resultado.items():
                module_forms = [
                    {"name": m, "form": forms}
                    for m, forms in modules.items()
                ]
                menu.append({
                    "rol": rol,
                    "moduleForm": module_forms
                })

            return menu