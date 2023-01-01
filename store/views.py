import random
from django.shortcuts import render, redirect
from products import models as product_models
from orders.models import OrderProduct
from django.core.paginator import Paginator


def store(request):
    data = request.GET or None
    filter_args = {}
    if data is not None:
        name = data.get("name")
        try:
            minimum_amount = int(str(data.get("minamount")).replace("#", ""))
            maximum_amount = int(str(data.get("maxamount")).replace("#", ""))
            filter_args["price__gte"] = minimum_amount
            filter_args["price__lte"] = maximum_amount
        except ValueError:
            pass
        if name is not None:
            filter_args["name__icontains"] = name
        products = product_models.Product.objects.filter(**filter_args)
    else:
        products = product_models.Product.objects.all()
    try:
        minimum_price = min(products.values_list("price", flat=True))
        maximum_price = max(products.values_list("price", flat=True))
    except ValueError:
        minimum_price = 0
        maximum_price = 0
    product_count = products.count()
    paginator = Paginator(products, 12, orphans=2)
    page = request.GET.get("page", 1)
    products = paginator.get_page(page)
    context = {
        "products": products,
        "product_count": product_count,
        "minimum_price": int(minimum_price),
        "maximum_price": int(maximum_price),
    }
    return render(request, "store/store.html", context)


def product_detail(request, id):
    refer_url = request.META.get("HTTP_REFERER", None)
    review_permission = False
    try:
        product = product_models.Product.objects.get(id=id)
        cat = None
        for cat in product.category.all():
            cat = cat
        related_products = product_models.Product.objects.filter(category=cat).exclude(pk=product.pk)
        if len(related_products) >= 4:
            related_products = random.sample(list(related_products), 4)

        if request.user.is_authenticated:
            ordered_product_exist = OrderProduct.objects.filter(user=request.user, product=product).exists()
            if ordered_product_exist:
                review_permission = True
    except product_models.Product.DoesNotExist:
        # todo: add message here
        if refer_url is not None:
            return redirect(refer_url)
        return redirect("core:home")
    context = {"product": product, "related_products": related_products, "review_permission": review_permission}
    return render(request, "store/product-detail.html", context)
