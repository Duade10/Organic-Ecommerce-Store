from rest_framework import status, views, generics
from rest_framework.response import Response
from . import serializers
from products import models


class ProductListView(views.APIView):
    def get(self, request):
        products = models.Product.objects.all()
        serializer = serializers.ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetailView(views.APIView):
    def get(self, request, id):
        product = models.Product.objects.get(id=id)
        serializer = serializers.ProductSerializer(product)
        return Response(serializer.data)


class ProductEditView(views.APIView):
    def post(self, request, id):
        try:
            product = models.Product.objects.get(id=id)
        except models.Product.DoesNotExist:
            serializer = serializers.ProductSerializer(product, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDeleteView(views.APIView):
    def post(self, request, id):
        try:
            product = models.Product.objects.get(id=id)
        except models.Product.DoesNotExist:
            product.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)


class ProductFilterView(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        featured = self.request.query_params.get("featured", None)
        if featured is not None:
            featured = str.capitalize(featured)
        return models.Product.objects.filter(featured=featured)


class ProductImageListView(views.APIView):
    def get(self, request, id):
        productimages = models.ProductImage.objects.filter(product__id=id)
        serializer = serializers.ProductImageSerializer(productimages, many=True)
        return Response(serializer.data)
