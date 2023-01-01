from . import models, views


def total_cart_items(request, cart_items_count=0):
    if request.user.is_authenticated:
        cart_items = models.CartItem.objects.filter(user=request.user)
    else:
        try:
            cart = models.Cart.objects.get(cart_id=views._cart_id(request))
        except models.Cart.DoesNotExist:
            cart = models.Cart.objects.create(cart_id=views._cart_id(request))
        cart_items = models.CartItem.objects.filter(cart=cart)
    for cart_item in cart_items:
        cart_items_count += cart_item.quantity
    return dict(cart_items_count=cart_items_count)
