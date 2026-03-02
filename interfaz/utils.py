def obtener_dashboard_por_rol(usuario):
    if not usuario.is_authenticated:
        return "login"
    
    rol = usuario.perfil.rol

    dashboards = {
        "tecnico" : "dashboard_tecnico",
        "admin" : "dashboard_admin",
        "consulta" : "dashboard_admin",
    }

    return dashboards.get(rol, "dashboard_admin")