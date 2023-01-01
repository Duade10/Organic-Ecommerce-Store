import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from carts.api.serializers import CartItemSerializer
from products.api.serializers import ProductSerializer
from products.models import Product
from wishlists.models import Wishlist

from .models import Cart, CartItem


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def remove_cart_item(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(cart=cart, product=product, is_active=True)
        cart_item.delete()
    except:
        pass
    return JsonResponse({}, status=201)


def cart(request, *args, **kwargs):
    if request.is_ajax():
        if request.method == "GET":
            return redirect("carts_api:cart_list")
        elif request.method == "POST":
            json_body = json.loads(request.body)
            product_id = json_body.get("product_id", None)
            action = json_body.get("action", None)
            value = json_body.get("value", None)
            print(action)
            if action == "add":
                return redirect("carts_api:add_to_cart", product_id)
            elif action == "remove":
                return redirect("carts_api:remove_from_cart", product_id)
            elif action == "value":
                print(value)
                return redirect("carts_api:add_to_cart_value", product_id, value)
            elif action == "delete":
                return redirect("carts_api:delete_cart", product_id)
    return render(request, "carts/cart.html")


@login_required(login_url="users:login")
def checkout(request):
    url = request.META.get("HTTP_REFERER")
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            if cart_items.count() <= 0:
                return redirect(url)
            context = {"cart_items": cart_items}
    except CartItem.DoesNotExist:
        context = {}
        return redirect(url)
    return render(request, "carts/checkout.html", context)
