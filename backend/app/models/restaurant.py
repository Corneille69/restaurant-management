import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class RestaurantTable(Base):
    __tablename__ = "restaurant_tables"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False) # Ex: Table 1, Terrasse 3
    capacity = Column(Integer, default=4)
    status = Column(String(20), default="available") # available, occupied, reserved
    odoo_table_id = Column(Integer, nullable=True, index=True) # ID dans Odoo (restaurant.table)

    orders = relationship("Order", back_populates="table")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    odoo_category_id = Column(Integer, nullable=True, index=True) # ID dans Odoo (pos.category)

    menu_items = relationship("MenuItem", back_populates="category")


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    odoo_product_id = Column(Integer, nullable=True, index=True) # ID dans Odoo (product.product)
    odoo_template_id = Column(Integer, nullable=True) # ID dans Odoo (product.template)

    category = relationship("Category", back_populates="menu_items")
    order_items = relationship("OrderItem", back_populates="menu_item")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    table_id = Column(Integer, ForeignKey("restaurant_tables.id"), nullable=True)
    status = Column(String(30), default="pending") # pending, preparing, served, paid, cancelled
    total_amount = Column(Float, default=0.0)

    # Synchronisation Odoo & Données Gérant
    odoo_pos_order_id = Column(Integer, nullable=True, index=True) # ID dans Odoo (pos.order)
    odoo_sync_status = Column(String(20), default="pending") # synced, pending, error
    odoo_sync_error = Column(Text, nullable=True)
    manager_name = Column(String(100), nullable=True) # Nom du gérant qui a encaissé
    manager_login = Column(String(50), nullable=True) # Identifiant (login) du gérant
    session_name = Column(String(50), nullable=True) # Réf de la session de caisse
    payment_method = Column(String(100), default="Espèces (Cash)") # Mode de paiement utilisé
    tendered_amount = Column(Float, nullable=True) # Montant versé / reçu par le gérant
    change_amount = Column(Float, nullable=True) # Monnaie rendue au client
    work_session_id = Column(Integer, ForeignKey("manager_work_sessions.id"), nullable=True) # Prise de service rattachée

    # Certification DGI de la commande
    is_certified_dgi = Column(Boolean, default=False)
    dgi_invoice_number = Column(String(100), nullable=True)
    dgi_signature = Column(String(255), nullable=True)
    dgi_certified_at = Column(DateTime, nullable=True)

    # Rattachement Facturation Globale Admin
    global_invoice_id = Column(Integer, ForeignKey("global_invoices.id"), nullable=True, index=True)
    is_invoiced = Column(Boolean, default=False, index=True)
    invoiced_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    table = relationship("RestaurantTable", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    global_invoice = relationship("GlobalInvoice", back_populates="orders")


class DailyInvoice(Base):
    __tablename__ = "daily_invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_date = Column(Date, unique=True, index=True, nullable=False) # Date de la journée (YYYY-MM-DD)
    invoice_number = Column(String(100), unique=True, nullable=False) # Ex: FACT-GEN-20261007-001
    total_ttc = Column(Float, default=0.0) # Total TTC en FCFA
    total_ht = Column(Float, default=0.0) # Total Hors Taxes (HT)
    total_tva = Column(Float, default=0.0) # TVA 18% norme DGI
    total_orders = Column(Integer, default=0) # Nombre de commandes dans la journée

    # Ventilations détaillées (JSON)
    payment_breakdown = Column(Text, nullable=True) # Détail par mode de paiement
    manager_breakdown = Column(Text, nullable=True) # Détail par gérant (nom, login, ventes)

    # Certification DGI officielle
    is_certified_dgi = Column(Boolean, default=False)
    dgi_nif = Column(String(50), default="000123456789A") # NIF officiel du restaurant
    dgi_nim = Column(String(50), default="RESTO-DGI-MCF-01") # NIM (e-MCF)
    dgi_reference = Column(String(100), nullable=True) # Réf Fiscale DGI (ex: DGI-FNE-20261007-A4B7)
    dgi_security_code = Column(String(255), nullable=True) # Hash SHA-256 de certification
    dgi_qr_code_data = Column(Text, nullable=True) # Données pour QR code fiscal
    dgi_certified_at = Column(DateTime, nullable=True) # Horodatage certification
    certified_by = Column(String(100), default="Administrateur")

    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class PosSession(Base):
    __tablename__ = "pos_sessions"

    id = Column(Integer, primary_key=True, index=True)
    odoo_session_id = Column(Integer, unique=True, index=True, nullable=False)
    session_name = Column(String(50), nullable=False) # Ex: POS/00001
    manager_name = Column(String(100), nullable=True) # Nom du gérant
    manager_login = Column(String(50), nullable=True) # Login du gérant
    start_at = Column(DateTime, nullable=True)
    stop_at = Column(DateTime, nullable=True)
    state = Column(String(20), default="opened") # opened, closed
    total_sales = Column(Float, default=0.0)
    cash_difference = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)



