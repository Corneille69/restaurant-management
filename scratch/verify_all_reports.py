import odoo
from odoo import api, SUPERUSER_ID
from odoo.tools import config
import fitz

config.parse_config(['-d', 'restaurant_odoo', '--db_host', 'db', '-r', 'odoo', '-w', 'odoo'])
registry = odoo.registry('restaurant_odoo')

with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # 1. GM/2026/0016 DGI
    gm = env['restaurant.grand.marche'].search([('name', '=', 'GM/2026/0016')], limit=1)
    rep_dgi = env.ref('restaurant_core.action_report_marche_dgi_invoice')
    pdf_dgi, _ = rep_dgi._render_qweb_pdf(rep_dgi.id, [gm.id])
    doc_dgi = fitz.open(stream=pdf_dgi, filetype="pdf")
    last_b = doc_dgi[0].get_text('blocks')[-1]
    occ = round((last_b[3] / doc_dgi[0].rect.height) * 100, 1)
    print(f"GM DGI Report: Pages = {len(doc_dgi)}, Height occupied = {occ}% ({last_b[3]}/{doc_dgi[0].rect.height})")
    doc_dgi[0].get_pixmap(dpi=150).save("/tmp/final_gm16_dgi.png")

    # 2. GM standard
    rep_gm = env.ref('restaurant_core.action_report_restaurant_grand_marche')
    pdf_gm, _ = rep_gm._render_qweb_pdf(rep_gm.id, [gm.id])
    doc_gm = fitz.open(stream=pdf_gm, filetype="pdf")
    last_bgm = doc_gm[0].get_text('blocks')[-1]
    occ_gm = round((last_bgm[3] / doc_gm[0].rect.height) * 100, 1)
    print(f"GM Standard Report: Pages = {len(doc_gm)}, Height occupied = {occ_gm}%")
    doc_gm[0].get_pixmap(dpi=150).save("/tmp/final_gm16_standard.png")

    # 3. Daily report
    daily = env['restaurant.daily.report'].search([], limit=1)
    if daily:
        rep_daily = env.ref('restaurant_core.action_report_restaurant_daily_invoice')
        pdf_daily, _ = rep_daily._render_qweb_pdf(rep_daily.id, [daily.id])
        doc_daily = fitz.open(stream=pdf_daily, filetype="pdf")
        print(f"Daily Report: Pages = {len(doc_daily)}")

    # 4. Pos order
    pos_order = env['pos.order'].search([], limit=1)
    if pos_order:
        rep_pos = env.ref('restaurant_core.action_report_restaurant_pos_order_invoice')
        pdf_pos, _ = rep_pos._render_qweb_pdf(rep_pos.id, [pos_order.id])
        doc_pos = fitz.open(stream=pdf_pos, filetype="pdf")
        print(f"POS Order Report: Pages = {len(doc_pos)}")

    # 5. Account move
    move = env['account.move'].search([('move_type', '=', 'out_invoice')], limit=1)
    if move:
        rep_move = env.ref('restaurant_core.action_report_restaurant_account_move_invoice')
        pdf_move, _ = rep_move._render_qweb_pdf(rep_move.id, [move.id])
        doc_move = fitz.open(stream=pdf_move, filetype="pdf")
        print(f"Account Move Report: Pages = {len(doc_move)}")
