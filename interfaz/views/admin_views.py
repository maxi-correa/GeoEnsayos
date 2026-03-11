import json
from pyexpat.errors import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Count
from core.models import Perfil
from ensayos.models import Obra, Contratista, Ubicacion
from ..forms import ObraForm, ContratistaForm
from ..decorators import rol_requerido
from ..utils import obtener_dashboard_por_rol

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy(obtener_dashboard_por_rol(self.request.user))

@login_required
@rol_requerido("admin", "consulta")
def dashboard_admin(request):

    empresa = request.user.perfil.empresa

    # OBRAS ACTIVAS
    obras_activas_list = (
        Obra.objects
        .filter(activa=True, empresa=empresa)
        .annotate(cantidad_ensayos=Count('muestra__ensayos'))
        .order_by('nombre')
    )

    paginator_activas = Paginator(obras_activas_list, 5)
    page_activas = request.GET.get("page_activas")
    obras_activas = paginator_activas.get_page(page_activas)


    # OBRAS FINALIZADAS
    obras_finalizadas_list = (
        Obra.objects
        .filter(activa=False, empresa=empresa)
        .annotate(cantidad_ensayos=Count('muestra__ensayos'))
        .order_by('-fecha_inicio')
    )

    paginator_finalizadas = Paginator(obras_finalizadas_list, 5)
    page_finalizadas = request.GET.get("page_finalizadas")
    obras_finalizadas = paginator_finalizadas.get_page(page_finalizadas)


    context = {
        "empresa": empresa,
        "obras_activas": obras_activas,
        "obras_finalizadas": obras_finalizadas,
    }

    return render(request, "interfaz/admin/dashboard_admin.html", context)

@login_required
@rol_requerido("admin")
def crear_obra(request):
    if request.method == "POST":
        form = ObraForm(request.POST)

        if form.is_valid():
            obra = form.save(commit=False)

            """
            Si tu Obra tiene empresa o usuario creador,
            acá es donde lo asignamos.
            obra.empresa = request.user.empresa
            """
            obra.empresa = request.user.perfil.empresa
            obra.save()

            messages.success(request, "Obra creada correctamente.")
            return redirect('dashboard_admin')
    else:
        form = ObraForm()
        
    return render(request, 'interfaz/admin/obras/crear_obra.html', {'form': form})

@login_required
@rol_requerido("admin")
def editar_obra(request, pk):

    obra = get_object_or_404(Obra, pk=pk)

    if request.method == "POST":
        form = ObraForm(request.POST, instance=obra)

        if form.is_valid():
            form.save()
            messages.success(request, "Obra actualizada correctamente.")
            return redirect("dashboard_admin")

    else:
        form = ObraForm(instance=obra)

    return render(
        request,
        "interfaz/admin/obras/editar_obra.html",
        {
            "form": form,
            "obra": obra
        }
    )

@login_required
@rol_requerido("admin")
def lista_contratistas(request):
    contratistas = Contratista.objects.all().order_by("nombre")

    paginator = Paginator(contratistas, 6)  # 6 cards por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "interfaz/admin/contratistas/lista.html", {
        "page_obj": page_obj
    })

@login_required
@rol_requerido("admin")
def crear_contratista(request):
    if request.method == "POST":
        form = ContratistaForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Contratista creado correctamente.")
            return redirect('lista_contratistas')
    else:
        form = ContratistaForm() #Acá se instancia el form vacío para mostrarlo en la plantilla
        
    return render(request, 'interfaz/admin/contratistas/crear.html', {'form': form})

@login_required
@rol_requerido("admin")
def subir_logo_contratista(request, pk):
    contratista = get_object_or_404(Contratista, pk=pk)

    if request.method == "POST" and request.FILES.get("logo"):
        contratista.logo = request.FILES["logo"]
        contratista.save()

    return redirect("lista_contratistas")

@login_required
@rol_requerido("admin")
def eliminar_logo_contratista(request, pk):
    contratista = get_object_or_404(Contratista, pk=pk)

    if request.method == "POST":
        if contratista.logo:
            contratista.logo.delete(save=False)  # elimina archivo físico
            contratista.logo = None
            contratista.save()

    return redirect("lista_contratistas")

@login_required
@rol_requerido("admin")
def editar_contratista(request, pk):
    contratista = get_object_or_404(Contratista, pk=pk)

    if request.method == "POST":
        form = ContratistaForm(request.POST, instance=contratista)
        if form.is_valid():
            form.save()
            messages.success(request, "Contratista actualizada correctamente.")
            return redirect("lista_contratistas")
    else:
        form = ContratistaForm(instance=contratista)

    return render(request, "interfaz/admin/contratistas/editar.html", {
        "form": form,
        "contratista": contratista
    })

