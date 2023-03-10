from django.db import models
import uuid


class Bookstore(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=70, unique=True)
    publishing_houses = models.ManyToManyField('publishing_house.PublishingHouse', blank=True)

    def __str__(self):
        return self.name
