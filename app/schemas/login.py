# app/schemas/login.py
from pydantic import BaseModel, EmailStr

# ==============================
# 🧾 Esquema: Solicitud de inicio de sesión
# ==============================
class LoginRequest(BaseModel):
    """
    Representa los datos requeridos para que un usuario inicie sesión en el sistema.

    Atributos:
        email (EmailStr): Correo electrónico del usuario.
        password (str): Contraseña en texto plano ingresada por el usuario.
    """
    email: EmailStr
    password: str