from typing import List
from django.db import transaction
from rest_framework import serializers

from .models import Order, OrderItem
from catalog.models import Product


class OrderItemInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "unit_price_cents", "product_name"]
        read_only_fields = ["id", "unit_price_cents", "product_name"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "status", "total_cents", "created_at", "updated_at", "items"]
        read_only_fields = ["id", "total_cents", "created_at", "updated_at", "items"]


class CreateOrderSerializer(serializers.Serializer):
    items: List[OrderItemInputSerializer] = OrderItemInputSerializer(many=True)

    def validate(self, attrs):
        items = attrs.get("items", [])
        if not items:
            raise serializers.ValidationError("Order must contain at least one item")
        product_ids = [i["product_id"] for i in items]
        products = {p.id: p for p in Product.objects.filter(id__in=product_ids, is_available=True)}
        if len(products) != len(set(product_ids)):
            raise serializers.ValidationError("One or more products are invalid or unavailable")
        for i in items:
            if i["quantity"] <= 0:
                raise serializers.ValidationError("Quantity must be positive")
        attrs["_products"] = products
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user
        items = validated_data["items"]
        products = validated_data["_products"]
        order = Order.objects.create(user=user)
        total = 0
        order_items = []
        for i in items:
            product = products[i["product_id"]]
            unit_price = product.price_cents
            total += unit_price * i["quantity"]
            order_items.append(
                OrderItem(
                    order=order,
                    product=product,
                    quantity=i["quantity"],
                    unit_price_cents=unit_price,
                    product_name=product.name,
                )
            )
        OrderItem.objects.bulk_create(order_items)
        order.total_cents = total
        order.save(update_fields=["total_cents"])
        return order
