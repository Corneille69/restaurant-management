from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
import logging
from app.core.database import get_db
from app.services.odoo_service import odoo_service
from app.schemas.restaurant import OdooStatusResponse
from app.models.restaurant import (
    RestaurantTable, MenuItem, Order, OrderItem, Category, PosSession, 
    DailyInvoice, ManagerWorkSession, ManagerActivityLog
)
from app.models.user import User
from app.core.security import hash_password
from sqlalchemy import or_, func
import datetime

logger = logging.getLogger("odoo_api")
router = APIRouter(prefix="/odoo", tags=["Odoo Integration"])

@router.get("/status", response_model=OdooStatusResponse)
def get_odoo_status():
    """Vérifie la connexion et l'état de synchronisation avec Odoo."""
    return odoo_service.test_connection()

@router.post("/sync-all")
def sync_all_data_to_odoo(db: Session = Depends(get_db)):
    """Synchronise toutes les tables et plats de la base locale vers Odoo."""
    tables = db.query(RestaurantTable).all()
    synced_tables = 0
    for t in tables:
        try:
            odoo_id = odoo_service.sync_table_to_odoo(t.id, t.name, t.capacity)
            t.odoo_table_id = odoo_id
            synced_tables += 1
        except Exception:
            pass

    items = db.query(MenuItem).all()
    synced_items = 0
    for it in items:
        try:
            prod_id, tmpl_id = odoo_service.sync_product_to_odoo(it.id, it.name, it.price)
            it.odoo_product_id = prod_id
            it.odoo_template_id = tmpl_id
            synced_items += 1
        except Exception:
            pass

    db.commit()
    return {
        "status": "success",
        "synced_tables": synced_tables,
        "synced_menu_items": synced_items,
        "message": "Synchronisation complète avec Odoo terminée avec succès."
    }

@router.post("/sync-from-odoo")
@router.get("/sync-from-odoo")
def sync_data_from_odoo(db: Session = Depends(get_db)):
    """Importe et synchronise en temps réel toutes les actions faites dans Odoo (Plats, Gérants, Commandes, Tables)."""
    counts = odoo_service.sync_all_from_odoo(db)
    print(f" [ODOO SYNC ACTIVE] Données synchronisées depuis Odoo : {counts}")
    return {
        "status": "success",
        "synced": counts,
        "message": f"Synchronisation Odoo terminée : {counts['dishes']} plats, {counts['managers']} gérants, {counts['orders']} commandes synchronisés."
    }

@router.post("/webhook/manager")
async def webhook_manager(request: Request, db: Session = Depends(get_db)):
    """Webhook appelé en temps réel par Odoo lors de la création/modification d'un gérant."""
    data = await request.json()
    name = data.get("name")
    login = data.get("login")
    odoo_id = data.get("odoo_id")
    password = data.get("password", "Pass1234!")
    print(f" [ACTION ODOO REÇUE] Nouveau Gérant créé dans Odoo : {name} (login: {login})")

    user = db.query(User).filter((User.username == login) | (User.odoo_user_id == odoo_id)).first()
    if not user:
        user = User(
            username=login,
            email=f"{login}@restaurant.local",
            full_name=name,
            role="manager",
            hashed_password=hash_password(password),
            is_active=True,
            odoo_user_id=odoo_id
        )
        db.add(user)
    else:
        user.full_name = name
        user.is_active = True
        user.odoo_user_id = odoo_id
    db.commit()
    return {"status": "ok", "user_id": user.id}

@router.post("/webhook/dish")
async def webhook_dish(request: Request, db: Session = Depends(get_db)):
    """Webhook appelé en temps réel par Odoo lors de la création/modification d'un plat."""
    data = await request.json()
    name = data.get("name")
    price = float(data.get("price", 0.0))
    tmpl_id = data.get("tmpl_id")
    category_name = data.get("category", "Plats Principaux")
    print(f" [ACTION ODOO REÇUE] Nouveau Plat créé dans Odoo : {name} ({price} FCFA, Catégorie: {category_name})")

    # Associer la catégorie
    cat_id = None
    if category_name:
        category = db.query(Category).filter(Category.name == category_name).first()
        if not category:
            category = Category(name=category_name)
            db.add(category)
            db.flush()
        cat_id = category.id

    qty = int(data.get("available_quantity")) if data.get("available_quantity") is not None else 0
    item = db.query(MenuItem).filter((MenuItem.name == name) | (MenuItem.odoo_template_id == tmpl_id)).first()
    if not item:
        item = MenuItem(
            name=name,
            price=price,
            is_available=qty >0,
            available_quantity=qty,
            odoo_template_id=tmpl_id,
            category_id=cat_id
        )
        db.add(item)
    else:
        item.price = price
        item.odoo_template_id = tmpl_id
        if data.get("available_quantity") is not None:
            item.available_quantity = qty
            item.is_available = qty >0
        if cat_id:
            item.category_id = cat_id
    db.commit()
    return {"status": "ok", "item_id": item.id}

