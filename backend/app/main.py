from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.core.database import engine, SessionLocal, Base
from app.core.config import settings
from app.core.init_db import init_default_admin
from app.api.v1.auth import router as auth_router
from app.api.v1.admin import router as admin_router
from app.api.v1.manager import router as manager_router
from app.api.v1.odoo import router as odoo_router
from app.api.v1.tables import router as tables_router
from app.api.v1.menu import router as menu_router
from app.api.v1.orders import router as orders_router
from app.api.v1.billing import router as billing_router
from app.api.v1.communication import router as communication_router
from app.web.router import router as web_router
import app.models # S'assure que tous les modèles (User, Restaurant) sont chargés
from sqlalchemy import text

# Mise à jour de compatibilité du schéma PostgreSQL
try:
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE orders ADD COLUMN IF NOT EXISTS global_invoice_id INTEGER;"))
        conn.execute(text("ALTER TABLE orders ADD COLUMN IF NOT EXISTS is_invoiced BOOLEAN DEFAULT FALSE;"))
        conn.execute(text("ALTER TABLE orders ADD COLUMN IF NOT EXISTS invoiced_at TIMESTAMP WITHOUT TIME ZONE;"))
        conn.execute(text("ALTER TABLE restaurant_config ADD COLUMN IF NOT EXISTS billing_frequency VARCHAR(20) DEFAULT 'daily';"))
        conn.execute(text("ALTER TABLE restaurant_config ADD COLUMN IF NOT EXISTS menu_prices_include_tax BOOLEAN DEFAULT TRUE;"))
        conn.execute(text("ALTER TABLE restaurant_config ADD COLUMN IF NOT EXISTS default_tax_regime VARCHAR(100) DEFAULT 'Régime du Réel Normal d''Imposition (RNI)';"))
        conn.execute(text("ALTER TABLE restaurant_config ADD COLUMN IF NOT EXISTS ifu VARCHAR(50) DEFAULT '000123456789A';"))
        conn.execute(text("ALTER TABLE restaurant_config ADD COLUMN IF NOT EXISTS fiscal_division VARCHAR(150) DEFAULT 'DGI - Division Fiscale des Moyennes Entreprises';"))
        conn.execute(text("ALTER TABLE restaurant_config ADD COLUMN IF NOT EXISTS dgi_qr_enabled BOOLEAN DEFAULT TRUE;"))
        conn.execute(text("ALTER TABLE global_invoices ADD COLUMN IF NOT EXISTS manager_name TEXT;"))
        conn.execute(text("ALTER TABLE global_invoices ADD COLUMN IF NOT EXISTS manager_login TEXT;"))
        conn.execute(text("ALTER TABLE global_invoices ADD COLUMN IF NOT EXISTS manager_id INTEGER;"))
        conn.execute(text("ALTER TABLE global_invoices ADD COLUMN IF NOT EXISTS opened_at TIMESTAMP WITHOUT TIME ZONE;"))
        conn.execute(text("DROP INDEX IF EXISTS ix_global_invoice_items_order_id;"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS ix_global_invoice_items_order_id ON global_invoice_items (order_id);"))
        conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS uq_global_invoice_item_order ON global_invoice_items (global_invoice_id, order_id);"))
        conn.execute(text("ALTER TABLE menu_items ADD COLUMN IF NOT EXISTS available_quantity INTEGER DEFAULT 0;"))
        conn.execute(text("UPDATE menu_items SET available_quantity = 0 WHERE available_quantity IS NULL;"))
        conn.commit()

except Exception as e:
    print(f"Erreur vérification colonnes DB : {e}")

# Création automatique des tables dans PostgreSQL restaurant_db
Base.metadata.create_all(bind=engine)

# Initialisation du compte Administrateur par défaut si absent et des règles fiscales / factures globales
try:
    with SessionLocal() as db_session:
        init_default_admin(db_session)
        from app.services.billing_service import billing_service
        billing_service.ensure_default_tax_rules(db_session)
        billing_service.sync_all_existing_orders_to_invoices(db_session)
except Exception as e:
    print(f"Erreur lors de l'initialisation de l'administrateur et facturation : {e}")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend Restaurant (Patron & Moteur) avec Espaces Dédiés Administrateur et Gérant, et intégration Odoo ERP.",
    version=settings.VERSION
)

# Inclusion des routes API V1
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(admin_router, prefix=settings.API_V1_STR)
app.include_router(manager_router, prefix=settings.API_V1_STR)
app.include_router(odoo_router, prefix=settings.API_V1_STR)
app.include_router(tables_router, prefix=settings.API_V1_STR)
app.include_router(menu_router, prefix=settings.API_V1_STR)
app.include_router(orders_router, prefix=settings.API_V1_STR)
app.include_router(billing_router, prefix=settings.API_V1_STR)
app.include_router(communication_router, prefix=settings.API_V1_STR)

# Interface Visuelle Interactive des Espaces Dédiés
app.include_router(web_router)

@app.get("/login")
def login_redirect():
    return RedirectResponse(url="/app")

@app.get("/")
def root():
    return {
        "app": settings.PROJECT_NAME,
        "status": "running",
        "role": "Moteur & Patron de Gestion de Restaurant",
        "portail_web": "/app",
        "docs_url": "/docs",
        "odoo_target_db": settings.ODOO_DB
    }

@app.get("/api/v1/health")
def health():
    return {
        "status": "healthy"
    }

@app.get("/api/v1/settings")
def get_global_settings():
    with SessionLocal() as db:
        from app.models.restaurant import RestaurantConfig
        cfg = db.query(RestaurantConfig).first()
        if not cfg:
            cfg = RestaurantConfig()
            db.add(cfg)
            db.commit()
            db.refresh(cfg)
        return {
            "restaurant_name": cfg.restaurant_name,
            "restaurant_subtitle": cfg.restaurant_subtitle,
            "logo_url": cfg.logo_url,
            "ifu": cfg.ifu or cfg.nif,
            "nif": cfg.nif or cfg.ifu,
            "nim": cfg.nim,
            "rccm": cfg.rccm,
            "default_tax_regime": cfg.default_tax_regime,
            "fiscal_division": cfg.fiscal_division or cfg.tax_center,
            "tax_center": cfg.tax_center or cfg.fiscal_division,
            "tax_rate": cfg.tax_rate,
            "legal_mention": cfg.legal_mention,
            "dgi_qr_enabled": cfg.dgi_qr_enabled,
            "address": cfg.address,
            "phone": cfg.phone,
            "email": cfg.email,
            "website": cfg.website,
            "primary_color": cfg.primary_color,
            "bg_color": cfg.bg_color
        }


async def odoo_background_sync_worker():
    """Tâche de fond qui surveille et synchronise automatiquement toutes les actions d'Odoo vers PostgreSQL."""
    import asyncio
    from app.services.odoo_service import odoo_service
    await asyncio.sleep(5) # Pause initiale
    while True:
        try:
            with SessionLocal() as db_session:
                counts = odoo_service.sync_all_from_odoo(db_session)
                total_changes = sum(counts.values())
                if total_changes >0:
                    print(f" [ACTION ODOO DÉTECTÉE & SYNCHRONISÉE] {counts['dishes']} plats, {counts['managers']} gérants, {counts['orders']} commandes enregistrés dans PostgreSQL backend !")
        except Exception:
            pass
        await asyncio.sleep(8)

@app.on_event("startup")
async def startup_event():
    import asyncio
    asyncio.create_task(odoo_background_sync_worker())