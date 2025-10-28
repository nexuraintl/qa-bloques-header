# /var/www/html/servicios/serviciocontenido/services/content_service.py
import requests

from .. import config
from ..utils.exceptions import NetworkException


def get_html_from_url(url: str) -> str:
    """
    Obtiene una URL externa y devuelve su contenido HTML completo.

    Args:
        url: La URL para obtener.

    Returns:
        El contenido HTML de la página como una cadena de texto.

    Raises:
        NetworkException: Si hay un error al obtener la URL (ej. error de conexión, timeout, status code no exitoso).
    """
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': config.USER_AGENT})
        response.raise_for_status()  # Lanza un HTTPError para respuestas 4xx o 5xx
        return response.text
    except requests.exceptions.RequestException as e:
        raise NetworkException(f"{config.MSG_ERROR_OBTENER_CONTENIDO}: {e}")