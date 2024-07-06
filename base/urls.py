from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('showtables/', views.showtables, name="showtables"),
    path('basic/', views.basic, name="basic"),
    path('moderate/', views.moderate, name="moderate"),
    path('complex/', views.complex, name="complex"),
    path('userprofile/', views.userprofile, name="userprofile"),
    path('login/userprofile/', views.userprofile, name="userprofile"),
    path('logout', views.logout, name="logout")
]