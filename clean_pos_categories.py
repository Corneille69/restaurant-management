import subprocess

cmd = """
import odoo
from odoo.tools import config
config['db_host'] = 'db'
config['db_user'] = 'odoo'
config['db_password'] = 'odoo'
from odoo.modules.registry import Registry
from odoo import api, SUPERUSER_ID

reg = Registry('restaurant_odoo')
with reg.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    # Rename Cat 5 to "Desserts"
    c5 = env['pos.category'].browse(5)
    if c5.exists():
        c5.write({'name': 'Desserts'})
    # Remove Cat 6 (test) and Cat 4 (duplicate)
    c6 = env['pos.category'].browse(6)
    if c6.exists():
        c6.unlink()
    c4 = env['pos.category'].browse(4)
    if c4.exists():
        # check if any products reference c4
        prods = env['product.template'].search([('restaurant_category_id', '=', 4)])
        if prods:
            prods.write({'restaurant_category_id': 5})
        c4.unlink()
    cr.commit()
    print("Categories cleaned up!")
    for c in env['pos.category'].search([]):
        print(f" - {c.id}: {c.name}")
"""

subprocess.run(["docker", "exec", "odoo-odoo-1", "python3", "-c", cmd])
