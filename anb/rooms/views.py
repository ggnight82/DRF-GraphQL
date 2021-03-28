from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from .models import Room
from .serializers import RoomSerializer, DetailRoomSerializer

class ListRoomsView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class DetailRoomView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = DetailRoomSerializer