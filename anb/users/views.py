from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import User
from .serializers import ReadUserSerializer, CreateUserSerializer


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
            return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)
        return Response()
        


@api_view(["GET"])
def user_detail(request,pk):
    try:
        user = User.objects.get(pk=pk)
        return Response(data=ReadUserSerializer(user).data,status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)