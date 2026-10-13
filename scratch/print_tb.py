import requests

ODOO_URL = "http://localhost:8070"
s = requests.Session()
s.post(f"{ODOO_URL}/web/session/authenticate", json={
    "jsonrpc": "2.0",
    "params": {"db": "restaurant_odoo", "login": "admin", "password": "admin"}
})
r = s.get(f"{ODOO_URL}/report/html/restaurant_core.report_grand_marche_template/14")
idx = r.text.find("Traceback")
if idx != -1:
    print(r.text[idx:idx+1500])
else:
    print("No traceback found, output snippet:")
    print(r.text[1000:2500])
