import subprocess
import tempfile
import requests
import asyncio
import websockets
import json
import base64
import time

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

async def inspect_systray():
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
            
            # Login
            await call('Page.navigate', {'url': 'http://localhost:8070/web/login'})
            await asyncio.sleep(2)
            await call('Runtime.evaluate', {'expression': """
                document.querySelector('input[name="login"]').value = 'admin';
                document.querySelector('input[name="password"]').value = 'admin';
                document.querySelector('form.oe_login_form').submit();
            """})
            await asyncio.sleep(6)
            
            # Inspect systray items
            script = """
            (() => {
                const systray = document.querySelector('.o_menu_systray');
                if (!systray) return 'NO_SYSTRAY';
                const items = Array.from(systray.children).map(c => ({
                    tag: c.tagName,
                    className: c.className,
                    innerHTML: c.innerHTML.trim()
                }));
                return items;
            })()
            """
            res = await call('Runtime.evaluate', {'expression': script, 'returnByValue': True})
            print("Systray items:")
            import pprint
            pprint.pprint(res.get('result', {}).get('value'))
            
            # Click on that chat icon to see what dropdown opens!
            click_script = """
            (() => {
                const badge = document.querySelector('.o-mail-MessagingMenu-counter') || document.querySelector('.o_menu_systray i.fa-comments, .o_menu_systray .fa-comment');
                const btn = badge ? badge.closest('button, a, div') : null;
                if (btn) {
                    btn.click();
                    return "CLICKED_MSG_BUTTON";
                }
                const first = document.querySelector('.o_menu_systray > *');
                if (first) {
                    first.click();
                    return "CLICKED_FIRST";
                }
                return "NOT_FOUND";
            })()
            """
            res_click = await call('Runtime.evaluate', {'expression': click_script})
            print("Click chat icon:", res_click.get('result', {}).get('value'))
            await asyncio.sleep(2)
            
            # Read opened menu contents
            menu_script = """
            (() => {
                const menu = document.querySelector('.o-mail-MessagingMenu') || document.querySelector('.dropdown-menu.show');
                if (!menu) return 'NO_OPENED_MENU';
                return menu.innerText;
            })()
            """
            res_menu = await call('Runtime.evaluate', {'expression': menu_script, 'returnByValue': True})
            print("Opened menu text:")
            print(res_menu.get('result', {}).get('value'))
            
    finally:
        chrome_proc.terminate()

asyncio.run(inspect_systray())
