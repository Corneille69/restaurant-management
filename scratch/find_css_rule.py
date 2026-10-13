import subprocess
import tempfile
import requests
import asyncio
import websockets
import json
import time
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Login as Dam_as
s = requests.Session()
r_login = s.get('http://localhost:8070/web/login')
csrf = [line.split('value=')[1].split('"')[1] for line in r_login.text.splitlines() if 'csrf_token' in line and 'value=' in line][0]
s.post('http://localhost:8070/web/login', data={'login': 'Dam_as', 'password': 'password123', 'csrf_token': csrf})
session_id = s.cookies.get('session_id')

user_data = tempfile.mkdtemp()
proc = subprocess.Popen([
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--disable-gpu',
    '--remote-debugging-port=9226',
    f'--user-data-dir={user_data}',
    '--window-size=1440,900',
    'about:blank'
])

time.sleep(2)

async def send_cmd(ws, msg_id, method, params=None):
    payload = {'id': msg_id, 'method': method}
    if params:
        payload['params'] = params
    await ws.send(json.dumps(payload))
    while True:
        raw = await ws.recv()
        data = json.loads(raw)
        if data.get('id') == msg_id:
            return data

async def check_rules():
    try:
        tabs = requests.get('http://localhost:9226/json').json()
        target_tab = next(t for t in tabs if t.get('type') == 'page')
        ws_url = target_tab['webSocketDebuggerUrl']
        
        async with websockets.connect(ws_url, max_size=100*1024*1024) as ws:
            await send_cmd(ws, 1, 'Network.enable')
            await send_cmd(ws, 2, 'Page.enable')
            await send_cmd(ws, 3, 'Network.setCookie', {
                'name': 'session_id', 'value': session_id, 'domain': 'localhost', 'path': '/'
            })
            await send_cmd(ws, 4, 'Page.navigate', {'url': 'http://localhost:8070/web?db=restaurant_odoo'})
            time.sleep(6)
            
            check_script = """
            (function() {
                var el = Array.from(document.querySelectorAll('.o_menu_sections *')).find(e => (e.innerText || '').includes('Ventes'));
                if (!el) return 'Element not found';
                
                var matched = [];
                for (var sheet of document.styleSheets) {
                    try {
                        for (var rule of sheet.cssRules) {
                            if (rule.selectorText && el.matches(rule.selectorText)) {
                                matched.push({
                                    selector: rule.selectorText,
                                    pointerEvents: rule.style.pointerEvents,
                                    cssText: rule.style.cssText,
                                    href: sheet.href ? sheet.href.split('/').pop() : 'inline'
                                });
                            }
                        }
                    } catch(e) {}
                }
                return JSON.stringify({
                    tag: el.tagName,
                    classes: el.className,
                    attributes: Array.from(el.attributes).map(a => a.name + '=' + a.value),
                    computedPointerEvents: window.getComputedStyle(el).pointerEvents,
                    matchedRules: matched
                });
            })()
            """
            res = await send_cmd(ws, 5, 'Runtime.evaluate', {'expression': check_script})
            val = res.get('result', {}).get('result', {}).get('value')
            print("CSS DIAGNOSTIC RESULT:")
            print(val)
    finally:
        proc.terminate()

asyncio.run(check_rules())
