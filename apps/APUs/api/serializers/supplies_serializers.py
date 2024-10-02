from apps.APUs.models import *
from apps.users.models import *
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'last_name']

class SuppliesSerializer(serializers.ModelSerializer):
    fk_id_user_create = UserSerializer(read_only=True)
    fk_id_type_supplies = serializers.StringRelatedField(source='fk_id_type_supplies.description')
    fk_id_unit = serializers.StringRelatedField(source='fk_id_unit.short_name')
    fk_id_city = serializers.StringRelatedField(source='fk_id_city.description')
    
    class Meta:
        model = SuppliesModel
        fields = ['id', 'description', 'fk_id_unit', 'price', 'data_aditional','fk_id_type_supplies','data_aditional', 'date_uplated', 'fk_id_user_create', 'fk_id_city']