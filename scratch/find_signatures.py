import re

for filepath in [
    'odoo_addon/restaurant_core/views/report_invoice.xml',
    'backend/app/web/router.py'
]:
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    print(f"\n--- {filepath} ---")
    for i, line in enumerate(lines):
        if any(w in line.lower() for w in ['signature', 'cachet', '<svg']):
            print(f"Line {i+1}: {line.strip()[:100]}")
