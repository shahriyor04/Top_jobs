from django.urls import path
from . import views

urlpatterns = [
    path('', views.room, name='index'),
    path('room/<int:pk>/', views.message, name='room'),
]
