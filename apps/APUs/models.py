from django.db import models
from apps.users.models import User

"""Definición de modelos"""

"""NOTA: Los siguientes modelos pertenecen a la configuracion del programa, por lo tanto no podrán modificarse por el usuario"""
"""Tipo de moneda de cambio"""
class TypeMoneyModel(models.Model):

    id = models.AutoField(primary_key = True)
    money = models.CharField('Moneda', max_length=10, blank=False)
    money_simb = models.CharField('Simbolo de moneda', max_length=2, blank=False)
    
    """La clase Meta define en el admin como se muestra la información"""
    class Meta:
        verbose_name = ('Moneda')
        verbose_name_plural = ('Monedas')
    """La funcion __str__ Forma de mostrar la información tanto en Admin como en busquedas sencillas"""
    def __str__(self):
        return f"{self.money} - {self.money_simb}"

"""Paises"""    
class CountriesModel(models.Model):

    id = models.AutoField(primary_key = True)
    description = models.CharField('Nombre de pais', max_length=30, blank=False)
    
    class Meta:
        verbose_name = ('Pais')
        verbose_name_plural = ('Paises')
    def __str__(self):
        return f"{self.description}"
        
"""Ciudades"""
class CitiesModel(models.Model):

    id = models.AutoField(primary_key = True)
    description = models.CharField('Nombre de ciudad', max_length=30, blank=False)
    fk_id_countries = models.ForeignKey(CountriesModel, verbose_name='Pais', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name = ('Ciudad')
        verbose_name_plural = ('Ciudades')
    def __str__(self):
        return f"{self.description} - {self.fk_id_countries.description}"
        
"""Unidades de media (M, M3, Kg, Lb, etc)"""
class UnitsModel(models.Model):

    id = models.AutoField(primary_key = True)
    short_name = models.CharField('Simbolo', max_length=10, blank=False)
    name = models.CharField('Nombre', max_length=30, blank=False)
    
    class Meta:
        verbose_name = ('Unidad')
        verbose_name_plural = ('Unidades')
    def __str__(self):
        return f"{self.short_name} - {self.name}"

"""Tipo de proyecto (Edificio, via, puente)"""
class TypeProyectModels(models.Model):

    id = models.AutoField(primary_key = True)
    description = models.CharField('Tipo de proyecto', max_length=30, blank=False)
    
    class Meta:
        verbose_name = ('Tipo de proyecto')
        verbose_name_plural = ('Tipos de proyecto')
    def __str__(self):
        return f"{self.description}"

"""Tipos de insumos (Materiales, mano de obra, herramienta, trasiego)"""
class TypeSuppliesModel(models.Model):

    id = models.AutoField(primary_key = True)
    description = models.CharField('Insumos', max_length=15, blank=False)
    
    class Meta:
        verbose_name = ('Tipo de insumo')
        verbose_name_plural = ('Tipo de insumos')
    def __str__(self):
        return f"{self.description}"

"""Los siguientes modelos se podrán modificar por el Usuario"""
"""Compañias"""
class CompamiesModel(models.Model):

    id = models.AutoField(primary_key = True)
    nit = models.CharField('NIT', max_length=15, blank=True, default='')
    name = models.CharField('Nombre', max_length=40, blank=False)
    legal_rep = models.CharField('Representante legal', max_length=100, blank=True, default='')
    web_link = models.CharField('Pagina Web', max_length=100, blank=True, default='')
    email = models.CharField('Correo electrónico', max_length=100, blank=False)
    cellphone = models.CharField('Número de telefono', max_length=15, blank=True, default='')
    is_auditor = models.BooleanField('Es interventoria?', default=False)
    fk_id_cities = models.ForeignKey(CitiesModel, verbose_name='Ciudad y país', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = ('Empresa')
        verbose_name_plural = ('Empresas')
    def __str__(self):
        return f"{self.name}"
    
"""Información referente al proyecto"""
class ProjectsModel(models.Model):

    id = models.AutoField(primary_key = True)
    name = models.CharField('Nombre', max_length=100, blank=False, default="")
    cod_obra = models.CharField('Código de obra', max_length=30, blank=True)
    object = models.CharField('Objeto del proyecto', max_length=1000, blank=True)
    fk_id_project = models.ForeignKey(TypeProyectModels, verbose_name='Tipo de proyecto', on_delete=models.SET_NULL, null=True)
    date_create = models.DateTimeField('Fecha de creación', auto_now=False, auto_now_add=True)
    date_bidding = models.DateTimeField('Fecha de licitacion', auto_now=False, auto_now_add=False, blank=True)
    n_bidding = models.CharField('Número de licitación', max_length=20, blank=True)
    date_start = models.DateTimeField('Fecha inicio de obra', auto_now=False, auto_now_add=False, blank=False)
    date_end = models.DateTimeField('Fecha fin de obra', auto_now=False, auto_now_add=False, blank=True)
    addres = models.CharField('Diercción de obra', max_length=100, blank=False)
    fk_id_usercreate = models.ForeignKey(User, verbose_name='Nombre de usurio creador', on_delete=models.SET_NULL, null=True)
    fk_id_companie = models.ForeignKey(CompamiesModel, verbose_name='Empresa', on_delete=models.SET_NULL, null=True, related_name='companie_project')
    fk_id_auditor = models.ForeignKey(CompamiesModel, verbose_name='Interventoria', on_delete=models.SET_DEFAULT, blank=True, null=True, default=None, related_name='auditor_project')
    is_direct_cost = models.BooleanField('Es costo directo?', default=False)
    administration = models.DecimalField('Administración', max_digits=5, decimal_places=2, default=0.0)
    eventuality = models.DecimalField('Imprevistos', max_digits=5, decimal_places=2, default=0.0)
    utility = models.DecimalField('Utilidad', max_digits=5, decimal_places=2, default=0.0)
    fk_id_city = models.ForeignKey(CitiesModel, verbose_name='Ciudad', on_delete=models.SET_NULL, null=True)
    fk_id_money = models.ForeignKey(TypeMoneyModel, verbose_name='Moneda', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name = ('Proyecto')
        verbose_name_plural = ('Proyectos')
    def __str__(self):
        return f"{self.name} - {self.fk_id_companie.name} creado el {self.date_create.strftime('%Y-%m-%d')}"

"""Almacentamiento de Analisis de Precios Unitarios, se realiza tabla diferente a la WBS para dar acceso a la busqueda
a los usuarios de usar cualquier APU realizado por otrs usuarios"""
class AnalysisOfUnitaryPricesModel(models.Model):

    id = models.AutoField(primary_key = True)
    description = models.CharField('Descripción', max_length=500, blank=False)
    fk_id_unit = models.ForeignKey(UnitsModel, verbose_name='Unidad', on_delete=models.SET_NULL, null=True)
    fk_id_user_create = models.ForeignKey(User, verbose_name='Usuario creador', on_delete=models.SET_NULL, null=True)
    fk_id_type_project = models.ForeignKey(TypeProyectModels, verbose_name='Tipo de proyecto', on_delete=models.SET_NULL, default='', null=True)
    fk_id_city = models.ForeignKey(CitiesModel, verbose_name='Ciudad', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = ('Analisis de precios unitarios')
        verbose_name_plural = ('Analisis de precios unitarios')
    def __str__(self):
        return f"{self.description} - {self.fk_id_unit.short_name}"
    
"""Estructura de Desglose del Trabajo (EDS) o WBS de las siglas en ingles. Contiene toda la estructura del trabajo
tanto capítulos, subcapítulos y almacena los APUS que corresponden a la estructura"""
class WorkBreakdownStructureModel(models.Model):

    id = models.AutoField(primary_key = True)
    fk_id_analyst_of_unitary_prices = models.ForeignKey(AnalysisOfUnitaryPricesModel, verbose_name='APU', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    fk_id_project = models.ForeignKey(ProjectsModel, verbose_name='Proyecto', on_delete=models.CASCADE)
    grade = models.IntegerField('Grado', default=1, blank=False)
    description = models.CharField('Descripción', max_length=500, blank=True)
    cant = models.DecimalField('Cantidad', max_digits=20, decimal_places=10, default=0.0)
    fk_id_user_add = models.ForeignKey(User, verbose_name='Creado por', on_delete=models.SET_NULL, null=True)
    date_edit = models.DateTimeField('Fecha editado', auto_now=True, auto_now_add=False)
    date_start = models.DateTimeField('Fecha de inicio', auto_now=False, auto_now_add=True)
    date_end = models.DateTimeField('Fecha de fin', auto_now=False, auto_now_add=True)
    key_username_item = models.CharField('Clave de usuario', max_length=10, blank=False)
    
    class Meta:
        verbose_name = ('EDS')
        verbose_name_plural = ('EDS')
    def __str__(self):
        return f"{self.grade} - {self.key_username_item} - {self.description}"
    
"""Listado de todos los insumos"""
class SuppliesModel(models.Model):

    id = models.AutoField(primary_key = True)
    description = models.CharField('Descripción', max_length=50, blank=False)
    fk_id_unit = models.ForeignKey(UnitsModel, verbose_name='Unidad', on_delete=models.SET_NULL, null=True)
    data_aditional = models.CharField('Información adicional', max_length=100, blank=True, default="")
    date_uplated = models.DateTimeField('Fecha de actualización', auto_now=True, auto_now_add=False)
    price = models.DecimalField('Precio', max_digits=13, decimal_places=2, default=0.0)
    fk_id_user_create = models.ForeignKey(User, verbose_name='Usuario', on_delete=models.SET_NULL, null=True)
    fk_id_type_supplies = models.ForeignKey(TypeSuppliesModel, verbose_name='Insumo', on_delete=models.SET_NULL, null=True)
    fk_id_city = models.ForeignKey(CitiesModel, verbose_name='Ciudad', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = ('Insumo')
        verbose_name_plural = ('Insumos')
    def __str__(self):
        
        #key_projects = self.keyprojectmodel_set.all()
        #if key_projects:
        #    return f"{self.description}{' - '.join([kp.key_user for kp in key_projects])}"
        #else:
        return f"{self.description}"

"""Claves dadas por parte del usuario a cada uno de los insumos, este será para cada Insumo
Para cada proyecto manejará una nomenclatura para dar homogeneidad entre los usuarios que tienen acceso al proyecto"""
class KeySupplieProjectModel(models.Model):

    id = models.AutoField(primary_key = True)
    key_user = models.CharField('Clave', max_length=10, blank=False)
    fk_id_supplies = models.ForeignKey(SuppliesModel, verbose_name='Insumo', on_delete=models.CASCADE)
    fk_id_project = models.ForeignKey(ProjectsModel, verbose_name='Proyecto', on_delete=models.CASCADE)

    class Meta:
        verbose_name = ('Clave de insumo')
        verbose_name_plural = ('Claves de insumos')
    def __str__(self):
        return f"{self.key_user} - {self.fk_id_supplies.description}"
            
"""Para enlazar las cantidades de cada insumo con cada APU se usara esta tabla, almacena la cantidad y el precio,
que que puede variar dependiendo de cada proyecto"""
class SuppliesInAPUModel(models.Model):

    id = models.AutoField(primary_key = True)
    fk_id_APU = models.ForeignKey(AnalysisOfUnitaryPricesModel, verbose_name='APU', on_delete=models.CASCADE)
    fk_id_supplies = models.ForeignKey(SuppliesModel, verbose_name='Insumo', on_delete=models.CASCADE)
    price = models.DecimalField('Precio', max_digits=13, decimal_places=2, default=0.0)
    cant = models.DecimalField('Cantidad', max_digits=30, decimal_places=10, default=0.0)

    class Meta:
        verbose_name = ('Insumos - APU')
        verbose_name_plural = ('Insumos - APU')
    def __str__(self):
        return f"{self.fk_id_APU.description} - {self.price} - {self.cant}"