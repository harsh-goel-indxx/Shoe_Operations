# views.py
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Party_Master, Sub_Party_Master, Color,
    Product_Master, OrderItem, Orders
)
from .serializers import (
    PartyMasterSerializer, SubPartyMasterSerializer, ColorSerializer,
    ProductMasterSerializer, OrderItemSerializer, OrdersSerializer
)


# ── Color ViewSet ──────────────────────────────────────────────────────
class ColorViewSet(viewsets.ModelViewSet):
    queryset         = Color.objects.all()
    serializer_class = ColorSerializer
    filter_backends  = [filters.SearchFilter]
    search_fields    = ["name"]


# ── Party Master ViewSet ───────────────────────────────────────────────
class PartyMasterViewSet(viewsets.ModelViewSet):
    queryset         = Party_Master.objects.all()
    serializer_class = PartyMasterSerializer
    filter_backends  = [filters.SearchFilter]
    search_fields    = ["name", "whatsapp_number"]

    @action(methods=["GET"], detail=True, url_path="sub-parties")
    def sub_party(self, request , pk=None):
        queryset = Sub_Party_Master.objects.filter(parent_party=pk)
        serializer = SubPartyMasterSerializer(queryset, many=True, read_only=True)
        return Response(serializer.data)



# ── Sub Party Master ViewSet ───────────────────────────────────────────
class SubPartyMasterViewSet(viewsets.ModelViewSet):
    queryset         = Sub_Party_Master.objects.all()
    serializer_class = SubPartyMasterSerializer
    filter_backends  = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = [""]
    search_fields    = ["name", "station"]   


# ── Product Master ViewSet ─────────────────────────────────────────────
class ProductMasterViewSet(viewsets.ModelViewSet):
    queryset         = Product_Master.objects.prefetch_related("color").all()
    serializer_class = ProductMasterSerializer
    filter_backends  = [filters.SearchFilter]
    search_fields    = ["name"]

    @action(detail=True, methods=["get"], url_path="available-colors")
    def get_available_colors(self, request, pk=None):
        """Returns available colors for a specific product."""
        product    = self.get_object()
        serializer = ColorSerializer(product.color.all(), many=True)
        return Response(serializer.data)


# ── Single Order ViewSet ───────────────────────────────────────────────
class OrderItemViewset(viewsets.ModelViewSet):
    queryset         = OrderItem.objects.prefetch_related("color").all()
    serializer_class = OrderItemSerializer
    filter_backends  = [DjangoFilterBackend, filters.SearchFilter]
    search_fields    = ["name"]


# ── Orders ViewSet ─────────────────────────────────────────────────────
class OrdersViewSet(viewsets.ModelViewSet):
    queryset         = Orders.objects.select_related(
                            "party", "sub_party"
                       )
    serializer_class = OrdersSerializer
    filter_backends  = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["party", "sub_party", "date"]
    search_fields    = ["party__name", "marka"]

    @action(detail=True, methods=["get"], url_path="order-items")
    def get_order_items(self, request, pk=None):
        """Returns all product line items for a specific order."""
        order      = self.get_object()
        serializer = OrderItemSerializer(order.product_order.all(), many=True)
        return Response(serializer.data)