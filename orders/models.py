import requests
from django.db import models
from django.conf import settings
from django.urls import reverse

from users.models import User
from products.models import Product

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from core.models import AbstractTimeStampModel
from carts.models import CartItem


class Payment(AbstractTimeStampModel):
    PAYPAL = "paypal"
    PAYSTACK = "paystack"

    PAYMENT_CHOICES = (
        (PAYPAL, "PayPal"),
        (PAYSTACK, "PayStack"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    gateway_ref = models.CharField(max_length=100, null=True)
    payment_method = models.CharField(max_length=8, choices=PAYMENT_CHOICES, null=True, blank=True)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def verify_paystack_payment(self):
        url = f"https://api.paystack.co/transaction/verify/{self.payment_id}"
        headers = {"authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        request = requests.get(url, headers=headers)
        response = request.json()
        if response["data"]["status"] == "success":
            status = response["data"]["status"]
            amount = response["data"]["amount"]
            self.status = status
            self.amount_paid = amount
            self.save()

    def __str__(self):
        return self.payment_id


class OrderProduct(AbstractTimeStampModel):
    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name


class Order(AbstractTimeStampModel):
    STATUS = (
        ("New", "New"),
        ("Accepted", "Accepted"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=200)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField(null=True, blank=True)
    tax = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default="New")
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delivering = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    on_delivery = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=8, choices=Payment.PAYMENT_CHOICES, null=True)

    def make_paypal_payment(self):
        amount = self.order_total
        order_number = self.order_number
        user = self.user
        payment = Payment.objects.create(
            user=user,
            gateway_ref=None,
            payment_id=order_number,
            payment_method=self.payment_method,
            status="Pending",
            amount_paid=amount,
        )
        payment.verify_paystack_payment()
        cart_items = CartItem.objects.filter(user=user, is_active=True)
        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order = self
            orderproduct.payment = payment
            orderproduct.user = self.user
            orderproduct.product = item.product
            orderproduct.quantity = item.quantity
            orderproduct.product_price = float(item.product.price)
            orderproduct.ordered = True
            orderproduct.save()
            orderproduct.save()
        CartItem.objects.filter(user=user).delete()
        self.payment = payment
        self.is_ordered = True
        self.save()

    def get_make_payment_url(self):
        return reverse("orders:make_payment", kwargs={"id": self.pk})

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def full_address(self):
        return f"{self.address_line_1}, {self.address_line_2}"

    def __str__(self):
        return self.order_number

    def order_made(self):
        mail_subject = "An order has been made"
        message = render_to_string(
            "orders/order_made.html",
        )

        to_email = "paulicytop@gmail.com"
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()
