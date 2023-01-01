from rest_framework import serializers
from carts.models import Cart, CartItem
from products.api.serializers import ProductSerializer


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    sub_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = "__all__"

    def get_sub_total(self, data):
        return data.product.price * data.quantity
