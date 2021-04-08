from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .models import Room
from .serializers import RoomSerializer ,DetailRoomSerializer

class RoomViewSet(ModelViewSet):
    pass

class hi():
    pass





@api_view(["GET"])
def room_search(request):
    max_price = request.GET.get("max_price", None)
    min_price = request.GET.get("min_price", None)
    beds = request.GET.get("beds", None)
    bedrooms = request.GET.get("bedrooms", None)
    bathrooms = request.GET.get("bathrooms", None)
    lat = request.GET.get('lat',None)
    lng = request.GET.get('lng',None)
    filter_kwargs = {}
    if max_price is not None:
        filter_kwargs["price__lte"] = max_price
    if min_price is not None:
        filter_kwargs["price__gte"] = min_price
    if beds is not None:
        filter_kwargs["beds__gte"] = beds
    if bedrooms is not None:
        filter_kwargs["bedrooms__gte"] = bedrooms
    if bathrooms is not None:
        filter_kwargs["bathrooms__gte"] = bathrooms
    if lat is not None and lng is not None:
        filter_kwargs["lat__gte"] = float(lat) - 0.005
        filter_kwargs["lat__lte"] = float(lat) + 0.005
        filter_kwargs["lng__get"] = float(lng) - 0.005
        filter_kwargs["lng__lte"] = float(lng) + 0.005

    paginator = PageNumberPagination()
    paginator.page_size = 20
    try: 
        rooms = Room.objects.filter(**filter_kwargs)
    except:
        rooms = Room.objects.all()
    results = paginator.paginate_queryset(rooms, request)
    serializer = RoomSerializer(results, many=True)
    return paginator.get_paginated_response(serializer.data)