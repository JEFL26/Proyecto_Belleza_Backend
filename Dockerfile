# Backend Dockerfile
FROM python:3.12-slim

# Establecemos el directorio de trabajo
WORKDIR /app

# Instalar netcat y otras dependencias necesarias
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Copiamos solo los requirements primero (para aprovechar cache de Docker)
COPY ../requirements.txt .

# Instalamos dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el proyecto
COPY ../app ./app

# Copiamos archivo de variables de entorno
COPY ../.env .env

# Espera a que la DB esté lista
COPY ../wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

# Exponemos el puerto de FastAPI
EXPOSE 8000

# Comando para iniciar la app después de que la DB esté lista
CMD ["/wait-for-db.sh", "db", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]