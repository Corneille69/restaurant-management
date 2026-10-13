from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# --- ODOO STATUS ---
class OdooStatusResponse(BaseModel):
    connected: bool
    odoo_url: str
    database: str
    user_id: Optional[int] = None
    pos_config_id: Optional[int] = None
    message: str


# --- TABLES ---
class TableBase(BaseModel):
    name: str = Field(..., example="Table 1")
    capacity: int = Field(default=4, ge=1)
    status: str = Field(default="available", example="available")

class TableCreate(TableBase):
    pass

class TableResponse(TableBase):
    id: int
    odoo_table_id: Optional[int] = None

    class Config:
        from_attributes = True


# --- CATEGORIES ---
class CategoryBase(BaseModel):
    name: str = Field(..., example="Entrées")

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    odoo_category_id: Optional[int] = None

    class Config:
        from_attributes = True


# --- MENU ITEMS ---
class MenuItemBase(BaseModel):
    name: str = Field(..., example="Pizza Margherita")
    description: Optional[str] = Field(None, example="Tomate, mozzarella, basilic frais")
    price: float = Field(..., ge=0, example=12.50)
    is_available: bool = True
    category_id: Optional[int] = None

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemResponse(MenuItemBase):
    id: int
    odoo_product_id: Optional[int] = None

    class Config:
        from_attributes = True


# --- ORDERS ---
class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = Field(default=1, ge=1)
    notes: Optional[str] = None
    custom_price: Optional[float] = None # Prix personnalisable en FCFA par le gérant

class OrderItemResponse(BaseModel):
    id: int
    menu_item_id: int
    item_name: Optional[str] = None
    quantity: int
    unit_price: float
    subtotal: float
    notes: Optional[str] = None

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    table_id: Optional[int] = None
    items: List[OrderItemCreate]
    manager_name: Optional[str] = None
    manager_login: Optional[str] = None
    payment_method: Optional[str] = "Espèces (Cash)"
    tendered_amount: Optional[float] = None
    change_amount: Optional[float] = None

class OrderResponse(BaseModel):
    id: int
    order_number: str
    table_id: Optional[int] = None
    status: str
    total_amount: float
    manager_name: Optional[str] = None
    manager_login: Optional[str] = None
    session_name: Optional[str] = None
    payment_method: Optional[str] = "Espèces (Cash)"
    tendered_amount: Optional[float] = None
    change_amount: Optional[float] = None
    is_certified_dgi: Optional[bool] = False
    dgi_invoice_number: Optional[str] = None
    odoo_pos_order_id: Optional[int] = None
    odoo_sync_status: str
    global_invoice_id: Optional[int] = None
    is_invoiced: Optional[bool] = False
    created_at: datetime
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True


class DailyInvoiceResponse(BaseModel):
    id: Optional[int] = None
    invoice_date: str
    invoice_number: str
    total_ttc: float
    total_ht: float
    total_tva: float
    total_orders: int
    payment_breakdown: Optional[dict] = {}
    manager_breakdown: Optional[dict] = {}
    is_certified_dgi: bool
    dgi_nif: Optional[str] = None
    dgi_nim: Optional[str] = None
    dgi_reference: Optional[str] = None
    dgi_security_code: Optional[str] = None
    dgi_qr_code_data: Optional[str] = None
    dgi_certified_at: Optional[datetime] = None
    certified_by: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True



class PosSessionResponse(BaseModel):
    id: int
    odoo_session_id: int
    session_name: str
    manager_name: Optional[str] = None
    manager_login: Optional[str] = None
    start_at: Optional[datetime] = None
    stop_at: Optional[datetime] = None
    state: str
    total_sales: float
    cash_difference: float
    created_at: datetime

    class Config:
        from_attributes = True


class RestaurantConfigBase(BaseModel):
    restaurant_name: str = "Lemo Daje Restaurant"
    restaurant_subtitle: Optional[str] = "Restaurant & Grill Gastronomique"
    logo_url: Optional[str] = None
    ifu: Optional[str] = "000123456789A"
    nif: Optional[str] = "000123456789A"
    nim: Optional[str] = "RESTO-DGI-MCF-01"
    rccm: Optional[str] = "BF-OUA-01-2024-B12-00456"
    default_tax_regime: Optional[str] = "Régime du Réel Normal d'Imposition (RNI)"
    fiscal_division: Optional[str] = "DGI - Division Fiscale des Moyennes Entreprises"
    tax_center: Optional[str] = "DGI - Division Fiscale des Moyennes Entreprises"
    tax_rate: Optional[float] = 18.0
    legal_mention: Optional[str] = "Facture normalisée certifiée conforme aux exigences de la DGI"
    dgi_qr_enabled: Optional[bool] = True
    billing_frequency: Optional[str] = "daily"
    menu_prices_include_tax: Optional[bool] = True
    address: Optional[str] = "Avenue Kwame Nkrumah, Ouagadougou"
    phone: Optional[str] = "+226 25 30 00 00 / +226 70 00 00 00"
    email: Optional[str] = "contact@lemodaje.com"
    website: Optional[str] = "www.lemodaje.com"
    primary_color: Optional[str] = "#7d6b5c"
    bg_color: Optional[str] = "#f8f5f0"

class RestaurantConfigUpdate(RestaurantConfigBase):
    pass

class RestaurantConfigResponse(RestaurantConfigBase):
    id: int
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True



