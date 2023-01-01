import random
from . import models


def categories_dict(request):
    categories = models.Category.objects.all()
    return dict(categories=categories)
