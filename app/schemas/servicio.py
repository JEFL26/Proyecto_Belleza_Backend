# app/schemas/servicio.py
from pydantic import BaseModel, Field, constr, conint, condecimal
from typing import Optional
from decimal import Decimal

class ServiceBase(BaseModel):
    name: constr(strip_whitespace=True, min_length=1, max_length=100)
    description: Optional[str] = None
    duration_minutes: conint(gt=0)
    price: condecimal(max_digits=10, decimal_places=2, ge=0)
    state: Optional[bool] = True

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    name: Optional[constr(strip_whitespace=True, min_length=1, max_length=100)] = None
    description: Optional[str] = None
    duration_minutes: Optional[conint(gt=0)] = None
    price: Optional[condecimal(max_digits=10, decimal_places=2, ge=0)] = None
    state: Optional[bool] = None

class ServiceOut(ServiceBase):
    id_service: int

    class Config:
        orm_mode = True
