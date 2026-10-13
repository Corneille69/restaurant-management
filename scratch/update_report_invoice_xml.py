import re
import os

path = r"c:\Users\840 G5\Contacts\Bureau\restaurant-management\odoo_addon\restaurant_core\views\report_invoice.xml"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

print("Original length:", len(content))

# 1. Update report_marche_dgi_template
# 2. Update report_grand_marche_template
# 3. Update report_daily_invoice_template
# 4. Update report_pos_order_invoice_template
# 5. Update report_account_move_invoice_template

print("Contains report_marche_dgi_template:", "report_marche_dgi_template" in content)
print("Contains report_grand_marche_template:", "report_grand_marche_template" in content)
