import odoo
from odoo import api, SUPERUSER_ID
from odoo.tools import config
import fitz # PyMuPDF
import io

config.parse_config(['-d', 'restaurant_odoo', '--db_host', 'db', '-r', 'odoo', '-w', 'odoo'])
registry = odoo.registry('restaurant_odoo')

with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    gm = env['restaurant.grand.marche'].search([('name', '=', 'GM/2026/0016')], limit=1)
    print("Testing GM:", gm.name, "Lines:", len(gm.line_ids), "Certified:", gm.is_certified_dgi)

    # 1. Test DGI report
    rep = env.ref('restaurant_core.action_report_marche_dgi_invoice')
    pdf_bytes, _ = rep._render_qweb_pdf(rep.id, [gm.id])
    
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    print("DGI Report Page count:", len(doc))
    for page_num in range(len(doc)):
        text = doc[page_num].get_text()
        print(f"--- DGI Page {page_num + 1} --- (Length: {len(text)})")
        print(text[:400])
        print("...")
        print(text[-300:])
    
    # Save page 0 as PNG
    page = doc[0]
    pix = page.get_pixmap(dpi=150)
    pix.save("/tmp/gm16_dgi_preview.png")
    with open('/tmp/gm16_dgi.pdf', 'wb') as f:
        f.write(pdf_bytes)
    print("Saved /tmp/gm16_dgi_preview.png and /tmp/gm16_dgi.pdf")

    # 2. Test standard Grand Marche report
    rep2 = env.ref('restaurant_core.action_report_restaurant_grand_marche')
    pdf_bytes2, _ = rep2._render_qweb_pdf(rep2.id, [gm.id])
    doc2 = fitz.open(stream=pdf_bytes2, filetype="pdf")
    print("\nGrand Marche Report Page count:", len(doc2))
    page2 = doc2[0]
    pix2 = page2.get_pixmap(dpi=150)
    pix2.save("/tmp/gm16_main_preview.png")
    print("Saved /tmp/gm16_main_preview.png")
