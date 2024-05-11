from django.urls import path
from . import views


app_name = "app"

urlpatterns = [
    path('', views.home, name="home"),
    path('accounts/login/', views.user_login, name="login"),
    path('accounts/logout/', views.user_logout, name="logout"),
    path('accounts/signup/', views.signup, name="signup"),

    path('user/profile/', views.profile, name="profile"),
    path('user/profile-pic/update/', views.update_profile_pic, name="update_profile_pic"),


    path('room/offer/',views.offer_room, name="offer_room"),
    path('rooms/',views.rooms, name="rooms"),
    path('rooms/delete/<str:room_id>/',views.delete_room, name="delete_room"),
    path('rooms/<str:room_id>/',views.room_detail, name="room_detail"),


    path('rooms/livein/<str:room_id>/',views.live_in, name="live_in"),
    path('rooms/request/<str:room_id>/',views.request_room, name="request_room"),

    path('rooms/search/',views.search, name="search"),

    path('roommates/',views.roommates, name="roommates"),

    path('show_profile/<str:username>/',views.show_profile, name="show_profile"),
]
