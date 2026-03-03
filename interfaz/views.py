from pyexpat.errors import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Count
from ensayos.models import Ensayo, Obra, Contratista
from .forms import ObraForm
from ensayos.permissions import ensayos_visibles_para
from .decorators import rol_requerido
from .utils import obtener_dashboard_por_rol

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy(obtener_dashboard_por_rol(self.request.user))


@login_required
@rol_requerido("tecnico")
def dashboard_tecnico(request):
    
    # Ensayos visibles según el rol (usamos permissions)
    ensayos = ensayos_visibles_para(request.user)

    context = {
        'pendientes' : ensayos.filter(estado=Ensayo.ESTADO_PENDIENTE).count(),
        'en_proceso' : ensayos.filter(estado=Ensayo.ESTADO_EN_PROCESO).count(),
        'finalizados' : ensayos.filter(estado=Ensayo.ESTADO_FINALIZADO).count(),
        'validados' : ensayos.filter(estado=Ensayo.ESTADO_VALIDADO).count(),
        'obras' : Obra.objects.filter(empresa=request.user.perfil.empresa, activa=True),
    }

    return render(request, 'interfaz/dashboard_tecnico.html', context)

@login_required
@rol_requerido("admin", "consulta")
def dashboard_admin(request):

    obras = (Obra.objects
            .filter(activa = True)
            .annotate(cantidad_ensayos = Count('muestra__ensayos'))
            .order_by('nombre')
            ) 

    context = {
        'obras': obras,
        'empresa': Obra.objects.filter(empresa=request.user.perfil.empresa, activa=True).first().empresa
    }

    return render(request, 'interfaz/dashboard_admin.html', context)

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
        
    return render(request, 'interfaz/crear_obra.html', {'form': form})

@login_required
@rol_requerido("admin")
def editar_obra_modal(request, pk):
    obra = get_object_or_404(Obra, pk=pk)

    if request.method == "POST":
        form = ObraForm(request.POST, instance=obra)
        
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True})
        
        html = render_to_string("obras/partials/form_editar.html", {"form": form, "obra": obra}, request=request)
        return JsonResponse({"success": False, "html": html})

    form = ObraForm(instance=obra)

    html = render_to_string("obras/partials/form_editar.html", {"form": form, "obra": obra}, request=request)
    
    return JsonResponse({"html": html})

@login_required
@rol_requerido("admin")
def lista_contratistas(request):
    contratistas = Contratista.objects.all().order_by("nombre")

    paginator = Paginator(contratistas, 6)  # 6 cards por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "interfaz/contratistas/lista.html", {
        "page_obj": page_obj
    })
    



