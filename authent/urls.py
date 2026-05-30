from django.urls import path
from . import views
urlpatterns = [
    path('',views.loginpage,name="loginpage"),
    path('login/',views.registerpage,name="register"),
    path('home/',views.home,name="home"),
    path("logout/", views.logoutpage, name="logout"),
    path('edit/<int:id>/',views.edit,name='edit'),
    path('delete/<int:id>/',views.delete,name='delete'),
    path("add/",views.add,name="add_task"),
]
