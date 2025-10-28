# /var/www/html/servicios/servicioheader/app.py
import logging
from urllib.parse import urlparse
import redis.asyncio as redis

from fastapi import FastAPI, Query, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse

import config
from services.content_service import get_html_from_url
from utils.exceptions import (NetworkException, SecurityException,
                              ServiceException, ValidationException)
from utils.security import validate_url_is_public

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

# Instancia de la aplicación FastAPI
app = FastAPI(
    title="API de Extracción de Contenido HTML",
    description="Extrae el contenido HTML completo de una página web externa.",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """Crea una pool de conexiones a Redis al iniciar la app."""
    app.state.redis = redis.from_url("redis://localhost", encoding="utf-8", decode_responses=False)

@app.on_event("shutdown")
async def shutdown_event():
    """Cierra la conexión a Redis al apagar la app."""
    await app.state.redis.close()


def crear_respuesta_error(status_code: int, message: str):
    """Crea una respuesta de error estandarizada en formato JSON."""
    return JSONResponse(
        status_code=status_code,
        content={"status": status_code, "error": [message], "data": []}
    )

@app.exception_handler(ServiceException)
async def service_exception_handler(request: Request, exc: ServiceException):
    """Manejador centralizado para las excepciones del servicio."""
    status_code = 400
    message = str(exc)

    if isinstance(exc, (ValidationException, SecurityException, NetworkException)):
        status_code = 400
    else:
        status_code = 500
        message = "Ocurrió un error interno inesperado."

    logging.error(f"Error en {request.url}: {exc}")
    return crear_respuesta_error(status_code, message)

@app.get(
    "/api/content",
    summary="Extraer el HTML de una URL",
    response_class=HTMLResponse
)
async def get_content(request: Request, url: str = Query(..., description="La URL del sitio del cual extraer el HTML.")):
    """
    Obtiene el contenido HTML completo de una URL y lo devuelve.
    """
    if not url:
        raise ValidationException(config.MSG_ERROR_PARAMETRO_REQUERIDO)

    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = f"http://{url}"

    if urlparse(url).scheme not in config.PROTOCOLOS_PERMITIDOS:
        raise ValidationException(config.MSG_ERROR_URL_INVALIDA)

    # --- Validación de Seguridad ---
    # Previene ataques SSRF. Comentado para desarrollo si necesitas acceder a URLs locales.
    # ¡No deshabilitar en producción!
    # validate_url_is_public(url)

    html_content = await get_html_from_url(url, redis_client=request.app.state.redis)
    return HTMLResponse(content=html_content)