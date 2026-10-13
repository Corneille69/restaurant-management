import odoo
from odoo import api, SUPERUSER_ID
from odoo.tools import config
import PyPDF2
import io

config.parse_config(['-d', 'restaurant_odoo', '--db_host', 'db', '-r', 'odoo', '-w', 'odoo'])
registry = odoo.registry('restaurant_odoo')

with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    gm = env['restaurant.grand.marche'].search([('name', '=', 'GM/2026/0016')], limit=1)
    if not gm:
        gm = env['restaurant.grand.marche'].search([], limit=1)
    print("Found GM:", gm.name, "Lines:", len(gm.line_ids), "Certified:", gm.is_certified_dgi)

    report_action_dgi = env.ref('restaurant_core.action_report_marche_dgi_invoice')
    pdf_bytes_dgi, _ = report_action_dgi._render_qweb_pdf('restaurant_core.action_report_marche_dgi_invoice', [gm.id])
    
    r = PyPDF2.PdfFileReader(io.BytesIO(pdf_bytes_dgi))
    print(f"Num Pages: {r.numPages}, Size: {len(pdf_bytes_dgi)} bytes")
    
    with open('/tmp/gm16_test.pdf', 'wb') as f:
        f.write(pdf_bytes_dgi)
    print("Saved to /tmp/gm16_test.pdf")
