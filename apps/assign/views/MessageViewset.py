from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from apps.assign.entity.serializers.MessageSerializer import MessageSerializer
from apps.assign.services.MessageService import MessageService

class MessageViewset(viewsets.ViewSet):
    """
    ViewSet para listar, obtener y crear mensajes usando MessageService.
    """
    
    #-- List --
    @swagger_auto_schema(
        operation_description="Obtiene una lista de todos los mensajes.",
        responses={200: MessageSerializer(many=True)},
        tags=["Message"]
    )
    def list(self, request):
        queryset = MessageService().get()
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)

    #-- Retrieve by ID --
    @swagger_auto_schema(
        operation_description="Obtiene el detalle de un mensaje por id.",
        responses={200: MessageSerializer()},
        tags=["Message"]
    )
    def retrieve(self, request, pk=None):
        result = MessageService().get_by_id(pk)
        if isinstance(result, dict) and result.get('status') == 'error':
            # Only show the error message (detail)
            return Response(result.get('detail', 'Error'), status=status.HTTP_404_NOT_FOUND)
        serializer = MessageSerializer(result)
        return Response(serializer.data)

    #-- Create --
    @swagger_auto_schema(
        operation_description="Crea un nuevo mensaje.",
        request_body=MessageSerializer,
        responses={201: MessageSerializer()},
        tags=["Message"]
    )
    def create(self, request):
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = MessageService().create(serializer.validated_data)
        if isinstance(result, dict) and result.get('status') == 'error':
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        out = MessageSerializer(result)
        return Response(out.data, status=status.HTTP_201_CREATED)
    
    # (PATCH/partial_update removed by request)