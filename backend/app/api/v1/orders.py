import uuid
import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from app.core.database import get_db
from app.models.restaurant import Order, OrderItem, MenuItem, RestaurantTable, ManagerWorkSession, ManagerActivityLog
from app.models.user import User, UserRole
from app.schemas.restaurant import OrderCreate, OrderResponse
from app.services.odoo_service import odoo_service
from app.api.deps import get_current_user_optional

router = APIRouter(prefix="/orders", tags=["Restaurant Orders"])

@router.get("/", response_model=List[OrderResponse])
def list_orders(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Liste les commandes enregistrées.
    Si un gérant est connecté, il ne voit QUE ses propres commandes et ventes.
    """
    if current_user and current_user.role == UserRole.MANAGER.value:
        return db.query(Order).filter(
            or_(
                func.lower(Order.manager_login) == current_user.username.lower(),
                Order.manager_name == current_user.full_name
            )
        ).order_by(Order.id.desc()).all()
    return db.query(Order).order_by(Order.id.desc()).all()

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    """
    Crée une commande client (Le Backend pilote le processus).
    Valide les plats, calcule le montant total, et crée l'enregistrement local.
    """
    # Interdiction stricte : L'administrateur ne vend pas, seuls les gérants ont la capacité de vendre
    if payload.manager_login and payload.manager_login.strip().lower() == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="L'administrateur n'est pas autorisé à vendre. Seuls les gérants ont la capacité d'encaisser et de réaliser des ventes."
        )

    if not payload.items:
        raise HTTPException(status_code=400, detail="La commande doit contenir au moins un plat.")

    table = None
    if payload.table_id:
        table = db.query(RestaurantTable).filter(RestaurantTable.id == payload.table_id).first()
        if not table:
            raise HTTPException(status_code=404, detail="Table introuvable.")

    order_number = f"RST-{uuid.uuid4().hex[:6].upper()}"
    total_amount = 0.0

    mgr_login = payload.manager_login or "gerant"
    mgr_name = payload.manager_name or "Gérant"
    mgr_user = db.query(User).filter(User.username == mgr_login).first()

    # Trouver ou initialiser la session de travail active du gérant
    work_sess = db.query(ManagerWorkSession).filter(
        ManagerWorkSession.manager_login == mgr_login,
        ManagerWorkSession.is_online == True
    ).order_by(ManagerWorkSession.id.desc()).first()

    now = datetime.datetime.utcnow()
    if not work_sess:
        work_sess = ManagerWorkSession(
            user_id=mgr_user.id if mgr_user else None,
            manager_name=mgr_name,
            manager_login=mgr_login,
            login_at=now,
            is_online=True,
            total_sales_amount=0.0,
            total_orders_count=0,
            total_tendered_amount=0.0,
            total_change_amount=0.0,
            last_activity_at=now
        )
        db.add(work_sess)
        db.flush()

    new_order = Order(
        order_number=order_number,
        table_id=payload.table_id,
        status="paid",
        total_amount=0.0,
        manager_name=mgr_name,
        manager_login=mgr_login,
        payment_method=payload.payment_method or "Espèces (Cash)",
        tendered_amount=payload.tendered_amount,
        change_amount=payload.change_amount,
        work_session_id=work_sess.id,
        odoo_sync_status="pending"
    )
    db.add(new_order)
    db.flush()

    sync_items = []
    custom_price_notices = []
    for it in payload.items:
        menu_item = db.query(MenuItem).filter(MenuItem.id == it.menu_item_id).first()
        if not menu_item:
            raise HTTPException(status_code=404, detail=f"Plat ID {it.menu_item_id} introuvable.")
        
        # Vérification et décrémentation du stock disponible (Plats, Desserts, Boissons)
        current_stock = menu_item.available_quantity if menu_item.available_quantity is not None else 0
        if current_stock <= 0 or not menu_item.is_available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Rupture de stock : Il n'y a aucun(e) '{menu_item.name}' disponible actuellement dans le restaurant."
            )
        if it.quantity >current_stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock insuffisant pour '{menu_item.name}' : seulement {current_stock} disponible(s), vous avez demandé {it.quantity}."
            )

        # Diminution du nombre présent en temps réel
        menu_item.available_quantity = max(0, current_stock - it.quantity)
        if menu_item.available_quantity == 0:
            menu_item.is_available = False

        # Synchroniser la diminution du stock vers Odoo en temps réel
        try:
            tmpl_id = menu_item.odoo_template_id
            if not tmpl_id and menu_item.odoo_product_id:
                read_p = odoo_service.execute_kw('product.product', 'read', [[menu_item.odoo_product_id]], {'fields': ['product_tmpl_id']})
                if read_p and read_p[0].get('product_tmpl_id'):
                    tmpl_id = read_p[0]['product_tmpl_id'][0] if isinstance(read_p[0]['product_tmpl_id'], (list, tuple)) else read_p[0]['product_tmpl_id']
                    menu_item.odoo_template_id = tmpl_id
            if tmpl_id:
                odoo_service.execute_kw('product.template', 'write', [[tmpl_id], {'available_quantity': menu_item.available_quantity}])
        except Exception:
            pass

        # Le gérant peut ajuster le prix unitaire en FCFA ou conserver le prix du menu
        unit_price = it.custom_price if (it.custom_price is not None and it.custom_price >=0) else menu_item.price
        if it.custom_price is not None and it.custom_price != menu_item.price:
            custom_price_notices.append(f"{menu_item.name} ajusté à {unit_price:,.0f} FCFA (catalogue: {menu_item.price:,.0f} FCFA)")

        subtotal = unit_price * it.quantity
        total_amount += subtotal

        order_item = OrderItem(
            order_id=new_order.id,
            menu_item_id=menu_item.id,
            quantity=it.quantity,
            unit_price=unit_price,
            subtotal=subtotal,
            notes=it.notes
        )
        db.add(order_item)

        sync_items.append({
            'menu_item_id': menu_item.id,
            'name': menu_item.name,
            'price': unit_price,
            'quantity': it.quantity,
            'odoo_product_id': menu_item.odoo_product_id
        })

    new_order.total_amount = round(total_amount, 2)

    # Mise à jour des cumuls de la session de travail du gérant
    work_sess.total_sales_amount = round(work_sess.total_sales_amount + new_order.total_amount, 2)
    work_sess.total_orders_count += 1
    work_sess.total_tendered_amount = round(work_sess.total_tendered_amount + (payload.tendered_amount or new_order.total_amount), 2)
    work_sess.total_change_amount = round(work_sess.total_change_amount + (payload.change_amount or 0.0), 2)
    work_sess.last_activity_at = now

    # Traçabilité intégrale dans le journal d'activité (faits et gestes du gérant)
    item_summary = ", ".join([f"{it['name']} x{it['quantity']}" for it in sync_items])
    details_str = f" Vente encaissée #{new_order.order_number} : {item_summary} | Total : {new_order.total_amount:,.0f} FCFA via {new_order.payment_method}. Encaissé : {(payload.tendered_amount or new_order.total_amount):,.0f} FCFA, Monnaie : {(payload.change_amount or 0):,.0f} FCFA."
    if custom_price_notices:
        details_str += " [Ajustements prix: " + "; ".join(custom_price_notices) + "]"

    activity = ManagerActivityLog(
        user_id=mgr_user.id if mgr_user else None,
        manager_name=mgr_name,
        manager_login=mgr_login,
        action_type="ORDER_SALE",
        order_number=new_order.order_number,
        amount=new_order.total_amount,
        payment_method=new_order.payment_method,
        description=details_str,
        created_at=now
    )
    db.add(activity)

    db.commit()
    db.refresh(new_order)

    # Collaborer avec Odoo : Envoyer la commande au Point de Vente Odoo
    try:
        table_name = table.name if table else "A Emporter"
        odoo_order_id = odoo_service.sync_order_to_pos(
            order_number=new_order.order_number,
            table_name=table_name,
            items=sync_items,
            total_amount=new_order.total_amount,
            manager_id=mgr_user.odoo_user_id if mgr_user else None
        )
        new_order.odoo_pos_order_id = odoo_order_id
        new_order.odoo_sync_status = "synced"
        db.commit()
        db.refresh(new_order)
    except Exception as e:
        new_order.odoo_sync_status = "error"
        new_order.odoo_sync_error = str(e)
        db.commit()
        db.refresh(new_order)

    # Transmission automatique à la facturation globale dynamique de l'Administrateur (Exigences 1, 4, 5, 7)
    try:
        from app.services.billing_service import billing_service
        billing_service.integrate_order_into_global_invoicing(new_order, db)
        db.refresh(new_order)
    except Exception as e:
        print(f"Erreur intégration facturation globale : {e}")

    return new_order

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int, 
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Commande introuvable.")
    if current_user and current_user.role == UserRole.MANAGER.value:
        mgr_match = (
            (order.manager_login and order.manager_login.lower() == current_user.username.lower()) or
            (order.manager_name == current_user.full_name)
        )
        if not mgr_match:
            raise HTTPException(status_code=403, detail="Accès interdit : Cette commande a été réalisée par un autre gérant.")
    return order

@router.post("/{order_id}/cancel")
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Annulation d'une vente (Exigence 10 & 11) :
    - Si la vente est déjà certifiée dans une facture globale verrouillée : refus strict.
    - Si la facture est encore en cours / brouillon : la vente est retirée du calcul et la facture globale est immédiatement actualisée.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Commande introuvable.")

    # Vérifier si rattachée à une facture certifiée
    if order.is_certified_dgi:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Impossible d'annuler directement cette vente : elle a déjà été certifiée et verrouillée fiscalement auprès de la DGI."
        )

    from app.models.restaurant import GlobalInvoice
    if order.global_invoice_id:
        global_inv = db.query(GlobalInvoice).filter(GlobalInvoice.id == order.global_invoice_id).first()
        if global_inv and global_inv.is_certified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Impossible d'annuler cette vente : la facture globale de la période est déjà certifiée et verrouillée."
            )

    order.status = "cancelled"
    db.commit()

    # Répercussion immédiate sur la facture globale
    from app.services.billing_service import billing_service
    billing_service.handle_order_cancelled_or_modified(order, db)

    return {"status": "success", "message": f"Vente #{order.order_number} annulée et retirée de la facturation globale."}
