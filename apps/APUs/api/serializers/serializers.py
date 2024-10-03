from apps.APUs.models import *
from rest_framework import serializers


"""Serializadores de prueba para validar el correcto funcionamiento de las cosnultas sencillas a los modelos que puede
modificar los usuarios"""
class AllProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectsModel
        exclude = ('id', 'object', 'fk_id_project', 'date_create', 'date_end')
        
class WBSSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkBreakdownStructureModel
        exclude = ('id',)
        

        