from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    avatar = models.ImageField(upload_to="avatars", blank=True)
    superhost = models.BooleanField(default=False)
    favs = models.ManyToManyField("rooms.Room", related_name="favs",)

    def room_count(self):
        return self.rooms.count()

    def __str__(self):
        return self.username
    
    def _get_favs(self):
        return self.name

    room_count.short_description = "Room Count"