@login_required
@rol_requerido('admin')
def lista_usuarios(request):

    empresa = request.user.perfil.empresa
    usuarios = User.objects.filter(perfil__empresa=empresa)

    return render(request, 'interfaz/admin/usuarios/lista_usuarios.html', {
        'usuarios': usuarios
    })

@login_required
@rol_requerido('admin')
def crear_usuario(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        rol = request.POST['rol']

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe.")
            return redirect('crear_usuario')

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        # Forzar que el nuevo usuario no sea superusuario
        user.is_superuser = False

        Perfil.objects.create(
            user=user,
            empresa=request.user.perfil.empresa,
            rol=rol
        )

        messages.success(request, "Usuario creado correctamente.")
        return redirect('lista_usuarios')

    return render(request, 'interfaz/admin/usuarios/crear_usuario.html')

@login_required
@rol_requerido('admin')
def editar_usuario(request, pk):

    usuario = get_object_or_404(User, pk=pk)
    usuario_actual = request.user
    
    #El superusuario puede editar todo
    if not usuario_actual.is_superuser:
        # Si es admin
        if usuario_actual.perfil.rol == 'admin':
            # No puede editar superusuario
            if usuario.is_superuser:
                messages.error(request, "No puedes editar al superusuario.")
                return redirect('lista_usuarios')
            
            # No puede editar a otro admin (que no sea el mismo)
            if usuario.perfil.rol == 'admin' and usuario != usuario_actual:
                messages.error(request, "No puedes editar a otro administrador.")
                return redirect('lista_usuarios')

    user = User.objects.get(id=pk)
    perfil = user.perfil

    if request.method == 'POST':

        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']

        # Solo permitir cambiar rol si NO es el mismo usuario
        if usuario_actual != user:
            perfil.rol = request.POST['rol']

        # Solo permitir activar/desactivar si NO es el mismo usuario
        if usuario_actual != user:
            user.is_active = 'is_active' in request.POST

        nueva_password = request.POST.get('password')
        if nueva_password:
            user.set_password(nueva_password)

        # Forzar a que nunca se desactive el último admin
        if usuario_actual != user:
            nuevo_estado = 'is_active' in request.POST

            # Si se intenta desactivar un admin
            if not nuevo_estado and perfil.rol == 'admin':
                admins_activos = User.objects.filter(perfil_rol='admin', is_active=True).exclude(id=user.id)
                
                if not admins_activos.exists():
                    messages.error(request, "No puedes desactivar al último administrador.")
                    return redirect('lista_usuarios')
            
            user.is_active = nuevo_estado

        user.save()
        perfil.save()

        messages.success(request, "Usuario actualizado.")
        return redirect('lista_usuarios')

    context = {
        'usuario_editado': user
    }

    return render(request, 'interfaz/admin/usuarios/editar_usuario.html', context)

@login_required
@rol_requerido('admin')
def lista_ubicaciones(request):

    empresa = request.user.perfil.empresa

    ubicaciones = Ubicacion.objects.filter(
        empresa=empresa
    ).order_by('nombre')

    return render(request, 'interfaz/admin/ubicaciones/lista_ubicaciones.html', {
        'ubicaciones': ubicaciones
    })


@login_required
@rol_requerido('admin')
def crear_ubicacion(request):

    if request.method == 'POST':

        nombre = request.POST['nombre']

        if Ubicacion.objects.filter(nombre=nombre.upper()).exists():
            messages.error(request, "La ubicación ya existe.")
            return redirect('crear_ubicacion')

        Ubicacion.objects.create(
            nombre=nombre,
            empresa=request.user.perfil.empresa
        )

        next_url = request.GET.get('next')

        if next_url:
            return redirect(next_url)

        messages.success(request, "Ubicación creada correctamente.")
        return redirect('lista_ubicaciones')

    return render(request, 'interfaz/admin/ubicaciones/crear_ubicacion.html')


@login_required
@rol_requerido('admin')
def editar_ubicacion(request, pk):

    ubicacion = get_object_or_404(Ubicacion, pk=pk)

    if request.method == 'POST':

        ubicacion.nombre = request.POST['nombre']
        ubicacion.activa = 'activa' in request.POST

        ubicacion.save()

        messages.success(request, "Ubicación actualizada.")
        return redirect('lista_ubicaciones')

    return render(request, 'interfaz/admin/ubicaciones/editar_ubicacion.html', {
        'ubicacion': ubicacion
    })
