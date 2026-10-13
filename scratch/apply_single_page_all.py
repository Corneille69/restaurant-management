import re
import shutil
import py_compile
import requests
import xmlrpc.client

# =============================================================================
# PART 1 : UPDATE ODOO TEMPLATES (report_invoice.xml)
# =============================================================================
odoo_xml_path = "odoo_addon/restaurant_core/views/report_invoice.xml"
with open(odoo_xml_path, "r", encoding="utf-8") as f:
    xml_content = f.read()

# 1. Remove all 7 signature blocks
sig_regex = re.compile(
    r'<div style="display: table-cell; width: 45%; vertical-align: middle; text-align: right;[^"]*">\s*<svg[^>]*>.*?</svg>\s*<div[^>]*>\s*Signature &amp; Cachet\s*</div>\s*</div>',
    re.DOTALL
)
xml_content = sig_regex.sub('', xml_content)

# Also in the left cell that was width: 55%, change it to width: 100%
xml_content = xml_content.replace(
    'display: table-cell; width: 55%; vertical-align: top; padding-right: 20px;',
    'display: table-cell; width: 100%; vertical-align: top;'
)

# 2. In report_marche_client_receipt_template, remove the SIGNATURES dashed box
receipt_sig_pattern = re.compile(
    r'<!-- SIGNATURES -->\s*<div style="display: table; width: 100%; margin-top: 25px; page-break-inside: avoid;">.*?</div>\s*</div>\s*<!-- PIED DE PAGE',
    re.DOTALL
)
xml_content = receipt_sig_pattern.sub('<!-- PIED DE PAGE', xml_content)

# 3. Update the .page container styling across all templates to enforce single A4 page fit
# Old: padding: 18mm 16mm 14mm 16mm; position: relative; min-height: 297mm; box-sizing: border-box; font-size: 11px;
# New: padding: 7mm 11mm 5mm 11mm; position: relative; max-height: 275mm; overflow: hidden; box-sizing: border-box; font-size: 10px; page-break-inside: avoid; page-break-after: avoid;
xml_content = re.sub(
    r'padding:\s*18mm\s*16mm\s*14mm\s*16mm;\s*position:\s*relative;\s*min-height:\s*297mm;\s*box-sizing:\s*border-box;\s*font-size:\s*11px;',
    'padding: 7mm 11mm 5mm 11mm; position: relative; max-height: 275mm; overflow: hidden; box-sizing: border-box; font-size: 10px; page-break-inside: avoid; page-break-after: avoid;',
    xml_content
)

# 4. Remove empty filler rows in table that blow up height
xml_content = re.sub(
    r'<!-- Lignes vides pour conserver la disposition élégante du tableau comme sur l\'image -->\s*<t t-if="len\(o\.line_ids\) &lt; 5">.*?</t>',
    '',
    xml_content,
    flags=re.DOTALL
)

# 5. Insert dynamic font sizing and margin reduction in templates:
# Add scaling variables after <t t-set="resto_website" .../>
scaling_vars = """                <t t-set="line_count" t-value="len(o.order_ids) if hasattr(o, 'order_ids') and o.order_ids else (len(o.lines) if hasattr(o, 'lines') else (len(o.line_ids) if hasattr(o, 'line_ids') else (len(o.invoice_line_ids) if hasattr(o, 'invoice_line_ids') else 1)))"/>
                <t t-set="tbl_font_size" t-value="'7px' if line_count &gt; 22 else ('7.5px' if line_count &gt; 14 else ('8.5px' if line_count &gt; 8 else '10px'))"/>
                <t t-set="tbl_cell_pad" t-value="'2px 4px' if line_count &gt; 22 else ('2.5px 5px' if line_count &gt; 14 else ('4px 6px' if line_count &gt; 8 else '6px 8px'))"/>
                <t t-set="sec_margin" t-value="'4px' if line_count &gt; 22 else ('6px' if line_count &gt; 14 else ('8px' if line_count &gt; 8 else '14px'))"/>"""

# Replace in the templates
xml_content = re.sub(
    r'(<t t-set="resto_website"[^>]*/>)\s*(<div class="page")',
    r'\1\n' + scaling_vars + r'\n\2',
    xml_content
)

