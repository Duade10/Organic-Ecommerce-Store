from django.shortcuts import render
from products.models import Product
from . import models


def categories(request, category_slug):
    products = None
    product_count = 0
    minimum_price = 0
    maximum_price = 0
    try:
        category = models.Category.objects.get(slug=category_slug)
        products = Product.objects.filter(category=category)
        try:
            minimum_price = min(products.values_list("price", flat=True))
            maximum_price = max(products.values_list("price", flat=True))
        except ValueError:
            minimum_price = 0
            maximum_price = 0
        product_count = products.count()

    except models.Category.DoesNotExist:
        pass
    context = {
        "products": products,
        "product_count": product_count,
        "minimum_price": int(minimum_price),
        "maximum_price": int(maximum_price),
    }
    return render(request, "store/store.html", context)
