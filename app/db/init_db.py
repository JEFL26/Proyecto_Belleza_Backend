# app/db/init_db.py
import asyncio
from datetime import datetime
from loguru import logger
from sqlalchemy import select
from app.db.session import engine, async_session, Base
from app.db.models import Role, UserAccount, UserProfile
from app.core.security import hash_password

async def create_default_roles(session) -> dict:
    """
    Crea roles iniciales si no existen y devuelve un diccionario con sus IDs.
    """
    roles_ids = {}

    default_roles = [
        {"name": "Administrador", "description": "Rol con todos los privilegios"},
        {"name": "Cliente", "description": "Usuario cliente que puede hacer reservas"}
    ]

    for role_data in default_roles:
        result = await session.execute(select(Role).where(Role.name == role_data["name"]))
        role = result.scalar_one_or_none()

        if not role:
            role = Role(
                name=role_data["name"],
                description=role_data["description"],
                state=1
            )
            session.add(role)
            await session.flush()  # Asigna ID automáticamente
            logger.success(f"✅ Rol '{role_data['name']}' creado correctamente.")
        else:
            logger.info(f"👤 Rol '{role_data['name']}' ya existe.")

        roles_ids[role_data["name"]] = role.id

    return roles_ids

async def create_admin_user(session, admin_role_id: int) -> None:
    """
    Crea un usuario administrador si no existe.
    """
    result = await session.execute(
        select(UserAccount).where(UserAccount.email == "admin@centrobelleza.com")
    )
    existing_admin = result.scalar_one_or_none()

    if existing_admin:
        logger.info("👤 Usuario administrador ya existe.")
        return

    # Crear nuevo usuario admin
    admin_user = UserAccount(
        email="admin@centrobelleza.com",
        hashed_password=hash_password("admin123"),
        is_logged_in=False,
        state=1,
        id_role=admin_role_id,
        created_at=datetime.utcnow()
    )
    session.add(admin_user)
    await session.flush()  # Obtener ID

    # Crear perfil del admin
    admin_profile = UserProfile(
        id_user=admin_user.id,
        first_name="Administrador",
        last_name="Centro",
        phone="1234567890"
    )
    session.add(admin_profile)
    await session.commit()  # Confirma todo
    logger.success("✅ Usuario administrador creado correctamente.")

async def init_db() -> None:
    """
    Inicializa la base de datos creando todas las tablas, roles y usuario administrador.
    """
    logger.info("🚀 Iniciando inicialización de la base de datos...")

    try:
        # Crear todas las tablas
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.success("✅ Tablas creadas correctamente.")

        # Usar una sola sesión para roles y admin
        async with async_session() as session:
            roles = await create_default_roles(session)
            await create_admin_user(session, roles["Administrador"])
            # ==============================
            # Crear servicios iniciales
            # ==============================
            from app.db.models import Service

            default_services = [
                {"name": "Corte de Cabello", "description": "Corte clásico o moderno", "duration_minutes": 45, "price": 20000.0},
                {"name": "Manicure", "description": "Manicure tradicional", "duration_minutes": 30, "price": 15000.0},
                {"name": "Pedicure", "description": "Pedicure completo", "duration_minutes": 40, "price": 18000.0},
            ]

            for svc_data in default_services:
                result = await session.execute(select(Service).where(Service.name == svc_data["name"]))
                service = result.scalar_one_or_none()
                if not service:
                    service = Service(**svc_data)
                    session.add(service)
                    logger.success(f"💅 Servicio '{svc_data['name']}' creado correctamente.")
            
            await session.commit()

        logger.info("🎉 Inicialización completada exitosamente.")

    except Exception as e:
        logger.error(f"❌ Error al inicializar la base de datos: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(init_db())
