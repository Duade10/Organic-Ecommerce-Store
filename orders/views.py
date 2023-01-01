import datetime
from django.shortcuts import redirect, render
from django.conf import settings
from carts import models as cart_models
from . import forms, models
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import OrderSerializer


class OrderDetail(APIView):
    def post(self, request):
        order_id = request.data["order_id"]
        order = models.Order.objects.get(id=order_id)
        if order.is_ordered:
            public_key = {}
        else:
            public_key = settings.PAYSTACK_PUBLIC_KEY
        serializer = OrderSerializer(order)
        data = {"serializer": serializer.data, "public_key": public_key}
        return Response(data, status=status.HTTP_200_OK)


def place_order(request, quantity=0, total=0):
    user = request.user
    cart_items = cart_models.CartItem.objects.filter(user=user, is_active=True)
    if cart_items.count() <= 0:
        return redirect("store")
    tax = 0
    grand_total = 0
    for cart_item in cart_items:
        total += round(cart_item.product.price * cart_item.quantity, 2)
        quantity += cart_item.quantity
        tax = round((2 * total) / 100, 2)
        grand_total = tax + total
    form = forms.OrderForm(request.POST or None)
    if form.is_valid():
        data = form.save()
        data.user
        data.tax = tax
        data.order_total = grand_total
        data.user = user
        data.ip = request.META.get("REMOTE_ADDR")
        data.save()
        # Generate order number
        yr = int(datetime.date.today().strftime("%Y"))
        dt = int(datetime.date.today().strftime("%d"))
        mt = int(datetime.date.today().strftime("%m"))
        d = datetime.date(yr, mt, dt)
        current_date = d.strftime("%Y%m%d")  # 20210305
        order_number = current_date + str(data.pk)
        data.order_number = order_number
        data.save()

        order = models.Order.objects.get(user=user, is_ordered=False, order_number=order_number)
        context = {
            "order": order,
            "cart_items": cart_items,
            "total": total,
            "tax": tax,
            "grand_total": grand_total,
        }
        return render(request, "orders/payments.html", context)


def make_payment(request, id):
    url = request.META.get("HTTP_REFERER")
    if url is None:
        url = "core:home"
    order = models.Order.objects.get(id=id)
    if order.payment_method == models.Payment.PAYPAL:
        order.make_paypal_payment()
    elif order.payment_method == models.Payment.PAYSTACK:
        pass
    return redirect(url)


class MakePayment(APIView):
    def post(self, request):
        data = request.data
        order_number = data["order_number"]
        order_data = {}
        order = models.Order.objects.get(order_number=order_number)
        if order.payment_method == models.Payment.PAYPAL:
            pass
        elif order.payment_method == models.Payment.PAYSTACK:
            order_data = order.make_paypal_payment()
        return Response(order_data, status=status.HTTP_200_OK)


def receipt(request, order_number):
    order = models.Order.objects.get(order_number=order_number)
    ordered_products = models.OrderProduct.objects.filter(order=order)
    payment = models.Payment.objects.get(payment_id=order.order_number)
    if payment.status == "Pending":
        if payment.payment_method == models.Payment.PAYSTACK:
            payment.verify_paystack_payment()

    sub_total = 0
    for i in ordered_products:
        sub_total += i.product.price * i.quantity

    context = {
        "order": order,
        "ordered_products": ordered_products,
        "payment": payment,
        "sub_total": sub_total,
    }

    return render(request, "orders/order_complete.html", context)
