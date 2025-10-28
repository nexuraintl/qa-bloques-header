# /var/www/html/servicios/serviciofooter/services/footer_service.py
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


def get_footer_from_url(url: str) -> str:
    """
    Obtiene una URL externa y devuelve el HTML del <footer>.
    Utiliza un caché en memoria para evitar peticiones repetidas.
    El caché expira cada hora.

    Args:
        url: La URL para obtener.

    Returns:
        El contenido HTML del footer como una cadena de texto.

    Raises:
        NotFoundException: Si no se encuentra la etiqueta <footer> en la página.
        NetworkException: Si hay un error al obtener la URL.
    """
    # 1. Revisar el caché
    if url in html_cache:
        cached_html, timestamp = html_cache[url]
        if time.time() - timestamp < CACHE_EXPIRATION_SECONDS:
            return cached_html

    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': USER_AGENT})
        response.raise_for_status()  # Lanza un HTTPError para respuestas 4xx o 5xx
    except requests.exceptions.RequestException as e:
        raise NetworkException(f"{MSG_ERROR_OBTENER_CONTENIDO}: {e}")

    base_url = response.url
    soup = BeautifulSoup(response.text, "lxml")

    footer_tag = soup.footer

    if not footer_tag:
        raise NotFoundException(MSG_ERROR_FOOTER_NO_ENCONTRADO)

    _correct_paths_in_tag(footer_tag, base_url)

    html_cache[url] = (str(footer_tag), time.time())
    return str(footer_tag)
