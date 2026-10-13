from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import List
from app.core.database import get_db
from app.models.user import User
from app.models.restaurant import RestaurantTable, MenuItem, Order
from app.schemas.user import ManagerDashboardStats
from app.schemas.restaurant import TableResponse, OrderResponse
from app.api.deps import require_manager

router = APIRouter(prefix="/manager", tags=["Espace Gérant"])

@router.get("/dashboard", response_model=ManagerDashboardStats)
def get_manager_dashboard(
    db: Session = Depends(get_db),
    manager: User = Depends(require_manager)
):
    """
    Tableau de bord opérationnel du Gérant :
    - Tables libres vs occupées
    - Commandes en attente ou en préparation DU GÉRANT CONNECTÉ UNIQUEMENT
    - Total des plats disponibles
    """
    available_tables = db.query(RestaurantTable).filter(RestaurantTable.status == "available").count()
    occupied_tables = db.query(RestaurantTable).filter(RestaurantTable.status != "available").count()
    pending_orders = db.query(Order).filter(
        or_(
            func.lower(Order.manager_login) == manager.username.lower(),
            Order.manager_name == manager.full_name
        ),
        Order.status.in_(["pending", "cooking"])
    ).count()
    total_dishes = db.query(MenuItem).filter(MenuItem.is_available == True).count()

    return {
        "manager_name": manager.full_name,
        "manager_username": manager.username,
        "available_tables": available_tables,
        "occupied_tables": occupied_tables,
        "pending_orders": pending_orders,
        "total_dishes_on_menu": total_dishes
    }

@router.get("/tables", response_model=List[TableResponse])
def get_manager_tables(
    db: Session = Depends(get_db),
    manager: User = Depends(require_manager)
):
    """Permet au gérant de consulter l'état de toutes les tables du restaurant."""
    return db.query(RestaurantTable).all()

@router.patch("/tables/{table_id}/status", response_model=TableResponse)
def update_table_status(
    table_id: int,
    status_value: str,
    db: Session = Depends(get_db),
    manager: User = Depends(require_manager)
):
    """Permet au gérant de basculer une table en libre, occupée ou réservée."""
    valid_statuses = ["available", "occupied", "reserved"]
    if status_value not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Statut invalide. Choisissez parmi : {valid_statuses}"
        )

    table = db.query(RestaurantTable).filter(RestaurantTable.id == table_id).first()
    if not table:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table introuvable.")

    table.status = status_value
    db.commit()
    db.refresh(table)
    return table

@router.get("/orders", response_model=List[OrderResponse])
def get_manager_orders(
    db: Session = Depends(get_db),
    manager: User = Depends(require_manager)
):
    """
    Permet au gérant de suivre UNIQUEMENT ses propres commandes et ventes.
    Les commandes des autres gérants ne sont jamais visibles.
    """
    return db.query(Order).filter(
        or_(
            func.lower(Order.manager_login) == manager.username.lower(),
            Order.manager_name == manager.full_name
        )
    ).order_by(Order.id.desc()).all()

@router.patch("/orders/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    new_status: str,
    db: Session = Depends(get_db),
    manager: User = Depends(require_manager)
):
    """Permet au gérant de mettre à jour le statut uniquement de ses propres commandes."""
    valid_statuses = ["pending", "cooking", "served", "paid", "cancelled"]
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Statut invalide. Choisissez parmi : {valid_statuses}"
        )

    order = db.query(Order).filter(
        Order.id == order_id,
        or_(
            func.lower(Order.manager_login) == manager.username.lower(),
            Order.manager_name == manager.full_name
        )
    ).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Commande introuvable ou vous n'avez pas l'autorisation de modifier les ventes d'un autre gérant."
        )

    order.status = new_status
    db.commit()
    db.refresh(order)
    return order
