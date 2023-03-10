from django.db import models
from core.models import AbstractTimeStampModel


class Wishlist(AbstractTimeStampModel):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE, related_name="wishlist")
    product = models.ManyToManyField("products.Product")

    def __str__(self):
        return f"{self.user.get_full_name()} -  Wishlist"