@router.post("/webhook/dish_delete")
async def webhook_dish_delete(request: Request, db: Session = Depends(get_db)):
    """Webhook appelé en temps réel lors du retrait ou suppression d'un plat dans Odoo."""
    data = await request.json()
    tmpl_id = data.get("tmpl_id")
    name = data.get("name")
    print(f" [ACTION ODOO REÇUE] Suppression du Plat : {name} (tmpl_id: {tmpl_id})")

    item = db.query(MenuItem).filter((MenuItem.odoo_template_id == tmpl_id) | (MenuItem.name == name)).first()
    if item:
        db.delete(item)
        db.commit()
    return {"status": "ok"}


@router.post("/webhook/order")
async def webhook_order(request: Request, db: Session = Depends(get_db)):
    """Webhook appelé en temps réel par Odoo lors de la validation d'une commande POS."""
    data = await request.json()
    order_name = data.get("order_name")
    total = float(data.get("total", 0.0))
    tendered_amount = data.get("tendered_amount")
    change_amount = data.get("change_amount")
    odoo_id = data.get("odoo_id")
    state = data.get("state", "paid")
    manager_name = data.get("manager_name")
    manager_login = data.get("manager_login")
    session_name = data.get("session_name")
    payment_method = data.get("payment_method", "Espèces (Cash)")
    date_order_str = data.get("date_order")
    
    order_date = datetime.datetime.utcnow()
    if date_order_str:
        try:
            order_date = datetime.datetime.fromisoformat(date_order_str.replace("Z", "+00:00"))
        except Exception:
            pass

    print(f" [ACTION ODOO REÇUE] Vente validée dans Odoo : {order_name} ({total} FCFA sans monnaie) par {manager_name} ({manager_login}) - Mode: {payment_method}")

    clean_name = (order_name or "").replace("CMD-", "")
    order = db.query(Order).filter(
        (Order.order_number == order_name) | 
        (Order.order_number == clean_name) | 
        (Order.odoo_pos_order_id == odoo_id)
    ).first()
    if not order:
        order = Order(
            order_number=order_name,
            total_amount=total,
            tendered_amount=float(tendered_amount) if tendered_amount is not None else total,
            change_amount=float(change_amount) if change_amount is not None else 0.0,
            status="paid" if state in ("paid", "done") else "pending",
            odoo_pos_order_id=odoo_id,
            odoo_sync_status="synced",
            manager_name=manager_name,
            manager_login=manager_login,
            session_name=session_name,
            payment_method=payment_method,
            created_at=order_date
        )
        db.add(order)
    else:
        order.total_amount = total
        if tendered_amount is not None:
            order.tendered_amount = float(tendered_amount)
        if change_amount is not None:
            order.change_amount = float(change_amount)
        order.status = "paid" if state in ("paid", "done") else "pending"
        order.odoo_sync_status = "synced"
        if manager_name:
            order.manager_name = manager_name
        if manager_login:
            order.manager_login = manager_login
        if session_name:
            order.session_name = session_name
        if payment_method:
            order.payment_method = payment_method
        if date_order_str:
            order.created_at = order_date
    db.commit()
    db.refresh(order)

    # 1. Enregistrement des lignes d'articles de la commande (OrderItem)
    lines = data.get("lines", [])
    if lines:
        try:
            existing_items_count = db.query(OrderItem).filter(OrderItem.order_id == order.id).count()
            if existing_items_count == 0:
                for l in lines:
                    p_id = l.get("product_id")
                    item_name = l.get("name") or "Article"
                    qty = int(l.get("qty", 1))
                    price_unit = float(l.get("price_unit", 0.0))
                    subtotal = float(l.get("price_subtotal_incl", price_unit * qty))

                    # Retrouver ou créer le MenuItem correspondant
                    m_item = None
                    if p_id:
                        m_item = db.query(MenuItem).filter(MenuItem.odoo_product_id == p_id).first()
                    if not m_item and item_name:
                        m_item = db.query(MenuItem).filter(MenuItem.name == item_name).first()
                    if not m_item:
                        m_item = MenuItem(
                            name=item_name,
                            price=price_unit,
                            odoo_product_id=p_id,
                            is_available=True,
                            available_quantity=0
                        )
                        db.add(m_item)
                        db.flush()

                    db.add(OrderItem(
                        order_id=order.id,
                        menu_item_id=m_item.id,
                        quantity=qty,
                        unit_price=price_unit,
                        subtotal=subtotal
                    ))
                db.commit()
        except Exception as e:
            print(f"Erreur création lignes commande webhook_order: {e}")

    # 2. Mise à jour de la session de travail et traçabilité du gérant
    if manager_login or manager_name:
        try:
            mgr_user = db.query(User).filter(
                or_(
                    func.lower(User.username) == (manager_login or "").lower(),
                    User.full_name == manager_name
                )
            ).first()

            login_key = manager_login or (mgr_user.username if mgr_user else "gerant")
            work_sess = db.query(ManagerWorkSession).filter(
                func.lower(ManagerWorkSession.manager_login) == login_key.lower(),
                ManagerWorkSession.is_online == True
            ).order_by(ManagerWorkSession.id.desc()).first()

            if not work_sess:
                work_sess = ManagerWorkSession(
                    user_id=mgr_user.id if mgr_user else None,
                    manager_name=manager_name or (mgr_user.full_name if mgr_user else login_key),
                    manager_login=login_key,
                    is_online=True,
                    login_at=order_date
                )
                db.add(work_sess)
                db.flush()

            work_sess.total_sales_amount = round((work_sess.total_sales_amount or 0.0) + total, 2)
            work_sess.total_orders_count = (work_sess.total_orders_count or 0) + 1
            work_sess.total_tendered_amount = round((work_sess.total_tendered_amount or 0.0) + (float(tendered_amount) if tendered_amount is not None else total), 2)
            work_sess.total_change_amount = round((work_sess.total_change_amount or 0.0) + (float(change_amount) if change_amount is not None else 0.0), 2)
            work_sess.last_activity_at = order_date

            # Journal d'activité (faits et gestes du gérant)
            line_desc = ", ".join([f"{l.get('name', 'Article')} x{l.get('qty', 1)}" for l in lines]) if lines else "Articles variés"
            activity = ManagerActivityLog(
                user_id=mgr_user.id if mgr_user else None,
                manager_name=manager_name or (mgr_user.full_name if mgr_user else login_key),
                manager_login=login_key,
                action_type="ORDER_SALE",
                order_number=order.order_number,
                amount=total,
                payment_method=payment_method,
                description=f" Vente encaissée #{order.order_number} ({line_desc}) : {total:,.0f} FCFA nets ({payment_method}). Versé: {(float(tendered_amount) if tendered_amount is not None else total):,.0f} FCFA, Monnaie: {(float(change_amount) if change_amount is not None else 0):,.0f} FCFA.",
                created_at=order_date
            )
            db.add(activity)
            db.commit()
        except Exception as e:
            print(f"Erreur mise à jour session/activité gérant webhook_order: {e}")

    # 3. Transmission et intégration automatique à la facturation globale (Admin)
    try:
        from app.services.billing_service import billing_service
        billing_service.integrate_order_into_global_invoicing(order, db)
    except Exception as e:
        print(f"Erreur intégration facturation globale webhook_order: {e}")

    # 4. Accumulation en direct de la facturation de la journée (compatibilité)
    try:
        today_date = order_date.date()
        daily_inv = db.query(DailyInvoice).filter(DailyInvoice.invoice_date == today_date).first()
        start_dt = datetime.datetime.combine(today_date, datetime.time.min)
        end_dt = datetime.datetime.combine(today_date, datetime.time.max)
        day_orders = db.query(Order).filter(Order.created_at >=start_dt, Order.created_at <= end_dt).all()
        day_ttc = sum(o.total_amount for o in day_orders if o.status in ("paid", "done"))
        day_ht = round(day_ttc / 1.18, 2) if day_ttc >0 else 0.0
        day_tva = round(day_ttc - day_ht, 2) if day_ttc >0 else 0.0

        if not daily_inv:
            daily_inv = DailyInvoice(
                invoice_date=today_date,
                invoice_number=f"FACT-GEN-{today_date.strftime('%Y%m%d')}-01",
                total_ttc=day_ttc,
                total_ht=day_ht,
                total_tva=day_tva,
                total_orders=len(day_orders),
                is_certified_dgi=False
            )
            db.add(daily_inv)
        elif not daily_inv.is_certified_dgi:
            daily_inv.total_ttc = day_ttc
            daily_inv.total_ht = day_ht
            daily_inv.total_tva = day_tva
            daily_inv.total_orders = len(day_orders)
        db.commit()
    except Exception as e:
        print(f"Erreur mise à jour accumulation facturation journalière: {e}")

    return {"status": "ok", "order_id": order.id}

