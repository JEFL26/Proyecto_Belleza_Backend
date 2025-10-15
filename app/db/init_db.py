import asyncio
from app.db.session import engine, Base, async_session
from app.db import models
from loguru import logger
from sqlalchemy import select
from passlib.hash import bcrypt


async def create_admin_user():
    """
    Crea un usuario administrador si no existe.
    """
    async with async_session() as session:
        # Verificar si ya existe un usuario admin
        result = await session.execute(
            select(models.Usuario).where(models.Usuario.email == "admin@centrobelleza.com")
        )
        existing_admin = result.scalar_one_or_none()

        if existing_admin:
            logger.info("👤 Usuario administrador ya existe.")
            return

        # Crear nuevo usuario administrador
        admin_user = models.Usuario(
            nombre="Administrador",
            email="admin@centrobelleza.com",
            hashed_password=bcrypt.hash("admin123"),  # contraseña por defecto
            is_admin=True,
            is_active=True
        )

        session.add(admin_user)
        await session.commit()
        logger.info("✅ Usuario administrador creado correctamente.")


async def init_db():
    """
    Inicializa la base de datos creando todas las tablas definidas en los modelos
    y asegurando que exista un usuario administrador.
    """
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ Tablas creadas correctamente en la base de datos.")

        await create_admin_user()

    except Exception as e:
        logger.error(f"❌ Error al inicializar la base de datos: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(init_db())