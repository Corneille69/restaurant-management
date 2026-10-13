import datetime
import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Rôle : "admin" ou "manager"
    role = Column(String(20), default=UserRole.MANAGER.value, nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_online = Column(Boolean, default=False, nullable=False, index=True) # Connecté actuellement
    last_login_at = Column(DateTime, nullable=True) # Date et heure de dernière connexion
    last_logout_at = Column(DateTime, nullable=True) # Date et heure de dernière déconnexion

    # Synchronisation Odoo ERP
    odoo_user_id = Column(Integer, nullable=True, index=True)

    # Traçabilité : l'admin qui a créé ce compte gérant
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relation vers les gérants créés par cet admin
    created_users = relationship("User", backref="created_by", remote_side=[id])
