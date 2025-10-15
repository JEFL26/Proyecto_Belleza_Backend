# app/core/security.py
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings
from typing import Optional
from loguru import logger

# ==============================
# Configuración general
# ==============================
ALGORITHM = "HS256"
# Contexto para encriptar contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ==============================
# 🔑 Funciones para contraseñas
# ==============================
def hash_password(password: str) -> str:
    """
    Genera un hash seguro para una contraseña en texto plano usando bcrypt.

    Args:
        password (str): Contraseña en texto plano.

    Returns:
        str: Hash seguro de la contraseña.

    Raises:
        ValueError: Si el argumento no es un texto válido.
    """
    try:
        if not isinstance(password, str):
            raise ValueError("La contraseña debe ser un texto válido.")

        # Truncar si excede 72 bytes (por límite de bcrypt)
        password_bytes = password.encode("utf-8")
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
            password = password_bytes.decode("utf-8", errors="ignore")

        hashed = pwd_context.hash(password)
        logger.debug("Contraseña hasheada correctamente.")
        return hashed
    except Exception as e:
        logger.error(f"Error al hashear contraseña: {e}")
        raise

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña coincide con su hash.

    Args:
        plain_password (str): Contraseña en texto plano.
        hashed_password (str): Hash de la contraseña.

    Returns:
        bool: True si coinciden, False si no.
    """
    try:
        result = pwd_context.verify(plain_password, hashed_password)
        logger.debug(f"Verificación de contraseña: {result}")
        return result
    except Exception as e:
        logger.error(f"Error al verificar contraseña: {e}")
        return False

# ==============================
# Funciones para tokens JWT
# ==============================
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token JWT con tiempo de expiración.

    Args:
        data (dict): Datos a codificar en el token.
        expires_delta (Optional[timedelta]): Tiempo de expiración del token.

    Returns:
        str: Token JWT codificado.
    """
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + (
            expires_delta or timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
        logger.debug("Token JWT creado correctamente.")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error al crear token JWT: {e}")
        raise

def verify_token(token: str) -> Optional[dict]:
    """
    Verifica la validez de un token JWT y devuelve su payload si es válido.

    Args:
        token (str): Token JWT a verificar.

    Returns:
        Optional[dict]: Payload decodificado si el token es válido, None si no.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug("Token JWT verificado correctamente.")
        return payload
    except JWTError as e:
        logger.warning(f"Token JWT inválido: {e}")
        return None