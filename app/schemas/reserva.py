# app/schemas/reserva.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# =============================
#   Esquemas base
# =============================

class ReservaBase(BaseModel):
    usuario_id: int
    servicio_id: int
    fecha_reserva: datetime
    estado: Optional[str] = Field(default="pendiente", description="Estado de la reserva")

# =============================
#   Creación de reserva
# =============================

class ReservaCreate(ReservaBase):
    pass

# =============================
#   Lectura / Respuesta
# =============================

class ReservaRead(ReservaBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True