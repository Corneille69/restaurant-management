# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, HTTPException, status
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.restaurant import MenuItem, Category
from app.schemas.restaurant import MenuItemCreate, MenuItemResponse, CategoryCreate, CategoryResponse
from app.services.odoo_service import odoo_service
from app.api.deps import require_admin
from app.models.user import User

router = APIRouter(prefix="/menu", tags=["Restaurant Menu"])

# --- CATEGORIES ---
@router.get("/categories", response_model=List[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    """Crée une catégorie de menu (Réservé exclusivement à l'Administrateur)."""
    existing = db.query(Category).filter(Category.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Cette catégorie existe déjà.")
    cat = Category(name=payload.name)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    """Supprime une catégorie (Réservé exclusivement à l'Administrateur)."""
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Catégorie introuvable.")
    db.delete(cat)
    db.commit()
    return None


# --- ITEMS ---
@router.get("/items", response_model=List[MenuItemResponse])
def list_menu_items(db: Session = Depends(get_db)):
    """Liste tous les plats de la carte."""
    return db.query(MenuItem).all()

@router.post("/items", response_model=MenuItemResponse, status_code=status.HTTP_201_CREATED)
def create_menu_item(payload: MenuItemCreate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    """Crée un plat dans la carte et le synchronise dans Odoo (Réservé exclusivement à l'Administrateur)."""
    item = MenuItem(
        name=payload.name,
        description=payload.description,
        price=payload.price,
        is_available=payload.is_available,
        category_id=payload.category_id
    )
    db.add(item)
    db.commit()
    db.refresh(item)

    # Synchronisation vers Odoo
    try:
        cat = db.query(Category).filter(Category.id == item.category_id).first() if item.category_id else None
        cat_name = cat.name if cat else None
        product_id, tmpl_id = odoo_service.sync_product_to_odoo(
            item_id=item.id,
            name=item.name,
            price=item.price,
            category_name=cat_name
        )
        item.odoo_product_id = product_id
        item.odoo_template_id = tmpl_id
        db.commit()
        db.refresh(item)
    except Exception as e:
        pass

    return item

@router.get("/items/{item_id}", response_model=MenuItemResponse)
def get_menu_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Plat introuvable.")
    return item

@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    """Supprime un plat de la carte (Réservé exclusivement à l'Administrateur)."""
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Plat introuvable.")
    db.delete(item)
    db.commit()
    return None
