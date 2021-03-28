from rest_framework import serializers
from .models import Room
from users.serializers import UserSerializers

class RoomSerializer(serializers.ModelSerializer):

    user = UserSerializers()

    class Meta:
        model = Room
        exclude = ("modified",)

class DetailRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = "__all__"