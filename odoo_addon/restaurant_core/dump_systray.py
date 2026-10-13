import subprocess
import tempfile
import requests
import asyncio
import websockets
import json
import base64
import time
import os

user_data = tempfile.mkdtemp()
chrome_proc = subprocess.Popen([
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--disable-gpu',
    '--remote-debugging-port=9222',
    f'--user-data-dir={user_data}',
    '--window-size=1440,900',
    'about:blank'
])

time.sleep(2)

async def run_flow():
    try:
        tabs = requests.get('http://localhost:9222/json').json()
        target = [t for t in tabs if t.get('type') == 'page'][0]
        ws_url = target['webSocketDebuggerUrl']
        
        async with websockets.connect(ws_url, max_size=50*1024*1024) as ws:
            msg_counter = 0
            
            async def call(method, params=None):
                nonlocal msg_counter
                msg_counter += 1
                curr_id = msg_counter
                p = {'id': curr_id, 'method': method}
                if params:
                    p['params'] = params
                await ws.send(json.dumps(p))
                while True:
                    res = json.loads(await asyncio.wait_for(ws.recv(), timeout=15))
                    if res.get('id') == curr_id:
                        return res
            
            await call('Page.enable')
            await call('Runtime.enable')
            
            # 1. Login
            await call('Page.navigate', {'url': 'http://localhost:8070/web/login'})
            await asyncio.sleep(2)
            await call('Runtime.evaluate', {'expression': """
                document.querySelector('input[name="login"]').value = 'admin';
                document.querySelector('input[name="password"]').value = 'admin';
                document.querySelector('form.oe_login_form').submit();
            """})
            await asyncio.sleep(6)
            
            # 2. Inspect Systray OuterHTML
            res_html = await call('Runtime.evaluate', {
                'expression': 'document.querySelector(".o_menu_systray") ? document.querySelector(".o_menu_systray").outerHTML : "NOT_FOUND"'
            })
            html_val = res_html.get('result', {}).get('result', {}).get('value')
            print("Systray HTML:")
            print(html_val)
            
    finally:
        chrome_proc.terminate()

asyncio.run(run_flow())
