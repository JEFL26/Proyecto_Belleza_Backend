# app/schemas/servicio.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# =============================
#   Esquemas base
# =============================

class ServicioBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float = Field(..., gt=0, description="Precio del servicio")

# =============================
#   Creación de servicio
# =============================

class ServicioCreate(ServicioBase):
    pass

# =============================
#   Lectura / Respuesta
# =============================

class ServicioRead(ServicioBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True