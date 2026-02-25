from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_tecnico, name='dashboard_tecnico'),
    path('dashboard/', views.dashboard_tecnico, name='dashboard_tecnico'),
]