from django.db import models
from core.models import AbstractTimeStampModel


class Contact(AbstractTimeStampModel):
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=65)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name
