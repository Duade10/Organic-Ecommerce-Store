from django.contrib import admin
from . import models


class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created", "user")
    search_fields = ["name__icontains", "email", "user__first_name__icontains", "user__last_name__icontains"]


admin.site.register(models.Contact, ContactAdmin)
