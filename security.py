# /var/www/html/servicios/serviciofooter/utils/security.py
import socket
import ipaddress
from urllib.parse import urlparse

import config
from utils.exceptions import SecurityException, ValidationException

def validate_url_is_public(url: str):
    """
    Valida que la URL no resuelva a una dirección IP privada o reservada para prevenir SSRF.

    Args:
        url: La URL a validar.

    Raises:
        ValidationException: Si el hostname no puede ser resuelto.
        SecurityException: Si la URL resuelve a una IP privada, de loopback o no global.
    """
    hostname = urlparse(url).hostname
    if not hostname:
        raise ValidationException(config.MSG_ERROR_URL_INVALIDA)

    try:
        ip_addr = socket.gethostbyname(hostname)
        ip = ipaddress.ip_address(ip_addr)

        if not ip.is_global:
            raise SecurityException(config.MSG_ERROR_SSRF)

    except socket.gaierror: # pragma: no cover
        raise ValidationException(f"No se pudo resolver el hostname: {hostname}")