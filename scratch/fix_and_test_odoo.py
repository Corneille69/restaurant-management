import re
import shutil
import xmlrpc.client
import requests

xml_path = "odoo_addon/restaurant_core/views/report_invoice.xml"
with open(xml_path, "r", encoding="utf-8") as f:
    text = f.read()

# Remove the broken t-set expressions:
# <t t-set="tbl_font_size" ... /> etc.
broken_pattern = re.compile(
    r'<t t-set="tbl_font_size"[^>]*/>\s*<t t-set="tbl_cell_pad"[^>]*/>\s*<t t-set="sec_margin"[^>]*/>',
    re.DOTALL
)
text = broken_pattern.sub('', text)

# Also replace any line_count assignment if any
text = re.sub(r'<t t-set="line_count"[^>]*/>\s*', '', text)

# Let's add CSS inside the header or page style:
style_block = """
<style>
    .single-page-invoice {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #000000;
        background: #ffffff;
        padding: 6mm 10mm 4mm 10mm;
        position: relative;
        max-height: 275mm;
        overflow: hidden;
        box-sizing: border-box;
        font-size: 9.5px;
        page-break-inside: avoid !important;
        page-break-after: avoid !important;
    }
    .inv-table {
        width: 100%;
        border-collapse: collapse;
        border: 1px solid #000000;
        margin-bottom: 0;
    }
    .inv-table th {
        background-color: #000000 !important;
        color: #ffffff !important;
        padding: 5px 8px;
        font-size: 9px;
        font-weight: 900;
        text-transform: uppercase;
        border: 1px solid #000000;
    }
    .inv-table td {
        padding: 4px 8px;
        font-size: 8.5px;
        color: #000000;
        border: 1px solid #000000;
        vertical-align: middle;
    }
    .dense-inv-table th {
        padding: 3px 5px !important;
        font-size: 8px !important;
    }
    .dense-inv-table td {
        padding: 2.5px 5px !important;
        font-size: 7.5px !important;
    }
    .ultra-dense-inv-table th {
        padding: 2px 4px !important;
        font-size: 7px !important;
    }
    .ultra-dense-inv-table td {
        padding: 1.5px 4px !important;
        font-size: 6.8px !important;
    }
</style>
"""

# Ensure style is in templates and replace class="page" with class="page single-page-invoice"
text = text.replace('class="page" style="', 'class="page single-page-invoice" style="')
# Add style_block right after <odoo>
if '.single-page-invoice' not in text:
    text = text.replace('<odoo>', '<odoo>\n' + style_block, 1)

with open(xml_path, "w", encoding="utf-8") as f:
    f.write(text)

# Validate XML
import xml.etree.ElementTree as ET
ET.parse(xml_path)
print("XML validation passed!")

# Copy to docker mount
shutil.copyfile(xml_path, "../ODOO/addons/restaurant_core/views/report_invoice.xml")
print("Copied to docker mount!")

# Upgrade module
DB = "restaurant_odoo"
ADMIN_USER = "admin"
ADMIN_PASS = "admin"
ODOO_URL = "http://localhost:8070"

common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
uid = common.authenticate(DB, ADMIN_USER, ADMIN_PASS, {})
models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")
mod_ids = models.execute_kw(DB, uid, ADMIN_PASS, 'ir.module.module', 'search', [[['name', '=', 'restaurant_core']]])
if mod_ids:
    models.execute_kw(DB, uid, ADMIN_PASS, 'ir.module.module', 'button_immediate_upgrade', [mod_ids])
    print("Module upgraded!")

s = requests.Session()
s.post(f"{ODOO_URL}/web/session/authenticate", json={
    "jsonrpc": "2.0",
    "params": {"db": DB, "login": ADMIN_USER, "password": ADMIN_PASS}
})
marche_ids = models.execute_kw(DB, uid, ADMIN_PASS, 'restaurant.grand.marche', 'search', [[]], {'limit': 1})
if marche_ids:
    pdf_resp = s.get(f"{ODOO_URL}/report/pdf/restaurant_core.report_grand_marche_template/{marche_ids[0]}")
    pages = re.findall(rb'/Type\s*/Page\b', pdf_resp.content)
    print(f"===> GRAND MARCHE PDF RESULT: {len(pages)} PAGE(S) ! (bytes: {len(pdf_resp.content)})")
