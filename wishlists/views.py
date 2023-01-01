from django.shortcuts import render
from . import models, serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from products import models as products_models
from django.contrib.auth.decorators import login_required


@api_view(["POST"])
def toggle_wishlist(request):
    user = request.user
    data = request.data
    product_id = data["product_id"]
    product = products_models.Product.objects.get(id=product_id)
    if user.is_authenticated:
        try:
            wishlist = models.Wishlist.objects.get(user=user)
        except models.Wishlist.DoesNotExist:
            wishlist = models.Wishlist.objects.create(user=user)
        if product in wishlist.product.all():
            wishlist.product.remove(product)
            request_status = status.HTTP_204_NO_CONTENT
        else:
            wishlist.product.add(product)
            request_status = status.HTTP_201_CREATED
        wishlist.save()
        serializer = serializers.WishlistSerializer(wishlist)
        data = serializer.data
    else:
        data = {}
        request_status = status.HTTP_401_UNAUTHORIZED
    return Response(data, status=request_status)


@login_required(login_url="users:login")
def wishlist(request):
    products = request.user.wishlist.product.all()
    product_count = products.count()
    context = {"products": products, "product_count": product_count}
    return render(request, "store/store.html", context)
