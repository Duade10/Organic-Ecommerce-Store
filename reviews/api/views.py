from rest_framework import generics, exceptions
from . import serializers
from products.models import Product
from reviews.models import Review


class ReviewList(generics.ListCreateAPIView):
    serializer_class = serializers.ReviewSerializer

    def perform_create(self, serializer):
        user = self.request.user
        product_id = self.kwargs["product_id"]
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise exceptions.ValidationError

        review_exists = Review.objects.filter(user=user, product=product).exists()
        if review_exists:
            review_serializer = serializers.ReviewSerializer(data=serializer.data)
            if review_serializer.is_valid():
                subject = serializer.data["subject"]
                rating = serializer.data["rating"]
                review = serializer.data["review"]
                Review.objects.filter(user=user, product=product).update(subject=subject, rating=rating, review=review)
                product.save()
                review = Review.objects.get(user=user, product=product)
                serializer = serializers.ReviewSerializer(review)
                return serializer.data
        else:
            if serializer.is_valid():
                serializer.save(user=user, product=product)
                product.save()
                return serializer.data
