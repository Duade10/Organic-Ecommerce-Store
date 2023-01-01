from rest_framework import serializers
from products.models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            "description",
            "weight",
            "in_stock",
            "category",
            "image",
            "featured",
            "id",
        ]
