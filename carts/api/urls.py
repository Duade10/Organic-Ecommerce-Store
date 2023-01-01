from django.urls import path
from . import views

app_name = "carts_api"

urlpatterns = [
    path("cart-list/", views.CartList.as_view(), name="cart_list"),
    path("carts-data/", views.CartData.as_view(), name="cart_data"),
    path("add-to-cart/<int:product_id>/", views.AddToCart.as_view(), name="add_to_cart"),
    path("add-to-cart-value/<int:product_id>/<int:value>", views.AddToCart.as_view(), name="add_to_cart_value"),
    path("remove-from-cart/<int:product_id>", views.RemoveFromCart.as_view(), name="remove_from_cart"),
    path("delete-cart/<int:product_id>/", views.RemoveCartItem.as_view(), name="delete_cart"),
]
