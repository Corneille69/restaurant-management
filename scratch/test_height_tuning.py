import odoo
from odoo import api, SUPERUSER_ID
from odoo.tools import config
import fitz

config.parse_config(['-d', 'restaurant_odoo', '--db_host', 'db', '-r', 'odoo', '-w', 'odoo'])
registry = odoo.registry('restaurant_odoo')

with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    gm = env['restaurant.grand.marche'].search([('name', '=', 'GM/2026/0016')], limit=1)
    
    view = env.ref('restaurant_core.report_marche_dgi_template')
    orig_arch = view.arch
    
    new_arch = orig_arch.replace(
        "<t t-set=\"dyn_font\" t-value=\"'8px' if line_count &gt; 25 else '8.5px' if line_count &gt; 18 else '9.5px' if line_count &gt; 10 else '11px' if line_count &gt; 4 else '11.5px'\"/>",
        "<t t-set=\"dyn_font\" t-value=\"'8px' if line_count &gt; 25 else '8.5px' if line_count &gt; 18 else '9.5px' if line_count &gt; 10 else '11.5px' if line_count &gt; 4 else '12.5px'\"/>"
    ).replace(
        "<t t-set=\"dyn_pad\" t-value=\"'2.5px 5px' if line_count &gt; 25 else '3.5px 6px' if line_count &gt; 18 else '6px 8px' if line_count &gt; 10 else '10.5px 14px' if line_count &gt; 4 else '15px 16px'\"/>",
        "<t t-set=\"dyn_pad\" t-value=\"'2.5px 5px' if line_count &gt; 25 else '3.5px 6px' if line_count &gt; 18 else '6px 8px' if line_count &gt; 10 else '24px 14px' if line_count &gt; 4 else '32px 16px'\"/>"
    ).replace(
        "<t t-set=\"dyn_line_height\" t-value=\"'1.3' if line_count &gt; 25 else '1.35' if line_count &gt; 18 else '1.4' if line_count &gt; 10 else '1.5' if line_count &gt; 4 else '1.6'\"/>",
        "<t t-set=\"dyn_line_height\" t-value=\"'1.3' if line_count &gt; 25 else '1.35' if line_count &gt; 18 else '1.4' if line_count &gt; 10 else '1.6' if line_count &gt; 4 else '1.7'\"/>"
    ).replace(
        "<t t-set=\"sec_gap\" t-value=\"'4px' if line_count &gt; 25 else '6px' if line_count &gt; 18 else '8px' if line_count &gt; 10 else '16px' if line_count &gt; 4 else '20px'\"/>",
        "<t t-set=\"sec_gap\" t-value=\"'4px' if line_count &gt; 25 else '6px' if line_count &gt; 18 else '8px' if line_count &gt; 10 else '26px' if line_count &gt; 4 else '34px'\"/>"
    ).replace(
        "<t t-set=\"tot_font\" t-value=\"'8.5px' if line_count &gt; 25 else '9px' if line_count &gt; 18 else '9.5px' if line_count &gt; 10 else '11px' if line_count &gt; 4 else '11.5px'\"/>",
        "<t t-set=\"tot_font\" t-value=\"'8.5px' if line_count &gt; 25 else '9px' if line_count &gt; 18 else '9.5px' if line_count &gt; 10 else '11.5px' if line_count &gt; 4 else '12.5px'\"/>"
    ).replace(
        "<t t-set=\"tot_pad\" t-value=\"'3px 5px' if line_count &gt; 25 else '3.5px 6px' if line_count &gt; 18 else '5px 7px' if line_count &gt; 10 else '8px 10px' if line_count &gt; 4 else '10px 12px'\"/>",
        "<t t-set=\"tot_pad\" t-value=\"'3px 5px' if line_count &gt; 25 else '3.5px 6px' if line_count &gt; 18 else '5px 7px' if line_count &gt; 10 else '14px 12px' if line_count &gt; 4 else '18px 14px'\"/>"
    ).replace(
        "<t t-set=\"tot_ttc_font\" t-value=\"'10px' if line_count &gt; 25 else '10.5px' if line_count &gt; 18 else '11px' if line_count &gt; 10 else '13px' if line_count &gt; 4 else '13.5px'\"/>",
        "<t t-set=\"tot_ttc_font\" t-value=\"'10px' if line_count &gt; 25 else '10.5px' if line_count &gt; 18 else '11px' if line_count &gt; 10 else '14px' if line_count &gt; 4 else '15px'\"/>"
    ).replace(
        "padding: 6mm 10mm 4mm 10mm;",
        "padding: 8mm 12mm 6mm 12mm;"
    ).replace(
        "padding-top: 10px; margin-top: 20px; font-size: 8.5px;",
        "padding-top: 16px; margin-top: 60px; font-size: 10px;"
    )
    
    view.write({'arch': new_arch})
    
    rep = env.ref('restaurant_core.action_report_marche_dgi_invoice')
    pdf_bytes, _ = rep._render_qweb_pdf(rep.id, [gm.id])
    
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    print(f"Result with targeted 85% settings: Pages = {len(doc)}")
    blocks = doc[0].get_text('blocks')
    last_block = blocks[-1] if blocks else None
    print("Last block y1:", last_block[3] if last_block else 0, "out of", doc[0].rect.height)
    print("Percentage occupied:", round((last_block[3] / doc[0].rect.height) * 100, 1), "%")
    
    page = doc[0]
    pix = page.get_pixmap(dpi=150)
    pix.save("/tmp/gm16_85_preview.png")
    print("Saved /tmp/gm16_85_preview.png")
    
    cr.rollback()
