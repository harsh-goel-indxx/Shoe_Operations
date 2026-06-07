# serializers.py
from rest_framework import serializers
from .models import (
    Party_Master, Sub_Party_Master, Color,
    Product_Master, OrderItem, Orders
)


# ── Color ──────────────────────────────────────────────────────────────
class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Color
        fields = ["name", "id"]


# ── Sub Party Master ───────────────────────────────────────────────────
class SubPartyMasterSerializer(serializers.ModelSerializer):
    parent_party_name = serializers.CharField(
        source="parent_party.name",
        read_only=True
    )

    class Meta:
        model  = Sub_Party_Master
        fields = ["id", "name", "parent_party", "parent_party_name",
                  "transport", "marka", "station"]


# ── Party Master ───────────────────────────────────────────────────────
class PartyMasterSerializer(serializers.ModelSerializer):
    sub_parties = serializers.PrimaryKeyRelatedField(
                        many=True,
                        read_only=True)
    
    class Meta:
        model  = Party_Master
        fields = ["id", "name", "whatsapp_number", "transport", "station", "sub_parties", "marka"]


# ── Sub Party Master ───────────────────────────────────────────────────
class SubPartyMasterSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Sub_Party_Master
        fields = ["id", "name", "parent_party",
                  "transport", "marka", "station"]


# ── Product Master ─────────────────────────────────────────────────────
class ProductMasterSerializer(serializers.ModelSerializer):
    colors          = ColorSerializer(many=True, read_only=True, source="color")
    color_ids       = serializers.PrimaryKeyRelatedField(
                            queryset=Color.objects.all(),
                            many=True,
                            write_only=True,
                            source="color"
                      )


    class Meta:
        model  = Product_Master
        fields = ["id", "name", "size_min", "size_max",
                  "colors", "color_ids", "packing",
                  "opening_balance"]

    def create(self, validated_data):
        return self._save_product(validated_data)

    def update(self, instance, validated_data):
        return self._save_product(validated_data, instance)

    def _save_product(self, validated_data, instance=None):
        """Handles both create and update for Product_Master with M2M colors."""
        color_data = validated_data.pop("color", [])

        if instance is None:
            instance = Product_Master.objects.create(**validated_data)
        else:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

        instance.color.set(color_data)
        return Product_Master.objects.prefetch_related("color").get(pk=instance.pk)


# ── Single Order ───────────────────────────────────────────────────────
class OrderItemSerializer(serializers.ModelSerializer):
    color          = ColorSerializer(many=True, read_only=True)
    color_id       = serializers.PrimaryKeyRelatedField(
                            queryset=Color.objects.all(),
                            many=True,
                            write_only=True,
                            source="color"
                      )
    class Meta:
        model  = OrderItem
        fields = ["id", "size_min", "size_max", "quantity",
                  "color", "color_id", "packing", "product", "order"]
        read_only_fields = ["color"]



# ── Orders ─────────────────────────────────────────────────────────────
class OrdersSerializer(serializers.ModelSerializer):
    party_name      = serializers.CharField(source="party.name",     read_only=True)
    sub_party_name  = serializers.CharField(source="sub_party.name", read_only=True)

    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model  = Orders
        fields = ["id", "date", "party", "party_name",
                  "sub_party", "sub_party_name", "transport",
                  "marka", "items"]

    # def create(self, validated_data):
    #     return self._save_order(validated_data)

    # def update(self, instance, validated_data):
    #     return self._save_order(validated_data, instance)






