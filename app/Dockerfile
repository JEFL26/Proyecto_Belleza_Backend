# Backend Dockerfile
# estaba usando python:3.10, pero slim es mas estable y ligera tengo entendido
FROM python:3.10-slim

# Establecemos el directorio de trabajo(por verificar)
WORKDIR /code

# Instalamos dependencias del sistema necesarias
#el rm es para eliminar cache que nos añade peso innecesario
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Copiamos primero el archivo de requerimientos para aprovechar la caché de Docker
COPY requirements.txt .

# Instalamos las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el contenido de la aplicación(lo cambie para que fueran todos los archivos)
COPY . .

# Copiamos el archivo de entorno
COPY .env .

# Comando para iniciar la aplicación (la BD se asegura con depends_on en docker-compose)
CMD ["sh", "-c", "python -m app.db.init_db && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]