from django.core.exceptions import PermissionDenied
from functools import wraps


def rol_requerido(*roles_permitidos):
    """
    Permite acceso solo si el usuario tiene uno
    de los roles indicados.
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied

            if request.user.perfil.rol not in roles_permitidos:
                raise PermissionDenied

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator