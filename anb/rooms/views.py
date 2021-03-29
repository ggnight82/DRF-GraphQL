from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Room
from .serializers import ReadRoomSerializer, CreateRoomSerializer ,DetailRoomSerializer

@api_view(["GET","POST"])
def rooms_view(request):
    if request.method  == "GET":
        rooms = Room.objects.all()
        serializer = ReadRoomSerializer(rooms, many=True).data
        return Response(serializer)

    elif request.method == "POST":
        serializer = CreateRoomSerializer(data = request.data)
        if serializer.is_valid:
            return Response(status=status.HTTP_200_OK)
        else :
            return Response(status=status.HTTP_400_BAD_REQUEST)

class DetailRoomView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = DetailRoomSerializer