class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    notes = Column(String(255), nullable=True)

    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem", back_populates="order_items")

    @property
    def item_name(self) -> str:
        return self.menu_item.name if self.menu_item else f"Plat #{self.menu_item_id}"


class ManagerWorkSession(Base):
    __tablename__ = "manager_work_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    manager_name = Column(String(100), nullable=False)
    manager_login = Column(String(50), nullable=False, index=True)
    login_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False) # Date et heure de connexion
    logout_at = Column(DateTime, nullable=True) # Date et heure de déconnexion
    is_online = Column(Boolean, default=True, index=True) # Actuellement en service
    total_sales_amount = Column(Float, default=0.0) # Ventes totales de la session (argent encaissé)
    total_orders_count = Column(Integer, default=0) # Nombre de commandes
    total_tendered_amount = Column(Float, default=0.0) # Argent liquide/paiements reçus
    total_change_amount = Column(Float, default=0.0) # Monnaie rendue aux clients
    last_activity_at = Column(DateTime, default=datetime.datetime.utcnow)

    orders = relationship("Order", backref="work_session")


class ManagerActivityLog(Base):
    __tablename__ = "manager_activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    manager_name = Column(String(100), nullable=False)
    manager_login = Column(String(50), nullable=False, index=True)
    action_type = Column(String(50), nullable=False, index=True) # LOGIN, LOGOUT, ORDER_SALE, PRICE_CHANGE, SESSION_CLOSE
    description = Column(Text, nullable=False) # Faits et gestes détaillés
    order_number = Column(String(50), nullable=True, index=True)
    amount = Column(Float, nullable=True) # Montant en jeu
    payment_method = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)


class RestaurantConfig(Base):
    __tablename__ = "restaurant_config"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_name = Column(String(150), default="Lemo Daje Restaurant")
    restaurant_subtitle = Column(String(150), default="Restaurant & Grill Gastronomique")
    logo_url = Column(Text, nullable=True) # URL ou Data URL base64

    # Informations Fiscales Obligatoires DGI (e-MCF)
    ifu = Column(String(50), default="000123456789A") # IFU officiel (Identifiant Fiscal Unique)
    nif = Column(String(50), default="000123456789A") # NIF officiel (compatibilité)
    nim = Column(String(50), default="RESTO-DGI-MCF-01") # NIM (e-MCF)
    rccm = Column(String(100), default="BF-OUA-01-2024-B12-00456") # Registre du commerce
    fiscal_division = Column(String(150), default="DGI - Division Fiscale des Moyennes Entreprises") # Division Fiscale DGI
    tax_center = Column(String(150), default="DGI - Division Fiscale des Moyennes Entreprises") # Centre des impôts
    tax_rate = Column(Float, default=18.0) # Taux TVA standard 18%
    legal_mention = Column(Text, default="Facture normalisée certifiée conforme aux exigences de la DGI")

    # Configuration Facturation Globale & DGI
    billing_frequency = Column(String(20), default="daily") # daily, weekly, monthly
    menu_prices_include_tax = Column(Boolean, default=True) # True si les prix de vente au menu sont TTC
    default_tax_regime = Column(String(100), default="Régime du Réel Normal d'Imposition (RNI)") # Régime fiscal par défaut
    dgi_qr_enabled = Column(Boolean, default=True) # Toujours afficher le code QR d'approbation DGI en haut de la facture

    # Coordonnées Établissement
    address = Column(String(255), default="Avenue Kwame Nkrumah, Ouagadougou")
    phone = Column(String(100), default="+226 25 30 00 00 / +226 70 00 00 00")
    email = Column(String(150), default="contact@lemodaje.com")
    website = Column(String(150), default="www.lemodaje.com")

    # Style visuel
    primary_color = Column(String(30), default="#7d6b5c")
    bg_color = Column(String(30), default="#f8f5f0")

    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)



