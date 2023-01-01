from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.store, name="store"),
    path("<int:id>/", views.product_detail, name="detail"),
]
