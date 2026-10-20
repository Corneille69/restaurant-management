import urllib.request
import json

def post(url, data=None, token=None):
    req = urllib.request.Request(url, method='POST')
    if token:
        req.add_header('Authorization', f'Bearer {token}')
    if data:
        req.add_header('Content-Type', 'application/json')
        body = json.dumps(data).encode('utf-8')
    else:
        body = None
    with urllib.request.urlopen(req, data=body) as resp:
        return json.loads(resp.read().decode())

def get(url, token=None):
    req = urllib.request.Request(url)
    if token:
        req.add_header('Authorization', f'Bearer {token}')
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

# 1. Admin login
admin_tok = post('http://127.0.0.1:8000/api/v1/auth/login', {'username': 'admin', 'password': 'admin123'})['access_token']

# 2. Get current active invoice
live = get('http://127.0.0.1:8000/api/v1/billing/live-status', admin_tok)
inv_id = live.get('current_invoice_id')
inv_before = get(f'http://127.0.0.1:8000/api/v1/billing/global-invoices/{inv_id}', admin_tok)

print('=== 1. ÉTAT FACTURE ADMIN AVANT LA VENTE ===')
print(f"Facture N°: {inv_before['invoice_number']}")
print(f"Statut: {inv_before['status']}")
print(f"Nombre de ventes: {inv_before['total_sales_count']}")
print(f"Total HT: {inv_before['total_ht']:,.0f} FCFA")
print(f"Total Taxes (TVA 18%): {inv_before['total_taxes']:,.0f} FCFA")
print(f"Total TTC: {inv_before['total_ttc']:,.0f} FCFA")

# 3. Manager logs in and makes a sale
mgr_tok = post('http://127.0.0.1:8000/api/v1/auth/login', {'username': 'Dam_as', 'password': 'password123'})['access_token']
menu_items = get('http://127.0.0.1:8000/api/v1/menu/items', mgr_tok)
item = menu_items[0]

sale_amount = 100000.0
sale_data = {
    'payment_method': 'Espèces (Cash)',
    'items': [{'menu_item_id': item['id'], 'quantity': 1, 'custom_price': sale_amount}]
}
print(f"\n=== 2. LE GÉRANT 'Dam_as' ENCAISSE UNE VENTE DE {sale_amount:,.0f} FCFA ===")
order = post('http://127.0.0.1:8000/api/v1/orders/', sale_data, mgr_tok)
print(f"->Vente #{order['order_number']} validée par le Gérant à la caisse.")
print(f"->Montant: {order['total_amount']:,.0f} FCFA")
print(f"->Rattachée à la facture globale ID: {order['global_invoice_id']}")

# 4. Check admin invoice immediately
inv_id_used = order['global_invoice_id']
inv_after = get(f'http://127.0.0.1:8000/api/v1/billing/global-invoices/{inv_id_used}', admin_tok)
print('\n=== 3. ÉTAT FACTURE ADMIN IMMÉDIATEMENT APRÈS (SANS AUCUNE ACTION MANUELLE) ===')
print(f"Facture N°: {inv_after['invoice_number']}")
print(f"Nombre de ventes: {inv_after['total_sales_count']}")
print(f"Total HT: {inv_after['total_ht']:,.0f} FCFA (Calculé automatiquement selon TVA DGI 18%)")
print(f"Total Taxes: {inv_after['total_taxes']:,.0f} FCFA (Calculé automatiquement)")
print(f"Total TTC: {inv_after['total_ttc']:,.0f} FCFA")

# Find the item line
matching_lines = [it for it in inv_after['items'] if it['order_number'] == order['order_number']]
if matching_lines:
    new_line = matching_lines[0]
    print(f"\n=== 4. LIGNE PRÉ-REMPLIE AUTOMATIQUEMENT DANS LE TABLEAU ADMIN ===")
    print(f"• Vente: #{new_line['order_number']}")
    print(f"• Gérant: {new_line['manager_name']} ({new_line['manager_login']})")
    print(f"• Articles: {new_line['items_summary']}")
    print(f"• Quantité: {new_line['total_items_count']}")
    print(f"• Montant HT: {new_line['amount_ht']:,.0f} FCFA")
    print(f"• Taxe TVA DGI: {new_line['amount_tax']:,.0f} FCFA")
    print(f"• Total TTC: {new_line['amount_ttc']:,.0f} FCFA")

# Manager summary
mgr_summary = json.loads(inv_after['manager_summary'] or '[]')
print(f"\n=== 5. RÉCAPITULATIF PAR GÉRANT MIS À JOUR AUTOMATIQUEMENT ===")
for m in mgr_summary:
    print(f" {m['manager_name']}: {m['sales_count']} vente(s) | HT: {m['total_ht']:,.0f} FCFA | Taxes: {m['total_tax']:,.0f} FCFA | TTC: {m['total_ttc']:,.0f} FCFA")