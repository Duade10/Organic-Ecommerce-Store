from django.db import models
from core.models import AbstractTimeStampModel


class Review(AbstractTimeStampModel):
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    is_edited = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
