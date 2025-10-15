# app/db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.core.config import settings
from loguru import logger
from typing import AsyncGenerator

# ==============================
# 🔧 Configuración de la BD
# ==============================

# Motor de conexión asíncrono a la base de datos
engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)

# Creador de sesiones asíncronas
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

# Alias más corto y claro para reutilizar en otros módulos
async_session = AsyncSessionLocal

# Base declarativa para definir los modelos ORM
Base = declarative_base()

# ==============================
# 🔄 Dependencia para obtener sesión
# ==============================
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Proporciona una sesión de base de datos asíncrona para usar con Depends en FastAPI.

    Yields:
        AsyncSession: sesión de base de datos asíncrona

    Maneja correctamente la apertura y cierre de la sesión.
    """
    session: AsyncSession | None = None
    try:
        session = AsyncSessionLocal()
        yield session
    except Exception as e:
        logger.error(f"Error al obtener sesión de base de datos: {e}")
        raise
    finally:
        if session:
            await session.close()
            logger.debug("Sesión de base de datos cerrada correctamente.")