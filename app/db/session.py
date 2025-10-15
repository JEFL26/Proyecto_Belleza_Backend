# app/db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.core.config import settings
from loguru import logger
from typing import AsyncGenerator

# ==============================
# 🔧 Configuración de la BD
# ==============================

# Motor asíncrono de conexión a la base de datos
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,        # Cambia a True si deseas ver las queries
    future=True
)

# Creador de sesiones asíncronas
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# Alias corto para uso rápido en módulos internos
async_session = AsyncSessionLocal

# Base declarativa para los modelos
Base = declarative_base()


# ==============================
# 🔄 Dependencia de sesión para FastAPI
# ==============================
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Proporciona una sesión de base de datos asíncrona para usar con Depends en FastAPI.
    Maneja apertura, cierre y registro de errores de manera segura.
    """
    session = None
    try:
        session = AsyncSessionLocal()
        yield session
    except Exception as e:
        logger.error(f"❌ Error al obtener sesión de base de datos: {e}")
        raise
    finally:
        if session:
            await session.close()
            logger.debug("🔒 Sesión de base de datos cerrada correctamente.")
