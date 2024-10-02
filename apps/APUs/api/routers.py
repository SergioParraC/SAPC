from rest_framework.routers import DefaultRouter
from apps.APUs.api.views.supplies_views import SuppliesViewSet
from apps.APUs.api.views.apu_details_views import APUDetailsViewSet

router = DefaultRouter()
router.register(r'insumos', SuppliesViewSet)
router.register(r'APU', APUDetailsViewSet)
urlpatterns = router.urls