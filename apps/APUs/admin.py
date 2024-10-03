from django.contrib import admin
from apps.APUs.models import *

"""Se registra todas las bases de datos que se podrán utilizar por parte del Admnistrador"""
admin.site.register(TypeMoneyModel)
admin.site.register(CountriesModel)
admin.site.register(CitiesModel)
admin.site.register(UnitsModel)
admin.site.register(TypeProyectModels)
admin.site.register(TypeSuppliesModel)
admin.site.register(CompamiesModel)
admin.site.register(ProjectsModel)
admin.site.register(AnalysisOfUnitaryPricesModel)
admin.site.register(WorkBreakdownStructureModel)
admin.site.register(SuppliesModel)
admin.site.register(KeySupplieProjectModel)
admin.site.register(SuppliesInAPUModel)
