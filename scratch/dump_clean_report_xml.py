import odoo
from odoo import api, SUPERUSER_ID
from odoo.tools import config
import xml.etree.ElementTree as ET

config.parse_config(['-d', 'restaurant_odoo', '--db_host', 'db', '-r', 'odoo', '-w', 'odoo'])
registry = odoo.registry('restaurant_odoo')

with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    v_wiz = env.ref('restaurant_core.report_invoice_wizard_preview_restaurant')
    v_doc = env.ref('restaurant_core.report_invoice_document_inherit_restaurant')
    
    with open('/tmp/wiz_arch.xml', 'w', encoding='utf-8') as f:
        f.write(v_wiz.arch_db)
    with open('/tmp/doc_arch.xml', 'w', encoding='utf-8') as f:
        f.write(v_doc.arch_db)
        
    print("Wiz len:", len(v_wiz.arch_db), "Doc len:", len(v_doc.arch_db))
