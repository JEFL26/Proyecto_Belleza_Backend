# app/schemas/usuario.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# ==============================
# 👤 Schemas para Usuario
# ==============================

class UsuarioBase(BaseModel):
    """
    Esquema base para un usuario.
    
    Atributos:
        nombre (str): Nombre completo del usuario.
        email (EmailStr): Correo electrónico válido.
        is_active (bool, opcional): Indica si el usuario está activo. Por defecto True.
        is_admin (bool, opcional): Indica si el usuario tiene permisos de administrador. Por defecto False.
    """
    nombre: str
    email: EmailStr
    is_active: Optional[bool] = True
    is_admin: Optional[bool] = False

class UsuarioCreate(UsuarioBase):
    """
    Esquema para la creación de un usuario.
    
    Atributos:
        password (str): Contraseña en texto plano (será hasheada antes de guardar).
    """
    password: str

class UsuarioUpdate(BaseModel):
    """
    Esquema para actualizar un usuario.
    Todos los campos son opcionales para permitir actualizaciones parciales.
    
    Atributos:
        nombre (str, opcional): Nuevo nombre del usuario.
        email (EmailStr, opcional): Nuevo correo electrónico.
        password (str, opcional): Nueva contraseña en texto plano.
    """
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UsuarioOut(UsuarioBase):
    """
    Esquema de salida para un usuario.
    Incluye atributos adicionales que se generan en la base de datos.
    
    Atributos:
        id (int): Identificador único del usuario.
        created_at (datetime): Fecha de creación del usuario.
    """
    id: int
    created_at: datetime

    class Config:
        # Permite crear el schema desde un objeto ORM (modelo SQLAlchemy)
        from_attributes = True