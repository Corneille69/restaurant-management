import xmlrpc.client
import base64

url = 'http://localhost:8070'
db = 'restaurant_odoo'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

print(f"Authenticated UID: {uid}")

# 1. Check if record exists or open via action_open_configuration
config_action = models.execute_kw(db, uid, password, 'restaurant.configuration', 'action_open_configuration', [])
print(f"action_open_configuration returned: res_id={config_action.get('res_id')}")

config_id = config_action.get('res_id')
config_data = models.execute_kw(db, uid, password, 'restaurant.configuration', 'read', [[config_id]], {
    'fields': ['id', 'name', 'subtitle', 'phone', 'email', 'address', 'ifu', 'rccm', 'tax_regime', 'fiscal_division', 'nim', 'tax_rate', 'legal_mention', 'logo']
})

rec = config_data[0]
print(f"Current configuration:")
for k, v in rec.items():
    if k == 'logo':
        print(f" - {k}: {'[Binary present: ' + str(len(v)) + ' chars]' if v else 'None'}")
    else:
        print(f" - {k}: {v}")

# 2. Test saving new values
test_name = "Le Gourmet Royal - Test Save"
test_ifu = "999888777A"
# 1x1 png image
test_logo_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="

print("\nUpdating configuration fields...")
models.execute_kw(db, uid, password, 'restaurant.configuration', 'write', [[config_id], {
    'name': test_name,
    'ifu': test_ifu,
    'logo': test_logo_b64
}])
print("Write successful!")

# 3. Call action_save_and_sync
print("\nCalling action_save_and_sync...")
sync_res = models.execute_kw(db, uid, password, 'restaurant.configuration', 'action_save_and_sync', [[config_id]])
print("action_save_and_sync completed with result:", sync_res.get('tag'))

# 4. Verify res.company was updated
company = models.execute_kw(db, uid, password, 'res.company', 'read', [[1]], {'fields': ['name', 'vat', 'logo']})
c = company[0]
print(f"\nres.company updated:")
print(f" - name: {c['name']} (Matches: {c['name'] == test_name})")
print(f" - vat: {c['vat']} (Matches: {c['vat'] == test_ifu})")
print(f" - logo updated: {bool(c['logo'])}")

# Restore original clean name
models.execute_kw(db, uid, password, 'restaurant.configuration', 'write', [[config_id], {
    'name': "Lemo Daje Restaurant",
    'ifu': "000123456789A",
}])
models.execute_kw(db, uid, password, 'restaurant.configuration', 'action_save_and_sync', [[config_id]])
print("\nRestored name and synced cleanly!")
