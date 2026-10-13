from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict
from datetime import datetime, date

# --- RÈGLES FISCALES DGI ---
class TaxRuleBase(BaseModel):
    name: str = Field(..., example="TVA 18% (Norme DGI)")
    tax_type: str = Field(default="VAT", example="VAT") # VAT, SPECIFIC, WITHHOLDING, EXCISE
    rate: float = Field(..., ge=0, example=18.0) # Taux en %
    calculation_base: str = Field(default="HT", example="HT") # "HT" ou "TTC"
    calculation_order: int = Field(default=1, ge=1)
    tax_regime: str = Field(default="TOUS", example="REEL_NORMAL")
    rounding_mode: str = Field(default="round_2_decimals") # round_2_decimals, round_integer, ceil, floor
    application_condition: str = Field(default="always") # always, threshold_min
    min_threshold: float = Field(default=0.0, ge=0)
    valid_from: Optional[date] = None
    valid_to: Optional[date] = None
    is_active: bool = True
    description: Optional[str] = None

class TaxRuleCreate(TaxRuleBase):
    pass

class TaxRuleUpdate(BaseModel):
    name: Optional[str] = None
    tax_type: Optional[str] = None
    rate: Optional[float] = None
    calculation_base: Optional[str] = None
    calculation_order: Optional[int] = None
    tax_regime: Optional[str] = None
    rounding_mode: Optional[str] = None
    application_condition: Optional[str] = None
    min_threshold: Optional[float] = None
    valid_from: Optional[date] = None
    valid_to: Optional[date] = None
    is_active: Optional[bool] = None
    description: Optional[str] = None

class TaxRuleResponse(TaxRuleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- LIGNES DE FACTURE GLOBALE ---
class GlobalInvoiceItemResponse(BaseModel):
    id: int
    order_id: int
    order_number: str
    order_date: datetime
    manager_name: Optional[str] = None
    manager_login: Optional[str] = None
    payment_method: str
    items_summary: Optional[str] = None
    total_items_count: int
    unit_price: float
    amount_ht: float
    amount_tax: float
    amount_ttc: float
    tax_details: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# --- HISTORIQUE D'AUDIT ---
class GlobalInvoiceAuditLogResponse(BaseModel):
    id: int
    global_invoice_id: int
    action_type: str
    description: str
    user_name: str
    details_json: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# --- FACTURE GLOBALE ---
class GlobalInvoiceResponse(BaseModel):
    id: int
    invoice_number: str
    period_type: str
    period_start: datetime
    period_end: datetime
    period_label: str
    status: str
    manager_name: Optional[str] = None
    manager_login: Optional[str] = None
    manager_id: Optional[int] = None
    opened_at: Optional[datetime] = None
    total_sales_count: int
    total_ht: float
    total_taxes: float
    total_ttc: float
    tax_details: Optional[str] = None
    manager_summary: Optional[str] = None
    payment_summary: Optional[str] = None
    anomalies: Optional[str] = None
    has_anomalies: bool
    is_certified: bool
    certified_at: Optional[datetime] = None
    certified_by: Optional[str] = None
    certification_notes: Optional[str] = None
    dgi_nif: Optional[str] = None
    dgi_nim: Optional[str] = None
    dgi_fiscal_reference: Optional[str] = None
    dgi_security_code: Optional[str] = None
    dgi_qr_code_data: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class GlobalInvoiceDetailResponse(GlobalInvoiceResponse):
    items: List[GlobalInvoiceItemResponse] = []
    audit_logs: List[GlobalInvoiceAuditLogResponse] = []


# --- CONFIGURATION FACTURATION ---
class BillingConfigResponse(BaseModel):
    billing_frequency: str = "daily" # daily, weekly, monthly
    menu_prices_include_tax: bool = True
    default_tax_regime: str = "REEL_NORMAL"

class BillingConfigUpdate(BaseModel):
    billing_frequency: Optional[str] = None
    menu_prices_include_tax: Optional[bool] = None
    default_tax_regime: Optional[str] = None

class GenerateInvoiceRequest(BaseModel):
    period_type: Optional[str] = "daily" # daily, weekly, monthly, custom
    target_date: Optional[str] = None # YYYY-MM-DD
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class CertifyInvoiceRequest(BaseModel):
    notes: Optional[str] = None
