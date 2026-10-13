from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class LoginRequest(BaseModel):
    username: str = Field(..., example="admin")
    password: str = Field(..., example="admin123")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    username: str
    full_name: str
    assigned_space: str # "admin" ou "manager"

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    role: str
    is_active: bool
    is_online: bool = False
    last_login_at: Optional[datetime] = None
    last_logout_at: Optional[datetime] = None
    odoo_user_id: Optional[int] = None
    created_by_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ManagerCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, example="gerant_jean")
    email: str = Field(..., example="jean@restaurant.com")
    full_name: str = Field(..., min_length=2, max_length=100, example="Jean Dupont")
    password: str = Field(..., min_length=6, example="MonMotDePasseGerant2026!")

class ManagerUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

class AdminDashboardStats(BaseModel):
    total_managers: int
    active_managers: int
    online_managers: int = 0
    total_tables: int
    total_menu_items: int
    total_orders: int
    total_revenue: float
    odoo_connected: bool
    odoo_target_db: str

class ManagerWorkSessionResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    manager_name: str
    manager_login: str
    login_at: datetime
    logout_at: Optional[datetime] = None
    is_online: bool
    total_sales_amount: float
    total_orders_count: int
    total_tendered_amount: float
    total_change_amount: float
    last_activity_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ManagerActivityLogResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    manager_name: str
    manager_login: str
    action_type: str
    description: str
    order_number: Optional[str] = None
    amount: Optional[float] = None
    payment_method: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ManagerDashboardStats(BaseModel):
    manager_name: str
    manager_username: str
    available_tables: int
    occupied_tables: int
    pending_orders: int
    total_dishes_on_menu: int

