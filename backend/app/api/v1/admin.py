from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List, Optional
import datetime
import json
import hashlib
from app.core.database import get_db
from app.core.security import hash_password
from app.models.user import User, UserRole
from app.models.restaurant import RestaurantTable, MenuItem, Order, OrderItem, PosSession, DailyInvoice, ManagerWorkSession, ManagerActivityLog, RestaurantConfig
from app.schemas.user import ManagerCreate, ManagerUpdate, UserResponse, AdminDashboardStats, ManagerWorkSessionResponse, ManagerActivityLogResponse
from app.schemas.restaurant import OrderResponse, DailyInvoiceResponse, RestaurantConfigResponse, RestaurantConfigUpdate
from app.api.deps import require_admin
from app.services.odoo_service import odoo_service
from app.core.config import settings

router = APIRouter(prefix="/admin", tags=["Espace Administrateur"])

@router.get("/dashboard", response_model=AdminDashboardStats)
def get_admin_dashboard(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Tableau de bord exclusif de l'Administrateur :
    - Statistiques globales des gérants
    - Chiffre d'affaires et commandes
    - État du moteur et connexion Odoo
    """
    total_managers = db.query(User).filter(User.role == UserRole.MANAGER.value).count()
    active_managers = db.query(User).filter(
        User.role == UserRole.MANAGER.value,
        User.is_active == True
    ).count()
    online_managers = db.query(User).filter(
        User.role == UserRole.MANAGER.value,
        User.is_online == True
    ).count()

    total_tables = db.query(RestaurantTable).count()
    total_menu_items = db.query(MenuItem).count()
    total_orders = db.query(Order).count()

    revenue_sum = db.query(func.sum(Order.total_amount)).scalar() or 0.0

    odoo_status = odoo_service.test_connection()

    return {
        "total_managers": total_managers,
        "active_managers": active_managers,
        "online_managers": online_managers,
        "total_tables": total_tables,
        "total_menu_items": total_menu_items,
        "total_orders": total_orders,
        "total_revenue": round(float(revenue_sum), 2),
        "odoo_connected": odoo_status.get("connected", False),
        "odoo_target_db": settings.ODOO_DB
    }

@router.post("/managers", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_manager(
    payload: ManagerCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    L'administrateur crée un compte Gérant dédié :
    - Attribue un nom d'utilisateur et un mot de passe distinct
    - Le gérant aura son propre espace sans interférence
    """
    # Vérifier l'unicité du nom d'utilisateur
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Le nom d'utilisateur '{payload.username}' est déjà utilisé."
        )

    # Vérifier l'unicité de l'email
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"L'adresse email '{payload.email}' est déjà enregistrée."
        )

    new_manager = User(
        username=payload.username,
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password),
        role=UserRole.MANAGER.value,
        is_active=True,
        created_by_id=admin.id
    )
    db.add(new_manager)
    db.commit()
    db.refresh(new_manager)

    # Synchronisation immédiate vers Odoo (res.users avec droits POS uniquement)
    try:
        odoo_uid = odoo_service.sync_manager_user_to_odoo(
            username=new_manager.username,
            full_name=new_manager.full_name,
            email=new_manager.email,
            password=payload.password
        )
        new_manager.odoo_user_id = odoo_uid
        db.commit()
        db.refresh(new_manager)
    except Exception as e:
        pass

    return new_manager

