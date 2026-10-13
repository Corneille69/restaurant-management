import re

path = r"c:\Users\840 G5\Contacts\Bureau\restaurant-management\odoo_addon\restaurant_core\views\report_invoice.xml"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Dynamic variables tuned so 7 lines (and other line counts) take ~85% of page height
dyn_vars_replacement = """                <t t-set="line_count" t-value="len(o.line_ids) if o.line_ids else 1"/>
                <t t-set="dyn_font" t-value="'8.5px' if line_count &gt; 25 else '9.5px' if line_count &gt; 18 else '10.5px' if line_count &gt; 10 else '11px' if line_count &gt; 4 else '11.5px'"/>
                <t t-set="dyn_pad" t-value="'3.5px 6px' if line_count &gt; 25 else '5px 8px' if line_count &gt; 18 else '8px 10px' if line_count &gt; 10 else '12px 14px' if line_count &gt; 4 else '15px 16px'"/>
                <t t-set="dyn_line_height" t-value="'1.35' if line_count &gt; 25 else '1.4' if line_count &gt; 18 else '1.48' if line_count &gt; 10 else '1.55' if line_count &gt; 4 else '1.6'"/>
                <t t-set="sec_gap" t-value="'6px' if line_count &gt; 25 else '8px' if line_count &gt; 18 else '12px' if line_count &gt; 10 else '18px' if line_count &gt; 4 else '22px'"/>
                <t t-set="tot_font" t-value="'9px' if line_count &gt; 25 else '9.5px' if line_count &gt; 18 else '10.5px' if line_count &gt; 10 else '11px' if line_count &gt; 4 else '11.5px'"/>
                <t t-set="tot_pad" t-value="'4px 6px' if line_count &gt; 25 else '5px 7px' if line_count &gt; 18 else '7px 9px' if line_count &gt; 10 else '9px 12px' if line_count &gt; 4 else '11px 14px'"/>
                <t t-set="tot_ttc_font" t-value="'10.5px' if line_count &gt; 25 else '11px' if line_count &gt; 18 else '12px' if line_count &gt; 10 else '13px' if line_count &gt; 4 else '13.5px'"/>"""

# Replace in report_marche_dgi_template and report_grand_marche_template
pat_dyn = r'<t t-set="line_count" t-value="len\(o\.line_ids\) if o\.line_ids else 1"/>.*?<t t-set="tot_ttc_font" t-value="[^"]*"/>'
content = re.sub(pat_dyn, dyn_vars_replacement, content, flags=re.DOTALL)

# Let's also adjust the spacing between Totaux and Footer: margin-top: 22px; padding-top: 10px;
content = content.replace('border-top: 1.5px solid #000000; padding-top: 8px; margin-top: 14px;',
                          'border-top: 1.5px solid #000000; padding-top: 10px; margin-top: 22px;')

# Let's adjust padding of the Homologation box so it feels comfortable
content = content.replace('padding: 6px 8px; font-size: 9px; color: #14532d; line-height: 1.4;',
                          'padding: 8px 10px; font-size: 9.5px; color: #14532d; line-height: 1.45;')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated spacing in report_invoice.xml successfully!")
