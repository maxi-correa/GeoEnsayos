from django.core.exceptions import PermissionDenied
from .models import Ensayo, Obra


# ==============================
# CONSULTAS GENERALES
# ==============================

def ensayos_visibles_para(usuario):
    empresa = usuario.perfil.empresa

    return Ensayo.objects.filter(
        muestra__obra__empresa=empresa
    ).select_related(
        "muestra",
        "muestra__obra",
        "tecnico",
    )


def obras_visibles_para(usuario):
    empresa = usuario.perfil.empresa

    return Obra.objects.filter(
        empresa=empresa
    )


# ==============================
# PERMISOS SOBRE ENSAYOS
# ==============================

def puede_editar_ensayo(usuario, ensayo):
    rol = usuario.perfil.rol

    # ADMIN nunca edita ensayos
    if rol == "admin":
        return False

    # CONSULTA nunca edita
    if rol == "consulta":
        return False

    # TECNICO
    if rol == "tecnico":
        # No se puede editar si está validado
        if ensayo.estado == Ensayo.ESTADO_VALIDADO:
            return False

        # Puede editar en cualquier otro estado
        return True

    return False


def puede_validar_ensayo(usuario, ensayo):
    rol = usuario.perfil.rol

    # Solo ADMIN puede validar
    if rol != "admin":
        return False

    # Solo si está FINALIZADO
    return ensayo.estado == Ensayo.ESTADO_FINALIZADO


def puede_cambiar_estado(usuario, ensayo, nuevo_estado):
    """
    Controla permisos + transición.
    """

    rol = usuario.perfil.rol

    # Primero verificar que la transición exista
    if not ensayo.puede_transicionar_a(nuevo_estado):
        return False

    # Validar transición a VALIDADO
    if nuevo_estado == Ensayo.ESTADO_VALIDADO:
        return rol == "admin"

    # Transiciones normales
    if rol == "tecnico":
        # Técnico no puede modificar si está VALIDADO
        if ensayo.estado == Ensayo.ESTADO_VALIDADO:
            return False

        return True

    return False


# ==============================
# PERMISOS SOBRE OBRAS
# ==============================

def puede_editar_obra(usuario):
    return usuario.perfil.rol == "admin"


def puede_crear_obra(usuario):
    return usuario.perfil.rol == "admin"


# ==============================
# HELPERS
# ==============================

def verificar_permiso(condicion):
    if not condicion:
        raise PermissionDenied