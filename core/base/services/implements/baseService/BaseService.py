from typing import TypeVar, List, Optional, Dict, Any
from core.base.repositories.interfaces.IBaseRepository import IBaseRepository

T = TypeVar("T")

class BaseService:
    """
    Implementación concreta del servicio con funcionalidades extendidas.
    """

    def __init__(self, repository: IBaseRepository[T]):
        self.repository = repository

    def error_response(self, message, error_type="error"):
        return {"status": "error", "type": error_type, "message": str(message)}

    def list(self) -> List[T]:
        try:
            return self.repository.get_all()
        except Exception as e:
            return self.error_response(f"Error al listar: {e}", "list")

    def get(self, id: int) -> Optional[T]:
        try:
            return self.repository.get_by_id(id)
        except Exception as e:
            return self.error_response(f"Error al obtener: {e}", "get")

    def create(self, data: Dict[str, Any]) -> T:
        try:
            return self.repository.create(data)
        except Exception as e:
            return self.error_response(f"Error al crear: {e}", "create")

    def update(self, id: int, data: Dict[str, Any]) -> T:
        try:
            instance = self.get(id)
            if instance is None or (isinstance(instance, dict) and instance.get('status') == 'error'):
                return self.error_response(f"Instancia con id {id} no encontrada", "not_found")
            for key, value in data.items():
                # Permitir None o "" solo para parentId
                if value in [None, ""] and key != "parentId":
                    return self.error_response(f"El campo '{key}' no puede estar vacío", "invalid_field")
                setattr(instance, key, value)
            return self.repository.update(instance)
        except Exception as e:
            return self.error_response(f"Error al actualizar: {e}", "update")

    def partial_update(self, id: int, data: Dict[str, Any]) -> T:
        try:
            instance = self.get(id)
            if instance is None or (isinstance(instance, dict) and instance.get('status') == 'error'):
                return self.error_response(f"Instancia con id {id} no encontrada", "not_found")
            for key, value in data.items():
                if value not in [None, ""]:
                    setattr(instance, key, value)
            return self.repository.update(instance)
        except Exception as e:
            return self.error_response(f"Error al actualizar parcialmente: {e}", "partial_update")

    def delete(self, id: int) -> bool:
        try:
            return self.repository.delete(id)
        except Exception as e:
            return self.error_response(f"Error al eliminar: {e}", "delete")

    def soft_delete(self, id: int) -> bool:
        try:
            return self.repository.soft_delete(id)
        except Exception as e:
            return self.error_response(f"Error al eliminar lógicamente: {e}", "soft_delete")
