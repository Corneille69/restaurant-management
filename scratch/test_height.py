import odoo
from odoo import api, SUPERUSER_ID
from odoo.tools import config
import subprocess
import PyPDF2
import io
import re

config.parse_config(['-d', 'restaurant_odoo', '--db_host', 'db', '-r', 'odoo', '-w', 'odoo'])
registry = odoo.registry('restaurant_odoo')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    marches = env['restaurant.grand.marche'].search([], limit=1)
    report_action = env.ref('restaurant_core.action_report_restaurant_grand_marche')
    html_bytes, _ = report_action._render_qweb_html('restaurant_core.action_report_restaurant_grand_marche', marches.ids)
    html_str = html_bytes.decode('utf-8')
    
    # Let's test with min-height: 248mm on single-page-invoice
    modified_html = html_str.replace('max-height: 275mm;', 'min-height: 248mm; max-height: 255mm;')
    with open('/tmp/test_stretch.html', 'w', encoding='utf-8') as f:
        f.write(modified_html)
        
    cmd = ['/usr/local/bin/wkhtmltopdf', '--page-size', 'A4', '--margin-top', '2', '--margin-bottom', '2', '--margin-left', '4', '--margin-right', '4', '/tmp/test_stretch.html', '/tmp/test_stretch.pdf']
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    reader = PyPDF2.PdfFileReader('/tmp/test_stretch.pdf')
    print("Modified HTML pages:", reader.numPages)
