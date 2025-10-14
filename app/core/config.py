# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Configuración principal de la aplicación utilizando Pydantic BaseSettings.

    Atributos:
        APP_NAME (str): Nombre de la aplicación.
        DATABASE_URL (str): URL de conexión a la base de datos.
        SECRET_KEY (str): Clave secreta para generación de tokens JWT.
        ACCESS_TOKEN_EXPIRE_HOURS (int): Tiempo de expiración de los tokens en horas. Por defecto 8 horas.
    """
    APP_NAME: str = "Centro de Belleza API"
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_HOURS: int = 8

    class Config:
        """
        Configuración interna de Pydantic.

        env_file (str): Archivo donde se cargan las variables de entorno.
        """
        env_file = ".env"
        extra = "ignore"  

# Instancia global para acceder a la configuración desde cualquier parte del proyecto
settings = Settings()