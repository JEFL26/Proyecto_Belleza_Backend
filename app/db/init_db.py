# app/db/init_db.py
import asyncio
from app.db.session import engine, Base
from app.db import models  # Asegura que los modelos estén importados
from loguru import logger

async def init_db():
    """
    Inicializa la base de datos creando todas las tablas definidas en los modelos.
    """
    try:
        async with engine.begin() as conn:
            # Crear todas las tablas
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ Tablas creadas correctamente en la base de datos.")
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(init_db())
