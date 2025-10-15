# app/core/config.py
from pydantic_settings import BaseSettings
from pydantic import validator
from loguru import logger

class Settings(BaseSettings):
    """
    Configuración principal de la aplicación utilizando Pydantic BaseSettings.

    Atributos:
        APP_NAME (str): Nombre de la aplicación.
        DATABASE_URL (str): URL de conexión a la base de datos.
        SECRET_KEY (str): Clave secreta para generación de tokens JWT.
        ACCESS_TOKEN_EXPIRE_HOURS (int): Tiempo de expiración de los tokens en horas.
    """
    APP_NAME: str = "Centro de Belleza API"
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"  # fallback para desarrollo
    SECRET_KEY: str = "defaultsecretkey"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 8

    class Config:
        env_file = ".env"
        extra = "ignore"

    # ==========================
    # ✅ Validadores
    # ==========================
    @validator("DATABASE_URL", pre=True)
    def validar_url(cls, v: str) -> str:
        """
        Valida y corrige el prefijo de la URL de la base de datos si es necesario.
        """
        if v.startswith("postgresql://"):
            logger.warning("⚠️ Ajustando DATABASE_URL a formato asíncrono (postgresql+asyncpg).")
            return v.replace("postgresql://", "postgresql+asyncpg://", 1)
        elif v.startswith("mysql://"):
            logger.warning("⚠️ Ajustando DATABASE_URL a formato asíncrono (mysql+asyncmy).")
            return v.replace("mysql://", "mysql+asyncmy://", 1)
        return v


# ==========================
# 🟢 Instancia global
# ==========================
settings = Settings()

logger.info(f"Configuración cargada correctamente: {settings.APP_NAME}")
logger.debug(f"URL de base de datos: {settings.DATABASE_URL}")
