# app/api.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from passlib.context import CryptContext
from datetime import timedelta
from jose import jwt
from loguru import logger

from app.db.session import get_session
from app.db import models
from app.schemas.usuario import UsuarioCreate, UsuarioRead, LoginRequest, TokenResponse
from app.schemas.servicio import ServicioCreate, ServicioRead
from app.schemas.reserva import ReservaCreate, ReservaRead
from app.utils.response_handler import response_success, response_error
from app.core.config import settings
from app.core.security import create_access_token

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# =======================================================
# 🧍 USUARIOS
# =======================================================
@router.post("/usuarios", response_model=UsuarioRead)
async def crear_usuario(usuario: UsuarioCreate, session: AsyncSession = Depends(get_session)):
    """
    Crea un nuevo usuario (cliente o empleado).
    """
    try:
        result = await session.execute(select(models.Usuario).filter_by(email=usuario.email))
        existente = result.scalar_one_or_none()
        if existente:
            raise HTTPException(status_code=400, detail="El correo ya está registrado.")

        hashed_password = pwd_context.hash(usuario.password)
        nuevo_usuario = models.Usuario(
            nombre=usuario.nombre,
            email=usuario.email,
            hashed_password=hashed_password,
            is_active=usuario.is_active,
            is_admin=usuario.is_admin,
        )
        session.add(nuevo_usuario)
        await session.commit()
        await session.refresh(nuevo_usuario)
        logger.info(f"👤 Usuario creado: {nuevo_usuario.email}")
        return nuevo_usuario
    except Exception as e:
        logger.error(f"Error creando usuario: {e}")
        await session.rollback()
        raise HTTPException(status_code=500, detail="Error al crear el usuario.")


@router.get("/usuarios", response_model=list[UsuarioRead])
async def listar_usuarios(session: AsyncSession = Depends(get_session)):
    """
    Lista todos los usuarios registrados.
    """
    result = await session.execute(select(models.Usuario))
    usuarios = result.scalars().all()
    return usuarios


# =======================================================
# 🔐 LOGIN
# =======================================================
@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, session: AsyncSession = Depends(get_session)):
    """
    Verifica credenciales y devuelve un token JWT.
    """
    try:
        result = await session.execute(select(models.Usuario).filter_by(email=request.email))
        usuario = result.scalar_one_or_none()

        if not usuario or not pwd_context.verify(request.password, usuario.hashed_password):
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        access_token_expires = timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
        access_token = create_access_token(
            data={"sub": usuario.email, "is_admin": usuario.is_admin},
            expires_delta=access_token_expires
        )

        logger.info(f"✅ Usuario logueado: {usuario.email}")
        return TokenResponse(access_token=access_token)
    except Exception as e:
        logger.error(f"Error en login: {e}")
        raise HTTPException(status_code=500, detail="Error en el proceso de autenticación.")


# =======================================================
# 💅 SERVICIOS
# =======================================================
@router.post("/servicios", response_model=ServicioRead)
async def crear_servicio(servicio: ServicioCreate, session: AsyncSession = Depends(get_session)):
    """
    Crea un nuevo servicio.
    """
    nuevo_servicio = models.Servicio(
        nombre=servicio.nombre,
        descripcion=servicio.descripcion,
        precio=servicio.precio,
    )
    session.add(nuevo_servicio)
    await session.commit()
    await session.refresh(nuevo_servicio)
    logger.info(f"💅 Servicio creado: {nuevo_servicio.nombre}")
    return nuevo_servicio


@router.get("/servicios", response_model=list[ServicioRead])
async def listar_servicios(session: AsyncSession = Depends(get_session)):
    """
    Lista todos los servicios disponibles.
    """
    result = await session.execute(select(models.Servicio))
    servicios = result.scalars().all()
    return servicios


@router.delete("/servicios/{servicio_id}")
async def eliminar_servicio(servicio_id: int, session: AsyncSession = Depends(get_session)):
    """
    Elimina un servicio por su ID.
    """
    result = await session.execute(select(models.Servicio).filter_by(id=servicio_id))
    servicio = result.scalar_one_or_none()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    await session.delete(servicio)
    await session.commit()
    return response_success({"mensaje": f"Servicio {servicio.nombre} eliminado correctamente"})


# =======================================================
# 📅 RESERVAS
# =======================================================
@router.post("/reservas", response_model=ReservaRead)
async def crear_reserva(reserva: ReservaCreate, session: AsyncSession = Depends(get_session)):
    """
    Crea una nueva reserva.
    """
    nueva_reserva = models.Reserva(
        usuario_id=reserva.usuario_id,
        servicio_id=reserva.servicio_id,
        fecha_reserva=reserva.fecha_reserva,
        estado=reserva.estado
    )
    session.add(nueva_reserva)
    await session.commit()
    await session.refresh(nueva_reserva)
    logger.info(f"📅 Reserva creada para usuario {reserva.usuario_id}")
    return nueva_reserva


@router.get("/reservas", response_model=list[ReservaRead])
async def listar_reservas(session: AsyncSession = Depends(get_session)):
    """
    Lista todas las reservas registradas.
    """
    result = await session.execute(select(models.Reserva))
    reservas = result.scalars().all()
    return reservas

@router.get("/ping")
async def ping():
    return {"message": "pong 🏓"}