import requests
import json

s = requests.Session()
r_login = s.get('http://localhost:8070/web/login')
csrf = ''
for line in r_login.text.splitlines():
    if 'csrf_token' in line and 'value=' in line:
        csrf = line.split('value=')[1].split('"')[1]
        break

post_resp = s.post('http://localhost:8070/web/login', data={'login':'admin', 'password':'admin', 'csrf_token':csrf})
print('Login post status:', post_resp.status_code)

r_backend = s.get('http://localhost:8070/web')
print('Backend status:', r_backend.status_code)
print('Backend final URL:', r_backend.url)

# Read session info
for line in r_backend.text.splitlines():
    if 'odoo.__session_info__' in line:
        start = line.find('{')
        end = line.rfind('}')
        if start != -1 and end != -1:
            try:
                data = json.loads(line[start:end+1])
                print("Session info found:")
                print(" - uid:", data.get('uid'))
                print(" - name:", data.get('name'))
                print(" - home_action_id:", data.get('home_action_id'))
                print(" - is_system:", data.get('is_system'))
            except Exception as e:
                print("JSON parse error:", e)

# Test XML-RPC reading action 414
import xmlrpc.client
models = xmlrpc.client.ServerProxy('http://localhost:8070/xmlrpc/2/object')
act = models.execute_kw('restaurant_odoo', 2, 'admin', 'ir.actions.act_window', 'read', [[414]], {'fields': ['id', 'name', 'res_model', 'view_mode']})
print("Home Action 414 details:", act)
