from django.urls import path
from . import views
urlpatterns = [
    path('',views.loginpage,name="loginpage"),
    path('login/',views.registerpage,name="register"),
    path('home/',views.home,name="home"),
    path("logout/", views.logoutpage, name="logout"),
]
