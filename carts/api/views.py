import math
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CartItemSerializer
from carts import models, views
from wishlists import models as wishlists_models
from products.models import Product
from products.api.serializers import ProductSerializer


class CartException(Exception):
    pass


@api_view(["GET"])
def cart_items_count(request, cart_items_count=0):
    if request.user.is_authenticated:
        cart_items = models.CartItem.objects.filter(user=request.user)
    else:
        cart_items = models.CartItem.objects.filter(cart=views._cart_id(request))
    for cart_item in cart_items:
        cart_items_count += cart_item.quantity
    return Response({"cart_items_count": cart_items_count})


class CartData(APIView):
    def get(self, request):
        total = 0
        quantity = 0
        tax = 0
        grand_total = 0
        wishlist_count = 0
        cart_items_count = 0
        try:
            user = request.user
            if user.is_authenticated:
                cart_items = models.CartItem.objects.filter(user=user, is_active=True)
                try:
                    wishlist = wishlists_models.Wishlist.objects.get(user=user)
                    wishlist_count = wishlist.product.count()
                except wishlists_models.Wishlist.DoesNotExist:
                    pass
            else:
                cart = models.Cart.objects.get(cart_id=views._cart_id(request))
                cart_items = models.CartItem.objects.filter(cart=cart, is_active=True)

            for cart_item in cart_items:
                total += cart_item.product.price * cart_item.quantity
                quantity += cart_item.quantity
                cart_items_count += cart_item.quantity
            if cart_items_count > 0:
                tax = (2 * total) / 100
                grand_total = tax + int(total)
            request_status = status.HTTP_200_OK
        except CartException:
            request_status = status.HTTP_400_BAD_REQUEST
        data = {
            "cart_items_count": cart_items_count,
            "tax": math.ceil(tax),
            "grand_total": math.ceil(grand_total),
            "quantity": quantity,
            "sub_total": math.ceil(total),
            "wishlist_count": wishlist_count,
        }
        return Response(data, status=request_status)


class AddToCart(APIView):
    def get(self, request, product_id, value=None, *args, **kwargs):
        try:
            user = request.user
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise CartException

            if user.is_authenticated:
                cart_item, created = models.CartItem.objects.get_or_create(product=product, user=user, is_active=True)
                if value is not None:
                    cart_item.quantity = value
                    cart_item.save()
                    request_status = status.HTTP_202_ACCEPTED
                else:
                    cart_item.quantity += 1
                    cart_item.save()
                    request_status = status.HTTP_201_CREATED
                cart_items = models.CartItem.objects.filter(user=user, is_active=True)
            else:
                cart, created = models.Cart.objects.get_or_create(cart_id=views._cart_id(request))
                cart_item, created = models.CartItem.objects.get_or_create(product=product, cart=cart, is_active=True)
                if value is not None:
                    cart_item.quantity = value
                    cart_item.save()
                    request_status = status.HTTP_202_ACCEPTED
                else:
                    cart_item.quantity += 1
                    cart_item.save()
                    request_status = status.HTTP_200_OK
                cart_items = models.CartItem.objects.filter(cart=cart, is_active=True)
            serializer = CartItemSerializer(cart_items, many=True)
            response = serializer.data
        except CartException:
            response = {"message": "Error Bad Request"}
            request_status = status.HTTP_400_BAD_REQUEST
        return Response(response, status=request_status)


class RemoveFromCart(APIView):
    def get(self, request, product_id):
        try:
            user = request.user
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise CartException
            if user.is_authenticated:
                try:
                    cart_item = models.CartItem.objects.get(product=product, user=user, is_active=True)
                    cart_items = models.CartItem.objects.filter(user=user, is_active=True)
                except models.CartItem.DoesNotExist:
                    raise CartException
            else:
                cart = models.Cart.objects.get(cart_id=views._cart_id(request))
                try:
                    cart_item = models.CartItem.objects.get(product=product, cart=cart, is_active=True)
                    cart_items = models.CartItem.objects.filter(cart=cart, is_active=True)
                except models.CartItem.DoesNotExist:
                    raise CartException
            if cart_item:
                if int(cart_item.quantity) > 0:
                    cart_item.quantity -= 1
                    cart_item.save()
                elif int(cart_item.quantity):
                    cart_item.delete()
            serializer = CartItemSerializer(cart_items, many=True)
            response = serializer.data
            request_status = status.HTTP_200_OK
        except CartException:
            request_status = status.HTTP_400_BAD_REQUEST
            response = {"message": "Error Bad Request"}
        return Response(response, status=request_status)


class RemoveCartItem(APIView):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        try:
            if request.user.is_authenticated:
                try:
                    cart_item = models.CartItem.objects.get(product=product, user=request.user, is_active=True)
                    cart_item.delete()
                    cart_items = models.CartItem.objects.filter(user=request.user, is_active=True)
                except models.CartItem.DoesNotExist:
                    raise CartException
            else:
                try:
                    cart = models.Cart.objects.get(cart_id=views._cart_id(request))
                    cart_item = models.CartItem.objects.get(product=product, cart=cart, is_active=True)
                    cart_item.delete()
                    cart_items = models.CartItem.objects.filter(cart=cart, is_active=True)
                except models.CartItem.DoesNotExist:
                    raise CartException
            serializer = CartItemSerializer(cart_items, many=True)
            response = serializer.data
            request_status = status.HTTP_200_OK
        except CartException:
            request_status = status.HTTP_400_BAD_REQUEST
            response = {"message": "Bad request"}
        return Response(response, status=request_status)


class CartList(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            cart_items = models.CartItem.objects.filter(user=user, is_active=True)
        else:
            cart = models.Cart.objects.get(cart_id=views._cart_id(request))
            cart_items = models.CartItem.objects.filter(cart=cart, is_active=True)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
