from rest_framework import serializers

from apps.APUs.models import *
from apps.APUs.api.serializers.supplies_serializers import *

class SuppliesDetailsSerializer(serializers.ModelSerializer):
    fk_id_type_supplies = serializers.StringRelatedField(source='fk_id_type_supplies.description')
    fk_id_unit = serializers.StringRelatedField(source='fk_id_unit.short_name')
    class Meta:
        model = SuppliesModel
        fields = ['description', 'fk_id_type_supplies', 'fk_id_unit']

class SuppliesInAPUSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    fk_id_supplies = SuppliesDetailsSerializer()
    class Meta:
        model = SuppliesInAPUModel
        fields = ['fk_id_supplies','price','cant', 'total']
        
    def get_total(self, obj):
        return obj.price * obj.cant
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        supplies = SuppliesModel.objects.filter(id=instance.fk_id_supplies.id)
        if supplies.exists():
            representation['fk_id_supplies'] = SuppliesDetailsSerializer(supplies.first()).data
        else:
            representation['fk_id_supplies'] = None
        return representation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'last_name']
        
class APUSerializer(serializers.ModelSerializer):
    
    total_apu = serializers.SerializerMethodField()
    fk_id_user_create = UserSerializer(read_only=True)
    fk_id_unit = serializers.StringRelatedField(source='fk_id_unit.short_name')
    suppliesinapumodel_set = SuppliesInAPUSerializer(many=True, read_only=True)
    
    class Meta:
        model = AnalysisOfUnitaryPricesModel
        fields = ['id', 'description', 'fk_id_unit','total_apu', 'fk_id_user_create', 'suppliesinapumodel_set']
        
    def get_total_apu(self, obj):
        serializer = SuppliesInAPUSerializer(obj.suppliesinapumodel_set.all(), many=True)
        return sum(item['total'] for item in serializer.data)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        suppliesinapumodel_set = instance.suppliesinapumodel_set.all()
        representation['suppliesinapumodel_set'] = SuppliesInAPUSerializer(suppliesinapumodel_set, many=True).data
        return representation