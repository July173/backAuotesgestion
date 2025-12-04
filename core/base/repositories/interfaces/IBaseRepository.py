from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

T = TypeVar("T")


class IBaseRepository(ABC, Generic[T]):
    """Interfaz base para repositorios."""

    @abstractmethod
    def get_all(self) -> List[T]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        pass

    @abstractmethod
    def create(self, data: dict) -> T:
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        pass

    @abstractmethod
    def partial_update(self, entity: T, data: dict) -> T:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        """Elimina completamente el registro por id."""
        pass

    @abstractmethod
    def soft_delete(self, id: int) -> bool:
        """Elimina lógicamente el registro por id (cambia active y delete_at)."""
        pass
