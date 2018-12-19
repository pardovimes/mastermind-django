from django.contrib import admin
from django.urls import path
from mastermind import views

urlpatterns = [
    path('', views.index, name='index'),
    path('game/', views.game, name='game'),
]