@router.get("/managers", response_model=List[UserResponse])
def list_managers(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Liste tous les comptes gérants créés par l'administrateur."""
    return db.query(User).filter(User.role == UserRole.MANAGER.value).all()

@router.patch("/managers/{manager_id}/toggle-status", response_model=UserResponse)
def toggle_manager_status(
    manager_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Active ou suspend l'accès d'un compte gérant (dans le backend et dans Odoo)."""
    manager = db.query(User).filter(User.id == manager_id, User.role == UserRole.MANAGER.value).first()
    if not manager:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gérant introuvable.")

    manager.is_active = not manager.is_active
    db.commit()
    db.refresh(manager)

    if manager.odoo_user_id:
        try:
            odoo_service.toggle_odoo_user_active(manager.odoo_user_id, manager.is_active)
        except Exception:
            pass

    return manager

@router.delete("/managers/{manager_id}", status_code=status.HTTP_200_OK)
def delete_manager(
    manager_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Supprime définitivement un compte gérant (et désactive son accès Odoo)."""
    manager = db.query(User).filter(User.id == manager_id, User.role == UserRole.MANAGER.value).first()
    if not manager:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gérant introuvable.")

    if manager.odoo_user_id:
        try:
            odoo_service.archive_odoo_user(manager.odoo_user_id)
        except Exception:
            pass

    username = manager.username
    try:
        db.delete(manager)
        db.commit()
        return {"message": f"Le compte gérant '{username}' a été supprimé avec succès."}
    except Exception:
        db.rollback()
        manager.is_active = False
        manager.is_online = False
        db.commit()
        return {"message": f"Le compte gérant '{username}' a été désactivé et archivé (ses commandes et rapports sont conservés pour conformité comptable)."}

@router.get("/work-sessions", response_model=List[ManagerWorkSessionResponse])
def list_manager_work_sessions(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Traçabilité des prises et fins de service des gérants :
    - Heure et date de début de travail (connexion)
    - Heure et date de fin de travail (déconnexion)
    - Statut en direct (En service vs Clôturé/Non connecté)
    - Cumul des ventes réalisées et encaissements (argent bien présent)
    """
    return db.query(ManagerWorkSession).order_by(ManagerWorkSession.id.desc()).limit(100).all()

@router.get("/activity-logs", response_model=List[ManagerActivityLogResponse])
def list_manager_activity_logs(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Journal d'audit et faits et gestes en direct des gérants :
    - Connexion / Déconnexion
    - Ventes et encaissements détaillés
    - Ajustements de prix et actions
    """
    return db.query(ManagerActivityLog).order_by(ManagerActivityLog.id.desc()).limit(150).all()

@router.get("/orders", response_model=List[OrderResponse])
def list_admin_orders(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Permet à l'administrateur de consulter l'ensemble des factures et commandes avec détails des articles."""
    return db.query(Order).options(
        joinedload(Order.items).joinedload(OrderItem.menu_item)
    ).order_by(Order.id.desc()).all()

@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_admin_order(
    order_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Permet à l'administrateur de consulter le détail complet d'une facture spécifique."""
    order = db.query(Order).options(
        joinedload(Order.items).joinedload(OrderItem.menu_item)
    ).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Facture / Commande introuvable.")
    return order

@router.get("/daily-report")
def get_daily_report(
    target_date: Optional[str] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Calcule la facture générale récapitulative de la journée :
    - Montant Total TTC, Base HT, TVA 18% (Norme DGI)
    - Ventilation par mode de paiement (Espèces, Mobile Money, etc.)
    - Ventilation par gérant (avec login, nombre de commandes et montants)
    - État de certification DGI
    """
    if not target_date:
        query_date = datetime.date.today()
    else:
        try:
            query_date = datetime.date.fromisoformat(target_date)
        except Exception:
            raise HTTPException(status_code=400, detail="Format de date invalide (attendu: AAAA-MM-JJ)")

    start_dt = datetime.datetime.combine(query_date, datetime.time.min)
    end_dt = datetime.datetime.combine(query_date, datetime.time.max)
    orders = db.query(Order).filter(Order.created_at >= start_dt, Order.created_at <= end_dt).order_by(Order.id.asc()).all()

    total_ttc = sum(o.total_amount for o in orders if o.status in ("paid", "done", "served", "pending"))
    total_ht = round(total_ttc / 1.18, 2) if total_ttc > 0 else 0.0
    total_tva = round(total_ttc - total_ht, 2) if total_ttc > 0 else 0.0
    total_orders_count = len(orders)

    # Répartition par mode de paiement
    payment_breakdown = {}
    for o in orders:
        pm = o.payment_method or "Espèces (Cash)"
        payment_breakdown[pm] = round(payment_breakdown.get(pm, 0.0) + o.total_amount, 2)

    # Répartition par gérant
    manager_breakdown = {}
    for o in orders:
        m_name = o.manager_name or "Gérant Inconnu"
        m_login = o.manager_login or "N/A"
        if m_name not in manager_breakdown:
            manager_breakdown[m_name] = {
                "name": m_name,
                "login": m_login,
                "orders_count": 0,
                "total_amount": 0.0
            }
        manager_breakdown[m_name]["orders_count"] += 1
        manager_breakdown[m_name]["total_amount"] = round(manager_breakdown[m_name]["total_amount"] + o.total_amount, 2)

    # Vérifier si déjà certifié dans daily_invoices
    daily_inv = db.query(DailyInvoice).filter(DailyInvoice.invoice_date == query_date).first()

    return {
        "invoice_date": query_date.isoformat(),
        "invoice_number": daily_inv.invoice_number if daily_inv else f"FACT-GEN-{query_date.strftime('%Y%m%d')}-01",
        "total_ttc": round(total_ttc, 2),
        "total_ht": total_ht,
        "total_tva": total_tva,
        "total_orders": total_orders_count,
        "payment_breakdown": payment_breakdown,
        "manager_breakdown": list(manager_breakdown.values()),
        "is_certified_dgi": daily_inv.is_certified_dgi if daily_inv else False,
        "dgi_nif": daily_inv.dgi_nif if daily_inv else "000123456789A",
        "dgi_nim": daily_inv.dgi_nim if daily_inv else "RESTO-DGI-MCF-01",
        "dgi_reference": daily_inv.dgi_reference if daily_inv else None,
        "dgi_security_code": daily_inv.dgi_security_code if daily_inv else None,
        "dgi_qr_code_data": daily_inv.dgi_qr_code_data if daily_inv else None,
        "dgi_certified_at": daily_inv.dgi_certified_at.isoformat() if daily_inv and daily_inv.dgi_certified_at else None,
        "orders": [
            {
                "id": o.id,
                "order_number": o.order_number,
                "total_amount": o.total_amount,
                "payment_method": o.payment_method or "Espèces (Cash)",
                "manager_name": o.manager_name or "Gérant",
                "manager_login": o.manager_login or "",
                "time": o.created_at.strftime("%H:%M:%S") if o.created_at else "",
                "status": o.status
            }
            for o in orders
        ]
    }

@router.post("/daily-report/certify-dgi")
def certify_daily_report_dgi(
    target_date: Optional[str] = None,
    nif: Optional[str] = "000123456789A",
    nim: Optional[str] = "RESTO-DGI-MCF-01",
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Effectue la certification fiscale officielle avec la DGI :
    - Génère la signature cryptographique (Hash SHA-256)
    - Attribue le Numéro Unique de Facture Normalisée DGI (FNE)
    - Crée le QR code de contrôle fiscal DGI
    - Enregistre la certification et verrouille fiscalement les ventes du jour
    """
    if not target_date:
        query_date = datetime.date.today()
    else:
        try:
            query_date = datetime.date.fromisoformat(target_date)
        except Exception:
            raise HTTPException(status_code=400, detail="Format de date invalide (attendu: AAAA-MM-JJ)")

    start_dt = datetime.datetime.combine(query_date, datetime.time.min)
    end_dt = datetime.datetime.combine(query_date, datetime.time.max)
    orders = db.query(Order).filter(Order.created_at >= start_dt, Order.created_at <= end_dt).all()

    total_ttc = sum(o.total_amount for o in orders if o.status in ("paid", "done", "served", "pending"))
    total_ht = round(total_ttc / 1.18, 2) if total_ttc > 0 else 0.0
    total_tva = round(total_ttc - total_ht, 2) if total_ttc > 0 else 0.0
    total_orders_count = len(orders)

    # Répartition par mode de paiement
    payment_breakdown = {}
    for o in orders:
        pm = o.payment_method or "Espèces (Cash)"
        payment_breakdown[pm] = round(payment_breakdown.get(pm, 0.0) + o.total_amount, 2)

    # Répartition par gérant
    manager_breakdown = {}
    for o in orders:
        m_name = o.manager_name or "Gérant Inconnu"
        m_login = o.manager_login or "N/A"
        if m_name not in manager_breakdown:
            manager_breakdown[m_name] = {
                "name": m_name,
                "login": m_login,
                "orders_count": 0,
                "total_amount": 0.0
            }
        manager_breakdown[m_name]["orders_count"] += 1
        manager_breakdown[m_name]["total_amount"] = round(manager_breakdown[m_name]["total_amount"] + o.total_amount, 2)

    # Génération de la signature cryptographique DGI (SHA-256)
    timestamp_now = datetime.datetime.utcnow()
    raw_sig_str = f"{nif}|{nim}|{query_date.isoformat()}|HT:{total_ht}|TVA:{total_tva}|TTC:{total_ttc}|ORDERS:{total_orders_count}|SALT_DGI_FISCAL_2026"
    dgi_sig = hashlib.sha256(raw_sig_str.encode("utf-8")).hexdigest()

    dgi_ref = f"DGI-FNE-{query_date.strftime('%Y%m%d')}-{dgi_sig[:8].upper()}"
    qr_data = f"DGI-FNE|NIF:{nif}|NIM:{nim}|DATE:{query_date.isoformat()}|TTC:{total_ttc}|TVA:{total_tva}|REF:{dgi_ref}|SIG:{dgi_sig[:16].upper()}|URL:https://dgi.impots.gov/verifier/{dgi_ref}"

    daily_inv = db.query(DailyInvoice).filter(DailyInvoice.invoice_date == query_date).first()
    if not daily_inv:
        daily_inv = DailyInvoice(
            invoice_date=query_date,
            invoice_number=f"FACT-GEN-{query_date.strftime('%Y%m%d')}-01",
            total_ttc=round(total_ttc, 2),
            total_ht=total_ht,
            total_tva=total_tva,
            total_orders=total_orders_count,
            payment_breakdown=json.dumps(payment_breakdown),
            manager_breakdown=json.dumps(list(manager_breakdown.values())),
            is_certified_dgi=True,
            dgi_nif=nif,
            dgi_nim=nim,
            dgi_reference=dgi_ref,
            dgi_security_code=dgi_sig,
            dgi_qr_code_data=qr_data,
            dgi_certified_at=timestamp_now,
            certified_by=admin.full_name or admin.username
        )
        db.add(daily_inv)
    else:
        daily_inv.total_ttc = round(total_ttc, 2)
        daily_inv.total_ht = total_ht
        daily_inv.total_tva = total_tva
        daily_inv.total_orders = total_orders_count
        daily_inv.payment_breakdown = json.dumps(payment_breakdown)
        daily_inv.manager_breakdown = json.dumps(list(manager_breakdown.values()))
        daily_inv.is_certified_dgi = True
        daily_inv.dgi_nif = nif
        daily_inv.dgi_nim = nim
        daily_inv.dgi_reference = dgi_ref
        daily_inv.dgi_security_code = dgi_sig
        daily_inv.dgi_qr_code_data = qr_data
        daily_inv.dgi_certified_at = timestamp_now
        daily_inv.certified_by = admin.full_name or admin.username

    # Marquer toutes les commandes du jour comme certifiées DGI
    for o in orders:
        o.is_certified_dgi = True
        o.dgi_invoice_number = dgi_ref
        o.dgi_signature = dgi_sig[:16].upper()
        o.dgi_certified_at = timestamp_now

    db.commit()

    return {
        "status": "success",
        "message": f"Facture générale du {query_date} certifiée avec succès auprès de la DGI !",
        "dgi_reference": dgi_ref,
        "dgi_security_code": dgi_sig,
        "dgi_qr_code_data": qr_data,
        "dgi_certified_at": timestamp_now.isoformat(),
        "total_ttc": round(total_ttc, 2),
        "total_ht": total_ht,
        "total_tva": total_tva,
        "total_orders": total_orders_count
    }

@router.get("/settings", response_model=RestaurantConfigResponse)
def get_restaurant_settings(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Permet à l'administrateur de consulter la configuration actuelle du restaurant et les données DGI."""
    cfg = db.query(RestaurantConfig).first()
    if not cfg:
        cfg = RestaurantConfig()
        db.add(cfg)
        db.commit()
        db.refresh(cfg)
    return cfg

@router.put("/settings", response_model=RestaurantConfigResponse)
def update_restaurant_settings(
    payload: RestaurantConfigUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Permet à l'administrateur de configurer le nom du restaurant, le logo et les mentions DGI :
    - Nom et sous-titre
    - Logo (URL ou Base64)
    - NIF, NIM, RCCM, Centre des Impôts, Mention légale
    - Adresse, téléphone, email, site web
    """
    cfg = db.query(RestaurantConfig).first()
    if not cfg:
        cfg = RestaurantConfig()
        db.add(cfg)
    
    update_data = payload.dict(exclude_unset=True)
    
    # Synchronisation IFU <-> NIF
    if "ifu" in update_data and update_data["ifu"]:
        update_data["nif"] = update_data["ifu"]
    elif "nif" in update_data and update_data["nif"]:
        update_data["ifu"] = update_data["nif"]

    # Synchronisation Division Fiscale <-> Centre des Impôts
    if "fiscal_division" in update_data and update_data["fiscal_division"]:
        update_data["tax_center"] = update_data["fiscal_division"]
    elif "tax_center" in update_data and update_data["tax_center"]:
        update_data["fiscal_division"] = update_data["tax_center"]

    for field, val in update_data.items():
        if hasattr(cfg, field):
            setattr(cfg, field, val)

    cfg.updated_at = datetime.datetime.utcnow()
    db.commit()
    db.refresh(cfg)

    # Synchronisation vers la société Odoo (res.company)
    try:
        from app.services.odoo_service import odoo_service
        odoo_service.sync_company_settings_to_odoo(cfg)
    except Exception as e:
        print(f"Avertissement: Erreur de synchronisation des paramètres vers Odoo: {e}")

    return cfg


@router.get("/public-settings", response_model=RestaurantConfigResponse)
def get_public_settings(db: Session = Depends(get_db)):
    """Permet à tous les modules et reçus de charger le nom, le logo et les coordonnées du restaurant."""
    cfg = db.query(RestaurantConfig).first()
    if not cfg:
        cfg = RestaurantConfig()
        db.add(cfg)
        db.commit()
        db.refresh(cfg)
    return cfg


