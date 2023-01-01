from django.urls import path
from . import views

app_name = "wishlists"


urlpatterns = [
    path("", views.wishlist, name="list"),
    path("toggle/", views.toggle_wishlist, name="toggle_wishlist"),
]
