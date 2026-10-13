import odoo
from odoo import api, SUPERUSER_ID
from odoo.tools import config
import PyPDF2
import io

config.parse_config(['-d', 'restaurant_odoo', '--db_host', 'db', '-r', 'odoo', '-w', 'odoo'])
registry = odoo.registry('restaurant_odoo')

with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # Test daily report
    daily_model = env['restaurant.daily.report']
    daily = daily_model.search([], limit=1)
    if daily:
        report_daily = env.ref('restaurant_core.action_report_restaurant_daily_invoice')
        pdf_daily, _ = report_daily._render_qweb_pdf('restaurant_core.action_report_restaurant_daily_invoice', daily.ids)
        r_daily = PyPDF2.PdfFileReader(io.BytesIO(pdf_daily))
        print(f"[DAILY INVOICE REPORT] Pages: {r_daily.numPages}, Size: {len(pdf_daily)} bytes")

    # Test pos order invoice if exists
    pos_model = env['pos.order']
    pos_order = pos_model.search([], limit=1)
    if pos_order:
        report_pos = env.ref('restaurant_core.action_report_restaurant_pos_order_invoice')
        pdf_pos, _ = report_pos._render_qweb_pdf('restaurant_core.action_report_restaurant_pos_order_invoice', pos_order.ids)
        r_pos = PyPDF2.PdfFileReader(io.BytesIO(pdf_pos))
        print(f"[POS ORDER INVOICE REPORT] Pages: {r_pos.numPages}, Size: {len(pdf_pos)} bytes")