@router.post("/webhook/daily_report_certified")
async def webhook_daily_report_certified(request: Request, db: Session = Depends(get_db)):
    """Webhook appelé lorsqu'une Facture Générale est certifiée DGI dans Odoo."""
    data = await request.json()
    invoice_date_str = data.get("invoice_date")
    invoice_number = data.get("invoice_number")
    total_ttc = float(data.get("total_ttc", 0.0))
    total_ht = float(data.get("total_ht", 0.0))
    total_tva = float(data.get("total_tva", 0.0))
    total_orders = int(data.get("total_orders", 0))
    dgi_reference = data.get("dgi_reference")
    dgi_security_code = data.get("dgi_security_code")
    certified_by = data.get("certified_by", "Administrateur")

    query_date = datetime.date.today()
    if invoice_date_str:
        try:
            query_date = datetime.date.fromisoformat(invoice_date_str)
        except Exception:
            pass

    daily_inv = db.query(DailyInvoice).filter(DailyInvoice.invoice_date == query_date).first()
    if not daily_inv:
        daily_inv = DailyInvoice(
            invoice_date=query_date,
            invoice_number=invoice_number,
            total_ttc=total_ttc,
            total_ht=total_ht,
            total_tva=total_tva,
            total_orders=total_orders,
            is_certified_dgi=True,
            dgi_reference=dgi_reference,
            dgi_security_code=dgi_security_code,
            dgi_certified_at=datetime.datetime.utcnow(),
            certified_by=certified_by
        )
        db.add(daily_inv)
    else:
        daily_inv.invoice_number = invoice_number
        daily_inv.total_ttc = total_ttc
        daily_inv.total_ht = total_ht
        daily_inv.total_tva = total_tva
        daily_inv.total_orders = total_orders
        daily_inv.is_certified_dgi = True
        daily_inv.dgi_reference = dgi_reference
        daily_inv.dgi_security_code = dgi_security_code
        daily_inv.dgi_certified_at = datetime.datetime.utcnow()
        daily_inv.certified_by = certified_by
    db.commit()
    print(f" [DGI CERTIFICATION SYNC] Facture Générale Odoo {invoice_number} certifiée DGI : {dgi_reference} ({total_ttc} FCFA)")
    return {"status": "ok"}

