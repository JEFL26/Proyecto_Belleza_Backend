# app/api/deps.py
from typing import AsyncGenerator
from app.db.session import AsyncSessionLocal
from app.db import models
from loguru import logger

async def get_db() -> AsyncGenerator:
    """
    Dependencia para obtener una sesión de base de datos asíncrona.

    Yields:
    - session: AsyncSession para interactuar con la base de datos.

    Garantiza que la sesión se cierre correctamente al finalizar.
    """
    session = None
    try:
        session = AsyncSessionLocal()
        yield session
    except Exception as e:
        logger.error(f"Error en get_db: {e}")
        raise
    finally:
        if session:
            await session.close()
            logger.debug("Sesión de base de datos cerrada correctamente.")

async def get_current_user() -> models.Usuario:
    """
    Dependencia simulada para obtener el usuario actual.

    Retorna:
    - models.Usuario: usuario de ejemplo.
    
    NOTA: Esta función actualmente retorna un usuario demo.
    """
    try:
        demo_user = models.Usuario(
            id=1,
            nombre="Usuario Demo",
            email="demo@example.com",
            hashed_password="x",
            is_active=True
        )
        logger.debug(f"Usuario demo obtenido: {demo_user.email}")
        return demo_user
    except Exception as e:
        logger.error(f"Error en get_current_user: {e}")
        raise