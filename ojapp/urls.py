from django.contrib import admin
from django.urls import path
from ojapp import views

urlpatterns = [
    path("",views.index,name='home'),
    path("problem1",views.problem1,name='problem1')
]
