# app/db/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, func
from sqlalchemy.orm import relationship
from app.db.session import Base

# ==============================
# 👤 Modelo Usuario
# ==============================
class Usuario(Base):
    """
    Representa un usuario del sistema.

    Atributos:
        id (int): Identificador único del usuario.
        nombre (str): Nombre completo.
        email (str): Correo electrónico único.
        hashed_password (str): Contraseña hasheada.
        is_active (bool): Indica si el usuario está activo.
        is_admin (bool): Indica si el usuario tiene permisos de administrador.
        created_at (datetime): Fecha de creación del registro.
        reservas (List[Reserva]): Relación con las reservas realizadas por el usuario.
    """
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relación con reservas
    reservas = relationship("Reserva", back_populates="usuario")

# ==============================
# 💅 Modelo Servicio
# ==============================
class Servicio(Base):
    """
    Representa un servicio ofrecido en el centro de belleza.

    Atributos:
        id (int): Identificador único del servicio.
        nombre (str): Nombre del servicio.
        descripcion (str): Descripción breve del servicio.
        precio (float): Precio en moneda local.
        duracion_minutos (int): Duración del servicio en minutos.
        is_active (bool): Indica si el servicio está disponible.
        reservas (List[Reserva]): Relación con las reservas asociadas a este servicio.
    """
    __tablename__ = "servicios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255))
    precio = Column(Float, nullable=False)
    duracion_minutos = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)

    reservas = relationship("Reserva", back_populates="servicio")

# ==============================
# 📅 Modelo Reserva
# ==============================
class Reserva(Base):
    """
    Representa una reserva realizada por un usuario para un servicio específico.

    Atributos:
        id (int): Identificador único de la reserva.
        usuario_id (int): FK al usuario que realiza la reserva.
        servicio_id (int): FK al servicio reservado.
        fecha_hora (datetime): Fecha y hora de la reserva.
        estado (str): Estado de la reserva ("pendiente", "confirmado", "cancelado").
        created_at (datetime): Fecha de creación del registro.
        usuario (Usuario): Relación con el usuario.
        servicio (Servicio): Relación con el servicio.
    """
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    servicio_id = Column(Integer, ForeignKey("servicios.id"), nullable=False)
    fecha_hora = Column(DateTime(timezone=True), nullable=False)
    estado = Column(String(50), default="pendiente")  # pendiente, confirmado, cancelado
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    usuario = relationship("Usuario", back_populates="reservas")
    servicio = relationship("Servicio", back_populates="reservas")