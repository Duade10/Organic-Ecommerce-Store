from django.shortcuts import render
from products.models import Product


def home(request):
    products = Product.objects.all()
    featured_products = products.filter(featured=True)[:8]
    top_rated_products = products.order_by("-average_rating")
    context = {"products": featured_products, "top_rated_products": top_rated_products}
    return render(request, "core/index.html", context)


def about(request):
    return render(request, "core/about.html")
