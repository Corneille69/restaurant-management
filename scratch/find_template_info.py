with open('odoo_addon/restaurant_core/views/report_invoice.xml', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'template id=' in line or 'single-page-invoice' in line or 'dyn_font' in line:
        print(f'{i+1}: {line.strip()[:110]}')
