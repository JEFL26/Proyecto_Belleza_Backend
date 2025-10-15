# app/db/models.py
from sqlalchemy import Numeric, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from app.db.session import Base

# ==============================
# Rol de usuario
# ==============================
class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    state: Mapped[bool] = mapped_column(Boolean, default=True)

    users: Mapped[list["UserAccount"]] = relationship("UserAccount", back_populates="role")

# ==============================
# Cuenta de usuario
# ==============================
class UserAccount(Base):
    __tablename__ = "user_accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_logged_in: Mapped[bool] = mapped_column(Boolean, default=False)
    state: Mapped[bool] = mapped_column(Boolean, default=True)
    id_role: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relaciones
    role: Mapped["Role"] = relationship("Role", back_populates="users")
    profile: Mapped["UserProfile"] = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")

# ==============================
# Perfil de usuario
# ==============================
class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    id_user: Mapped[int] = mapped_column(Integer, ForeignKey("user_accounts.id", ondelete="CASCADE"), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)
    state: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relaciones
    user: Mapped["UserAccount"] = relationship("UserAccount", back_populates="profile")


class Service(Base):
    __tablename__ = "services"

    id_service: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    state: Mapped[bool] = mapped_column(Boolean, default=True)