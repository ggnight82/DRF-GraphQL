from django.urls import path
from . import views
 

app_name = "rooms"

urlpatterns = [
   path("list/", views.rooms_view),
   path("<int:pk>/", views.DetailRoomView.as_view())
]
