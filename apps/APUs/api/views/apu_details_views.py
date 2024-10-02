from rest_framework import viewsets
from apps.APUs.api.serializers.apu_serializer import *

class APUDetailsViewSet(viewsets.ModelViewSet):
    serializer_class = APUSerializer
    queryset = APUSerializer.Meta.model.objects.all()
    
    def get_actions(self):
        actions = super().get_actions()
        del actions['list']
        return actions