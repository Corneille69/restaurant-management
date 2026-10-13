import re

path = 'odoo_addon/restaurant_core/views/report_invoice.xml'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

def repl(match):
    prefix = match.group(1)
    field_attr = match.group(2)
    return f'{prefix}><span {field_attr}/></td>'

new_content = re.sub(r'(<td\b[^>]*?)\s+(t-field="[^"]+")\s*/>', repl, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated successfully!")
