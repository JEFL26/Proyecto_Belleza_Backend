# app/schemas/servicio.py
from pydantic import BaseModel, Field, constr, conint, condecimal
from typing import Optional
from decimal import Decimal

# ==============================
# 💇‍♀️ Esquemas para Gestión de Servicios
# ==============================


# -----------------------------
# 📘 Base: definición común de atributos
# -----------------------------
class ServiceBase(BaseModel):
    """
    Define los campos base compartidos por todos los esquemas de servicio.
    """
    name: constr(strip_whitespace=True, min_length=1, max_length=100)
    description: Optional[str] = None
    duration_minutes: conint(gt=0)
    price: condecimal(max_digits=10, decimal_places=2, ge=0)
    state: Optional[bool] = True


# -----------------------------
# 🟢 Creación de servicios
# -----------------------------
class ServiceCreate(ServiceBase):
    """
    Esquema para creación de un nuevo servicio.
    """
    pass


# -----------------------------
# 📝 Actualización de servicios
# -----------------------------
class ServiceUpdate(BaseModel):
    """
    Esquema para actualización parcial de un servicio existente.
    """
    name: Optional[constr(strip_whitespace=True, min_length=1, max_length=100)] = None
    description: Optional[str] = None
    duration_minutes: Optional[conint(gt=0)] = None
    price: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    state: Optional[bool] = None


# -----------------------------
# 📤 Esquema de salida (consulta)
# -----------------------------
class ServiceOut(ServiceBase):
    """
    Esquema utilizado al devolver información de un servicio desde la API.
    """
    id_service: int

    model_config = {"from_attributes": True}