# app/schemas/usuario.py
from pydantic import BaseModel, EmailStr, Field, constr
from typing import Optional

# -----------------------------
# Role
# -----------------------------
class RoleBase(BaseModel):
    name: constr(strip_whitespace=True, min_length=1, max_length=50)
    description: Optional[str] = None
    state: Optional[bool] = True

class RoleCreate(RoleBase):
    pass

class RoleOut(RoleBase):
    id_role: int

    class Config:
        orm_mode = True

# -----------------------------
# UserAccount
# -----------------------------
class UserAccountBase(BaseModel):
    email: EmailStr
    state: Optional[bool] = True
    is_logged_in: Optional[bool] = False

class UserAccountCreate(UserAccountBase):
    password: constr(min_length=6, max_length=255)
    id_role: int

class UserAccountUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[constr(min_length=6, max_length=255)] = None
    is_logged_in: Optional[bool] = None
    state: Optional[bool] = None
    id_role: Optional[int] = None

class UserAccountOut(UserAccountBase):
    id_user: int = Field(..., alias="id")  # <- aquí mapeamos id -> id_user
    id_role: int

    class Config:
        orm_mode = True

# -----------------------------
# UserProfile
# -----------------------------
class UserProfileBase(BaseModel):
    first_name: constr(strip_whitespace=True, min_length=1, max_length=50)
    last_name: constr(strip_whitespace=True, min_length=1, max_length=50)
    phone: constr(strip_whitespace=True, min_length=7, max_length=15)
    state: Optional[bool] = True

class UserProfileCreate(UserProfileBase):
    pass  # <-- id_user eliminado, se asignará en backend

class UserProfileUpdate(BaseModel):
    first_name: Optional[constr(strip_whitespace=True, min_length=1, max_length=50)] = None
    last_name: Optional[constr(strip_whitespace=True, min_length=1, max_length=50)] = None
    phone: Optional[constr(strip_whitespace=True, min_length=7, max_length=15)] = None
    state: Optional[bool] = None

class UserProfileOut(UserProfileBase):
    id_profile: int = Field(..., alias="id")  # mapear id -> id_profile
    id_user: int  # aquí sí necesitamos mostrarlo

    class Config:
        orm_mode = True
