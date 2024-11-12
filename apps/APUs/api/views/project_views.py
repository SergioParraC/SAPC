from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.APUs.models import *
from apps.APUs.api.serializers.project_serializer import ProjectsSerializer

class ProjectsViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectsSerializer
    permission_classes = [IsAuthenticated]

    # Filtrar los proyectos por el usuario que ha iniciado sesión
    def get_queryset(self):
        user = self.request.user
        return ProjectsModel.objects.filter(fk_id_usercreate=user)