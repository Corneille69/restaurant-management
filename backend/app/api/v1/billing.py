import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.core.database import get_db
from app.models.restaurant import (
    TaxRule, GlobalInvoice, GlobalInvoiceItem, 
    GlobalInvoiceAuditLog, RestaurantConfig, Order
)
from app.models.user import User
from app.schemas.billing import (
    TaxRuleCreate, TaxRuleUpdate, TaxRuleResponse,
    GlobalInvoiceResponse, GlobalInvoiceDetailResponse,
    GlobalInvoiceAuditLogResponse, BillingConfigResponse,
    BillingConfigUpdate, GenerateInvoiceRequest, CertifyInvoiceRequest
)
from app.services.billing_service import billing_service
from app.api.deps import require_admin, get_current_user_optional

router = APIRouter(prefix="/billing", tags=["Facturation Globale & Fiscalité DGI"])


# =========================================================================
# 1. RÈGLES FISCALES DGI CONFIGURABLES (Exigence 6)
# =========================================================================

@router.get("/tax-rules", response_model=List[TaxRuleResponse])
def list_tax_rules(
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Liste toutes les règles fiscales DGI configurées dans le système."""
    billing_service.ensure_default_tax_rules(db)
    query = db.query(TaxRule)
    if is_active is not None:
        query = query.filter(TaxRule.is_active == is_active)
    return query.order_by(TaxRule.calculation_order.asc(), TaxRule.id.asc()).all()


@router.post("/tax-rules", response_model=TaxRuleResponse, status_code=status.HTTP_201_CREATED)
def create_tax_rule(
    payload: TaxRuleCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Crée une nouvelle règle fiscale paramétrable (TVA, Prélèvements, etc.).
    Réservé à l'Administrateur habilité.
    """
    new_rule = TaxRule(
        name=payload.name,
        tax_type=payload.tax_type,
        rate=payload.rate,
        calculation_base=payload.calculation_base.upper(),
        calculation_order=payload.calculation_order,
        tax_regime=payload.tax_regime,
        rounding_mode=payload.rounding_mode,
        application_condition=payload.application_condition,
        min_threshold=payload.min_threshold,
        valid_from=payload.valid_from,
        valid_to=payload.valid_to,
        is_active=payload.is_active,
        description=payload.description
    )
    db.add(new_rule)
    db.commit()
    db.refresh(new_rule)
    return new_rule


@router.put("/tax-rules/{rule_id}", response_model=TaxRuleResponse)
def update_tax_rule(
    rule_id: int,
    payload: TaxRuleUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Modifie une règle fiscale existante (taux, base, ordre, conditions...)."""
    rule = db.query(TaxRule).filter(TaxRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Règle fiscale introuvable.")

    update_dict = payload.dict(exclude_unset=True)
    if "calculation_base" in update_dict and update_dict["calculation_base"]:
        update_dict["calculation_base"] = update_dict["calculation_base"].upper()

    for k, v in update_dict.items():
        setattr(rule, k, v)

    rule.updated_at = datetime.datetime.utcnow()
    db.commit()
    db.refresh(rule)
    return rule


@router.delete("/tax-rules/{rule_id}")
def delete_tax_rule(
    rule_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Désactive ou supprime une règle fiscale."""
    rule = db.query(TaxRule).filter(TaxRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Règle fiscale introuvable.")
    
    # Au lieu de supprimer brutalement, on désactive pour préserver la traçabilité
    rule.is_active = False
    rule.updated_at = datetime.datetime.utcnow()
    db.commit()
    return {"status": "success", "message": f"Règle fiscale '{rule.name}' désactivée avec succès."}


@router.post("/tax-rules/reset-defaults", response_model=List[TaxRuleResponse])
def reset_default_tax_rules(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Restaure la règle standard TVA 18% DGI par défaut."""
    rule = db.query(TaxRule).filter(TaxRule.tax_type == "VAT").first()
    if not rule:
        rule = TaxRule(
            name="TVA 18% (Norme DGI)",
            tax_type="VAT",
            rate=18.0,
            calculation_base="HT",
            calculation_order=1,
            tax_regime="TOUS",
            rounding_mode="round_2_decimals",
            application_condition="always",
            min_threshold=0.0,
            is_active=True,
            description="TVA standard 18% DGI réinitialisée."
        )
        db.add(rule)
    else:
        rule.name = "TVA 18% (Norme DGI)"
        rule.rate = 18.0
        rule.calculation_base = "HT"
        rule.calculation_order = 1
        rule.is_active = True
    db.commit()
    return db.query(TaxRule).all()


# =========================================================================
# 2. FACTURES GLOBALES ADMIN (Exigences 1, 2, 3, 5, 8, 11, 16)
# =========================================================================

@router.get("/global-invoices", response_model=List[GlobalInvoiceResponse])
def list_global_invoices(
    status: Optional[str] = None,
    period_type: Optional[str] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Liste toutes les factures globales de l'Administrateur avec filtres (statut, période).
    """
    billing_service.ensure_default_tax_rules(db)
    query = db.query(GlobalInvoice)
    if status:
        query = query.filter(GlobalInvoice.status == status)
    if period_type:
        query = query.filter(GlobalInvoice.period_type == period_type)

    return query.order_by(desc(GlobalInvoice.period_start), desc(GlobalInvoice.id)).all()


@router.post("/global-invoices/generate", response_model=GlobalInvoiceDetailResponse)
def generate_or_get_global_invoice(
    payload: GenerateInvoiceRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Ouvre ou génère la facture globale pour une période donnée (quotidienne, hebdomadaire, mensuelle).
    Recalcule automatiquement toutes les ventes existantes de cette période.
    """
    billing_service.ensure_default_tax_rules(db)
    period_type = payload.period_type or "daily"
    target_date = payload.target_date or datetime.date.today().isoformat()

    start_dt, end_dt, period_label = billing_service.get_period_bounds(period_type, target_date)

    # Chercher si la facture existe
    invoice = db.query(GlobalInvoice).filter(
        GlobalInvoice.period_type == period_type,
        GlobalInvoice.period_start == start_dt,
        GlobalInvoice.period_end == end_dt
    ).first()

    if not invoice:
        inv_number = billing_service.generate_invoice_number(period_type, start_dt, db)
        cfg = db.query(RestaurantConfig).first()
        invoice = GlobalInvoice(
            invoice_number=inv_number,
            period_type=period_type,
            period_start=start_dt,
            period_end=end_dt,
            period_label=period_label,
            status="in_progress",
            dgi_nif=cfg.nif if cfg else "000123456789A",
            dgi_nim=cfg.nim if cfg else "RESTO-DGI-MCF-01"
        )
        db.add(invoice)
        db.commit()
        db.refresh(invoice)

    # Recalcul automatique immédiat
    if not invoice.is_certified:
        invoice = billing_service.recalculate_global_invoice(
            invoice_id=invoice.id,
            db=db,
            trigger_source=admin.full_name or admin.username,
            action_description=f"Ouverture / recalcul de la facture globale #{invoice.invoice_number} par l'Administrateur."
        )

    return invoice


@router.get("/global-invoices/{invoice_id}", response_model=GlobalInvoiceDetailResponse)
def get_global_invoice_detail(
    invoice_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Détail complet d'une facture globale :
    - En-tête et montants pré-remplis
    - Lignes de facture détaillées
    - Récapitulatif par gérant
    - Ventilation fiscale DGI
    - Liste des anomalies
    - Historique d'audit
    - Informations de certification
    """
    invoice = db.query(GlobalInvoice).filter(GlobalInvoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Facture globale introuvable.")
    return invoice


@router.post("/global-invoices/{invoice_id}/recalculate", response_model=GlobalInvoiceDetailResponse)
def recalculate_invoice_endpoint(
    invoice_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Action [ RECALCULER ] :
    Recalcule manuellement à la demande les totaux, taxes et anomalies de la facture globale.
    """
    invoice = db.query(GlobalInvoice).filter(GlobalInvoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Facture globale introuvable.")

    if invoice.is_certified:
        raise HTTPException(
            status_code=400,
            detail="Impossible de recalculer une facture déjà certifiée et verrouillée fiscalement."
        )

    try:
        updated = billing_service.recalculate_global_invoice(
            invoice_id=invoice_id,
            db=db,
            trigger_source=admin.full_name or admin.username,
            action_description=f"Recalcul manuel déclenché par l'Administrateur {admin.full_name or admin.username}."
        )
        return updated
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/global-invoices/{invoice_id}/certify", response_model=GlobalInvoiceDetailResponse)
def certify_invoice_endpoint(
    invoice_id: int,
    payload: Optional[CertifyInvoiceRequest] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Action [ CERTIFIER LA FACTURE ] :
    Scelle officiellement la facture globale auprès de la DGI :
    - Vérification et recalcul définitif
    - Signature cryptographique SHA-256
    - Référence FNE DGI
    - QR code fiscal de vérification
    - Verrouillage total et définitif
    """
    invoice = db.query(GlobalInvoice).filter(GlobalInvoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Facture globale introuvable.")

    if invoice.is_certified:
        raise HTTPException(status_code=400, detail="Cette facture globale est déjà certifiée.")

    notes = payload.notes if payload else None
    try:
        certified = billing_service.certify_global_invoice(
            invoice_id=invoice_id,
            admin_user=admin,
            db=db,
            notes=notes
        )
        return certified
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la certification : {str(e)}")


@router.get("/global-invoices/{invoice_id}/audit-logs", response_model=List[GlobalInvoiceAuditLogResponse])
def get_invoice_audit_logs(
    invoice_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Historique exhaustif des calculs et modifications d'une facture globale (Exigence 14)."""
    return db.query(GlobalInvoiceAuditLog).filter(
        GlobalInvoiceAuditLog.global_invoice_id == invoice_id
    ).order_by(desc(GlobalInvoiceAuditLog.created_at)).all()


# =========================================================================
# 3. CONFIGURATION DE LA FACTURATION (Exigences 6 & 8)
# =========================================================================

@router.get("/config", response_model=BillingConfigResponse)
def get_billing_config(db: Session = Depends(get_db)):
    """Récupère les paramètres de facturation : fréquence par défaut, mode TTC/HT, régime fiscal."""
    cfg = db.query(RestaurantConfig).first()
    if not cfg:
        cfg = RestaurantConfig()
        db.add(cfg)
        db.commit()
        db.refresh(cfg)
    return {
        "billing_frequency": cfg.billing_frequency or "daily",
        "menu_prices_include_tax": cfg.menu_prices_include_tax if cfg.menu_prices_include_tax is not None else True,
        "default_tax_regime": cfg.default_tax_regime or "REEL_NORMAL"
    }


@router.put("/config", response_model=BillingConfigResponse)
def update_billing_config(
    payload: BillingConfigUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Modifie la configuration de facturation globale (Fréquence, Régime fiscal, etc.)."""
    cfg = db.query(RestaurantConfig).first()
    if not cfg:
        cfg = RestaurantConfig()
        db.add(cfg)

    update_dict = payload.dict(exclude_unset=True)
    for k, v in update_dict.items():
        setattr(cfg, k, v)

    cfg.updated_at = datetime.datetime.utcnow()
    db.commit()
    db.refresh(cfg)
    return {
        "billing_frequency": cfg.billing_frequency,
        "menu_prices_include_tax": cfg.menu_prices_include_tax,
        "default_tax_regime": cfg.default_tax_regime
    }


# =========================================================================
# 4. SURVEILLANCE EN TEMPS RÉEL (Exigence 7)
# =========================================================================

@router.get("/live-status")
def get_live_billing_status(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """
    Endpoint temps réel léger pour la synchronisation automatique de l'écran Admin :
    Renvoie le timestamp de la dernière vente, l'ID de la facture globale courante,
    le montant cumulé et les alertes éventuelles.
    """
    cfg = db.query(RestaurantConfig).first()
    freq = cfg.billing_frequency if cfg and cfg.billing_frequency else "daily"

    now = datetime.datetime.utcnow()
    start_dt, end_dt, period_label = billing_service.get_period_bounds(freq, now)

    # Priorité à la facture ouverte non-certifiée en cours
    current_invoice = db.query(GlobalInvoice).filter(
        GlobalInvoice.period_type == freq,
        GlobalInvoice.period_start == start_dt,
        GlobalInvoice.period_end == end_dt,
        GlobalInvoice.is_certified == False
    ).order_by(desc(GlobalInvoice.id)).first()

    if not current_invoice:
        current_invoice = db.query(GlobalInvoice).filter(
            GlobalInvoice.period_type == freq,
            GlobalInvoice.period_start == start_dt,
            GlobalInvoice.period_end == end_dt
        ).order_by(desc(GlobalInvoice.id)).first()

    last_order = db.query(Order).order_by(desc(Order.id)).first()

    total_invoices_count = db.query(GlobalInvoice).count()
    certified_count = db.query(GlobalInvoice).filter(GlobalInvoice.is_certified == True).count()
    pending_count = total_invoices_count - certified_count

    return {
        "frequency": freq,
        "period_label": period_label,
        "current_invoice_id": current_invoice.id if current_invoice else None,
        "current_invoice_number": current_invoice.invoice_number if current_invoice else None,
        "current_invoice_status": current_invoice.status if current_invoice else "none",
        "current_invoice_ttc": current_invoice.total_ttc if current_invoice else 0.0,
        "current_invoice_ht": current_invoice.total_ht if current_invoice else 0.0,
        "current_invoice_taxes": current_invoice.total_taxes if current_invoice else 0.0,
        "current_invoice_sales_count": current_invoice.total_sales_count if current_invoice else 0,
        "current_invoice_is_certified": current_invoice.is_certified if current_invoice else False,
        "has_anomalies": current_invoice.has_anomalies if current_invoice else False,
        "last_order_number": last_order.order_number if last_order else None,
        "last_order_amount": last_order.total_amount if last_order else 0.0,
        "last_order_manager": last_order.manager_name if last_order else None,
        "last_order_time": last_order.created_at.isoformat() if last_order and last_order.created_at else None,
        "total_invoices_count": total_invoices_count,
        "certified_count": certified_count,
        "pending_count": pending_count,
        "server_time": now.isoformat()
    }
