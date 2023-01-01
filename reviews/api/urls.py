from django.urls import path
from . import views

app_name = "reviews_api"

urlpatterns = [
    path("<int:product_id>/", views.ReviewList.as_view(), name="list"),
]