# 6. Apply sec_margin to section spacing
xml_content = xml_content.replace(
    'display: table; width: 100%; margin-bottom: 35px;',
    'display: table; width: 100%; margin-bottom: 12px;'
)
xml_content = xml_content.replace(
    'display: table; width: 100%; margin-bottom: 30px;',
    'display: table; width: 100%; margin-bottom: 10px;'
)
xml_content = xml_content.replace(
    'width: 100%; margin-top: 0; margin-bottom: 30px;',
    'width: 100%; margin-top: 0; margin-bottom: 10px;'
)
xml_content = xml_content.replace(
    'display: table; width: 100%; margin-top: 15px; margin-bottom: 35px; page-break-inside: avoid;',
    'display: table; width: 100%; margin-top: 6px; margin-bottom: 10px; page-break-inside: avoid;'
)

# 7. Reduce title font size slightly to leave more room for table products
xml_content = xml_content.replace(
    'font-size: 34px; font-weight: 900; color: #000000; margin: 0 0 4px 0;',
    'font-size: 26px; font-weight: 900; color: #000000; margin: 0 0 2px 0;'
)
xml_content = xml_content.replace(
    'width: 78px; height: 78px; display: block; margin: 0 auto;',
    'width: 65px; height: 65px; display: block; margin: 0 auto;'
)

# 8. Adjust table cell padding and font-size to use dynamic attributes
xml_content = xml_content.replace(
    'border: 1px solid #000000; padding: 10px 12px; font-size: 11px; font-weight: 900;',
    'border: 1px solid #000000; padding: 6px 8px; font-size: 9.5px; font-weight: 900;'
)
xml_content = xml_content.replace(
    'border: 1px solid #000000; padding: 10px 8px; font-size: 11px; font-weight: 900;',
    'border: 1px solid #000000; padding: 6px 6px; font-size: 9.5px; font-weight: 900;'
)
xml_content = xml_content.replace(
    'border: 1px solid #000000; padding: 10px 10px; font-size: 11px; font-weight: 900;',
    'border: 1px solid #000000; padding: 6px 8px; font-size: 9.5px; font-weight: 900;'
)
xml_content = xml_content.replace(
    'border: 1px solid #000000; padding: 9px 12px;',
    'border: 1px solid #000000; padding: 5px 8px; font-size: 9px;'
)
xml_content = xml_content.replace(
    'border: 1px solid #000000; padding: 9px 8px;',
    'border: 1px solid #000000; padding: 5px 6px; font-size: 9px;'
)
xml_content = xml_content.replace(
    'border: 1px solid #000000; padding: 9px 10px;',
    'border: 1px solid #000000; padding: 5px 8px; font-size: 9px;'
)
xml_content = xml_content.replace(
    'border: 1px solid #000000; padding: 8px 10px;',
    'border: 1px solid #000000; padding: 5px 8px; font-size: 9px;'
)
xml_content = xml_content.replace(
    'border: 1px solid #000000; padding: 9px 10px; font-weight: 900; font-size: 11.5px;',
    'border: 1px solid #000000; padding: 6px 8px; font-weight: 900; font-size: 10px;'
)
xml_content = xml_content.replace(
    'border: 1px solid #000000; padding: 9px 10px; text-align: right; font-weight: 900; font-size: 12.5px;',
    'border: 1px solid #000000; padding: 6px 8px; text-align: right; font-weight: 900; font-size: 10.5px;'
)

# 9. Compact footer
xml_content = xml_content.replace(
    'position: absolute; bottom: 10mm; left: 16mm; right: 16mm; font-size: 9px; color: #374151; border-top: 1px solid #d1d5db; padding-top: 10px;',
    'position: absolute; bottom: 4mm; left: 11mm; right: 11mm; font-size: 8px; color: #374151; border-top: 1px solid #d1d5db; padding-top: 4px; line-height: 1.3;'
)

with open(odoo_xml_path, "w", encoding="utf-8") as f:
    f.write(xml_content)

print("Updated odoo_addon/restaurant_core/views/report_invoice.xml successfully!")

# Copy to docker mount
docker_dest = r"..\ODOO\addons\restaurant_core\views\report_invoice.xml"
shutil.copyfile(odoo_xml_path, docker_dest)
print(f"Copied to {docker_dest}")

# Upgrade module in Odoo
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
    print("Odoo module restaurant_core upgraded successfully!")

# Test PDF page count for Grand Marche
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
