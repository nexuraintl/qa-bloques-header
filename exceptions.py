# /var/www/html/servicios/serviciofooter/utils/exceptions.py

class ServiceException(Exception):
    """Excepción base para todos los errores controlados del servicio."""
    pass

class ValidationException(ServiceException):
    """Para errores relacionados con la validación de datos de entrada (p. ej., formato de URL)."""
    pass

class SecurityException(ServiceException):
    """Para errores de seguridad (p. ej., intento de SSRF a una IP privada)."""
    pass

class NetworkException(ServiceException):
    """Para errores de red al intentar acceder a la URL externa."""
    pass

class NotFoundException(ServiceException):
    """Cuando el recurso específico (p. ej., el footer) no se encuentra en la página."""
    pass