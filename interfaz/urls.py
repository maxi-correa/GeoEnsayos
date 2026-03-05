from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/tecnico/', views.dashboard_tecnico, name='dashboard_tecnico'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    
    path('obras/crear/', views.crear_obra, name='crear_obra'),
    path("obras/<int:pk>/editar-modal/", views.editar_obra_modal, name="editar_obra_modal"),
    
    path('contratistas/', views.lista_contratistas, name='lista_contratistas'),
    path('contratistas/crear/', views.crear_contratista, name='crear_contratista'),
    path('contratistas/<int:pk>/subir-logo/', views.subir_logo_contratista, name='subir_logo_contratista'),
    path('contratistas/<int:pk>/eliminar-logo/', views.eliminar_logo_contratista, name='eliminar_logo_contratista'),
    path('contratistas/<int:pk>/editar/', views.editar_contratista, name='editar_contratista'),
    
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/<int:pk>/editar/', views.editar_usuario, name='editar_usuario'),
]