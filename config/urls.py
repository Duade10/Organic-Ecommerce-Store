"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

normal_urls = [
    path("admin/", admin.site.urls),
    path("", include("core.urls", namespace="core")),
    path("accounts/", include("users.urls", namespace="users")),
    path("store/", include("store.urls", namespace="store")),
    path("carts/", include("carts.urls", namespace="carts")),
    path("orders/", include("orders.urls", namespace="orders")),
    path("wishlists/", include("wishlists.urls", namespace="wishlists")),
    path("contacts/", include("contacts.urls", namespace="contacts")),
    path("category/", include("categories.urls", namespace="categories")),
]

api_urls = [
    path("api/contacts/", include("contacts.api.urls", namespace="contacts_api")),
    path("api/categories/", include("categories.api.urls", namespace="categories_api")),
    path("api/products/", include("products.api.urls", namespace="products_api")),
    path("api/carts/", include("carts.api.urls", namespace="carts_api")),
    path("api/reviews/", include("reviews.api.urls", namespace="reviews_api")),
]


urlpatterns = normal_urls + api_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
