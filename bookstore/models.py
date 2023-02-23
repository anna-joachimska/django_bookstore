from django.db import models
import uuid
# from book.models import *
# from publishing_house.models import *

class Bookstore(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=70, blank=False,unique=True)
    books = models.ManyToManyField('book.Book', blank=True, unique=False)
    publishing_houses = models.ManyToManyField('publishing_house.PublishingHouse', blank=True, unique=False)

    def __str__(self):
        return self.name