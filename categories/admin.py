from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "get_products_count"]

    def get_products_count(self, obj):
        return obj.products.count()

    get_products_count.short_description = "Total Product Count"
