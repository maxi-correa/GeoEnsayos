from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/tecnico/', views.dashboard_tecnico, name='dashboard_tecnico'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin')
]