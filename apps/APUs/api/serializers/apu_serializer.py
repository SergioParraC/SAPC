from rest_framework import serializers

from apps.APUs.models import *
from apps.APUs.api.serializers.supplies_serializers import *

"""Los serializadores se usan para transformar las consultas en JSON, se estructuran acá"""

"""Configura los detalles a mostrar en cada insumo"""
class SuppliesDetailsSerializer(serializers.ModelSerializer):
    """Usa las relaciones para traer información"""
    fk_id_type_supplies = serializers.StringRelatedField(source='fk_id_type_supplies.description')
    fk_id_unit = serializers.StringRelatedField(source='fk_id_unit.short_name')
    class Meta:
        model = SuppliesModel
        fields = ['description', 'fk_id_type_supplies', 'fk_id_unit']

"""Configura cada uno de los insumos que se encuentran dentro de cada APU"""
class SuppliesInAPUSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    
    """Hereda la clase para mostrar los detalles de los insumos"""
    fk_id_supplies = SuppliesDetailsSerializer()
    class Meta:
        model = SuppliesInAPUModel
        fields = ['fk_id_supplies','price','cant', 'total']
    
    """Funcion que calcula el total para cada insumo"""
    def get_total(self, obj):
        return obj.price * obj.cant

"""Muestra información del usuario"""
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'last_name']
        
"""Clase principal donde adjunta toda la información procesada anteriormente"""
class APUSerializer(serializers.ModelSerializer):
    
    total_apu = serializers.SerializerMethodField()
    fk_id_user_create = UserSerializer(read_only=True)
    fk_id_unit = serializers.StringRelatedField(source='fk_id_unit.short_name')
    suppliesinapumodel_set = SuppliesInAPUSerializer(many=True, read_only=True)
    
    class Meta:
        model = AnalysisOfUnitaryPricesModel
        fields = ['id', 'description', 'fk_id_unit','total_apu', 'fk_id_user_create', 'suppliesinapumodel_set']
    """Funcion que calcula el precio total de todo el APU"""
    def get_total_apu(self, obj):
        serializer = SuppliesInAPUSerializer(obj.suppliesinapumodel_set.all(), many=True)
        return sum(item['total'] for item in serializer.data)
    