@router.post("/webhook/session")
async def webhook_session(request: Request, db: Session = Depends(get_db)):
    """Webhook appelé en temps réel par Odoo lors de l'ouverture, mise à jour ou clôture d'une session de caisse gérant."""
    data = await request.json()
    session_id = data.get("session_id")
    session_name = data.get("session_name", f"POS/{session_id}")
    manager_name = data.get("manager_name")
    manager_login = data.get("manager_login")
    start_at_str = data.get("start_at")
    stop_at_str = data.get("stop_at")
    state = data.get("state", "opened")
    total_sales = float(data.get("total_sales", 0.0) or 0.0)
    cash_diff = float(data.get("cash_difference", 0.0) or 0.0)
    
    print(f" [SESSION ODOO REÇUE] Session {session_name} - Gérant: {manager_name} ({manager_login}) - État: {state} - Total: {total_sales} FCFA - Écart: {cash_diff} FCFA")

    start_at = None
    if start_at_str:
        try:
            start_at = datetime.datetime.fromisoformat(start_at_str.replace("Z", "+00:00"))
        except Exception:
            pass

    stop_at = None
    if stop_at_str:
        try:
            stop_at = datetime.datetime.fromisoformat(stop_at_str.replace("Z", "+00:00"))
        except Exception:
            pass

    session_rec = db.query(PosSession).filter(PosSession.odoo_session_id == session_id).first()
    if not session_rec:
        session_rec = PosSession(
            odoo_session_id=session_id,
            session_name=session_name,
            manager_name=manager_name,
            manager_login=manager_login,
            start_at=start_at or datetime.datetime.utcnow(),
            stop_at=stop_at,
            state=state,
            total_sales=total_sales,
            cash_difference=cash_diff
        )
        db.add(session_rec)
    else:
        session_rec.session_name = session_name
        if manager_name:
            session_rec.manager_name = manager_name
        if manager_login:
            session_rec.manager_login = manager_login
        if start_at:
            session_rec.start_at = start_at
        if stop_at:
            session_rec.stop_at = stop_at
        session_rec.state = state
        session_rec.total_sales = total_sales
        session_rec.cash_difference = cash_diff

    db.commit()
    return {"status": "ok", "session_id": session_rec.id}

