from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from ensayos.models import Ensayo, Obra
from ensayos.permissions import ensayos_visibles_para
from .decorators import rol_requerido


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        usuario = self.request.user
        rol = usuario.perfil.rol

        if rol == 'tecnico':
            return reverse_lazy('dashboard_tecnico')
        
        if rol == 'admin':
            return reverse_lazy('dashboard_admin')
        
        if rol == 'consulta':
            return reverse_lazy('dashboard_admin')
        
        return reverse_lazy('dashboard_admin')


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

    return render(request, 'interfaz/dashboard.html', context)

@login_required
@rol_requerido("admin", "consulta")
def dashboard_admin(request):

    ensayos = ensayos_visibles_para(request.user)

    context = {
        'pendientes' : ensayos.filter(estado=Ensayo.ESTADO_PENDIENTE).count(),
        'en_proceso' : ensayos.filter(estado=Ensayo.ESTADO_EN_PROCESO).count(),
        'finalizados' : ensayos.filter(estado=Ensayo.ESTADO_FINALIZADO).count(),
        'validados' : ensayos.filter(estado=Ensayo.ESTADO_VALIDADO).count(),
        'obras' : Obra.objects.filter(empresa=request.user.perfil.empresa, activa=True),
    }

    return render(request, 'interfaz/dashboard_admin.html', context)

