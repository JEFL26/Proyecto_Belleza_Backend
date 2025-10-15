# app/schemas/usuario.py
from pydantic import BaseModel, EmailStr, Field, constr
from typing import Optional

# ==============================
# 👤 Esquemas para Usuarios y Roles
# ==============================


# -----------------------------
# 🧩 Role (Rol de usuario)
# -----------------------------
class RoleBase(BaseModel):
    """
    Esquema base que define los atributos comunes de un rol.
    """
    name: constr(strip_whitespace=True, min_length=1, max_length=50)
    description: Optional[str] = None
    state: Optional[bool] = True


class RoleCreate(RoleBase):
    """
    Esquema para crear un nuevo rol.
    """
    pass


class RoleOut(RoleBase):
    """
    Esquema de salida para devolver información de roles existentes.
    """
    id_role: int

    model_config = {"from_attributes": True}


# -----------------------------
# 🧍 UserAccount (Cuenta de usuario)
# -----------------------------
class UserAccountBase(BaseModel):
    """
    Define los atributos básicos comunes a cualquier cuenta de usuario.
    """
    email: EmailStr
    state: Optional[bool] = True
    is_logged_in: Optional[bool] = False


class UserAccountCreate(UserAccountBase):
    """
    Esquema para crear una cuenta de usuario.
    """
    password: constr(min_length=6, max_length=255)
    id_role: int


class UserAccountUpdate(BaseModel):
    """
    Esquema para actualizar parcialmente una cuenta de usuario existente.
    """
    email: Optional[EmailStr] = None
    password: Optional[constr(min_length=6, max_length=255)] = None
    is_logged_in: Optional[bool] = None
    state: Optional[bool] = None
    id_role: Optional[int] = None


class UserAccountOut(UserAccountBase):
    """
    Esquema de salida para mostrar información de una cuenta de usuario.
    """
    id_user: int = Field(..., alias="id")  # Mapea id -> id_user
    id_role: int

    model_config = {"from_attributes": True}


# -----------------------------
# 🪪 UserProfile (Perfil de usuario)
# -----------------------------
class UserProfileBase(BaseModel):
    """
    Define la información personal asociada a una cuenta de usuario.
    """
    first_name: constr(strip_whitespace=True, min_length=1, max_length=50)
    last_name: constr(strip_whitespace=True, min_length=1, max_length=50)
    phone: constr(strip_whitespace=True, min_length=7, max_length=15)
    state: Optional[bool] = True


class UserProfileCreate(UserProfileBase):
    """
    Esquema para crear un perfil de usuario.
    El `id_user` se asigna desde el backend automáticamente.
    """
    pass


class UserProfileUpdate(BaseModel):
    """
    Esquema para actualizar información del perfil del usuario.
    """
    first_name: Optional[constr(strip_whitespace=True, min_length=1, max_length=50)] = None
    last_name: Optional[constr(strip_whitespace=True, min_length=1, max_length=50)] = None
    phone: Optional[constr(strip_whitespace=True, min_length=7, max_length=15)] = None
    state: Optional[bool] = None


class UserProfileOut(UserProfileBase):
    """
    Esquema de salida que muestra la información pública del perfil.
    """
    id_profile: int = Field(..., alias="id")  # Mapea id -> id_profile
    id_user: int

    model_config = {"from_attributes": True}