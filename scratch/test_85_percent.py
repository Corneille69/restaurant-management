import odoo
from odoo import api, SUPERUSER_ID
from odoo.tools import config
import PyPDF2
import io

config.parse_config(['-d', 'restaurant_odoo', '--db_host', 'db', '-r', 'odoo', '-w', 'odoo'])
registry = odoo.registry('restaurant_odoo')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # Test 1: Standard 2-item invoice
    marches = env['restaurant.grand.marche'].search([], limit=1)
    report_action = env.ref('restaurant_core.action_report_restaurant_grand_marche')
    pdf1, _ = report_action._render_qweb_pdf('restaurant_core.action_report_restaurant_grand_marche', marches.ids)
    r1 = PyPDF2.PdfFileReader(io.BytesIO(pdf1))
    print(f"Test 1 (2 lines): {r1.numPages} page(s), size: {len(pdf1)}")