@router.get("/sessions")
def list_pos_sessions(db: Session = Depends(get_db)):
    """Retourne la liste des sessions de caisse avec état de service du gérant, heures de début/fin, ventes et écarts."""
    sessions = db.query(PosSession).order_by(PosSession.id.desc()).all()
    return [
        {
            "id": s.id,
            "odoo_session_id": s.odoo_session_id,
            "session_name": s.session_name,
            "manager_name": s.manager_name,
            "manager_login": s.manager_login,
            "start_at": s.start_at.isoformat() if s.start_at else None,
            "stop_at": s.stop_at.isoformat() if s.stop_at else None,
            "state": s.state,
            "is_active": s.state in ("opened", "opening_control"),
            "total_sales": s.total_sales,
            "cash_difference": s.cash_difference,
            "created_at": s.created_at.isoformat() if s.created_at else None
        }
        for s in sessions
    ]

@router.post("/webhook/manager_toggle")
async def webhook_manager_toggle(request: Request, db: Session = Depends(get_db)):
    """Webhook appelé en temps réel par Odoo lors de la suspension ou réactivation d'un gérant."""
    data = await request.json()
    login = data.get("login")
    odoo_id = data.get("odoo_id")
    is_active = data.get("is_active", True)
    print(f" [ACTION ODOO REÇUE] Statut Gérant modifié : {login} ->Actif={is_active}")

    user = db.query(User).filter((User.username == login) | (User.odoo_user_id == odoo_id)).first()
    if user:
        user.is_active = is_active
        db.commit()
    return {"status": "ok"}

@router.post("/webhook/manager_delete")
async def webhook_manager_delete(request: Request, db: Session = Depends(get_db)):
    """Webhook appelé en temps réel par Odoo lors de la suppression d'un gérant."""
    data = await request.json()
    login = data.get("login")
    odoo_id = data.get("odoo_id")
    print(f" [ACTION ODOO REÇUE] Suppression du Gérant : {login}")

    user = db.query(User).filter((User.username == login) | (User.odoo_user_id == odoo_id)).first()
    if user:
        try:
            db.delete(user)
            db.commit()
            print(f" Gérant {login} supprimé de la base PostgreSQL.")
        except Exception as e:
            db.rollback()
            print(f" Suppression physique bloquée par contraintes d'intégrité ({e}), archivage et désactivation du compte gérant.")
            user.is_active = False
            user.is_online = False
            db.commit()
            print(f" Gérant {login} désactivé avec succès dans PostgreSQL.")
    return {"status": "ok"}

@router.post("/webhook/sync_settings_from_odoo")
async def webhook_sync_settings_from_odoo(request: Request, db: Session = Depends(get_db)):
    """Reçoit la mise à jour des paramètres et de la fiscalité DGI depuis Odoo."""
    data = await request.json()
    from app.models.restaurant import RestaurantConfig
    cfg = db.query(RestaurantConfig).first()
    if not cfg:
        cfg = RestaurantConfig()
        db.add(cfg)
    
    for k, v in data.items():
        if hasattr(cfg, k) and v is not None:
            setattr(cfg, k, v)
    
    # Synchronisation IFU <->NIF
    if "ifu" in data and data["ifu"]:
        cfg.nif = data["ifu"]
    if "fiscal_division" in data and data["fiscal_division"]:
        cfg.tax_center = data["fiscal_division"]

    db.commit()
    print(" [ACTION ODOO REÇUE] Configuration Restaurant & Fiscalité DGI synchronisée depuis Odoo !")
    return {"status": "ok"}
