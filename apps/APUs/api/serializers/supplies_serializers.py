from apps.APUs.models import *
from apps.users.models import *
from rest_framework import serializers

"""Los serializadores se usan para transformar las consultas en JSON, se estructuran acá"""

"""Muestra información de los usuarios"""
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'last_name']

"""Listado de Insumos"""
class SuppliesSerializer(serializers.HyperlinkedModelSerializer):
    """Se hereda la clase de Usuarios"""
    fk_id_user_create = UserSerializer(read_only=True)
    
    """Para lectura (GET)"""
    fk_id_type_supplies = serializers.StringRelatedField(source='fk_id_type_supplies.description')
    fk_id_unit = serializers.StringRelatedField(source='fk_id_unit.short_name')
    fk_id_city = serializers.StringRelatedField(source='fk_id_city.description')
    
    """Enlaces para detalles"""
    url_detail = serializers.SerializerMethodField()
    
    """Fields que deben aparecer en el serializador"""
    class Meta:
        model = SuppliesModel
        fields = [
            'id', 
            'description', 
            'fk_id_unit', 
            'price', 
            'data_aditional',
            'fk_id_type_supplies',
            'date_uplated', 
            'fk_id_user_create', 
            'fk_id_city',
            'url_detail'
        ]
    
    """Hyperlink para generar enlace de detalles del insumo y modificarlo"""
    def get_url_detail(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return request.build_absolute_uri(f'/ppto/insumos/{obj.id}/')
