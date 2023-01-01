from . import models


def lastest_products_dict(request):
    products = models.Product.objects.order_by("-id")
    latest_product1 = products[:3]
    latest_product2 = products[3:6]
    return dict(latest_products1=latest_product1, latest_products2=latest_product2)
