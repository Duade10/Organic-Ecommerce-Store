from rest_framework import serializers
from products import models as products_models
from products.api.serializers import ProductSerializer
from . import models


class WishlistSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = models.Wishlist
        fields = "__all__"

    def get_product(self, obj):
        products = obj.product.all()
        serializers = ProductSerializer(products, many=True)
        return serializers.data
