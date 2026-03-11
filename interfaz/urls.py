from django.urls import path
from .views import admin_views, tecnico_views

urlpatterns = [
    # VISTAS PARA ADMINISTRADOR
    path('dashboard/admin/', admin_views.dashboard_admin, name='dashboard_admin'),
    
    path('obras/crear/', admin_views.crear_obra, name='crear_obra'),
    path('obras/<int:pk>/editar/', admin_views.editar_obra, name='editar_obra'),
    
    path('contratistas/', admin_views.lista_contratistas, name='lista_contratistas'),
    path('contratistas/crear/', admin_views.crear_contratista, name='crear_contratista'),
    path('contratistas/<int:pk>/subir-logo/', admin_views.subir_logo_contratista, name='subir_logo_contratista'),
    path('contratistas/<int:pk>/eliminar-logo/', admin_views.eliminar_logo_contratista, name='eliminar_logo_contratista'),
    path('contratistas/<int:pk>/editar/', admin_views.editar_contratista, name='editar_contratista'),
    
    path('usuarios/', admin_views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', admin_views.crear_usuario, name='crear_usuario'),
    path('usuarios/<int:pk>/editar/', admin_views.editar_usuario, name='editar_usuario'),

    path('ubicaciones/', admin_views.lista_ubicaciones, name='lista_ubicaciones'),
    path('ubicaciones/crear/', admin_views.crear_ubicacion, name='crear_ubicacion'),
    path('ubicaciones/<int:pk>/editar/', admin_views.editar_ubicacion, name='editar_ubicacion'),
    
    #VISTAS PARA TÉCNICO
    path('dashboard/tecnico/', tecnico_views.dashboard_tecnico, name='dashboard_tecnico'),
]