import datetime
import calendar
import json
import hashlib
import math
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_

from app.models.restaurant import (
    Order, OrderItem, RestaurantConfig, TaxRule, 
    GlobalInvoice, GlobalInvoiceItem, GlobalInvoiceAuditLog
)
from app.models.user import User

class BillingService:
    """
    Moteur de Facturation Globale Dynamique & Fiscalité DGI
    Gère l'agrégation temps réel des ventes, le calcul fiscal paramétrable,
    la détection des anomalies, et la certification officielle sécurisée.
    """

    def ensure_default_tax_rules(self, db: Session) -> List[TaxRule]:
        """
        Vérifie et initialise les règles fiscales DGI par défaut si aucune n'est configurée.
        La taxe officielle principale est la TVA 18% norme DGI (e-MCF).
        """
        count = db.query(TaxRule).count()
        if count == 0:
            default_rule = TaxRule(
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
                description="Taxe sur la Valeur Ajoutée standard 18% conforme aux exigences DGI / e-MCF."
            )
            db.add(default_rule)
            db.commit()
            db.refresh(default_rule)
            return [default_rule]
        return db.query(TaxRule).filter(TaxRule.is_active == True).order_by(TaxRule.calculation_order.asc()).all()

    def get_period_bounds(
        self, 
        frequency: str, 
        date_or_dt: Any
    ) -> Tuple[datetime.datetime, datetime.datetime, str]:
        """
        Calcule les bornes de début et fin de période (start_dt, end_dt) et le libellé lisible.
        Fréquences supportées : daily, weekly, monthly
        """
        if isinstance(date_or_dt, datetime.datetime):
            target_date = date_or_dt.date()
        elif isinstance(date_or_dt, datetime.date):
            target_date = date_or_dt
        elif isinstance(date_or_dt, str):
            target_date = datetime.date.fromisoformat(date_or_dt[:10])
        else:
            target_date = datetime.date.today()

        freq = (frequency or "daily").lower()

        if freq == "daily":
            start_dt = datetime.datetime.combine(target_date, datetime.time.min)
            end_dt = datetime.datetime.combine(target_date, datetime.time.max)
            period_label = f"Journée du {target_date.strftime('%d/%m/%Y')}"

        elif freq == "weekly":
            # Semaine débutant le lundi (weekday() == 0)
            monday = target_date - datetime.timedelta(days=target_date.weekday())
            sunday = monday + datetime.timedelta(days=6)
            start_dt = datetime.datetime.combine(monday, datetime.time.min)
            end_dt = datetime.datetime.combine(sunday, datetime.time.max)
            week_num = target_date.isocalendar()[1]
            period_label = f"Semaine {week_num} ({monday.strftime('%d/%m')} au {sunday.strftime('%d/%m/%Y')})"

        elif freq == "monthly":
            year = target_date.year
            month = target_date.month
            first_day = datetime.date(year, month, 1)
            last_day_num = calendar.monthrange(year, month)[1]
            last_day = datetime.date(year, month, last_day_num)
            start_dt = datetime.datetime.combine(first_day, datetime.time.min)
            end_dt = datetime.datetime.combine(last_day, datetime.time.max)
            mois_noms = ["", "Janvier", "Février", "Mars", "Avril", "Mai", "Juin", 
                         "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
            period_label = f"Mois de {mois_noms[month]} {year}"

        else: # Par défaut daily
            start_dt = datetime.datetime.combine(target_date, datetime.time.min)
            end_dt = datetime.datetime.combine(target_date, datetime.time.max)
            period_label = f"Période du {target_date.strftime('%d/%m/%Y')}"

        return start_dt, end_dt, period_label

    def generate_invoice_number(self, frequency: str, start_dt: datetime.datetime, db: Session) -> str:
        """Génère un numéro unique de facture globale lisible et chronologique."""
        date_part = start_dt.strftime("%Y%m%d")
        prefix = "FACT-GLOB"
        if frequency == "daily":
            prefix = "FACT-GLOB-J"
        elif frequency == "weekly":
            prefix = "FACT-GLOB-S"
        elif frequency == "monthly":
            prefix = "FACT-GLOB-M"

        # Chercher le nombre de factures existantes ayant ce préfixe pour incrémenter
        count = db.query(GlobalInvoice).filter(
            GlobalInvoice.invoice_number.like(f"{prefix}-{date_part}-%")
        ).count() + 1

        return f"{prefix}-{date_part}-{count:03d}"

    def apply_rounding(self, value: float, rounding_mode: str) -> float:
        """Applique l'arrondi fiscal configuré."""
        if rounding_mode == "round_integer":
            return float(round(value))
        elif rounding_mode == "ceil":
            return float(math.ceil(value))
        elif rounding_mode == "floor":
            return float(math.floor(value))
        else: # round_2_decimals par défaut
            return round(value, 2)

    def calculate_taxes_for_amount(
        self,
        amount_ttc: float,
        db: Session,
        date_ref: Optional[datetime.date] = None,
        tax_regime: Optional[str] = None,
        prices_include_tax: bool = True
    ) -> Dict[str, Any]:
        """
        Moteur de calcul fiscal configurable.
        Calcule les montants HT, taxes et TTC en appliquant les règles fiscales actives.
        Prend en charge plusieurs taxes ordonnées, base de calcul HT ou TTC, et arrondis.
        """
        # Récupérer les règles fiscales actives
        query = db.query(TaxRule).filter(TaxRule.is_active == True)
        
        if date_ref:
            query = query.filter(
                or_(TaxRule.valid_from == None, TaxRule.valid_from <= date_ref),
                or_(TaxRule.valid_to == None, TaxRule.valid_to >= date_ref)
            )

        if tax_regime and tax_regime != "TOUS":
            query = query.filter(
                or_(TaxRule.tax_regime == "TOUS", TaxRule.tax_regime == tax_regime)
            )

        rules = query.order_by(TaxRule.calculation_order.asc()).all()

        # Si aucune règle active configurée
        if not rules:
            return {
                "amount_ht": round(amount_ttc, 2),
                "amount_tax": 0.0,
                "amount_ttc": round(amount_ttc, 2),
                "breakdown": [],
                "has_no_tax_rules": True
            }

        # Cas 1 : Les prix de vente sont TTC (cas standard en restauration)
        if prices_include_tax:
            # Somme des taux s'appliquant sur la base HT
            ht_tax_sum = sum(r.rate for r in rules if r.calculation_base.upper() == "HT")
            ttc_tax_sum = sum(r.rate for r in rules if r.calculation_base.upper() == "TTC")
            
            # Formule d'extraction de la base Hors Taxes
            divisor = 1.0 + (ht_tax_sum / 100.0)
            if divisor <= 0:
                divisor = 1.0
            
            # Base HT déduite
            base_ht = amount_ttc / divisor
            base_ht = round(base_ht, 2)

            tax_breakdown = []
            total_tax_calc = 0.0

            for rule in rules:
                if rule.application_condition == "threshold_min" and amount_ttc < rule.min_threshold:
                    continue

                if rule.calculation_base.upper() == "TTC":
                    tax_val = amount_ttc * (rule.rate / 100.0)
                    base_used = amount_ttc
                else: # HT
                    tax_val = base_ht * (rule.rate / 100.0)
                    base_used = base_ht

                tax_val = self.apply_rounding(tax_val, rule.rounding_mode)
                total_tax_calc += tax_val

                tax_breakdown.append({
                    "rule_id": rule.id,
                    "rule_name": rule.name,
                    "tax_type": rule.tax_type,
                    "rate": rule.rate,
                    "base": rule.calculation_base,
                    "base_amount": round(base_used, 2),
                    "tax_amount": round(tax_val, 2),
                    "formula": f"Base {rule.calculation_base} ({base_used:,.2f} FCFA) × {rule.rate}%"
                })

            total_tax = round(total_tax_calc, 2)
            calculated_ttc = round(base_ht + total_tax, 2)

            return {
                "amount_ht": base_ht,
                "amount_tax": total_tax,
                "amount_ttc": round(amount_ttc, 2), # Préserver le TTC encaissé exact
                "breakdown": tax_breakdown,
                "has_no_tax_rules": False
            }

        else: # Cas 2 : Prix saisis en HT
            base_ht = round(amount_ttc, 2)
            tax_breakdown = []
            total_tax_calc = 0.0

            for rule in rules:
                if rule.application_condition == "threshold_min" and base_ht < rule.min_threshold:
                    continue

                tax_val = base_ht * (rule.rate / 100.0)
                tax_val = self.apply_rounding(tax_val, rule.rounding_mode)
                total_tax_calc += tax_val

                tax_breakdown.append({
                    "rule_id": rule.id,
                    "rule_name": rule.name,
                    "tax_type": rule.tax_type,
                    "rate": rule.rate,
                    "base": rule.calculation_base,
                    "base_amount": base_ht,
                    "tax_amount": round(tax_val, 2),
                    "formula": f"Base HT ({base_ht:,.2f} FCFA) × {rule.rate}%"
                })

            total_tax = round(total_tax_calc, 2)
            return {
                "amount_ht": base_ht,
                "amount_tax": total_tax,
                "amount_ttc": round(base_ht + total_tax, 2),
                "breakdown": tax_breakdown,
                "has_no_tax_rules": False
            }

    def create_invoice_for_manager_session(self, user: User, db: Session) -> GlobalInvoice:
        """
        Crée automatiquement une facture globale dédiée au gérant dès sa connexion :
        - Pré-remplie avec son nom complet, identifiant, date et heure exacte de prise de service.
        - Montants initiaux à 0 FCFA (TTC, HT, TVA) prêts à accumuler les ventes dès qu'il commence.
        - Synchronisée immédiatement dans Odoo (Facturation Générale & Facture Client) pour l'administrateur.
        """
        now = datetime.datetime.utcnow()
        clean_mgr = "".join(c for c in (user.full_name or user.username) if c.isalnum() or c in "-_")
        date_str = now.strftime("%Y%m%d")
        time_str = now.strftime("%H%M")

        # Vérifier si une facture ouverte pour ce gérant existe déjà pour aujourd'hui
        existing = db.query(GlobalInvoice).filter(
            GlobalInvoice.manager_id == user.id,
            GlobalInvoice.is_certified == False,
            GlobalInvoice.status.in_(["in_progress", "draft"])
        ).order_by(GlobalInvoice.id.desc()).first()

        if existing and existing.created_at.date() == now.date():
            existing.opened_at = existing.opened_at or now
            existing.manager_name = user.full_name
            existing.manager_login = user.username
            db.commit()
            return existing

        inv_number = f"FACT-MGR-{date_str}-{clean_mgr[:10].upper()}-{time_str}"
        dup = db.query(GlobalInvoice).filter(GlobalInvoice.invoice_number == inv_number).first()
        if dup:
            inv_number = f"FACT-MGR-{date_str}-{clean_mgr[:8].upper()}-{time_str}-{now.second:02d}"

        start_dt = datetime.datetime.combine(now.date(), datetime.time.min)
        end_dt = datetime.datetime.combine(now.date(), datetime.time.max)
        period_label = f"Session {user.full_name} ({now.strftime('%d/%m/%Y à %H:%M')})"

        cfg = db.query(RestaurantConfig).first()
        invoice = GlobalInvoice(
            invoice_number=inv_number,
            period_type="session",
            period_start=start_dt,
            period_end=end_dt,
            period_label=period_label,
            manager_id=user.id,
            manager_name=user.full_name,
            manager_login=user.username,
            opened_at=now,
            status="in_progress",
            total_sales_count=0,
            total_ht=0.0,
            total_taxes=0.0,
            total_ttc=0.0,
            is_certified=False,
            dgi_nif=cfg.nif if cfg else "000123456789A",
            dgi_nim=cfg.nim if cfg else "RESTO-DGI-MCF-01",
            manager_summary=json.dumps([{
                "manager_id": user.id,
                "name": user.full_name,
                "login": user.username,
                "sales_count": 0,
                "total_ttc": 0.0,
                "total_ht": 0.0,
                "total_taxes": 0.0,
                "opened_at": now.strftime("%H:%M:%S")
            }])
        )
        db.add(invoice)
        db.flush()

        log = GlobalInvoiceAuditLog(
            global_invoice_id=invoice.id,
            action_type="CREATED",
            description=f"Création automatique à la connexion du gérant {user.full_name} ({user.username}) à {now.strftime('%H:%M:%S')}.",
            user_name="Système Connexion Gérant",
            details_json=json.dumps({"manager": user.full_name, "login_at": now.isoformat()})
        )
        db.add(log)
        db.commit()
        db.refresh(invoice)

        # Synchronisation dans Odoo ERP (Facturation Générale & Facture Client)
        try:
            from app.services.odoo_service import odoo_service
            odoo_service.sync_manager_session_invoice(
                invoice_number=inv_number,
                manager_name=user.full_name,
                manager_id=user.odoo_user_id or 1,
                date_str=now.strftime("%Y-%m-%d"),
                time_str=now.strftime("%H:%M:%S")
            )
        except Exception as e:
            print(f"Erreur synchro session gérant Odoo: {e}")

        return invoice

    def get_or_create_global_invoice_for_order(self, order: Order, db: Session) -> GlobalInvoice:
        """
        Identifie ou crée la facture globale correspondant à la vente du gérant.
        Se base sur la session active du gérant ou la configuration de période.
        """
        # 1. Si la commande émane d'un gérant ayant une facture de session ouverte aujourd'hui
        mgr_login = getattr(order, 'manager_login', None)
        mgr_name = getattr(order, 'manager_name', None)
        if mgr_login or mgr_name:
            filters = []
            if mgr_login:
                filters.append(func.lower(GlobalInvoice.manager_login) == mgr_login.lower())
            if mgr_name:
                filters.append(GlobalInvoice.manager_name == mgr_name)
            
            mgr_invoice = db.query(GlobalInvoice).filter(
                or_(*filters),
                GlobalInvoice.is_certified == False,
                GlobalInvoice.status.in_(["in_progress", "draft"])
            ).order_by(GlobalInvoice.id.desc()).first()
            if mgr_invoice:
                return mgr_invoice

        # 2. Sinon, rechercher selon la fréquence configurée
        cfg = db.query(RestaurantConfig).first()
        frequency = cfg.billing_frequency if cfg and cfg.billing_frequency else "daily"

        order_dt = order.created_at or datetime.datetime.utcnow()
        start_dt, end_dt, period_label = self.get_period_bounds(frequency, order_dt)

        # Rechercher une facture globale existante non certifiée (ouverte) pour cette période
        invoice = db.query(GlobalInvoice).filter(
            GlobalInvoice.period_type == frequency,
            GlobalInvoice.period_start == start_dt,
            GlobalInvoice.period_end == end_dt,
            GlobalInvoice.is_certified == False
        ).order_by(GlobalInvoice.id.desc()).first()

        # Si aucune facture n'existe, on la crée automatiquement en statut 'in_progress' ou 'draft'
        if not invoice:
            inv_number = self.generate_invoice_number(frequency, start_dt, db)
            invoice = GlobalInvoice(
                invoice_number=inv_number,
                period_type=frequency,
                period_start=start_dt,
                period_end=end_dt,
                period_label=period_label,
                status="in_progress",
                total_sales_count=0,
                total_ht=0.0,
                total_taxes=0.0,
                total_ttc=0.0,
                is_certified=False,
                dgi_nif=cfg.nif if cfg else "000123456789A",
                dgi_nim=cfg.nim if cfg else "RESTO-DGI-MCF-01"
            )
            db.add(invoice)
            db.flush()

            # Enregistrer dans le journal d'audit
            log = GlobalInvoiceAuditLog(
                global_invoice_id=invoice.id,
                action_type="CREATED",
                description=f"Création automatique de la facture globale #{inv_number} ({period_label}). Fréquence : {frequency}.",
                user_name="Système Automatique",
                details_json=json.dumps({"period": period_label, "frequency": frequency})
            )
            db.add(log)
            db.commit()
            db.refresh(invoice)

        return invoice

    def recalculate_global_invoice(
        self,
        invoice_id: int,
        db: Session,
        trigger_source: str = "Système Automatique",
        action_description: Optional[str] = None
    ) -> GlobalInvoice:
        """
        Recalcule automatiquement et complètement la facture globale :
        1. Agrège toutes les ventes éligibles de la période
        2. Détecte les anomalies (vente sans prix, taxes non configurées, doublon, etc.)
        3. Applique le moteur fiscal configurable à chaque vente
        4. Remplit les lignes de facture pré-remplies (GlobalInvoiceItem)
        5. Calcule les totaux HT, Taxes et TTC
        6. Génère la répartition par gérant et par mode de paiement
        7. Met à jour le statut et conserve un historique d'audit exhaustif
        """
        if isinstance(invoice_id, GlobalInvoice):
            invoice = invoice_id
            invoice_id = invoice.id
        else:
            invoice = db.query(GlobalInvoice).filter(GlobalInvoice.id == invoice_id).first()
        if not invoice:
            raise ValueError(f"Facture globale ID {invoice_id} introuvable.")

        # Protection stricte : interdiction de recalculer ou modifier une facture certifiée
        if invoice.is_certified:
            return invoice

        cfg = db.query(RestaurantConfig).first()
        prices_include_tax = cfg.menu_prices_include_tax if cfg else True
        tax_regime = cfg.default_tax_regime if cfg else "REEL_NORMAL"

        # 1. Sélectionner toutes les commandes dans l'intervalle temporel de la période
        order_query = db.query(Order).filter(
            Order.created_at >= invoice.period_start,
            Order.created_at <= invoice.period_end
        )
        if invoice.manager_login or invoice.manager_name:
            mgr_filters = []
            if invoice.manager_login:
                mgr_filters.append(func.lower(Order.manager_login) == invoice.manager_login.lower())
            if invoice.manager_name:
                mgr_filters.append(Order.manager_name == invoice.manager_name)
            order_query = order_query.filter(or_(*mgr_filters))

        all_period_orders = order_query.order_by(Order.created_at.asc()).all()

        orders = []
        for o in all_period_orders:
            # Exigence 9 : Avant d'ajouter une vente, vérifier qu'elle n'est pas déjà rattachée à une facture certifiée
            if o.global_invoice_id and o.global_invoice_id != invoice.id:
                other_inv = db.query(GlobalInvoice).filter(GlobalInvoice.id == o.global_invoice_id).first()
                if other_inv and other_inv.is_certified:
                    continue
            orders.append(o)

        # 2. Détection des anomalies (Exigence 15)
        anomalies = []
        tax_rules_count = db.query(TaxRule).filter(TaxRule.is_active == True).count()
        if tax_rules_count == 0:
            anomalies.append({
                "type": "TAX_RULE_MISSING",
                "severity": "CRITICAL",
                "message": "Aucune règle fiscale DGI active n'est configurée dans le système."
            })

        seen_order_numbers = set()
        seen_canonical_numbers = set()
        seen_odoo_ids = set()
        active_orders = []

        for o in orders:
            raw_num = o.order_number or ""
            canon_num = raw_num.replace("CMD-", "").strip()

            # Vérification doublon absolue (Exigence 9 : Une vente ne doit jamais être comptée deux fois)
            is_dup = (
                (raw_num in seen_order_numbers) or 
                (canon_num and canon_num in seen_canonical_numbers) or
                (o.odoo_pos_order_id and o.odoo_pos_order_id in seen_odoo_ids)
            )

            if is_dup:
                anomalies.append({
                    "type": "DUPLICATE_ORDER",
                    "severity": "WARNING",
                    "order_number": raw_num,
                    "message": f"Doublon écarté pour la vente n° {raw_num} (déjà comptabilisée dans la facture)."
                })
                continue # Ne JAMAIS compter un doublon deux fois

            seen_order_numbers.add(raw_num)
            if canon_num:
                seen_canonical_numbers.add(canon_num)
            if o.odoo_pos_order_id:
                seen_odoo_ids.add(o.odoo_pos_order_id)

            # Vérification vente annulée
            if o.status == "cancelled":
                anomalies.append({
                    "type": "CANCELLED_ORDER",
                    "severity": "INFO",
                    "order_number": o.order_number,
                    "message": f"La vente n° {o.order_number} a été annulée et est exclue du calcul."
                })
                # Les ventes annulées ne sont pas intégrées dans le calcul actif (Exigence 10)
                continue

            # Vérification vente sans prix / montant nul
            if (o.total_amount is None or o.total_amount <= 0) and o.status != "cancelled":
                anomalies.append({
                    "type": "ZERO_AMOUNT",
                    "severity": "WARNING",
                    "order_number": o.order_number,
                    "message": f"Vente n° {o.order_number} enregistrée avec un montant nul (0 FCFA)."
                })

            # Vérification cohérence de période
            if o.created_at < invoice.period_start or o.created_at > invoice.period_end:
                anomalies.append({
                    "type": "PERIOD_MISMATCH",
                    "severity": "CRITICAL",
                    "order_number": o.order_number,
                    "message": f"Vente n° {o.order_number} hors de la période de facturation."
                })

            active_orders.append(o)

        # 3. Synchronisation des lignes de facture pré-remplies (GlobalInvoiceItem)
        # Supprimer les lignes existantes pour regénérer un état propre et exact
        db.query(GlobalInvoiceItem).filter(GlobalInvoiceItem.global_invoice_id == invoice.id).delete()

        total_ht_sum = 0.0
        total_tax_sum = 0.0
        total_ttc_sum = 0.0
        tax_rules_breakdown_agg = {}
        manager_stats = {}
        payment_stats = {}

        for o in active_orders:
            # Calcul fiscal pour cette vente
            date_ref = o.created_at.date() if o.created_at else datetime.date.today()
            tax_res = self.calculate_taxes_for_amount(
                amount_ttc=o.total_amount,
                db=db,
                date_ref=date_ref,
                tax_regime=tax_regime,
                prices_include_tax=prices_include_tax
            )

            # Résumé des articles vendus
            items_list = []
            total_qty = 0
            if o.items:
                for it in o.items:
                    items_list.append(f"{it.item_name} x{it.quantity}")
                    total_qty += it.quantity
            else:
                items_list.append(f"Vente globale ({o.order_number})")
                total_qty = 1

            items_summary_str = ", ".join(items_list) if items_list else "Articles non spécifiés"
            unit_price_ref = round(o.total_amount / total_qty, 2) if total_qty > 0 else o.total_amount

            # Créer la ligne de facture
            invoice_item = GlobalInvoiceItem(
                global_invoice_id=invoice.id,
                order_id=o.id,
                order_number=o.order_number,
                order_date=o.created_at or datetime.datetime.utcnow(),
                manager_name=o.manager_name or "Gérant Inconnu",
                manager_login=o.manager_login or "N/A",
                payment_method=o.payment_method or "Espèces (Cash)",
                items_summary=items_summary_str,
                total_items_count=total_qty,
                unit_price=unit_price_ref,
                amount_ht=tax_res["amount_ht"],
                amount_tax=tax_res["amount_tax"],
                amount_ttc=tax_res["amount_ttc"],
                tax_details=json.dumps(tax_res["breakdown"]),
                status="active"
            )
            db.add(invoice_item)

            # Rattacher la commande à la facture globale et marquer comme facturée (Exigence 9)
            o.global_invoice_id = invoice.id
            o.is_invoiced = True
            o.invoiced_at = datetime.datetime.utcnow()

            # Cumuls généraux
            total_ht_sum += tax_res["amount_ht"]
            total_tax_sum += tax_res["amount_tax"]
            total_ttc_sum += tax_res["amount_ttc"]

            # Cumul taxes par règle
            for r_item in tax_res["breakdown"]:
                r_id = r_item["rule_id"]
                if r_id not in tax_rules_breakdown_agg:
                    tax_rules_breakdown_agg[r_id] = {
                        "rule_id": r_id,
                        "rule_name": r_item["rule_name"],
                        "rate": r_item["rate"],
                        "tax_type": r_item["tax_type"],
                        "total_base": 0.0,
                        "total_tax": 0.0
                    }
                tax_rules_breakdown_agg[r_id]["total_base"] = round(tax_rules_breakdown_agg[r_id]["total_base"] + r_item["base_amount"], 2)
                tax_rules_breakdown_agg[r_id]["total_tax"] = round(tax_rules_breakdown_agg[r_id]["total_tax"] + r_item["tax_amount"], 2)

            # Récapitulatif par gérant (Exigence 13)
            mgr_key = o.manager_name or "Gérant Inconnu"
            if mgr_key not in manager_stats:
                manager_stats[mgr_key] = {
                    "manager_name": mgr_key,
                    "manager_login": o.manager_login or "N/A",
                    "sales_count": 0,
                    "total_ht": 0.0,
                    "total_tax": 0.0,
                    "total_ttc": 0.0
                }
            manager_stats[mgr_key]["sales_count"] += 1
            manager_stats[mgr_key]["total_ht"] = round(manager_stats[mgr_key]["total_ht"] + tax_res["amount_ht"], 2)
            manager_stats[mgr_key]["total_tax"] = round(manager_stats[mgr_key]["total_tax"] + tax_res["amount_tax"], 2)
            manager_stats[mgr_key]["total_ttc"] = round(manager_stats[mgr_key]["total_ttc"] + tax_res["amount_ttc"], 2)

            # Récapitulatif modes de paiement
            pm = o.payment_method or "Espèces (Cash)"
            payment_stats[pm] = round(payment_stats.get(pm, 0.0) + tax_res["amount_ttc"], 2)

        # 4. Mettre à jour l'en-tête de la facture globale
        invoice.total_sales_count = len(active_orders)
        invoice.total_ht = round(total_ht_sum, 2)
        invoice.total_taxes = round(total_tax_sum, 2)
        invoice.total_ttc = round(total_ttc_sum, 2)
        invoice.tax_details = json.dumps(list(tax_rules_breakdown_agg.values()))
        invoice.manager_summary = json.dumps(list(manager_stats.values()))
        invoice.payment_summary = json.dumps(payment_stats)
        invoice.anomalies = json.dumps(anomalies)
        invoice.has_anomalies = (len(anomalies) > 0)

        # Détermination du statut :
        # - Brouillon : 0 vente
        # - En cours : des ventes existent mais anomalies bloquantes ou période non terminée
        # - Prête pour certification : des ventes existent et aucune anomalie bloquante
        has_critical = any(a.get("severity") == "CRITICAL" for a in anomalies)
        if len(active_orders) == 0:
            invoice.status = "draft"
        elif has_critical:
            invoice.status = "in_progress"
        else:
            invoice.status = "ready_for_certification"

        invoice.updated_at = datetime.datetime.utcnow()

        # 5. Journaliser dans l'historique d'audit (Exigence 14)
        desc = action_description or f"Recalcul automatique : {len(active_orders)} ventes traitées, Total TTC : {invoice.total_ttc:,.0f} FCFA."
        audit = GlobalInvoiceAuditLog(
            global_invoice_id=invoice.id,
            action_type="RECALCULATED",
            description=desc,
            user_name=trigger_source,
            details_json=json.dumps({
                "sales_count": len(active_orders),
                "total_ht": invoice.total_ht,
                "total_taxes": invoice.total_taxes,
                "total_ttc": invoice.total_ttc,
                "anomalies_count": len(anomalies),
                "status": invoice.status
            })
        )
        db.add(audit)
        db.commit()
        db.refresh(invoice)

        return invoice

    def integrate_order_into_global_invoicing(self, order: Order, db: Session) -> Optional[GlobalInvoice]:
        """
        Intègre automatiquement une vente dès sa validation par un gérant (Exigences 1, 4, 5, 7).
        Trouve la facture globale active et la recalcule immédiatement.
        """
        # S'assurer que les règles fiscales DGI existent
        self.ensure_default_tax_rules(db)

        # Vérifier si la vente n'est pas déjà dans une facture certifiée verrouillée
        if order.global_invoice_id:
            existing_inv = db.query(GlobalInvoice).filter(GlobalInvoice.id == order.global_invoice_id).first()
            if existing_inv and existing_inv.is_certified:
                # Interdiction d'ajouter ou modifier une vente rattachée à une facture certifiée
                return existing_inv

        invoice = self.get_or_create_global_invoice_for_order(order, db)
        
        # Recalculer immédiatement la facture globale
        mgr_name = order.manager_name or "Gérant"
        desc = f"Nouvelle vente #{order.order_number} de {order.total_amount:,.0f} FCFA validée par {mgr_name} et intégrée automatiquement."
        return self.recalculate_global_invoice(
            invoice_id=invoice.id,
            db=db,
            trigger_source=f"Gérant ({mgr_name})",
            action_description=desc
        )

    def handle_order_cancelled_or_modified(self, order: Order, db: Session) -> Optional[GlobalInvoice]:
        """
        Gère la répercussion immédiate en cas de modification ou annulation d'une vente (Exigence 10).
        """
        if not order.global_invoice_id:
            return None

        invoice = db.query(GlobalInvoice).filter(GlobalInvoice.id == order.global_invoice_id).first()
        if not invoice or invoice.is_certified:
            return None # Facture scellée, modifications directes interdites

        desc = f"Mise à jour de la vente #{order.order_number} (Statut: {order.status}, Montant: {order.total_amount:,.0f} FCFA). Recalcul automatique appliqué."
        return self.recalculate_global_invoice(
            invoice_id=invoice.id,
            db=db,
            trigger_source="Système de Vente",
            action_description=desc
        )

    def certify_global_invoice(
        self,
        invoice_id: int,
        admin_user: User,
        db: Session,
        notes: Optional[str] = None
    ) -> GlobalInvoice:
        """
        Procédure officielle de certification fiscale DGI (Exigences 11 & 16) :
        1. Vérifie toutes les ventes de la période
        2. Recalcule les totaux définitifs
        3. Contrôle l'absence d'anomalies bloquantes
        4. Génère la signature cryptographique SHA-256 et la référence FNE officielle
        5. Génère le QR code fiscal de vérification
        6. Enregistre l'horodatage et l'administrateur
        7. Change le statut en CERTIFIÉE
        8. Verrouille définitivement la facture et les ventes associées
        """
        invoice = db.query(GlobalInvoice).filter(GlobalInvoice.id == invoice_id).first()
        if not invoice:
            raise ValueError(f"Facture globale ID {invoice_id} introuvable.")

        if invoice.is_certified:
            raise ValueError("Cette facture globale est déjà certifiée et verrouillée.")

        # 1 & 2. Recalcul pré-certification rigoureux
        invoice = self.recalculate_global_invoice(
            invoice_id=invoice.id,
            db=db,
            trigger_source=admin_user.full_name or admin_user.username,
            action_description="Recalcul rigoureux de pré-certification fiscale."
        )

        # 3. Contrôle des anomalies bloquantes
        anomalies = json.loads(invoice.anomalies or "[]")
        critical_anomalies = [a for a in anomalies if a.get("severity") == "CRITICAL"]
        if critical_anomalies:
            crit_msgs = "; ".join(a.get("message", "") for a in critical_anomalies)
            raise ValueError(f"Certification impossible. Anomalies bloquantes détectées : {crit_msgs}")

        if invoice.total_sales_count == 0:
            raise ValueError("Impossible de certifier une facture ne contenant aucune vente.")

        cfg = db.query(RestaurantConfig).first()
        nif = cfg.nif if cfg and cfg.nif else "000123456789A"
        nim = cfg.nim if cfg and cfg.nim else "RESTO-DGI-MCF-01"

        now = datetime.datetime.utcnow()
        date_str = now.strftime("%Y%m%d")

        # 4. Signature cryptographique SHA-256 (Norme DGI e-MCF)
        raw_signature_payload = (
            f"DGI-MCF-BF|{nif}|{nim}|{invoice.invoice_number}|"
            f"HT:{invoice.total_ht}|TAXES:{invoice.total_taxes}|TTC:{invoice.total_ttc}|"
            f"SALES:{invoice.total_sales_count}|TIME:{now.isoformat()}|SALT_DGI_BURKINA_2026"
        )
        sig_hash = hashlib.sha256(raw_signature_payload.encode("utf-8")).hexdigest()
        fiscal_ref = f"DGI-FNE-GLOB-{date_str}-{sig_hash[:8].upper()}"

        # 5. Données QR Code fiscal officiel
        qr_code_str = (
            f"DGI-FNE-GLOBAL|NIF:{nif}|NIM:{nim}|REF:{fiscal_ref}|"
            f"HT:{invoice.total_ht}|TVA:{invoice.total_taxes}|TTC:{invoice.total_ttc}|"
            f"VENTES:{invoice.total_sales_count}|SIG:{sig_hash[:16].upper()}|"
            f"URL:https://dgi.bf.impots.gov/fne/verifier/{fiscal_ref}"
        )

        # 6 & 7. Enregistrement de la certification et verrouillage
        invoice.is_certified = True
        invoice.status = "certified"
        invoice.certified_at = now
        invoice.certified_by = admin_user.full_name or admin_user.username
        invoice.certification_notes = notes
        invoice.dgi_nif = nif
        invoice.dgi_nim = nim
        invoice.dgi_fiscal_reference = fiscal_ref
        invoice.dgi_security_code = sig_hash
        invoice.dgi_qr_code_data = qr_code_str

        # 8. Verrouillage des commandes individuelles rattachées
        orders = db.query(Order).filter(Order.global_invoice_id == invoice.id).all()
        for o in orders:
            o.is_certified_dgi = True
            o.dgi_invoice_number = fiscal_ref
            o.dgi_signature = sig_hash[:16].upper()
            o.dgi_certified_at = now

        # Journal d'audit de certification
        audit = GlobalInvoiceAuditLog(
            global_invoice_id=invoice.id,
            action_type="CERTIFIED",
            description=(
                f"Certification officielle DGI réussie par l'Administrateur {invoice.certified_by}. "
                f"Référence fiscale FNE : {fiscal_ref}. Signature SHA-256 apposée. Facture définitivement verrouillée."
            ),
            user_name=invoice.certified_by,
            details_json=json.dumps({
                "fiscal_reference": fiscal_ref,
                "certified_at": now.isoformat(),
                "total_ttc": invoice.total_ttc,
                "notes": notes
            })
        )
        db.add(audit)
        db.commit()
        db.refresh(invoice)

        return invoice

    def sync_all_existing_orders_to_invoices(self, db: Session) -> int:
        """
        Synchronise au démarrage toutes les commandes déjà présentes dans la base de données
        vers les factures globales correspondantes.
        """
        self.ensure_default_tax_rules(db)
        orders = db.query(Order).filter(Order.status != "cancelled").order_by(Order.created_at.asc()).all()
        if not orders:
            return 0

        invoices_to_recalc = set()
        for o in orders:
            if not o.global_invoice_id:
                inv = self.get_or_create_global_invoice_for_order(o, db)
                o.global_invoice_id = inv.id
                o.is_invoiced = True
                o.invoiced_at = o.created_at
                invoices_to_recalc.add(inv.id)
            else:
                invoices_to_recalc.add(o.global_invoice_id)

        db.commit()

        for inv_id in invoices_to_recalc:
            try:
                self.recalculate_global_invoice(
                    invoice_id=inv_id,
                    db=db,
                    trigger_source="Initialisation Système",
                    action_description="Synchronisation initiale des commandes existantes."
                )
            except Exception as e:
                print(f"Erreur recalcul facture {inv_id} : {e}")

        return len(orders)


billing_service = BillingService()
