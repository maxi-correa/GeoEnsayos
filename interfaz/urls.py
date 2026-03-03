from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/tecnico/', views.dashboard_tecnico, name='dashboard_tecnico'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path('obras/crear/', views.crear_obra, name='crear_obra'),
    path("obras/<int:pk>/editar-modal/", views.editar_obra_modal, name="editar_obra_modal"),
    path('contratistas/', views.lista_contratistas, name='lista_contratistas'),
]