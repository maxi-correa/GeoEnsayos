from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ensayos.models import Ensayo
from ensayos.models import Obra

@login_required
def dashboard_tecnico(request):
    if not request.user.groups.filter(name='Técnico').exists():
        return render(request, 'interfaz/sin_permiso.html')
    
    ensayos = Ensayo.objects.all()

    context = {
        'pendientes' : ensayos.filter(estado='PENDIENTE').count(),
        'en_proceso' : ensayos.filter(estado='EN_PROCESO').count(),
        'finalizados' : ensayos.filter(estado='FINALIZADO').count(),
        'validados' : ensayos.filter(estado='VALIDADO').count(),
        'obras' : Obra.objects.filter(tecnicos=request.user, activa=True),
    }

    return render(request, 'interfaz/dashboard.html', context)