from rest_framework import serializers
from .models import Room
from users.serializers import RoomUserSerializers

class RoomSerializer(serializers.ModelSerializer):

    user = RoomUserSerializers()

    class Meta:
        model = Room
        fields = ("pk", "name", "price", "instant_book", "user")

class DetailRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = "__all__"