from rest_framework import serializers
from .models import Room
from users.serializers import UserSerializers

class ReadRoomSerializer(serializers.ModelSerializer):

    user = UserSerializers()

    class Meta:
        model = Room
        exclude = ("modified",)

class CreateRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        exclude = ("user", "modified", "created")

    
    def validate(self, data):
        if self.instance:
            check_in = data.get("check_in",self.instance.check_in)
            check_out = data.get("check_out",self.instance.check_out)
        else:
            check_in = data.get("check_in")
            check_out = data.get("check_out")
        if check_in == check_out:
            raise serializers.ValidationError("Check your 'check in' and 'check out' once again")
        return data



class DetailRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = "__all__"