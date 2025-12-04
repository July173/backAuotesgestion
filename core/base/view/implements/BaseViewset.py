from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.request import Request
from typing import Type, Any
from core.base.view.interfaces.IBaseViewset import IBaseViewSet
from core.base.services.interfaces.IBaseService import IBaseService
from rest_framework.serializers import Serializer
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet



class BaseViewSet(ModelViewSet, IBaseViewSet):
    """
    Implementación concreta del ViewSet que sigue nuestra arquitectura.
    """
    service_class: Type[IBaseService] = None
    serializer_class: Type[Serializer] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._validate_dependencies()
        self.service = self.service_class()

    def _validate_dependencies(self):
        if not self.service_class:
            raise NotImplementedError("Debe definir 'service_class'")
        if not self.serializer_class:
            raise NotImplementedError("Debe definir 'serializer_class'")

    def get_serializer_class(self) -> Type[Serializer]:
        return self.serializer_class

    def get_serializer(self, *args, **kwargs) -> Serializer:
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def list(self, request: Request) -> Response:
        items = self.service.list()
        if isinstance(items, dict) and items.get('status') == 'error':
            return Response(items, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)

    def retrieve(self, request: Request, pk: Any = None) -> Response:
        item = self.service.get(pk)
        if not item or (isinstance(item, dict) and item.get('status') == 'error'):
            return Response(
                item if isinstance(item, dict) else {"detail": "No encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(item)
        return Response(serializer.data)

    def create(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.service.create(serializer.validated_data)
        if isinstance(instance, dict) and instance.get('status') == 'error':
            return Response(instance, status=status.HTTP_400_BAD_REQUEST)
        output_serializer = self.get_serializer(instance)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request: Request, pk: Any = None) -> Response:
        instance = self.service.get(pk)
        if not instance or (isinstance(instance, dict) and instance.get('status') == 'error'):
            return Response(
                instance if isinstance(instance, dict) else {"detail": "No encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_instance = self.service.update(pk, serializer.validated_data)
        if isinstance(updated_instance, dict) and updated_instance.get('status') == 'error':
            return Response(updated_instance, status=status.HTTP_400_BAD_REQUEST)
        output_serializer = self.get_serializer(updated_instance)
        return Response(output_serializer.data)

    def partial_update(self, request: Request, pk: Any = None) -> Response:
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_instance = self.service.partial_update(pk, serializer.validated_data)
        if isinstance(updated_instance, dict) and updated_instance.get('status') == 'error':
            return Response(updated_instance, status=status.HTTP_400_BAD_REQUEST)
        response_serializer = self.get_serializer(updated_instance)
        return Response(response_serializer.data)

    def destroy(self, request: Request, pk: Any = None) -> Response:
        deleted = self.service.delete(pk)
        if isinstance(deleted, dict) and deleted.get('status') == 'error':
            return Response(deleted, status=status.HTTP_400_BAD_REQUEST)
        if deleted:
            return Response({"detail": "Eliminado correctamente."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['delete'], url_path='soft-delete')
    def soft_destroy(self, request: Request, pk: Any = None) -> Response:
        deleted = self.service.soft_delete(pk)
        if isinstance(deleted, dict) and deleted.get('status') == 'error':
            return Response(deleted, status=status.HTTP_400_BAD_REQUEST)
        if deleted:
            return Response({"detail": "Eliminado lógicamente correctamente."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)


    def render_message(self, result, ok_status=status.HTTP_200_OK, error_status=status.HTTP_400_BAD_REQUEST):
        # Determina el status_code correcto si está presente en el resultado
        status_code = None
        if isinstance(result, dict) and 'status_code' in result:
            status_code = result['status_code']
        # Si el resultado es un dict y tiene 'detail', retorna solo el contenido de 'detail'
        if isinstance(result, dict) and 'detail' in result:
            return Response(result['detail'], status=status_code or ok_status)
        # Si es string plano, retorna tal cual
        if isinstance(result, str):
            return Response(result, status=status_code or ok_status)
        # Si es dict con un solo key, retorna su valor
        if isinstance(result, dict) and len(result) == 1:
            key = list(result.keys())[0]
            return Response(result[key], status=status_code or ok_status)
        # Fallback
        return Response('Sin información disponible', status=status_code or ok_status)