from django.contrib import admin
from django.urls import path
from ojapp import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path("",views.index,name='home'),
    path("dashboard",views.dashboard,name="dashboard"),
    path("login",LoginView.as_view(),name="login_url"),
    path("register",views.register,name="register"),
    path("logout",LogoutView.as_view(),name="logout"),
    path("problem1",views.problem1,name='problem1')
]
