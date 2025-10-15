# app/api.py
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from datetime import timedelta
import pandas as pd
import io

# Importaciones locales
from app.db import models
from app.db.session import get_session
from app.schemas.usuario import UserAccountCreate, UserAccountOut, UserProfileCreate
from app.schemas.servicio import ServiceCreate, ServiceUpdate, ServiceOut
from app.schemas.login import LoginRequest
from app.core.security import hash_password, verify_password, create_access_token
from app.core.config import settings
from app.utils.response_handler import (
    response_success,
    response_bad_request,
    response_not_found,
    response_error,
    ResponseHandler
)

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ======================================================
# 👤 Crear usuario + perfil
# ======================================================
@router.post("/usuarios", response_model=UserAccountOut)
async def create_user(
    user_in: UserAccountCreate,
    profile_in: UserProfileCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Crea un nuevo usuario junto a su perfil.
    - Valida que el email no esté registrado.
    - Crea la cuenta y su perfil asociado.
    """
    try:
        # Verificar email único
        result = await session.execute(select(models.UserAccount).filter_by(email=user_in.email))
        if result.scalar_one_or_none():
            return ResponseHandler.bad_request("Email ya registrado")

        # Crear cuenta de usuario
        hashed = hash_password(user_in.password)
        user = models.UserAccount(
            email=user_in.email,
            hashed_password=hashed,
            id_role=user_in.id_role
        )
        session.add(user)
        await session.flush()  # Obtener ID antes de crear el perfil

        # Crear perfil asociado
        profile = models.UserProfile(
            id_user=user.id,
            first_name=profile_in.first_name,
            last_name=profile_in.last_name,
            phone=profile_in.phone
        )
        session.add(profile)

        await session.commit()
        await session.refresh(user)

        return response_success(
            data={"id": user.id, "email": user.email},
            message="Usuario creado exitosamente"
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        await session.rollback()
        return response_error(f"Error al crear usuario: {str(e)}")


# ======================================================
# 🔐 Login
# ======================================================
@router.post("/login")
async def login(login_data: LoginRequest, session: AsyncSession = Depends(get_session)):
    """
    Valida las credenciales del usuario y genera un token JWT.
    """
    try:
        result = await session.execute(select(models.UserAccount).filter_by(email=login_data.email))
        user = result.scalar_one_or_none()

        if not user or not verify_password(login_data.password, user.hashed_password):
            return response_bad_request("Credenciales inválidas")

        # Generar token
        access_token_expires = timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
        token = create_access_token(
            {"sub": user.email, "id_role": user.id_role},
            expires_delta=access_token_expires
        )

        # Obtener perfil
        result_profile = await session.execute(
            select(models.UserProfile).filter_by(id_user=user.id)
        )
        profile = result_profile.scalar_one_or_none()

        # Determinar tipo de usuario
        tipo = (
            "admin" if user.id_role == 1
            else "cliente" if user.id_role == 2
            else "empleado"
        )

        return response_success(
            data={
                "access_token": token,
                "usuario": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": profile.first_name if profile else "",
                    "tipo": tipo
                }
            },
            message="Inicio de sesión exitoso"
        )

    except Exception as e:
        return response_error(f"Error al iniciar sesión: {str(e)}")


# ======================================================
# 💇 CRUD de Servicios
# ======================================================

@router.post("/services", response_model=ServiceOut)
async def create_service(service: ServiceCreate, session: AsyncSession = Depends(get_session)):
    """
    Crea un nuevo servicio.
    """
    try:
        new_service = models.Service(**service.dict())
        session.add(new_service)
        await session.commit()
        await session.refresh(new_service)
        return response_success(ServiceOut.model_validate(new_service), "Servicio creado correctamente")
    except Exception as e:
        await session.rollback()
        return response_error(f"Error al crear servicio: {str(e)}")


@router.get("/services", response_model=list[ServiceOut])
async def get_services(session: AsyncSession = Depends(get_session)):
    """
    Obtiene todos los servicios disponibles.
    """
    try:
        result = await session.execute(select(models.Service))
        services = result.scalars().all()
        return response_success(
            [ServiceOut.model_validate(s) for s in services],
            "Servicios obtenidos correctamente"
        )
    except Exception as e:
        return response_error(f"Error al obtener servicios: {str(e)}")


@router.get("/services/{service_id}", response_model=ServiceOut)
async def get_service(service_id: int, session: AsyncSession = Depends(get_session)):
    """
    Obtiene un servicio por su ID.
    """
    try:
        result = await session.execute(select(models.Service).filter_by(id_service=service_id))
        service = result.scalar_one_or_none()
        if not service:
            return response_not_found("Servicio no encontrado")
        return response_success(ServiceOut.model_validate(service), "Servicio obtenido correctamente")
    except Exception as e:
        return response_error(f"Error al obtener servicio: {str(e)}")


@router.put("/services/{service_id}", response_model=ServiceOut)
async def update_service(service_id: int, update_data: ServiceUpdate, session: AsyncSession = Depends(get_session)):
    """
    Actualiza la información de un servicio.
    """
    try:
        result = await session.execute(select(models.Service).filter_by(id_service=service_id))
        service = result.scalar_one_or_none()
        if not service:
            return response_not_found("Servicio no encontrado")

        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(service, key, value)

        await session.commit()
        await session.refresh(service)
        return response_success(ServiceOut.model_validate(service), "Servicio actualizado correctamente")

    except Exception as e:
        await session.rollback()
        return response_error(f"Error al actualizar servicio: {str(e)}")


@router.delete("/services/{service_id}")
async def delete_service(service_id: int, session: AsyncSession = Depends(get_session)):
    """
    Elimina un servicio por su ID.
    """
    try:
        result = await session.execute(select(models.Service).filter_by(id_service=service_id))
        service = result.scalar_one_or_none()
        if not service:
            return response_not_found("Servicio no encontrado")

        await session.delete(service)
        await session.commit()
        return response_success(message="Servicio eliminado correctamente")

    except Exception as e:
        await session.rollback()
        return response_error(f"Error al eliminar servicio: {str(e)}")


# ======================================================
# 📦 Carga masiva de servicios (Excel)
# ======================================================
@router.post("/services/bulk-upload")
async def bulk_upload_services(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session)
):
    """
    Carga masiva de servicios desde un archivo Excel (.xls, .xlsx).
    Requiere las columnas: name, description, duration_minutes, price.
    """
    if not file.filename.endswith(('.xls', '.xlsx')):
        return response_bad_request("Solo se aceptan archivos .xls o .xlsx")

    try:
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))

        required_columns = ['name', 'description', 'duration_minutes', 'price']
        missing_columns = [c for c in required_columns if c not in df.columns]
        if missing_columns:
            return response_bad_request(f"Faltan columnas requeridas: {', '.join(missing_columns)}")

        services_created = []
        errors = []

        for index, row in df.iterrows():
            try:
                if pd.isna(row['name']) or pd.isna(row['duration_minutes']) or pd.isna(row['price']):
                    errors.append({
                        "fila": index + 2,
                        "error": "Campos obligatorios vacíos (name, duration_minutes, price)"
                    })
                    continue

                new_service = models.Service(
                    name=str(row['name']).strip(),
                    description=str(row['description']).strip() if not pd.isna(row['description']) else "",
                    duration_minutes=int(row['duration_minutes']),
                    price=float(row['price']),
                    state=True
                )
                session.add(new_service)
                services_created.append(new_service.name)

            except Exception as e:
                errors.append({"fila": index + 2, "error": str(e)})

        await session.commit()
        return response_success(
            data={
                "servicios_creados": len(services_created),
                "servicios": services_created,
                "errores": errors if errors else None
            },
            message="Carga masiva completada"
        )

    except pd.errors.EmptyDataError:
        return response_bad_request("El archivo está vacío")
    except Exception as e:
        await session.rollback()
        return response_error(f"Error al procesar el archivo: {str(e)}")