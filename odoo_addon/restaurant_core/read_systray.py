import asyncio
import websockets
import json
import requests

async def get_html():
    try:
        tabs = requests.get('http://localhost:9222/json').json()
    except Exception as e:
        print("Chrome not running:", e)
        return
    ws_url = [t for t in tabs if t.get('type') == 'page'][0]['webSocketDebuggerUrl']
    async with websockets.connect(ws_url) as ws:
        expr = 'document.querySelector(".o_menu_systray") ? document.querySelector(".o_menu_systray").outerHTML : "NOT_FOUND"'
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr}}))
        while True:
            res = json.loads(await ws.recv())
            if res.get('id') == 1:
                val = res.get('result', {}).get('result', {}).get('value')
                print("Systray HTML:")
                print(val)
                break

asyncio.run(get_html())
