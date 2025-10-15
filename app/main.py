# app/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from loguru import logger
from fastapi.middleware.cors import CORSMiddleware

from app.api import router as api_router
from app.db.session import get_session
from app.utils.response_handler import response_success, response_error

app = FastAPI(title="Centro de Belleza API", version="1.0")

# ==============================
#  Configuración CORS
# ==============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
#  Registro del router único
# ==============================
app.include_router(api_router)

# ==============================
#  Eventos de arranque
# ==============================
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 API del Centro de Belleza iniciada correctamente")

# ==============================
#  Endpoints generales
# ==============================
@app.get("/")
async def root():
    return response_success({"message": "Bienvenido al backend del Centro de Belleza 💅"})

# @app.get("/check_db")
# async def check_db(session: AsyncSession = Depends(get_session)):
#     try:
#         query = text("SELECT COUNT(*) FROM usuarios;")
#         result = await session.execute(query)
#         count = result.scalar()
#         return response_success({"usuarios_en_bd": count})
#     except Exception as e:
#         logger.error(f"Error al consultar la base de datos: {e}")
#         return response_error("Error al consultar la base de datos", 500)