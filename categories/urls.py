from django.urls import path
from . import views

app_name = "categories"

urlpatterns = [
    path("product/<str:category_slug>", views.categories, name="products"),
]
