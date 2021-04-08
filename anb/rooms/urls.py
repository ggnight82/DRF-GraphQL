from django.urls import path
from . import views 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("",views.RoomViewSet)

app_name = "rooms"

urlpatterns = router.urls
