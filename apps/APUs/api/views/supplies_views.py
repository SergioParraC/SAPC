from rest_framework import viewsets, status
from rest_framework.response import Response
from apps.users.models import *
from apps.APUs.api.serializers.supplies_serializers import *

"""Vista generica, contiene todos lo metodos HTTP"""
class SuppliesViewSet(viewsets.ModelViewSet):
    serializer_class = SuppliesSerializer
    queryset = SuppliesSerializer.Meta.model.objects.all()

    """Modificacion de metodo de crear insumo"""
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(fk_id_user_create=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """Modificacion de metodo de actualizar insumo"""
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """Modificacion de metodo de eliminar insumo"""
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {'error': 'No se puede eliminar este insumo porque está siendo utilizado'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    """Modificación del queryset para implementar de mejor manera la creación y modificacion de insumos"""
    def get_queryset(self):
        # Filtrar por ciudad o tipo de insumo
        queryset = super().get_queryset()
        city = self.request.query_params.get('city', None)
        if city:
            queryset = queryset.filter(fk_id_city=city)
        return queryset

    """Modificacion del metodo crear"""
    def perform_create(self, serializer):
        serializer.save(fk_id_user_create=self.request.user)

    """Modificacion del método actualizar"""
    def perform_update(self, serializer):
        serializer.save()
        
    """Modifica el contexto, para generar URLs absolutas"""
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context