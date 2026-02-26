from django.db import models
from core.models import Empresa
from django.contrib.auth.models import User

# Create your models here.

class Contratista(models.Model):
    nombre = models.CharField(max_length=200)
    cuit = models.CharField(max_length=20, unique=True, blank=True)
    contacto = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Contratista"
        verbose_name_plural = "Contratistas"

class Obra(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=200, blank=True)
    contratista = models.ForeignKey(Contratista, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    activa = models.BooleanField(default=True)

    tecnicos = models.ManyToManyField(User, blank=True, related_name='obras_asignadas') #Permite asignar técnicos a una obra

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Obra"
        verbose_name_plural = "Obras"

class Muestra(models.Model):
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha_toma = models.DateField(blank=True, null=True)
    recibida_en_laboratorio = models.DateField(blank=True, null=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.codigo
    
    class Meta:
        verbose_name = "Muestra"
        verbose_name_plural = "Muestras"
        unique_together = ('obra', 'codigo')

class TipoEnsayo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Tipo de Ensayo"
        verbose_name_plural = "Tipos de Ensayo"

class Ensayo(models.Model):
    muestra = models.ForeignKey(Muestra, on_delete=models.CASCADE, related_name='ensayos')
    tipo = models.ForeignKey(TipoEnsayo, on_delete=models.PROTECT) #PROTECT evita que se borre un tipo de ensayo si hay ensayos asociados
    tecnico = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='ensayos_realizados')
    fecha = models.DateField(auto_now_add=True)
    observaciones = models.TextField(blank=True)

    creado_en = models.DateTimeField(auto_now_add=True)
    modificado_en = models.DateTimeField(auto_now=True)

    # Constantes
    ESTADO_PENDIENTE = 'PENDIENTE'
    ESTADO_EN_PROCESO = 'EN_PROCESO'
    ESTADO_FINALIZADO = 'FINALIZADO'
    ESTADO_VALIDADO = 'VALIDADO'
    
    ESTADOS = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_EN_PROCESO, 'En Proceso'),
        (ESTADO_FINALIZADO, 'Finalizado'),
        (ESTADO_VALIDADO, 'Validado'),
    ]

    # Transiciones permitidas
    TRANSICIONES = {
        ESTADO_PENDIENTE: [ESTADO_EN_PROCESO],
        ESTADO_EN_PROCESO: [ESTADO_FINALIZADO],
        ESTADO_FINALIZADO: [ESTADO_EN_PROCESO, ESTADO_VALIDADO],
        ESTADO_VALIDADO: []
    }

    estado = models.CharField(max_length=20, choices=ESTADOS, default=ESTADO_PENDIENTE)

    def __str__(self):
        return f"{self.tipo.nombre} - {self.muestra.codigo}"
    
    def puede_transicionar_a(self, nuevo_estado):
        """
        Solo verifica si la transición es válida
        desde el punto de vista estructural.
        """
        return nuevo_estado in self.TRANSICIONES.get(self.estado, [])

    def cambiar_estado(self, nuevo_estado):
        """
        Cambia el estado si la transición es válida.
        NO valida permisos de usuario.
        """
        if nuevo_estado == self.ESTADO_VALIDADO:
            if not self.puede_transicionar_a(nuevo_estado):
                raise ValueError(f"No se puede cambiar de {self.estado} a {nuevo_estado}")

        # Aplicar cambio
        self.estado = nuevo_estado
        self.save() # Guarda el cambio de estado

    class Meta:
        verbose_name = "Ensayo"
        verbose_name_plural = "Ensayos"

class EnsayoGranulometria(models.Model):
    ensayo = models.OneToOneField(Ensayo, on_delete=models.CASCADE, related_name='granulometria')
    peso_inicial = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Granulometría - {self.ensayo}"
    
class ResultadoTamiz(models.Model):
    ensayo_granulometria = models.ForeignKey(EnsayoGranulometria, on_delete=models.CASCADE, related_name='resultados')
    tamiz = models.CharField(max_length=50)
    peso_retenido = models.DecimalField(max_digits=10, decimal_places=2)
