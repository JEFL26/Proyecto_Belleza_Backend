# app/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from loguru import logger
from fastapi.middleware.cors import CORSMiddleware

from app.api import router as api_router
from app.db.session import get_session
from app.utils.response_handler import response_success, response_error

# ======================================================
# Inicialización de la app
# ======================================================
app = FastAPI(
    title="Centro de Belleza API",
    version="1.0",
    description="Backend para la gestión de usuarios, servicios y reservas de un Centro de Belleza"
)

# ======================================================
# Configuración CORS
# ======================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes (ajustar en producción)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================================
# Registro del router principal
# ======================================================
app.include_router(api_router)


# ======================================================
# Eventos de arranque
# ======================================================
@app.on_event("startup")
async def startup_event():
    """
    Evento que se ejecuta al iniciar la aplicación.
    Se recomienda usarlo para inicializar conexiones o logs.
    """
    logger.info("🚀 API del Centro de Belleza iniciada correctamente")


# ======================================================
# 🏠 Endpoints generales
# ======================================================
@app.get("/")
async def root():
    """
    Endpoint de prueba para verificar que la API está corriendo.
    """
    return response_success({"message": "Bienvenido al backend del Centro de Belleza 💅"})


@app.get("/check_db")
async def check_db(session: AsyncSession = Depends(get_session)):
    """
    Endpoint para verificar la conexión con la base de datos.
    Retorna el número de usuarios registrados.
    """
    try:
        query = text("SELECT COUNT(*) FROM user_accounts;")
        result = await session.execute(query)
        count = result.scalar()
        return response_success({"usuarios_en_bd": count}, "Conexión a la base de datos exitosa")
    except Exception as e:
        logger.error(f"Error al consultar la base de datos: {e}")
        return response_error(f"Error al consultar la base de datos: {str(e)}")