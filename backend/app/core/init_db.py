import logging
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import hash_password
from app.models.user import User, UserRole

from sqlalchemy import text

logger = logging.getLogger("init_db")

def init_default_admin(db: Session) -> None:
    """Initialise le compte Administrateur par défaut s'il n'existe pas encore et applique les migrations douces."""
    # Migrations de schéma douces (compatibilité colonnes)
    try:
        db.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS is_online BOOLEAN DEFAULT FALSE;"))
        db.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login_at TIMESTAMP;"))
        db.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS last_logout_at TIMESTAMP;"))
        db.execute(text("ALTER TABLE orders ADD COLUMN IF NOT EXISTS work_session_id INTEGER;"))
        db.commit()
    except Exception as e:
        logger.warning(f"Note migration schéma: {e}")
        db.rollback()

    admin_exists = db.query(User).filter(User.role == UserRole.ADMIN.value).first()
    if not admin_exists:
        logger.info("Aucun administrateur détecté. Création de l'Administrateur par défaut...")
        admin = User(
            username=settings.FIRST_ADMIN_USERNAME,
            email=settings.FIRST_ADMIN_EMAIL,
            full_name=settings.FIRST_ADMIN_FULL_NAME,
            hashed_password=hash_password(settings.FIRST_ADMIN_PASSWORD),
            role=UserRole.ADMIN.value,
            is_active=True
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        logger.info(f"Administrateur '{admin.username}' créé avec succès pour l'Espace Admin.")
    else:
        logger.info(f"Administrateur déjà présent ({admin_exists.username}).")

