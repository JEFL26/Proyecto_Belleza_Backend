# app/schemas/servicio.py
from pydantic import BaseModel
from typing import Optional

# ==============================
# 💇‍♂️ Schemas para Servicio
# ==============================

class ServicioBase(BaseModel):
    """
    Esquema base para un servicio.

    Atributos:
        nombre (str): Nombre del servicio.
        descripcion (str, opcional): Descripción del servicio.
        precio (float): Precio del servicio.
        duracion_minutos (int): Duración estimada del servicio en minutos.
        is_active (bool, opcional): Indica si el servicio está activo. Por defecto True.
    """
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    duracion_minutos: int
    is_active: Optional[bool] = True

class ServicioCreate(ServicioBase):
    """
    Esquema para la creación de un servicio.
    Hereda todos los campos de ServicioBase.
    """
    pass

class ServicioUpdate(BaseModel):
    """
    Esquema para actualizar un servicio.
    Todos los campos son opcionales para permitir actualizaciones parciales.

    Atributos:
        nombre (str, opcional): Nuevo nombre del servicio.
        descripcion (str, opcional): Nueva descripción del servicio.
        precio (float, opcional): Nuevo precio.
        duracion_minutos (int, opcional): Nueva duración.
        is_active (bool, opcional): Nuevo estado de activación.
    """
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    duracion_minutos: Optional[int] = None
    is_active: Optional[bool] = None

class ServicioOut(ServicioBase):
    """
    Esquema de salida para un servicio.
    Incluye atributos adicionales que se generan en la base de datos.

    Atributos:
        id (int): Identificador único del servicio.
    """
    id: int

    class Config:
        # Permite crear el schema desde un objeto ORM (modelo SQLAlchemy)
        from_attributes = True