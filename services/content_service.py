# /var/www/html/servicios/servicioheader/services/content_service.py
import time

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import config
from utils.exceptions import NetworkException, NotFoundException

# --- Caché en memoria ---
# La clave es la URL, el valor es una tupla (html_contenido, timestamp)
html_cache = {}
CACHE_EXPIRATION_SECONDS = 3600  # 1 hora

def _correct_paths_in_tag(soup_tag, base_url: str) -> None:
    """
    Función auxiliar para encontrar y corregir rutas relativas en un fragmento de HTML.
    Modifica el objeto soup_tag directamente.
    """
    if not soup_tag:
        return

    # Corregir atributos 'href' y 'src'
    for attribute in ["href", "src"]:
        for tag in soup_tag.find_all(attrs={attribute: True}):
            # Construye la URL absoluta y actualiza el atributo
            tag[attribute] = urljoin(base_url, tag[attribute])


def get_html_from_url(url: str) -> str:
    """
    Obtiene una URL externa y devuelve el HTML del <head> y <header>.
    Utiliza un caché en memoria para evitar peticiones repetidas.
    El caché expira cada hora.

    Args:
        url: La URL para obtener.

    Returns:
        El contenido HTML de la página como una cadena de texto.

    Raises:
        NotFoundException: Si no se encuentra la etiqueta <header> en la página.
        NetworkException: Si hay un error al obtener la URL (ej. error de conexión, timeout, status code no exitoso).
    """
    # 1. Revisar el caché
    if url in html_cache:
        cached_html, timestamp = html_cache[url]
        if time.time() - timestamp < CACHE_EXPIRATION_SECONDS:
            return cached_html

    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': config.USER_AGENT})
        response.raise_for_status()  # Lanza un HTTPError para respuestas 4xx o 5xx
        
        base_url = response.url
        soup = BeautifulSoup(response.text, "lxml")

        head_tag = soup.head
        header_tag = soup.header

        if not header_tag:
            raise NotFoundException(config.MSG_ERROR_HEADER_NO_ENCONTRADO)

        # Usamos la función auxiliar para refactorizar la corrección de rutas
        _correct_paths_in_tag(head_tag, base_url)
        _correct_paths_in_tag(header_tag, base_url)

        # Unimos el contenido de <head> y <header>
        head_html = str(head_tag) if head_tag else ""
        header_html = str(header_tag)
        final_html = head_html + header_html

        # 2. Guardar el resultado en el caché antes de devolverlo
        html_cache[url] = (final_html, time.time())
        return final_html

    except requests.exceptions.RequestException as e:
        raise NetworkException(f"{config.MSG_ERROR_OBTENER_CONTENIDO}: {e}")