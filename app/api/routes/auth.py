# app/api/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select  # Corregido para SQLAlchemy 2.x
from app.db.session import get_session
from app.db import models
from app.core.security import verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger  # Para logging de errores y seguimiento

router = APIRouter(tags=["Autenticación"])

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_session)
):
    """
    Endpoint para iniciar sesión de un usuario.

    Parámetros:
    - form_data: OAuth2PasswordRequestForm (usuario y contraseña)
    - db: AsyncSession (sesión de la base de datos)

    Retorna:
    - Diccionario con access_token, token_type y nombre de usuario.
    - Lanza HTTPException 401 si las credenciales son inválidas.
    """
    try:
        # Consultar el usuario por email
        query = select(models.Usuario).where(models.Usuario.email == form_data.username)
        result = await db.execute(query)
        usuario = result.scalars().first()

        # Validar existencia de usuario y contraseña
        if not usuario or not verify_password(form_data.password, usuario.hashed_password):
            logger.warning(f"Login fallido para email: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas",
            )

        # Crear token de acceso
        access_token = create_access_token(data={"sub": usuario.email})
        logger.info(f"Usuario {usuario.email} autenticado correctamente.")
        return {"access_token": access_token, "token_type": "bearer", "usuario": usuario.nombre}

    except HTTPException:
        # Re-lanzamos excepciones HTTP para que FastAPI las maneje
        raise
    except Exception as e:
        # Loguear cualquier error inesperado
        logger.error(f"Error en login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
    finally:
        # Para AsyncSession de FastAPI, no necesitamos cerrar la sesión explícitamente
        # Pero podemos usar esto para debug si queremos
        logger.debug("Intento de login completado.")

# Función de ping para probar autenticación (opcional)
@router.get("/ping")
async def ping_auth():
    """
    Endpoint de prueba para verificar que la ruta de autenticación funciona.
    
    Retorna:
    - Diccionario con mensaje de estado.
    """
    try:
        logger.info("Ping en auth ejecutado correctamente.")
        return {"message": "Auth OK"}
    except Exception as e:
        logger.error(f"Error en ping_auth: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )