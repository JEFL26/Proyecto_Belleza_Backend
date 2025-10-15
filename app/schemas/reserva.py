# app/schemas/reserva.py
from pydantic import BaseModel, Field, constr, condecimal
from typing import Optional
from datetime import datetime
from decimal import Decimal

# ==============================
# 📘 Esquemas para Gestión de Reservas
# ==============================


# -----------------------------
# 🟢 ReservationStatus (Estado de reserva)
# -----------------------------
class ReservationStatusBase(BaseModel):
    """
    Define los atributos básicos de un estado de reserva.
    """
    name: constr(strip_whitespace=True, min_length=1, max_length=50)
    state: Optional[bool] = True


class ReservationStatusCreate(ReservationStatusBase):
    """
    Esquema para creación de un nuevo estado de reserva.
    """
    pass


class ReservationStatusOut(ReservationStatusBase):
    """
    Esquema de salida al consultar un estado de reserva.
    """
    id_reservation_status: int

    model_config = {"from_attributes": True}


# -----------------------------
# 📅 Reservation (Reserva)
# -----------------------------
class ReservationBase(BaseModel):
    """
    Define los atributos principales de una reserva.
    """
    id_user: int = Field(..., description="ID del cliente que hace la reserva")
    id_service: int
    scheduled_datetime: datetime
    total_price: condecimal(max_digits=10, decimal_places=2, ge=0)
    payment_method: constr(strip_whitespace=True, min_length=1, max_length=50)
    state: Optional[bool] = True
    id_reservation_status: Optional[int] = Field(1, description="Estado por defecto: Pending -> 1")


class ReservationCreate(ReservationBase):
    """
    Esquema para creación de nuevas reservas.
    """
    pass


class ReservationUpdate(BaseModel):
    """
    Esquema para actualización parcial de una reserva existente.
    """
    id_service: Optional[int] = None
    scheduled_datetime: Optional[datetime] = None
    total_price: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    payment_method: Optional[constr(strip_whitespace=True, min_length=1, max_length=50)] = None
    state: Optional[bool] = None
    id_reservation_status: Optional[int] = None


class ReservationOut(ReservationBase):
    """
    Esquema de salida al consultar una reserva.
    """
    id_reservation: int
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# -----------------------------
# ⏰ Reminder (Recordatorio)
# -----------------------------
class ReminderBase(BaseModel):
    """
    Define los atributos básicos de un recordatorio asociado a una reserva.
    """
    id_reservation: int
    reminder_datetime: datetime
    message: constr(strip_whitespace=True, min_length=1, max_length=255)
    state: Optional[bool] = True


class ReminderCreate(ReminderBase):
    """
    Esquema para creación de un recordatorio.
    """
    pass


class ReminderUpdate(BaseModel):
    """
    Esquema para actualización de un recordatorio existente.
    """
    reminder_datetime: Optional[datetime] = None
    message: Optional[constr(strip_whitespace=True, min_length=1, max_length=255)] = None
    state: Optional[bool] = None


class ReminderOut(ReminderBase):
    """
    Esquema de salida al consultar recordatorios.
    """
    id_reminder: int

    model_config = {"from_attributes": True}