class TaxRule(Base):
    """
    Règles fiscales DGI configurables pour le calcul automatique des taxes.
    Permet de définir types, taux, base, conditions, période d'application et régimes.
    """
    __tablename__ = "tax_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False) # Ex: "TVA 18% (Norme DGI)", "Prélèvement Spécifique 5%"
    tax_type = Column(String(50), default="VAT") # VAT, SPECIFIC, WITHHOLDING, EXCISE
    rate = Column(Float, nullable=False, default=18.0) # Taux en % (ex: 18.0)
    calculation_base = Column(String(20), default="HT") # "HT" ou "TTC"
    calculation_order = Column(Integer, default=1) # Ordre d'application dans la formule (1, 2, 3...)
    tax_regime = Column(String(50), default="TOUS") # "TOUS", "REEL_NORMAL", "RSI", "SIMPLIFIE"
    rounding_mode = Column(String(30), default="round_2_decimals") # "round_2_decimals", "round_integer", "ceil", "floor"
    application_condition = Column(String(50), default="always") # "always", "threshold_min"
    min_threshold = Column(Float, default=0.0) # Montant seuil si application_condition = "threshold_min"
    valid_from = Column(Date, nullable=True) # Période d'application début
    valid_to = Column(Date, nullable=True) # Période d'application fin
    is_active = Column(Boolean, default=True, index=True) # Active / Inactive
    description = Column(Text, nullable=True) # Notes ou références fiscales DGI
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class GlobalInvoice(Base):
    """
    Facture Globale de l'Administrateur :
    Regroupe et agrège dynamiquement les ventes de tous les gérants pour une période donnée.
    Recalculée automatiquement à chaque vente.
    Verrouillée définitivement après certification par l'Admin.
    """
    __tablename__ = "global_invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String(100), unique=True, index=True, nullable=False) # Ex: FACT-GLOB-20261008-001
    period_type = Column(String(30), default="daily", index=True) # "daily", "weekly", "monthly", "custom"
    period_start = Column(DateTime, nullable=False, index=True)
    period_end = Column(DateTime, nullable=False, index=True)
    period_label = Column(String(150), nullable=False) # Ex: "Journée du 08/10/2026", "Semaine 41 (05/10 - 11/10/2026)"
    
    status = Column(String(30), default="in_progress", index=True) # "draft", "in_progress", "ready_for_certification", "certified", "cancelled"
    
    total_sales_count = Column(Integer, default=0) # Nombre de ventes intégrées
    total_ht = Column(Float, default=0.0) # Somme Hors Taxes (HT) en FCFA
    total_taxes = Column(Float, default=0.0) # Somme des taxes DGI en FCFA
    total_ttc = Column(Float, default=0.0) # Somme Toutes Taxes Comprises (TTC) en FCFA

    # Gérant associé à la session / facture
    manager_name = Column(String(100), nullable=True, index=True) # Nom complet du gérant connecté
    manager_login = Column(String(50), nullable=True, index=True) # Identifiant (login) du gérant
    manager_id = Column(Integer, nullable=True, index=True) # ID utilisateur du gérant
    opened_at = Column(DateTime, nullable=True) # Date et heure de connexion / ouverture de service
    
    # Ventilations et agrégats détaillés (JSON formaté)
    tax_details = Column(Text, nullable=True) # Ventilation par règle fiscale appliquée
    manager_summary = Column(Text, nullable=True) # Récapitulatif ventilé par gérant (nom, login, ventes, HT, taxes, TTC)
    payment_summary = Column(Text, nullable=True) # Répartition par mode de règlement
    anomalies = Column(Text, nullable=True) # Liste des anomalies détectées (JSON array)
    has_anomalies = Column(Boolean, default=False)

    # Certification DGI officielle
    is_certified = Column(Boolean, default=False, index=True)
    certified_at = Column(DateTime, nullable=True)
    certified_by = Column(String(100), nullable=True)
    certification_notes = Column(Text, nullable=True)
    
    dgi_nif = Column(String(50), nullable=True)
    dgi_nim = Column(String(50), nullable=True)
    dgi_fiscal_reference = Column(String(100), nullable=True) # Numéro de Facture Normalisée FNE
    dgi_security_code = Column(String(255), nullable=True) # Signature cryptographique SHA-256
    dgi_qr_code_data = Column(Text, nullable=True) # Données pour QR code de contrôle fiscal

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    orders = relationship("Order", back_populates="global_invoice")
    items = relationship("GlobalInvoiceItem", back_populates="global_invoice", cascade="all, delete-orphan", order_by="GlobalInvoiceItem.id.asc()")
    audit_logs = relationship("GlobalInvoiceAuditLog", back_populates="global_invoice", cascade="all, delete-orphan", order_by="GlobalInvoiceAuditLog.id.desc()")


