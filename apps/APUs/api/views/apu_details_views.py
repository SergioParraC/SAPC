from rest_framework import viewsets
from apps.APUs.api.serializers.apu_serializer import *

"""Vista generica, contiene todos lo metodos HTTP"""
class APUDetailsViewSet(viewsets.ModelViewSet):
    serializer_class = APUSerializer
    queryset = APUSerializer.Meta.model.objects.all()
    