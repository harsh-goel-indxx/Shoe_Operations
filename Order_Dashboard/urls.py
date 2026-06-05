# urls.py
from rest_framework.routers import DefaultRouter
from .views import (
    ColorViewSet, PartyMasterViewSet, SubPartyMasterViewSet,
    ProductMasterViewSet, OrderItemViewset, OrdersViewSet
)

router = DefaultRouter()
router.register(r"colors",       ColorViewSet,          basename="color")
router.register(r"parties",      PartyMasterViewSet,    basename="party")
router.register(r"sub-parties",  SubPartyMasterViewSet, basename="sub-party")
router.register(r"products",     ProductMasterViewSet,  basename="product")
router.register(r"order-items",  OrderItemViewset,    basename="order-item")
router.register(r"orders",       OrdersViewSet,         basename="order")

urlpatterns = router.urls