with open('scratch/rebuild_complete_report_xml.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''<div t-if="hasattr(o, 'active_manager_name') and o.active_manager_name">Gérant : <span t-esc="o.active_manager_name"/></div>
                                <div t-elif="hasattr(o, 'manager_id') and o.manager_id">Gérant : <span t-esc="o.manager_id.name"/></div>
                                <div t-elif="o.create_uid">Gérant : <span t-esc="o.create_uid.name"/></div>'''

repl = '''<div t-if="o.active_manager_name">Gérant : <span t-esc="o.active_manager_name"/></div>
                                <div t-elif="o.create_uid">Gérant : <span t-esc="o.create_uid.name"/></div>
                                <div t-else="">Gérant : <span t-esc="resto_name"/></div>'''

if target in text:
    text = text.replace(target, repl)
    with open('scratch/rebuild_complete_report_xml.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Replaced successfully!")
else:
    print("Target not found!")
