from django.db import models
from django.urls import reverse
from core.models import AbstractTimeStampModel
from django.utils.text import slugify


class Category(AbstractTimeStampModel):
    image = models.ImageField(upload_to="uploads/categories/", null=True, blank=True)
    name = models.CharField(max_length=30)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def get_absolute_url(self):
        return reverse("categories:products", kwargs={"category_slug": self.slug})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = str.capitalize(self.name)
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
