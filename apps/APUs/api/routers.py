from rest_framework.routers import DefaultRouter
from apps.APUs.api.views.supplies_views import SuppliesViewSet
from apps.APUs.api.views.apu_details_views import APUDetailsViewSet

"""Genera todas las rutas de manera automatica para poder Usar todos los metodos HTTP"""
router = DefaultRouter()
router.register(r'insumos', SuppliesViewSet, basename = 'suppliesmodel')
router.register(r'APU', APUDetailsViewSet)
urlpatterns = router.urls