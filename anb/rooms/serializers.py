from rest_framework import serializers
from .models import Room
from users.serializers import UserSerializers

class ReadRoomSerializer(serializers.ModelSerializer):

    user = UserSerializers()

    class Meta:
        model = Room
        exclude = ("modified",)

class CreateRoomSerializer(serializers.Serializer):


    name = serializers.CharField(max_length=140)
    address = serializers.CharField(max_length=140)
    price = serializers.IntegerField()
    beds = serializers.IntegerField(default=1)
    lat = serializers.DecimalField(max_digits=10, decimal_places=6)
    lng = serializers.DecimalField(max_digits=10, decimal_places=6)
    bedrooms = serializers.IntegerField(default=1)
    bathrooms = serializers.IntegerField(default=1)
    check_in = serializers.TimeField(default="00:00:00")
    check_out = serializers.TimeField(default="00:00:00")
    instant_book = serializers.BooleanField(default=False)

    
class DetailRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = "__all__"