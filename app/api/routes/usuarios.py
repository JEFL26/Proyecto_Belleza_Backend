# app/api/routes/usuarios.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import models
from app.api.deps import get_db
from app.schemas import usuario as schemas
from app.core.security import hash_password
from loguru import logger

router = APIRouter(tags=["Usuarios"])

@router.get("/ping")
async def ping_usuarios():
    """
    Endpoint de prueba para verificar que la ruta de usuarios funciona.

    Retorna:
    - Diccionario con mensaje de estado.
    """
    try:
        logger.info("Ping en usuarios ejecutado correctamente.")
        return {"message": "Usuarios OK"}
    except Exception as e:
        logger.error(f"Error en ping_usuarios: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.post("/", response_model=schemas.UsuarioOut, status_code=201)
async def crear_usuario(user: schemas.UsuarioCreate, db: AsyncSession = Depends(get_db)):
    """
    Crea un nuevo usuario en la base de datos.

    Parámetros:
    - user: Objeto UsuarioCreate con los datos del usuario.
    - db: AsyncSession de la base de datos.

    Retorna:
    - Objeto UsuarioOut con el usuario creado.
    - Lanza HTTPException 400 si el email ya está registrado.
    """
    try:
        # Verificar si el email ya existe
        existe = await db.execute(select(models.Usuario).where(models.Usuario.email == user.email))
        if existe.scalar_one_or_none():
            logger.warning(f"Intento de registro fallido: email ya registrado {user.email}")
            raise HTTPException(status_code=400, detail="El email ya está registrado")

        # Crear y guardar el nuevo usuario
        nuevo_usuario = models.Usuario(
            nombre=user.nombre,
            email=user.email,
            hashed_password=hash_password(user.password)
        )
        db.add(nuevo_usuario)
        await db.commit()
        await db.refresh(nuevo_usuario)
        logger.info(f"Usuario creado correctamente: {nuevo_usuario.email}")
        return nuevo_usuario

    except HTTPException:
        # Re-lanzamos excepciones HTTP
        raise
    except Exception as e:
        logger.error(f"Error al crear usuario: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al crear usuario"
        )
    finally:
        logger.debug("Intento de creación de usuario completado.")

@router.get("/", response_model=list[schemas.UsuarioOut])
async def listar_usuarios(db: AsyncSession = Depends(get_db)):
    """
    Lista todos los usuarios registrados en la base de datos.

    Parámetros:
    - db: AsyncSession de la base de datos.

    Retorna:
    - Lista de objetos UsuarioOut.
    """
    try:
        result = await db.execute(select(models.Usuario))
        usuarios = result.scalars().all()
        logger.info(f"{len(usuarios)} usuarios listados correctamente.")
        return usuarios
    except Exception as e:
        logger.error(f"Error al listar usuarios: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al listar usuarios"
        )
    finally:
        logger.debug("Listado de usuarios completado.")

@router.get("/{usuario_id}", response_model=schemas.UsuarioOut)
async def obtener_usuario(usuario_id: int, db: AsyncSession = Depends(get_db)):
    """
    Obtiene un usuario específico por su ID.

    Parámetros:
    - usuario_id: ID del usuario a consultar.
    - db: AsyncSession de la base de datos.

    Retorna:
    - Objeto UsuarioOut con los datos del usuario.
    - Lanza HTTPException 404 si el usuario no existe.
    """
    try:
        result = await db.execute(select(models.Usuario).where(models.Usuario.id == usuario_id))
        usuario = result.scalar_one_or_none()
        if not usuario:
            logger.warning(f"Usuario no encontrado: ID {usuario_id}")
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        logger.info(f"Usuario obtenido correctamente: ID {usuario_id}")
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener usuario: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al obtener usuario"
        )
    finally:
        logger.debug(f"Intento de obtención de usuario ID {usuario_id} completado.")