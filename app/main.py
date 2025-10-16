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

@app.get("/")
async def root():
    return {"message": "endpoint base, si lo vez, funciono.", "status": "ok"}

# ======================================================
# 🏠 Endpoints generales
# ======================================================
# @app.get("/")
# async def root():
#     """
#     Endpoint de prueba para verificar que la API está corriendo.
#     """
#     return response_success({"message": "Bienvenido al backend del Centro de Belleza 💅"})
    
@app.get("/health")
async def health_check(session: AsyncSession = Depends(get_session)):
    """
    Endpoint de health check que valida la conexión con la base de datos.
    Se usa por Docker para determinar si el contenedor está "sano".
    """
    try:
        result = await session.execute(text("SELECT 1"))
        _ = result.scalar()
        return {"status": "ok", "message": "API y base de datos funcionando ✅"}
    except Exception as e:
        logger.error(f"❌ Error en health check: {e}")
        return {"status": "error", "message": str(e)}