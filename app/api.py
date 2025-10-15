# app/api.py
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from passlib.context import CryptContext
from app.db import models
from app.schemas.usuario import UserAccountCreate, UserAccountOut, UserProfileCreate
from app.schemas.servicio import ServiceCreate, ServiceUpdate, ServiceOut
from typing import List
from app.db.session import get_session
from app.core.security import hash_password, verify_password, create_access_token
from datetime import timedelta
from app.core.config import settings
from app.schemas.login import LoginRequest
import pandas as pd
import io

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Crear usuario + perfil
@router.post("/usuarios", response_model=UserAccountOut)
async def create_user(user_in: UserAccountCreate, profile_in: UserProfileCreate, session: AsyncSession = Depends(get_session)):
    # Validar email único
    result = await session.execute(select(models.UserAccount).filter_by(email=user_in.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email ya registrado")

    # Crear cuenta
    hashed = hash_password(user_in.password)
    user = models.UserAccount(
        email=user_in.email,
        hashed_password=hashed,
        id_role=user_in.id_role
    )
    session.add(user)
    await session.flush()  # Para obtener ID

    # Crear perfil
    profile = models.UserProfile(
        id_user=user.id,
        first_name=profile_in.first_name,
        last_name=profile_in.last_name,
        phone=profile_in.phone
    )
    session.add(profile)

    await session.commit()
    await session.refresh(user)
    return user

# Login
@router.post("/login")
async def login(login_data: LoginRequest, session: AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password

    result = await session.execute(select(models.UserAccount).filter_by(email=email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    access_token_expires = timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
    token = create_access_token(
        {"sub": user.email, "id_role": user.id_role},
        expires_delta=access_token_expires
    )

    # Obtener perfil (nombre)
    result_profile = await session.execute(
        select(models.UserProfile).filter_by(id_user=user.id)
    )
    profile = result_profile.scalar_one_or_none()

    # Mapear rol según id_role
    # Mapear rol según id_role
    if user.id_role == 1:
        tipo = "admin"
    elif user.id_role == 2:
        tipo = "cliente"
    else:
        tipo = "empleado"  # por si agregas otros roles
    # role_map = {1: "admin", 2: "cliente"}
    # tipo = role_map.get(user.id_role, "empleado")

    return {
        "access_token": token,
        "usuario": {
            "id": user.id,
            "email": user.email,
            "first_name": profile.first_name if profile else "",
            "tipo": tipo
        }
    }

# ==============================
# CRUD de Servicios
# ==============================

@router.post("/services", response_model=ServiceOut)
async def create_service(service: ServiceCreate, session: AsyncSession = Depends(get_session)):
    new_service = models.Service(**service.dict())
    session.add(new_service)
    await session.commit()
    await session.refresh(new_service)
    return new_service


@router.get("/services", response_model=List[ServiceOut])
async def get_services(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(models.Service))
    services = result.scalars().all()
    return services


@router.get("/services/{service_id}", response_model=ServiceOut)
async def get_service(service_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(models.Service).filter_by(id_service=service_id))
    service = result.scalar_one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return service


@router.put("/services/{service_id}", response_model=ServiceOut)
async def update_service(service_id: int, update_data: ServiceUpdate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(models.Service).filter_by(id_service=service_id))
    service = result.scalar_one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(service, key, value)

    await session.commit()
    await session.refresh(service)
    return service


@router.delete("/services/{service_id}")
async def delete_service(service_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(models.Service).filter_by(id_service=service_id))
    service = result.scalar_one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    await session.delete(service)
    await session.commit()
    return {"message": "Servicio eliminado correctamente"}


@router.post("/services/bulk-upload")
async def bulk_upload_services(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session)
):
    """
    Carga masiva de servicios desde archivo Excel (.xls, .xlsx)
    El archivo debe tener las columnas: name, description, duration_minutes, price
    """
    
    # Validar extensión del archivo
    if not file.filename.endswith(('.xls', '.xlsx')):
        raise HTTPException(
            status_code=400, 
            detail="Solo se aceptan archivos .xls o .xlsx"
        )
    
    try:
        # Leer el archivo Excel
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        
        # Validar columnas requeridas
        required_columns = ['name', 'description', 'duration_minutes', 'price']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise HTTPException(
                status_code=400,
                detail=f"Faltan columnas requeridas: {', '.join(missing_columns)}"
            )
        
        # Procesar y validar cada fila
        services_created = []
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Validar que los campos no estén vacíos
                if pd.isna(row['name']) or pd.isna(row['duration_minutes']) or pd.isna(row['price']):
                    errors.append({
                        "fila": index + 2,  # +2 porque Excel empieza en 1 y tiene header
                        "error": "Campos obligatorios vacíos (name, duration_minutes, price)"
                    })
                    continue
                
                # Crear servicio
                new_service = models.Service(
                    name=str(row['name']).strip(),
                    description=str(row['description']).strip() if not pd.isna(row['description']) else "",
                    duration_minutes=int(row['duration_minutes']),
                    price=float(row['price']),
                    state=1  # Activo por defecto
                )
                
                session.add(new_service)
                services_created.append(new_service.name)
                
            except Exception as e:
                errors.append({
                    "fila": index + 2,
                    "error": str(e)
                })
        
        # Guardar todos los servicios
        await session.commit()
        
        return {
            "message": "Carga masiva completada",
            "servicios_creados": len(services_created),
            "servicios": services_created,
            "errores": errors if errors else None
        }
        
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="El archivo está vacío")
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar el archivo: {str(e)}"
        )