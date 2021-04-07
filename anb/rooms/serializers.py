from rest_framework import serializers
from .models import Room
from users.serializers import UserSerializers


class RoomSerializer(serializers.ModelSerializer):
    
    user = UserSerializers()
    is_fav = serializers.SerializerMethodField()

    class Meta:
        model = Room
        exclude = ['modified']
        read_only_fields = [
            'user',
            'id',
            'created',
            'updated'
        ]

    
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
    
    def get_is_fav(self, obj):
        request = self.context.get('request')
        if request :
            user = request.user
            if user.is_authenticated:
                return obj in user.favs.all()
        return False



class DetailRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = "__all__"