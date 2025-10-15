# app/schemas/usuario.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# =============================
#   Esquemas base
# =============================

class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    is_active: Optional[bool] = True
    is_admin: Optional[bool] = False

# =============================
#   Creación de usuario
# =============================

class UsuarioCreate(UsuarioBase):
    password: str

# =============================
#   Lectura / Respuesta
# =============================

class UsuarioRead(UsuarioBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Permite convertir desde SQLAlchemy ORM

# =============================
#   Login
# =============================

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"