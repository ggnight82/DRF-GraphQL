import jwt
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import status
from rooms.models import Room
from .models import User
from .serializers import AccountSerializers,UserSerializers,ReadUserSerializer, CreateUserSerializer
from .permissions import IsSelf
from rooms.serializers import RoomSerializer
from django.shortcuts import get_object_or_404

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AccountSerializers

    def get_permissions(self):
        permission_classes = []
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        elif self.action == 'create' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsSelf]
        return [permission() for permission in permission_classes]

    @action(methods=['post'],detail=False)
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        login_try_user = authenticate(username=username,password=password)
        if login_try_user is not None:
            encoded_jwt = jwt.encode(
                    {'pk':login_try_user.pk},settings.SECRET_KEY,algorithm="HS256"
                )
            return Response(data={'token':encoded_jwt,'id':login_try_user.pk})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

class NewUserView(APIView):

    def post(self, request):
        serializer = AccountSerializers(data=request.data)
        if serializer.is_valid():
            new_account = serializer.save()
            return Response(AccountSerializers(new_account).data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        
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
