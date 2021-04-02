from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("",views.NewUserView.as_view()),
    path("me/",views.MyProfileView.as_view()),
    path("me/favs",views.MyFavsView.as_view()),
    path("<int:pk>/",views.user_detail)
]
