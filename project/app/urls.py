from django.urls import path
from . import views


app_name = "app"

urlpatterns = [
    path('', views.home, name="home"),
    path('accounts/login/', views.user_login, name="login"),
    path('accounts/signup/', views.signup, name="signup"),
]
