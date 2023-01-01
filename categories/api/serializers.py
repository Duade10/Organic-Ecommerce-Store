from rest_framework import serializers
from categories import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ("name", "id")
