from rest_framework import viewsets
from apps.APUs.api.serializers.supplies_serializers import *

"""Vista generica, contiene todos lo metodos HTTP"""
class SuppliesViewSet(viewsets.ModelViewSet):
    serializer_class = SuppliesSerializer
    queryset = SuppliesSerializer.Meta.model.objects.all()
    