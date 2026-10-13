import odoo
from odoo import api, SUPERUSER_ID
from odoo.tools import config
import PyPDF2
import io

config.parse_config(['-d', 'restaurant_odoo', '--db_host', 'db', '-r', 'odoo', '-w', 'odoo'])
registry = odoo.registry('restaurant_odoo')

with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # 1. Test Grand Marche with 2 lines
    gm_model = env['restaurant.grand.marche']
    gm_2 = gm_model.search([], limit=1)
    if gm_2:
        report_action = env.ref('restaurant_core.action_report_restaurant_grand_marche')
        pdf_bytes, _ = report_action._render_qweb_pdf('restaurant_core.action_report_restaurant_grand_marche', gm_2.ids)
        r = PyPDF2.PdfFileReader(io.BytesIO(pdf_bytes))
        print(f"[GRAND MARCHE 2 LINES] Pages: {r.numPages}, Size: {len(pdf_bytes)} bytes")
        with open('/tmp/test_gm_2.pdf', 'wb') as f:
            f.write(pdf_bytes)

    # 2. Test Marche DGI
    if gm_2:
        report_action_dgi = env.ref('restaurant_core.action_report_marche_dgi_invoice')
        pdf_bytes_dgi, _ = report_action_dgi._render_qweb_pdf('restaurant_core.action_report_marche_dgi_invoice', gm_2.ids)
        r_dgi = PyPDF2.PdfFileReader(io.BytesIO(pdf_bytes_dgi))
        print(f"[MARCHE DGI 2 LINES] Pages: {r_dgi.numPages}, Size: {len(pdf_bytes_dgi)} bytes")
        with open('/tmp/test_dgi_2.pdf', 'wb') as f:
            f.write(pdf_bytes_dgi)

    # 3. Test Grand Marche with 12 lines
    gm_temp = gm_model.create({
        'partner_name': 'Entreprise Test 12 Lignes',
        'partner_address': 'Cotonou, Bénin',
        'partner_phone': '+229 97 00 00 00',
        'partner_ifu': '1234567890123',
        'is_certified_dgi': True,
        'dgi_reference': 'DGI-TEST-12L-2026',
        'dgi_security_code': 'SEC-CODE-TEST-12-LINES-CERTIFIED-DGI-OK',
        'tax_rate': '18',
        'subject': 'Prestation et Fourniture Restauration',
    })
    for i in range(12):
        env['restaurant.grand.marche.line'].create({
            'marche_id': gm_temp.id,
            'name': f'Article de Restauration Délicieux #{i+1}',
            'quantity': 2 + (i % 3),
            'price_unit': 3500 + (i * 250),
        })
    pdf_bytes_12, _ = report_action._render_qweb_pdf('restaurant_core.action_report_restaurant_grand_marche', gm_temp.ids)
    r_12 = PyPDF2.PdfFileReader(io.BytesIO(pdf_bytes_12))
    print(f"[GRAND MARCHE 12 LINES] Pages: {r_12.numPages}, Size: {len(pdf_bytes_12)} bytes")
    with open('/tmp/test_gm_12.pdf', 'wb') as f:
        f.write(pdf_bytes_12)

    # 4. Test Grand Marche with 24 lines
    gm_temp24 = gm_model.create({
        'partner_name': 'Entreprise Test 24 Lignes',
        'partner_address': 'Cotonou, Bénin',
        'partner_phone': '+229 97 00 00 00',
        'partner_ifu': '1234567890123',
        'is_certified_dgi': True,
        'dgi_reference': 'DGI-TEST-24L-2026',
        'dgi_security_code': 'SEC-CODE-TEST-24-LINES-CERTIFIED-DGI-OK',
        'tax_rate': '18',
        'subject': 'Prestation et Fourniture Restauration',
    })
    for i in range(24):
        env['restaurant.grand.marche.line'].create({
            'marche_id': gm_temp24.id,
            'name': f'Plat Spécialité Gastronomique #{i+1}',
            'quantity': 1 + (i % 2),
            'price_unit': 4200 + (i * 150),
        })
    pdf_bytes_24, _ = report_action._render_qweb_pdf('restaurant_core.action_report_restaurant_grand_marche', gm_temp24.ids)
    r_24 = PyPDF2.PdfFileReader(io.BytesIO(pdf_bytes_24))
    print(f"[GRAND MARCHE 24 LINES] Pages: {r_24.numPages}, Size: {len(pdf_bytes_24)} bytes")
    with open('/tmp/test_gm_24.pdf', 'wb') as f:
        f.write(pdf_bytes_24)

    # Rollback to avoid cluttering db
    cr.rollback()
