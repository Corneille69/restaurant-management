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
    
    footer_old = 'style="border-top: 1.5px solid #000000; padding-top: 10px; margin-top: 20px; font-size: 8.5px; color: #374151; line-height: 1.45;"'
    footer_new = 't-attf-style="border-top: 1.5px solid #000000; padding-top: 14px; margin-top: #{\'10px\' if line_count &gt; 25 else \'16px\' if line_count &gt; 18 else \'26px\' if line_count &gt; 10 else \'55px\'}; font-size: #{\'8px\' if line_count &gt; 25 else \'8.5px\' if line_count &gt; 18 else \'9.5px\' if line_count &gt; 10 else \'10px\'}; color: #374151; line-height: 1.45;"'
    
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
        footer_old,
        footer_new
    )
    
    view.write({'arch': new_arch})
    rep = env.ref('restaurant_core.action_report_marche_dgi_invoice')

    # Test with 7 lines
    pdf_bytes_7, _ = rep._render_qweb_pdf(rep.id, [gm.id])
    doc_7 = fitz.open(stream=pdf_bytes_7, filetype="pdf")
    print(f"7 lines: Pages = {len(doc_7)}, Occupied = {round((doc_7[0].get_text('blocks')[-1][3] / doc_7[0].rect.height) * 100, 1)}%")

    # Create dummy lines to test 15 lines
    lines_to_add = []
    for i in range(8):
        lines_to_add.append((0, 0, {
            'name': f'Extra Item {i+1}',
            'quantity': 1,
            'price_unit': 1000,
            'price_subtotal': 1000,
        }))
    gm.write({'line_ids': lines_to_add})
    print(f"Total lines now: {len(gm.line_ids)}")
    pdf_bytes_15, _ = rep._render_qweb_pdf(rep.id, [gm.id])
    doc_15 = fitz.open(stream=pdf_bytes_15, filetype="pdf")
    print(f"15 lines: Pages = {len(doc_15)}, Occupied = {round((doc_15[0].get_text('blocks')[-1][3] / doc_15[0].rect.height) * 100, 1)}%")

    cr.rollback()
