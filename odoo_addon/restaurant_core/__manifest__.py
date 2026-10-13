{
    "name": "Restaurant Engine Connector",
    "version": "1.0",
    "category": "Point of Sale",
    "summary": "Module restaurant personnalisé connecté au backend FastAPI (Moteur & Patron)",
    "description": """
        Module Odoo Restaurant personnalisé :
        - Élargit pos.order, product.template et restaurant.table avec un identifiant de synchronisation externe.
        - Prêt pour la collaboration en temps réel avec le backend FastAPI.
        - Zéro données de démo, structure propre et extensible.
    """,
    "author": "Corneille / Restaurant Management",
    "depends": [
        "base",
        "mail",
        "point_of_sale",
        "pos_restaurant",
        "stock",
        "account"
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/pos_order_rules.xml",
        "data/categories_data.xml",
        "views/pos_order_views.xml",
        "views/product_views.xml",
        "views/manager_views.xml",
        "views/report_invoice.xml",
        "views/webclient_templates.xml"
    ],
    "assets": {
        "web.assets_frontend": [
            "restaurant_core/static/src/css/odoo_login_style.css",
        ],
        "web.assets_backend": [
            "restaurant_core/static/src/css/odoo_backend_sidebar.css",
            "restaurant_core/static/src/css/composer_voice_send.css",
            "restaurant_core/static/src/js/disable_odoobot.js",
            "restaurant_core/static/src/js/restaurant_navbar.js",
            "restaurant_core/static/src/js/composer_voice_send_patch.js",
            "restaurant_core/static/src/xml/composer_voice_send_patch.xml",
        ],
        "web.assets_web": [
            "restaurant_core/static/src/css/odoo_backend_sidebar.css",
            "restaurant_core/static/src/css/composer_voice_send.css",
            "restaurant_core/static/src/js/disable_odoobot.js",
            "restaurant_core/static/src/js/restaurant_navbar.js",
            "restaurant_core/static/src/js/composer_voice_send_patch.js",
            "restaurant_core/static/src/xml/composer_voice_send_patch.xml",
        ],
        "point_of_sale._assets_pos": [
            "restaurant_core/static/src/xml/payment_status_override.xml",
            "restaurant_core/static/src/css/pos_custom_style.css",
            "restaurant_core/static/src/js/pos_auto_sales_screen.js",
            "restaurant_core/static/src/js/pos_custom_enhancements.js",
        ],
    },
    "installable": True,
    "application": True,
    "license": "LGPL-3"
}
