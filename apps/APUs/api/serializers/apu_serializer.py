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
        
"""Clase para operacion de costo directo de APU"""
class SuppliesInAPUModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuppliesInAPUModel
        fields = ['price', 'cant']
        
"""Clase principal donde adjunta toda la informacion procesada anteriormente"""
class APUSerializer(serializers.HyperlinkedModelSerializer):
    
    direct_cost = serializers.SerializerMethodField()
    fk_id_user_create = UserSerializer(read_only=True)
    fk_id_unit = serializers.StringRelatedField(source='fk_id_unit.short_name')
    url_detail = serializers.SerializerMethodField()
    url_supplies_edit = serializers.SerializerMethodField()
    
    class Meta:
        model = AnalysisOfUnitaryPricesModel
        fields = ['id', 'description', 'fk_id_unit', 'fk_id_user_create','direct_cost', 'url_detail', 'url_supplies_edit']
    
    #Calcula el valor total de cada APU
    def get_direct_cost(self, obj):
        total = 0
        for supply in obj.suppliesinapumodel_set.all():
            total += supply.price * supply.cant
        return total
    
    #Genera la URL donde se puede detallar el APU
    def get_url_detail(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return request.build_absolute_uri(f'/ppto/APU/{obj.id}/')
    
    #Genera la url donde se editan los insumos
    def get_url_supplies_edit(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return request.build_absolute_uri(f'/ppto/APU/{obj.id}/supplies/')
    
"""Serializer para mostrar información de los insumos"""
class SuppliesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuppliesModel
        fields = ['id', 'description']

"""Serializer para listar los insumos dentro del APU"""
class SuppliesInAPUSerializer(serializers.HyperlinkedModelSerializer):
    fk_id_supplies = SuppliesSerializer(read_only=True)
    supplies_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=SuppliesModel.objects.all(),
        source='fk_id_supplies'
    )
    url_supplie_edit = serializers.SerializerMethodField()

    class Meta:
        model = SuppliesInAPUModel
        fields = ['id', 'fk_id_supplies', 'supplies_id', 'price', 'cant', 'url_supplie_edit']

    def create(self, validated_data):
        apu_id = self.context['apu_id']
        validated_data['fk_id_APU_id'] = apu_id
        return super().create(validated_data)
    
    #Se genera la url para editar el insumo indicado
    def get_url_supplie_edit(self, obj):
        request = self.context.get('request')
        if request is None or obj.fk_id_APU is None:
            return None
        apu_id = obj.fk_id_APU.id if obj.fk_id_APU else None
        if apu_id is None:
            return None
        return request.build_absolute_uri(f'/ppto/APU/{apu_id}/supplies/{obj.id}/')