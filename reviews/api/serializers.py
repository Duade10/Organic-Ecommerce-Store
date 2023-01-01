from reviews.models import Review
from rest_framework import serializers


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["product", "user", "subject", "review", "rating"]

    # def validate(self, data):
    #     if data["product"] == data["user"]:
    #         raise serializers.ValidationError("Name and Description should not be the same")
    #     else:
    #         return data
