from django.db import models
import uuid


class PublishingHouse(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=70, unique=True)

    def __str__(self):
        return self.name
