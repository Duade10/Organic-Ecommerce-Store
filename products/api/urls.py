from django.urls import path
from . import views


app_name = "products_api"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="list"),
    path("<int:id>/", views.ProductDetailView.as_view(), name="detail"),
    path("<int:id>/images/", views.ProductImageListView.as_view(), name="list"),
    path("filter/", views.ProductFilterView.as_view(), name="filter")
]
