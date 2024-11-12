from rest_framework import serializers
from apps.APUs.models import *

"""Muestra tipo de proyecto"""
class TypeProyectSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeProyectModels
        fields = ['description']

"""Muestra información del usuario"""
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'last_name']
        
"""Muestra el nombre de la empresa"""
class CompanieSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompamiesModel
        fields = ['name']
        
"""Serializa la ciudad del proyecto"""
class CitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitiesModel
        fields = ['description']

"""Serializa la moneda que se encuentra predeterminada para el proyecto"""
class TypeMoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeMoneyModel
        fields = ['money']
        
"""Une toda la informacion que muestra en el proyecto"""
class ProjectsSerializer(serializers.ModelSerializer):
    fk_id_project = TypeProyectSerializer(read_only=True)
    fk_id_usercreate = UserSerializer(read_only=True)
    fk_id_companie = CompanieSerializer(read_only=True)
    fk_id_auditor = CompanieSerializer(read_only=True)
    fk_id_city = CitiesSerializer(read_only=True)
    fk_id_money = TypeMoneySerializer(read_only=True)
    url_edit = serializers.SerializerMethodField()
    
    class Meta:
        model = ProjectsModel
        fields = [
            'id',
            'name',
            'cod_obra',
            'object',
            'fk_id_project',
            'date_create',
            'date_bidding',
            'n_bidding',
            'date_start',
            'date_end',
            'addres',
            'fk_id_usercreate',
            'fk_id_companie',
            'fk_id_auditor',
            'is_direct_cost',
            'administration',
            'eventuality',
            'utility',
            'fk_id_city',
            'fk_id_money',
            'url_edit',
        ]
    
    #Generando enlace para editar la info del proyecto
    def get_url_edit(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return request.build_absolute_uri(f'/ppto/projects/{obj.id}/')
