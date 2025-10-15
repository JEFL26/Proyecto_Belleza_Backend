# app/db/models.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base


# =============================
#   Modelo: Usuario
# =============================
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relación con reservas
    reservas = relationship("Reserva", back_populates="usuario", cascade="all, delete-orphan")


# =============================
#   Modelo: Servicio
# =============================
class Servicio(Base):
    __tablename__ = "servicios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)
    precio = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relación con reservas
    reservas = relationship("Reserva", back_populates="servicio", cascade="all, delete-orphan")


# =============================
#   Modelo: Reserva
# =============================
class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    servicio_id = Column(Integer, ForeignKey("servicios.id", ondelete="CASCADE"), nullable=False)
    fecha_reserva = Column(DateTime, nullable=False)
    estado = Column(String(50), default="pendiente")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relaciones inversas
    usuario = relationship("Usuario", back_populates="reservas")
    servicio = relationship("Servicio", back_populates="reservas")