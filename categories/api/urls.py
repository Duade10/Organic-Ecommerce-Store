from django.urls import path
from . import views

app_name = "categories_api"

urlpatterns = [
    path("", views.category_list_api, name="list"),
    path("<int:id>/", views.category_detail_api, name="detail"),
    path("create/", views.category_create_api, name="create"),
    path("edit/<int:id>/", views.category_edit_api, name="edit"),
    path("delete/<int:id>/", views.category_delete_api, name="delete"),
]
