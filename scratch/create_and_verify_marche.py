import subprocess
import tempfile
import requests
import asyncio
import websockets
import json
import base64
import time
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ARTIFACT_DIR = r"C:\Users\840 G5\.gemini\antigravity-ide\brain\4448bef7-2f67-4ff5-b4ab-14626ed5976f"

# 1. Login as Dam_as
s = requests.Session()
r_login = s.get('http://localhost:8070/web/login')
csrf = [line.split('value=')[1].split('"')[1] for line in r_login.text.splitlines() if 'csrf_token' in line and 'value=' in line][0]
s.post('http://localhost:8070/web/login', data={'login': 'Dam_as', 'password': 'password123', 'csrf_token': csrf})
session_id = s.cookies.get('session_id')

# 2. Créer une facture Grand Marché par API Odoo pour le gérant Dam_as
create_payload = {
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "model": "restaurant.grand.marche",
        "method": "create",
        "args": [{
            "subject": "Prestation Traiteur & Buffet VIP 150 Personnes - Séminaire International",
            "partner_name": "Ministère du Plan & du Développement",
            "partner_phone": "+229 97 55 44 33",
            "partner_email": "direction.marches@ministere.gouv.bj",
            "partner_address": "Palais des Congrès, Cotonou, Bénin",
            "partner_ifu": "0202611889944",
            "date_invoice": "2026-10-10",
            "date_due": "2026-10-31",
            "payment_method": "transfer",
            "payment_terms": "Virement bancaire sous 30 jours sur facture certifiée",
            "tax_rate": "18",
            "notes": "Prestation complète incluant vaisselle de gala, dressage des tables, service et rafraîchissements continus.",
            "line_ids": [
                (0, 0, {
                    "name": "Buffet Dîner de Gala 150 Personnes (Entrées variées, Plats cuisinés d'exception, Desserts & Fruits exotiques)",
                    "quantity": 150.0,
                    "price_unit": 8500.0,
                    "notes": "Service à table et buffet chaud à volonté"
                }),
                (0, 0, {
                    "name": "Pause-Café & Viennoiseries Matin & Après-Midi (Café pur, Thé, Croissants, Brioches, Jus naturels locaux)",
                    "quantity": 150.0,
                    "price_unit": 3000.0,
                    "notes": "Pause de 10h00 et pause de 15h30"
                }),
                (0, 0, {
                    "name": "Forfait Boissons Prestige & Eaux Minérales (Vins de table, Champagne d'honneur, Sodas & Cocktails de fruits)",
                    "quantity": 1.0,
                    "price_unit": 450000.0,
                    "notes": "Fourniture de 300 bouteilles et rafraîchissements"
                }),
                (0, 0, {
                    "name": "Équipe de Service & Maîtres d'Hôtel Dédiés (Coordination, 8 serveurs qualifiés en tenue de cérémonie)",
                    "quantity": 1.0,
                    "price_unit": 200000.0,
                    "notes": "Présence de 08h00 à 23h00"
                })
            ]
        }],
        "kwargs": {}
    }
}

resp = s.post('http://localhost:8070/web/dataset/call_kw', json=create_payload)
marche_id = resp.json().get('result')
print(f"Grand Marché créé avec succès ! ID = {marche_id}")

# Valider la commande
confirm_payload = {
    "jsonrpc": "2.0",
    "method": "call",
    "params": {
        "model": "restaurant.grand.marche",
        "method": "action_confirm",
        "args": [[marche_id]],
        "kwargs": {}
    }
}
s.post('http://localhost:8070/web/dataset/call_kw', json=confirm_payload)
print("Facture confirmée et validée.")

# Télécharger le PDF de la facture Grand Marché
pdf_resp = s.get(f'http://localhost:8070/report/pdf/restaurant_core.action_report_restaurant_grand_marche/{marche_id}')
pdf_path = os.path.join(ARTIFACT_DIR, f'facture_grand_marche_{marche_id}.pdf')
with open(pdf_path, 'wb') as f:
    f.write(pdf_resp.content)
print(f"PDF Facture Grand Marché généré ({len(pdf_resp.content)} octets) : {pdf_path}")

# Maintenant, ouvrons Chrome pour prendre une capture d'écran du formulaire complet et de la liste
user_data = tempfile.mkdtemp()
proc = subprocess.Popen([
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--disable-gpu',
    '--remote-debugging-port=9230',
    f'--user-data-dir={user_data}',
    '--window-size=1440,1100',
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

async def view_record():
    try:
        tabs = requests.get('http://localhost:9230/json').json()
        target_tab = next(t for t in tabs if t.get('type') == 'page')
        ws_url = target_tab['webSocketDebuggerUrl']
        
        async with websockets.connect(ws_url, max_size=100*1024*1024) as ws:
            await ws.send(json.dumps({'id': 1, 'method': 'Network.enable'}))
            await ws.recv()
            await ws.send(json.dumps({'id': 2, 'method': 'Page.enable'}))
            await ws.recv()
            await ws.send(json.dumps({'id': 3, 'method': 'Network.setCookie', 'params': {'name': 'session_id', 'value': session_id, 'domain': 'localhost', 'path': '/'}}))
            await ws.recv()
            
            # Naviguer directement vers le formulaire de la facture Grand Marché créée
            target_url = f'http://localhost:8070/web?db=restaurant_odoo#id={marche_id}&model=restaurant.grand.marche&view_type=form'
            print("Navigation vers la facture Grand Marché :", target_url)
            await send_cmd(ws, 4, 'Page.navigate', {'url': target_url})
            time.sleep(6)
            
            # Capture formulaire rempli
            snap = await send_cmd(ws, 5, 'Page.captureScreenshot', {'format': 'png'})
            with open(os.path.join(ARTIFACT_DIR, 'grand_marche_completed_form.png'), 'wb') as f:
                f.write(base64.b64decode(snap['result']['data']))
            print("Capture d'écran du Grand Marché complet enregistrée.")
            
            # Naviguer vers la liste
            list_url = 'http://localhost:8070/web?db=restaurant_odoo#action=restaurant_core.action_restaurant_grand_marche'
            await send_cmd(ws, 6, 'Page.navigate', {'url': list_url})
            time.sleep(4)
            
            snap_list = await send_cmd(ws, 7, 'Page.captureScreenshot', {'format': 'png'})
            with open(os.path.join(ARTIFACT_DIR, 'grand_marche_populated_list.png'), 'wb') as f:
                f.write(base64.b64decode(snap_list['result']['data']))
            print("Capture d'écran de la liste des Grands Marchés enregistrée.")
            
    finally:
        proc.terminate()

asyncio.run(view_record())
