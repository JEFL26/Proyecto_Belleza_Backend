# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from loguru import logger
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import get_session
from app.api.routes import auth, servicios, reservas, usuarios

# ==============================
# 🔹 Inicialización de FastAPI
# ==============================
app = FastAPI(title="Centro de Belleza API", version="1.0")

# ==============================
# 🔹 Configuración CORS
# ==============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # de momento permite cualquiera
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# 🔹 Registro de routers
# ==============================
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(servicios.router, prefix="/servicios", tags=["Servicios"])
app.include_router(reservas.router, prefix="/reservas", tags=["Reservas"])
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])

# ==============================
# 🔹 Eventos de arranque
# ==============================
@app.on_event("startup")
async def startup_event():
    """Evento que se ejecuta al iniciar la aplicación."""
    logger.info("🚀 API del Centro de Belleza iniciada correctamente")

# ==============================
# 🔹 Endpoints generales
# ==============================
@app.get("/")
async def root():
    """
    Endpoint raíz de la API.
    
    Retorna un mensaje de bienvenida.
    """
    return {"message": "Bienvenido al backend del Centro de Belleza 💅"}

@app.get("/check_db")
async def check_db(session: AsyncSession = Depends(get_session)):
    """
    Endpoint de verificación de la base de datos.

    Intenta contar los usuarios existentes en la tabla 'usuarios'.
    
    Parámetros:
        session (AsyncSession): Sesión asíncrona de la base de datos.

    Retorna:
        dict: Número de usuarios en la base de datos.
    """
    try:
        query = text("SELECT COUNT(*) FROM usuarios;")
        result = await session.execute(query)
        count = result.scalar()
        return {"usuarios_en_bd": count}
    except Exception as e:
        logger.error(f"Error al consultar la base de datos: {e}")
        raise HTTPException(status_code=500, detail="Error al consultar la base de datos")