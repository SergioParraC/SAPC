from rest_framework import serializers

from apps.APUs.models import *
from apps.APUs.api.serializers.supplies_serializers import *

"""Los serializadores se usan para transformar las consultas en JSON, se estructuran aca"""

"""Configura los detalles a mostrar en cada insumo"""
class SuppliesDetailsSerializer(serializers.ModelSerializer):
    """Usa las relaciones para traer información"""
    fk_id_type_supplies = serializers.StringRelatedField(source='fk_id_type_supplies.description')
    fk_id_unit = serializers.StringRelatedField(source='fk_id_unit.short_name')
    class Meta:
        model = SuppliesModel
        fields = ['description', 'fk_id_type_supplies', 'fk_id_unit']

"""Muestra información del usuario"""
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'last_name']
        
"""Clase principal donde adjunta toda la información procesada anteriormente"""
class APUSerializer(serializers.ModelSerializer):
    
    #total_apu = serializers.SerializerMethodField()
    fk_id_user_create = UserSerializer(read_only=True)
    fk_id_unit = serializers.StringRelatedField(source='fk_id_unit.short_name')
    
    class Meta:
        model = AnalysisOfUnitaryPricesModel
        fields = ['id', 'description', 'fk_id_unit', 'fk_id_user_create']
    
"""Serializer para mostrar información de los insumos"""
class SuppliesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuppliesModel
        fields = ['id', 'description']

"""Serializer para listar los insumos dentro del APU"""
class SuppliesInAPUSerializer(serializers.ModelSerializer):
    fk_id_supplies = SuppliesSerializer(read_only=True)
    supplies_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=SuppliesModel.objects.all(),
        source='fk_id_supplies'
    )

    class Meta:
        model = SuppliesInAPUModel
        fields = ['id', 'fk_id_supplies', 'supplies_id', 'price', 'cant']

    def create(self, validated_data):
        apu_id = self.context['apu_id']
        validated_data['fk_id_APU_id'] = apu_id
        return super().create(validated_data)