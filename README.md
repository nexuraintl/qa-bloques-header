# Servicio de Extracción de Footers HTML (serviciofooter)

Este microservicio en Python, construido con FastAPI, se encarga de extraer el contenido de la etiqueta `<footer>` de una URL externa. Además, corrige las rutas relativas de recursos (imágenes, CSS, JS) para que se visualicen correctamente y utiliza un caché en memoria para optimizar el rendimiento.

## Funcionalidades

- Extrae el HTML de la etiqueta `<footer>` de una URL dada.
- Convierte rutas relativas de recursos (CSS, JS, imágenes) a absolutas para una correcta visualización.
- Implementa un caché en memoria con expiración de 1 hora para reducir peticiones repetidas y mejorar la velocidad de respuesta.
- Incluye validación de seguridad para prevenir ataques SSRF.
- Manejo centralizado de excepciones.

## Configuración y Ejecución

Sigue estos pasos para configurar y ejecutar el servicio en tu entorno local.

### 1. Navegar al Directorio del Servicio

```bash
cd /var/www/html/servicios/serviciofooter
```

### 2. Crear y Activar un Entorno Virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
python3 -m pip install -r requirements.txt
```

### 4. Ejecutar el Servicio

```bash
uvicorn app:app --reload
```

El servicio estará disponible en `http://127.0.0.1:8000`.

## Uso del API

**Ejemplo con `curl`:**

```bash
curl "http://127.0.0.1:8000/api/content?url=https://www.ejemplo.com"
```

La respuesta será el HTML de la etiqueta `<footer>` de la URL proporcionada.

---

**Nota de Seguridad**: La validación `validate_url_is_public(url)` está comentada para facilitar el desarrollo. **¡No la deshabilites en un entorno de producción!**