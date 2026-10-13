import odoo
from odoo import api, SUPERUSER_ID
from odoo.tools import config

config.parse_config(['-d', 'restaurant_odoo', '--db_host', 'db', '-r', 'odoo', '-w', 'odoo'])
registry = odoo.registry('restaurant_odoo')

with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    report_action_dgi = env.ref('restaurant_core.action_report_marche_dgi_invoice')
    with open('/tmp/gm_render.html', 'r', encoding='utf-8') as f:
        html = f.read()
    html_with_article = html.replace('class="page single-page-invoice"', 'class="article page single-page-invoice"')
    bodies, res_ids, header, footer, specific_paperformat_args = report_action_dgi._prepare_html(html_with_article)
    print("Number of bodies with article:", len(bodies))
    print("Body starts with:")
    print(bodies[0][:400])
    with open('/tmp/body_article.html', 'w', encoding='utf-8') as f:
        f.write(bodies[0])