class GlobalInvoiceItem(Base):
    """
    Ligne de Facture Globale :
    Représente chaque vente intégrée dans la facture globale avec tous ses détails pré-remplis.
    """
    __tablename__ = "global_invoice_items"

    id = Column(Integer, primary_key=True, index=True)
    global_invoice_id = Column(Integer, ForeignKey("global_invoices.id", ondelete="CASCADE"), nullable=False, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    
    order_number = Column(String(50), nullable=False)
    order_date = Column(DateTime, nullable=False)
    manager_name = Column(String(100), nullable=True)
    manager_login = Column(String(50), nullable=True)
    payment_method = Column(String(100), default="Espèces (Cash)")
    
    items_summary = Column(Text, nullable=True) # Résumé des produits (ex: "Poulet grillé x2, Eau 1.5L x1")
    total_items_count = Column(Integer, default=0)
    
    unit_price = Column(Float, default=0.0) # Prix unitaire moyen ou de référence
    amount_ht = Column(Float, default=0.0) # Montant Hors Taxes (HT)
    amount_tax = Column(Float, default=0.0) # Montant des taxes calculées
    amount_ttc = Column(Float, default=0.0) # Montant TTC
    tax_details = Column(Text, nullable=True) # JSON détail du calcul fiscal
    
    status = Column(String(30), default="active") # active, cancelled, flagged
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    global_invoice = relationship("GlobalInvoice", back_populates="items")
    order = relationship("Order")


class GlobalInvoiceAuditLog(Base):
    """
    Historique et traçabilité des calculs et modifications de la facture globale.
    Permet à l'Admin de contrôler et justifier chaque montant calculé.
    """
    __tablename__ = "global_invoice_audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    global_invoice_id = Column(Integer, ForeignKey("global_invoices.id", ondelete="CASCADE"), nullable=False, index=True)
    action_type = Column(String(50), nullable=False, index=True) # CREATED, SALE_INTEGRATED, SALE_UPDATED, SALE_CANCELLED, RECALCULATED, CERTIFIED, ANOMALY_DETECTED
    description = Column(Text, nullable=False) # Explication lisible de l'action
    user_name = Column(String(100), default="Système Automatique") # Auteur (gérant, admin ou système)
    details_json = Column(Text, nullable=True) # Snapshot des données / montants
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    global_invoice = relationship("GlobalInvoice", back_populates="audit_logs")



