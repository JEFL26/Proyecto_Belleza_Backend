# app/schemas/reserva.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ==============================
# 📅 Schemas para Reserva
# ==============================

class ReservaBase(BaseModel):
    """
    Esquema base para una reserva.

    Atributos:
        usuario_id (int): ID del usuario que realiza la reserva.
        servicio_id (int): ID del servicio reservado.
        fecha_hora (datetime): Fecha y hora de la reserva.
        estado (str, opcional): Estado de la reserva (pendiente, confirmado, cancelado). Por defecto "pendiente".
    """
    usuario_id: int
    servicio_id: int
    fecha_hora: datetime
    estado: Optional[str] = "pendiente"

class ReservaCreate(ReservaBase):
    """
    Esquema para la creación de una reserva.
    Hereda todos los campos de ReservaBase.
    """
    pass

class ReservaUpdate(BaseModel):
    """
    Esquema para actualizar una reserva.
    Todos los campos son opcionales para permitir actualizaciones parciales.

    Atributos:
        fecha_hora (datetime, opcional): Nueva fecha y hora de la reserva.
        estado (str, opcional): Nuevo estado de la reserva (pendiente, confirmado, cancelado).
    """
    fecha_hora: Optional[datetime] = None
    estado: Optional[str] = None

class ReservaOut(ReservaBase):
    """
    Esquema de salida para una reserva.
    Incluye atributos adicionales generados por la base de datos.

    Atributos:
        id (int): Identificador único de la reserva.
        created_at (datetime): Fecha de creación de la reserva.
    """
    id: int
    created_at: datetime

    class Config:
        # Permite crear el schema desde un objeto ORM (modelo SQLAlchemy)
        from_attributes = True