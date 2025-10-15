# app/schemas/reserva.py
from pydantic import BaseModel, Field, constr, condecimal
from typing import Optional
from datetime import datetime
from decimal import Decimal

# -----------------------------
# ReservationStatus
# -----------------------------
class ReservationStatusBase(BaseModel):
    name: constr(strip_whitespace=True, min_length=1, max_length=50)
    state: Optional[bool] = True

class ReservationStatusCreate(ReservationStatusBase):
    pass

class ReservationStatusOut(ReservationStatusBase):
    id_reservation_status: int

    class Config:
        orm_mode = True

# -----------------------------
# Reservation (Reserva)
# -----------------------------
class ReservationBase(BaseModel):
    id_user: int = Field(..., description="ID del cliente que hace la reserva")
    id_service: int
    scheduled_datetime: datetime
    total_price: condecimal(max_digits=10, decimal_places=2, ge=0)
    payment_method: constr(strip_whitespace=True, min_length=1, max_length=50)
    state: Optional[bool] = True
    id_reservation_status: Optional[int] = Field(1, description="Estado por defecto: Pending -> 1")

class ReservationCreate(ReservationBase):
    pass

class ReservationUpdate(BaseModel):
    id_service: Optional[int] = None
    scheduled_datetime: Optional[datetime] = None
    total_price: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    payment_method: Optional[constr(strip_whitespace=True, min_length=1, max_length=50)] = None
    state: Optional[bool] = None
    id_reservation_status: Optional[int] = None

class ReservationOut(ReservationBase):
    id_reservation: int
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# -----------------------------
# Reminder (Recordatorio)
# -----------------------------
class ReminderBase(BaseModel):
    id_reservation: int
    reminder_datetime: datetime
    message: constr(strip_whitespace=True, min_length=1, max_length=255)
    state: Optional[bool] = True

class ReminderCreate(ReminderBase):
    pass

class ReminderUpdate(BaseModel):
    reminder_datetime: Optional[datetime] = None
    message: Optional[constr(strip_whitespace=True, min_length=1, max_length=255)] = None
    state: Optional[bool] = None

class ReminderOut(ReminderBase):
    id_reminder: int

    class Config:
        orm_mode = True
