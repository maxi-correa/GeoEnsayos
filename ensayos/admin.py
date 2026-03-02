from django.contrib import admin
from .models import (
    Contratista,
    Cantera,
    Obra,
    Muestra,
    TipoEnsayo,
    Ensayo,
    EnsayoGranulometria,
    ResultadoTamiz,
    ProctorReferencia,
    EnsayoDensidad,
    )

# Register your models here.

@admin.register(Obra)
class ObraAdmin(admin.ModelAdmin):

    def get_queryset(self, request): #Controla que datos se muestran
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(empresa=request.user.perfil.empresa)
    
    def save_model(self, request, obj, form, change): #Controla que datos se guardan
        if not request.user.is_superuser:
            obj.empresa = request.user.perfil.empresa
        super().save_model(request, obj, form, change)

@admin.register(Muestra)
class MuestraAdmin(admin.ModelAdmin):

    def get_queryset(self, request): #Controla que datos se muestran
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(obra__empresa=request.user.perfil.empresa)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "obra" and not request.user.is_superuser:
            kwargs["queryset"] = Obra.objects.filter(empresa=request.user.perfil.empresa)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    

admin.site.register(Contratista)
admin.site.register(Cantera)
admin.site.register(TipoEnsayo)
admin.site.register(Ensayo)
admin.site.register(EnsayoGranulometria)
admin.site.register(ResultadoTamiz)
admin.site.register(ProctorReferencia)
admin.site.register(EnsayoDensidad)