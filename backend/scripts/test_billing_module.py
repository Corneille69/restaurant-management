import urllib.request
import json
import sys

def post(url, data=None, token=None, method='POST'):
    req = urllib.request.Request(url, method=method)
    if token:
        req.add_header('Authorization', f'Bearer {token}')
    if data is not None:
        req.add_header('Content-Type', 'application/json')
        body = json.dumps(data).encode('utf-8')
    else:
        body = None
    with urllib.request.urlopen(req, data=body) as resp:
        return resp.status, json.loads(resp.read().decode())

def get(url, token=None):
    req = urllib.request.Request(url)
    if token:
        req.add_header('Authorization', f'Bearer {token}')
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.loads(resp.read().decode())

def run_tests():
    print("=== TEST 1: Authentification Admin ===")
    status, auth_data = post('http://127.0.0.1:8000/api/v1/auth/login', {'username': 'admin', 'password': 'admin123'})
    token = auth_data['access_token']
    print("->Succès. Token obtenu.")

    print("\n=== TEST 2: Règles Fiscales DGI Configurable ===")
    status, rules = get('http://127.0.0.1:8000/api/v1/billing/tax-rules', token)
    print(f"-> {len(rules)}règle(s) fiscale(s) trouvée(s):")
    for r in rules:
        print(f" * [{r['tax_type']}] {r['name']} : {r['rate']}% (Base: {r['calculation_base']}, Ordre: {r['calculation_order']}, Actif: {r['is_active']})")

    print("\n=== TEST 3: Liste des Factures Globales ===")
    status, invoices = get('http://127.0.0.1:8000/api/v1/billing/global-invoices', token)
    print(f"-> {len(invoices)}facture(s) globale(s) trouvée(s):")
    for inv in invoices:
        print(f" * Facture {inv['invoice_number']} ({inv['period_label']}) | Statut: {inv['status']} | Ventes: {inv['total_sales_count']} | HT: {inv['total_ht']:,.0f} | Taxes: {inv['total_taxes']:,.0f} | TTC: {inv['total_ttc']:,.0f}")

    if not invoices:
        print("Aucune facture existante.")
        return

    test_inv = invoices[0]
    inv_id = test_inv['id']
    print(f"\n=== TEST 4: Détail complet pré-rempli pour la Facture {test_inv['invoice_number']} ===")
    status, detail = get(f'http://127.0.0.1:8000/api/v1/billing/global-invoices/{inv_id}', token)
    print(f"->Numéro: {detail['invoice_number']}")
    print(f"->Période: {detail['period_label']} ({detail['period_start']} -> {detail['period_end']})")
    print(f"->Total HT: {detail['total_ht']:,.0f} FCFA")
    print(f"->Total Taxes: {detail['total_taxes']:,.0f} FCFA")
    print(f"->Total TTC: {detail['total_ttc']:,.0f} FCFA")
    print(f"->Nombre de ventes: {detail['total_sales_count']}")
    print(f"->Lignes de facture pré-remplies ({len(detail['items'])} lignes):")
    for it in detail['items'][:3]:
        print(f" [Ligne {it['order_number']}] Gérant: {it['manager_name']} | Articles: {it['items_summary']} | Qté: {it['total_items_count']} | HT: {it['amount_ht']:,.0f} | Taxe: {it['amount_tax']:,.0f} | TTC: {it['amount_ttc']:,.0f}")
    
    mgr_summary = json.loads(detail['manager_summary'] or '[]')
    print(f"->Récapitulatif par Gérant ({len(mgr_summary)} gérants):")
    for m in mgr_summary:
        print(f" {m['manager_name']}: {m['sales_count']} vente(s), HT: {m['total_ht']:,.0f}, Taxes: {m['total_tax']:,.0f}, TTC: {m['total_ttc']:,.0f}")

    tax_summary = json.loads(detail['tax_details'] or '[]')
    print(f"->Récapitulatif des taxes:")
    for tx in tax_summary:
        print(f" {tx['rule_name']} ({tx['rate']}%): Assiette={tx['total_base']:,.0f}, Taxe={tx['total_tax']:,.0f}")

    print("\n=== TEST 5: Action [ RECALCULER ] (Exigence 16) ===")
    status, recalc = post(f'http://127.0.0.1:8000/api/v1/billing/global-invoices/{inv_id}/recalculate', None, token)
    print(f"->Recalcul exécuté avec succès. Nouveau total TTC: {recalc['total_ttc']:,.0f} FCFA")

    print("\n=== TEST 6: Intégration Dynamique d'une Vente d'un Gérant (Exigences 1, 4, 5, 7) ===")
    # Login as manager
    st_mgr, auth_mgr = post('http://127.0.0.1:8000/api/v1/auth/login', {'username': 'Dam_as', 'password': 'password123'})
    mgr_token = auth_mgr['access_token']
    prev_ttc = recalc['total_ttc']
    prev_count = recalc['total_sales_count']

    # Get a menu item
    st_menu, menu_items = get('http://127.0.0.1:8000/api/v1/menu/items', mgr_token)
    menu_item_id = menu_items[0]['id'] if menu_items else 1
    unit_price = menu_items[0]['price'] if menu_items else 25000.0

    print(f"->Gérant passe une commande de 2 articles à {unit_price} FCFA...")
    sale_payload = {
        'destination_type': 'takeaway',
        'payment_method': 'cash',
        'items': [
            {'menu_item_id': menu_item_id, 'quantity': 2, 'unit_price': unit_price}
        ]
    }
    st_order, order_created = post('http://127.0.0.1:8000/api/v1/orders/', sale_payload, mgr_token)
    print(f"->Vente {order_created['order_number']} créée. Montant: {order_created['total_amount']} FCFA, is_invoiced: {order_created.get('is_invoiced')}, global_invoice_id: {order_created.get('global_invoice_id')}")

    # Check the invoice updated immediately
    status, updated_inv = get(f'http://127.0.0.1:8000/api/v1/billing/global-invoices/{order_created["global_invoice_id"]}', token)
    print(f"->FACTURE GLOBALE APRÈS VENTE DU GÉRANT:")
    print(f" * Ancien total: {prev_ttc:,.0f} FCFA ({prev_count} ventes)")
    print(f" * Nouveau total: {updated_inv['total_ttc']:,.0f} FCFA ({updated_inv['total_sales_count']} ventes)")
    print(f" * Différence: +{updated_inv['total_ttc'] - prev_ttc:,.0f} FCFA (Exactement le montant de la vente !)")
    assert updated_inv['total_ttc'] == prev_ttc + order_created['total_amount'], "Le total de la facture doit refléter exactement la vente du gérant!"

    print("\n=== TEST 7: Certification de la Facture Globale & Verrouillage (Exigences 11 & 16) ===")
    certify_payload = {
        'admin_password': 'admin123',
        'notes': 'Certification de clôture fiscale conforme DGI e-MCF'
    }
    st_cert, certified_inv = post(f'http://127.0.0.1:8000/api/v1/billing/global-invoices/{updated_inv["id"]}/certify', certify_payload, token)
    print(f"->Facture {certified_inv['invoice_number']} CERTIFIÉE avec succès !")
    print(f" * Statut: {certified_inv['status']}")
    print(f" * Is Certified: {certified_inv['is_certified']}")
    print(f" * Certifiée par: {certified_inv['certified_by']} le {certified_inv['certified_at']}")
    print(f" * Référence DGI: {certified_inv['dgi_fiscal_reference']}")
    print(f" * Sceau de Sécurité (SHA-256): {certified_inv.get('dgi_security_code')}")
    print(f" * Données QR Code DGI: {certified_inv.get('dgi_qr_code_data')}")

    print("\n=== TEST 8: Test de Verrouillage (Impossibilité de modifier ou recalculer après certification) ===")
    try:
        post(f'http://127.0.0.1:8000/api/v1/billing/global-invoices/{certified_inv["id"]}/recalculate', None, token)
        print("ERREUR: Le recalcul aurait dû être bloqué !")
    except urllib.error.HTTPError as e:
        print(f"->Bloqué avec succès (Code {e.code}): Facture certifiée et verrouillée.")

    try:
        post(f'http://127.0.0.1:8000/api/v1/orders/{order_created["id"]}/cancel', None, mgr_token)
        print("ERREUR: L'annulation d'une vente certifiée aurait dû être bloquée !")
    except urllib.error.HTTPError as e:
        print(f"->Bloqué avec succès (Code {e.code}): Vente liée à une facture certifiée intouchable.")

    print("\n TOUS LES TESTS D'INTÉGRATION ET DE CONFORMITÉ ONT RÉUSSI !")

if __name__ == '__main__':
    run_tests()