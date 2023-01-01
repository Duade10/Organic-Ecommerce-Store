from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("detail/", views.OrderDetail.as_view(), name="detail"),
    path("place-order/", views.place_order, name="place_order"),
    path("make-payment/", views.MakePayment.as_view(), name="make_payment"),
    path("receipt/<int:order_number>/", views.receipt, name="receipt"),
]
