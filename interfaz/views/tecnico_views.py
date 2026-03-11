from django.contrib.auth.decorators import login_required
from ..decorators import rol_requerido
from django.shortcuts import render

from django.db.models import Count
from django.core.paginator import Paginator

from ensayos.models import Obra

# Create your views here.

@login_required
@rol_requerido("tecnico")
def dashboard_tecnico(request):

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

    return render(request, "interfaz/tecnico/dashboard_tecnico.html", context)