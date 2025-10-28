# Imagen base liviana y estable
FROM python:3.11-slim

# Crear y establecer el directorio de trabajo
WORKDIR /app

# Copiar solo los archivos necesarios primero (optimiza la caché)
COPY requirements.txt .

# Instalar dependencias sin caché
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código fuente
COPY . .

# Exponer el puerto (Cloud Run usa variable $PORT)
EXPOSE 8080

# Comando de ejecución (ajustado para app.py en raíz)
CMD exec uvicorn app:app --host 0.0.0.0 --port ${PORT:-8080}
