# app/api/routes/reservas.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import models
from app.db.deps import get_db, get_current_user
from app.schemas import reserva as schemas
from loguru import logger

router = APIRouter(tags=["Reservas"])

@router.get("/ping")
async def ping_reservas():
    """
    Endpoint de prueba para verificar que la ruta de reservas funciona.

    Retorna:
    - Diccionario con mensaje de estado.
    """
    try:
        logger.info("Ping en reservas ejecutado correctamente.")
        return {"message": "Reservas OK"}
    except Exception as e:
        logger.error(f"Error en ping_reservas: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.post("/", response_model=schemas.ReservaOut, status_code=201)
async def crear_reserva(
    reserva: schemas.ReservaCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    """
    Crea una nueva reserva para un servicio específico.

    Parámetros:
    - reserva: Objeto ReservaCreate con los datos de la reserva.
    - db: AsyncSession de la base de datos.
    - current_user: Usuario autenticado que realiza la reserva.

    Retorna:
    - Objeto ReservaOut con la reserva creada.
    - Lanza HTTPException 404 si el servicio no existe.
    """
    try:
        # Verificar que el servicio existe
        servicio_result = await db.execute(select(models.Servicio).where(models.Servicio.id == reserva.servicio_id))
        if not servicio_result.scalar_one_or_none():
            logger.warning(f"Servicio no encontrado: ID {reserva.servicio_id}")
            raise HTTPException(status_code=404, detail="Servicio no encontrado")

        # Crear y guardar la nueva reserva
        nueva_reserva = models.Reserva(**reserva.dict())
        db.add(nueva_reserva)
        await db.commit()
        await db.refresh(nueva_reserva)
        logger.info(f"Reserva creada correctamente: ID {nueva_reserva.id} por usuario {current_user.email}")
        return nueva_reserva

    except HTTPException:
        # Re-lanzamos excepciones HTTP
        raise
    except Exception as e:
        logger.error(f"Error al crear reserva: {e}")
        await db.rollback()  # Asegurar que no queden cambios parciales
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al crear reserva"
        )
    finally:
        logger.debug("Intento de creación de reserva completado.")

@router.get("/", response_model=list[schemas.ReservaOut])
async def listar_reservas(db: AsyncSession = Depends(get_db)):
    """
    Lista todas las reservas registradas en la base de datos.

    Parámetros:
    - db: AsyncSession de la base de datos.

    Retorna:
    - Lista de objetos ReservaOut.
    """
    try:
        result = await db.execute(select(models.Reserva))
        reservas = result.scalars().all()
        logger.info(f"{len(reservas)} reservas listadas correctamente.")
        return reservas
    except Exception as e:
        logger.error(f"Error al listar reservas: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al listar reservas"
        )
    finally:
        logger.debug("Listado de reservas completado.")