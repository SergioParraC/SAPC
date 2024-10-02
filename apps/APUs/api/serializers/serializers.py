from apps.APUs.models import *
from rest_framework import serializers

class AllProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectsModel
        exclude = ('id', 'object', 'fk_id_project', 'date_create', 'date_end')
        
class AllAUPSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisOfUnitaryPricesModel
        exclude = ('id',)
        
class WBSSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkBreakdownStructureModel
        exclude = ('id',)
        

        