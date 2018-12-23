from django.contrib import admin
from django.urls import path
from mastermind import views

urlpatterns = [
    path('games/', views.games, name='games'),
    path('games/<int:pk>/move/', views.make_move, name='make_move'),
]
