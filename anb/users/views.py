import jwt
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rooms.models import Room
from .models import User
from .serializers import NewAccountSerializers,UserSerializers,ReadUserSerializer, CreateUserSerializer
from rooms.serializers import RoomSerializer
from django.shortcuts import get_object_or_404


class NewUserView(APIView):

    def post(self, request):
        serializer = NewAccountSerializers(data=request.data)
        if serializer.is_valid():
            new_account = serializer.save()
            return Response(NewAccountSerializers(new_account).data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class MyProfileView(APIView):

    permission_classes= [IsAuthenticated]

    def get(self, request):
        if request.user.is_authenticated:
            return Response(data=ReadUserSerializer(request.user).data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        
        serializer = CreateUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response()
        
class MyFavsView(APIView):

    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        serializer = RoomSerializer(user.favs.all(),many=True).data
        return Response(serializer)
    def put(self, request):
        user = request.user
        id = request.data.get("id",None)
        if id is not None:
            try:
                room = Room.objects.get(pk=id)
                if room in user.favs.all():
                    user.favs.remove(room)
                else:
                    user.favs.add(room)
                return Response(data=RoomSerializer(user.favs.all(),many=True).data)
            except Room.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else :
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def user_detail(request,pk):
    try:
        user = User.objects.get(pk=pk)
        return Response(data=ReadUserSerializer(user).data,status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    login_try_user = authenticate(username=username,password=password)
    if login_try_user is not None:
        encoded_jwt = jwt.encode(
                {'id':login_try_user.pk},settings.SECRET_KEY,algorithm="HS256"
            )
        return Response(data={'token':encoded_jwt})
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    