from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from .models import Room
from .serializers import ReadRoomSerializer, CreateRoomSerializer ,DetailRoomSerializer


class RoomsView(APIView):
    def get(self,request):
        rooms = Room.objects.all()[:5]
        serializer = ReadRoomSerializer(rooms, many=True).data
        return Response(serializer)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = CreateRoomSerializer(data = request.data)

        if serializer.is_valid():
            room = serializer.save(user=request.user)
            room_serializer = ReadRoomSerializer(room).data
            return Response(data=room_serializer,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    
    
class RoomView(APIView):
    def get_room(self,pk):
        try:
            room = Room.objects.get(pk=pk)
            return room
        except Room.DoesNotExist:
            return None

    def get(self, request,pk):
        room = self.get_room(pk)
        if room is not None:
            serializer = ReadRoomSerializer(room).data
            return Response(data=serializer, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
    def put(self, request,pk):
        room = self.get_room(pk)
        if room is not None:
            if room.user != request.user:
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
            serializer = CreateRoomSerializer(room,data=request.data,partial=True)
            if serializer.is_valid():
                room = serializer.save()
                return Response(data=ReadRoomSerializer(room).data,status=status.HTTP_200_OK)
            else :
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            return Response(data=serializer,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
    def delete(self, request,pk):
        room = self.get_room(pk)
        if room.user != request.user:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if room is not None:
            room.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)