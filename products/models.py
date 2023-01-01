from django.db import models
from django.urls import reverse
from core.models import AbstractTimeStampModel
from reviews.models import Review


class Product(AbstractTimeStampModel):
    SINGLE = "singles"
    BASKET = "baskets"

    SOLD_IN_CHOICES = ((SINGLE, "Singles"), (BASKET, "Baskets"))

    name = models.CharField(max_length=50)
    former_price = models.DecimalField(decimal_places=2, max_digits=9, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=9)
    description = models.TextField(null=True, blank=True)
    weight = models.DecimalField(decimal_places=2, max_digits=9)
    in_stock = models.BooleanField(default=True)
    category = models.ManyToManyField("categories.Category", related_name="products")
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to="uploads/product/", null=True, blank=True)
    sold_in = models.CharField(max_length=10, null=True, choices=SOLD_IN_CHOICES)
    average_rating = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

    def is_sale(self):
        result = False
        if self.former_price:
            result = True
        return result

    def get_sale_off_percentage(self):
        # todo: calculate percentage
        if self.former_price is not None:
            price = int(self.price)
            former_price = int(self.former_price)
            percentage = int((price / former_price) * 100)
            sale_off_percentage = 100 - percentage
            return sale_off_percentage

    def averageRating(self):
        reviews = Review.objects.filter(product=self, status=True).aggregate(average=models.Avg("rating"))
        avg = 0
        if reviews["average"] is not None:
            avg = float(reviews["average"])
        return avg

    def countReview(self):
        reviews = Review.objects.filter(product=self, status=True).aggregate(count=models.Count("review"))
        count = 0
        if reviews["count"] is not None:
            count = int(reviews["count"])
        return count

    def save(self, *args, **kwargs):
        self.name = str.capitalize(self.name)
        self.average_rating = self.averageRating()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("store:detail", kwargs={"id": self.pk})

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["-id"]


class ProductImage(AbstractTimeStampModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    file = models.ImageField()

    def __str__(self):
        return f"{self.file.url}"

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
