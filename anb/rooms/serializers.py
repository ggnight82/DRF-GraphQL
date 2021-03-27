from rest_framework import serializers
from .models import Room
from users.serializers import RoomUserSerializers
class RoomSerializer(serializers.ModelSerializer):

    user = RoomUserSerializers()

    class Meta:
        model = Room
        fields = ("name", "price", "instant_book", "user")