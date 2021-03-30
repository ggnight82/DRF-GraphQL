from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("me/",views.MyProfileView.as_view()),
    path("<int:pk>/",views.user_detail)
]
