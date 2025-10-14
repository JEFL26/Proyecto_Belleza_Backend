# app/api/routes/servicios.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import models
from app.db.deps import get_db
from app.schemas import servicio as schemas
from loguru import logger

router = APIRouter(tags=["Servicios"])

@router.get("/ping")
async def ping_servicios():
    """
    Endpoint de prueba para verificar que la ruta de servicios funciona.

    Retorna:
    - Diccionario con mensaje de estado.
    """
    try:
        logger.info("Ping en servicios ejecutado correctamente.")
        return {"message": "Servicios OK"}
    except Exception as e:
        logger.error(f"Error en ping_servicios: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.post("/", response_model=schemas.ServicioOut, status_code=201)
async def crear_servicio(servicio: schemas.ServicioCreate, db: AsyncSession = Depends(get_db)):
    """
    Crea un nuevo servicio en la base de datos.

    Parámetros:
    - servicio: Objeto ServicioCreate con los datos del servicio.
    - db: AsyncSession de la base de datos.

    Retorna:
    - Objeto ServicioOut con el servicio creado.
    """
    try:
        nuevo_servicio = models.Servicio(**servicio.dict())
        db.add(nuevo_servicio)
        await db.commit()
        await db.refresh(nuevo_servicio)
        logger.info(f"Servicio creado correctamente: ID {nuevo_servicio.id}")
        return nuevo_servicio
    except Exception as e:
        logger.error(f"Error al crear servicio: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al crear servicio"
        )
    finally:
        logger.debug("Intento de creación de servicio completado.")

@router.get("/", response_model=list[schemas.ServicioOut])
async def listar_servicios(db: AsyncSession = Depends(get_db)):
    """
    Lista todos los servicios registrados en la base de datos.

    Parámetros:
    - db: AsyncSession de la base de datos.

    Retorna:
    - Lista de objetos ServicioOut.
    """
    try:
        result = await db.execute(select(models.Servicio))
        servicios = result.scalars().all()
        logger.info(f"{len(servicios)} servicios listados correctamente.")
        return servicios
    except Exception as e:
        logger.error(f"Error al listar servicios: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al listar servicios"
        )
    finally:
        logger.debug("Listado de servicios completado.")

@router.get("/{servicio_id}", response_model=schemas.ServicioOut)
async def obtener_servicio(servicio_id: int, db: AsyncSession = Depends(get_db)):
    """
    Obtiene un servicio específico por su ID.

    Parámetros:
    - servicio_id: ID del servicio a consultar.
    - db: AsyncSession de la base de datos.

    Retorna:
    - Objeto ServicioOut con los datos del servicio.
    - Lanza HTTPException 404 si el servicio no existe.
    """
    try:
        result = await db.execute(select(models.Servicio).where(models.Servicio.id == servicio_id))
        servicio = result.scalar_one_or_none()
        if not servicio:
            logger.warning(f"Servicio no encontrado: ID {servicio_id}")
            raise HTTPException(status_code=404, detail="Servicio no encontrado")
        logger.info(f"Servicio obtenido correctamente: ID {servicio_id}")
        return servicio
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener servicio: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al obtener servicio"
        )
    finally:
        logger.debug(f"Intento de obtención de servicio ID {servicio_id} completado.")
