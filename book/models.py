from django.db import models
import uuid

book_types = (('Kryminał', "Kryminał"),
              ("Dramat", "Dramat"),
              ("Pamiętnik", "Pamiętnik"),
              ("Romans", "Romans"),
              ("Dla dzieci", "Dla dzieci"),
              ("Fantasy", "Fantasy"),
              ("Horror", "Horror"),
              ("Sci-Fi", "Sci-Fi"),
              ("Powieść historyczna", "Powieść historyczna"),
              ("Bibliografia", "Bibliografia"),
              ("Reportaż", "Reportaż"),
              ("Powieść młodzieżowa", "Powieść młodzieżowa"),
              ("Poradnik", "Poradnik"),
              ("Kucharska", "Kucharska"))


class Book(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=70, blank=False, unique=True)
    type = models.CharField(choices=book_types, max_length=150)
    publishing_house = models.ForeignKey('publishing_house.PublishingHouse', on_delete=models.CASCADE, null=True,
                                         blank=True)
    bookstores = models.ManyToManyField('bookstore.Bookstore', blank=True)

    def __str__(self):
        return self.name
