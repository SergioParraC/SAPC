from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.APUs.models import *
from apps.APUs.api.serializers.wbs_serializer import WBSSerializer

class WBSViewSet(viewsets.ModelViewSet):
    serializer_class = WBSSerializer
    permission_classes = [IsAuthenticated]
    
    queryset = WBSSerializer.Meta.model.objects.all()
    
    