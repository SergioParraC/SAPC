from apps.APUs.models import *
from apps.users.models import *
from rest_framework import serializers
from apps.APUs.api.serializers.apu_serializer import APUSerializer 

"""Se vincula dos bses de datos
WorkBreakdownStructureModel -> AnalysisOfUnitaryPricesModel
Para armar la estructura de trabajo del proyecto"""

class WBSSerializer(serializers.ModelSerializer):
    apu_details = APUSerializer(source='fk_id_analyst_of_unitary_prices', read_only=True)
    total_cost = serializers.SerializerMethodField()
    class Meta:
        model = WorkBreakdownStructureModel
        fields = [
            'id', 
            'apu_details', 
            'fk_id_project', 
            'grade', 
            'description', 
            'cant', 
            'fk_id_user_add', 
            'date_edit', 
            'date_start', 
            'date_end', 
            'key_username_item',
            'total_cost',
            ]

    """Obtiene el costo directo del APUSerializer"""
    def get_total_cost(self, obj):
        direct_cost = 0

        if obj.fk_id_analyst_of_unitary_prices:
            apu_serializer = APUSerializer(obj.fk_id_analyst_of_unitary_prices)
            direct_cost = apu_serializer.get_direct_cost(obj.fk_id_analyst_of_unitary_prices)
        quantity = obj.cant if obj.cant else 0
        return direct_cost * quantity