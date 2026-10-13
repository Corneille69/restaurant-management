from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.restaurant import RestaurantTable
from app.schemas.restaurant import TableCreate, TableResponse
from app.services.odoo_service import odoo_service

router = APIRouter(prefix="/tables", tags=["Restaurant Tables"])

@router.get("/", response_model=List[TableResponse])
def list_tables(db: Session = Depends(get_db)):
    """Liste toutes les tables du restaurant."""
    return db.query(RestaurantTable).all()

@router.post("/", response_model=TableResponse, status_code=status.HTTP_201_CREATED)
def create_table(payload: TableCreate, db: Session = Depends(get_db)):
    """Crée une nouvelle table et la synchronise automatiquement avec Odoo."""
    existing = db.query(RestaurantTable).filter(RestaurantTable.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Une table avec ce nom existe déjà.")

    table = RestaurantTable(
        name=payload.name,
        capacity=payload.capacity,
        status=payload.status
    )
    db.add(table)
    db.commit()
    db.refresh(table)

    # Synchronisation vers Odoo
    try:
        odoo_table_id = odoo_service.sync_table_to_odoo(
            table_id=table.id,
            table_name=table.name,
            seats=table.capacity
        )
        table.odoo_table_id = odoo_table_id
        db.commit()
        db.refresh(table)
    except Exception as e:
        # En cas d'indisponibilité momentanée d'Odoo, le backend reste fonctionnel
        pass

    return table

@router.get("/{table_id}", response_model=TableResponse)
def get_table(table_id: int, db: Session = Depends(get_db)):
    """Récupère les détails d'une table."""
    table = db.query(RestaurantTable).filter(RestaurantTable.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table introuvable.")
    return table
