import re

xml_path = 'odoo_addon/restaurant_core/views/report_invoice.xml'
with open(xml_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Helper function to remove duplicate inner dyn_font inside tbody
# Pattern 1:
# <t t-set="dyn_font" t-value="'5.8px' if line_count &gt; 25 else '6.6px' if line_count &gt; 18 else '7.5px' if line_count &gt; 12 else '8.2px' if line_count &gt; 6 else '9px'"/>
# <t t-set="dyn_pad" t-value="'1px 3px' if line_count &gt; 25 else '1.8px 4px' if line_count &gt; 18 else '2.5px 5px' if line_count &gt; 12 else '3.5px 6px' if line_count &gt; 6 else '5px 8px'"/>

pattern_inner_vars = re.compile(
    r'\s*<t t-set="dyn_font" t-value="\'5\.8px\'.*?/>\s*<t t-set="dyn_pad" t-value="\'1px 3px\'.*?/>',
    re.DOTALL
)

removed_count = len(pattern_inner_vars.findall(content))
content = pattern_inner_vars.sub('', content)
print(f"Removed {removed_count} duplicate inner dyn_font/dyn_pad blocks.")

# Helper function to remove any standalone inner dyn_font
pattern_single_inner = re.compile(
    r'\s*<t t-set="dyn_font" t-value="\'5\.8px\'.*?/>',
    re.DOTALL
)
content = pattern_single_inner.sub('', content)

# 1. Update dynamic variables at the top of templates
# Standard full set of dynamic scaling variables
def make_dyn_vars(line_count_expr):
    return f"""                <t t-set="line_count" t-value="{line_count_expr}"/>
                <t t-set="dyn_font" t-value="'8.5px' if line_count &gt; 25 else '9.5px' if line_count &gt; 18 else '10px' if line_count &gt; 10 else '11px' if line_count &gt; 4 else '11.5px'"/>
                <t t-set="dyn_pad" t-value="'3px 6px' if line_count &gt; 25 else '4.5px 7px' if line_count &gt; 18 else '6.5px 9px' if line_count &gt; 10 else '9px 12px' if line_count &gt; 4 else '12px 14px'"/>
                <t t-set="dyn_line_height" t-value="'1.35' if line_count &gt; 25 else '1.4' if line_count &gt; 18 else '1.45' if line_count &gt; 10 else '1.5' if line_count &gt; 4 else '1.55'"/>
                <t t-set="sec_gap" t-value="'6px' if line_count &gt; 25 else '8px' if line_count &gt; 18 else '12px' if line_count &gt; 10 else '17px' if line_count &gt; 4 else '22px'"/>
                <t t-set="tot_font" t-value="'9px' if line_count &gt; 25 else '9.5px' if line_count &gt; 18 else '10.5px' if line_count &gt; 10 else '11px' if line_count &gt; 4 else '11.5px'"/>
                <t t-set="tot_pad" t-value="'3.5px 6px' if line_count &gt; 25 else '4.5px 7px' if line_count &gt; 18 else '6px 8px' if line_count &gt; 10 else '7px 9px' if line_count &gt; 4 else '8px 10px'"/>
                <t t-set="tot_ttc_font" t-value="'10.5px' if line_count &gt; 25 else '11px' if line_count &gt; 18 else '12px' if line_count &gt; 10 else '12.5px' if line_count &gt; 4 else '13px'"/>"""

# Replace in report_grand_marche_template
gm_vars_old = re.compile(r'<t t-set="line_count" t-value="len\(o\.line_ids\) if o\.line_ids else 1"/>\s*<t t-set="dyn_font".*?<t t-set="sec_gap".*?/>', re.DOTALL)
content = gm_vars_old.sub(make_dyn_vars('len(o.line_ids) if o.line_ids else 1'), content)

# Replace in report_marche_dgi_template
content = re.sub(
    r'<t t-set="line_count" t-value="len\(o\.line_ids\) if o\.line_ids else 1"/>\s*<t t-set="dyn_font".*?<t t-set="sec_gap".*?/>',
    make_dyn_vars('len(o.line_ids) if o.line_ids else 1'),
    content
)

# Ensure report_daily_invoice_template has these variables
daily_top_old = re.compile(
    r'<t t-set="logo_src" t-value="image_data_uri\(config\.logo\) if \(config and config\.logo\) else \(image_data_uri\(env\.company\.logo\) if env\.company\.logo else False\)"/>\s*(<t t-set="line_count".*?/>)?\s*(<t t-set="dyn_font".*?/>)?\s*(<t t-set="dyn_pad".*?/>)?\s*(<t t-set="dyn_line_height".*?/>)?\s*(<t t-set="sec_gap".*?/>)?\s*<div class="page single-page-invoice"',
    re.DOTALL
)

daily_replacement = f"""<t t-set="logo_src" t-value="image_data_uri(config.logo) if (config and config.logo) else (image_data_uri(env.company.logo) if env.company.logo else False)"/>
{make_dyn_vars('len(o.order_ids) if o.order_ids else 1')}
                <div class="page single-page-invoice" style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #000000; background: #ffffff; padding: 6mm 10mm 4mm 10mm; position: relative; min-height: 250mm; max-height: 254mm; overflow: hidden; box-sizing: border-box; font-size: 10.5px; line-height: 1.45; page-break-inside: avoid; page-break-after: avoid;">"""

content = daily_top_old.sub(daily_replacement, content)

# Ensure report_pos_order_invoice_template has these variables
pos_top_old = re.compile(
    r'<t t-set="resto_website" t-value="\(config\.website if \(config and config\.website\) else False\) or \'www\.restaurant\.com\'"/>\s*<div class="page single-page-invoice"[^>]*>',
    re.DOTALL
)
pos_replacement = f"""<t t-set="resto_website" t-value="(config.website if (config and config.website) else False) or 'www.restaurant.com'"/>
{make_dyn_vars('len(o.lines) if o.lines else 1')}
                <div class="page single-page-invoice" style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #000000; background: #ffffff; padding: 6mm 10mm 4mm 10mm; position: relative; min-height: 250mm; max-height: 254mm; overflow: hidden; box-sizing: border-box; font-size: 10.5px; line-height: 1.45; page-break-inside: avoid; page-break-after: avoid;">"""
content = pos_top_old.sub(pos_replacement, content, count=1)

# Ensure report_account_move_invoice_template has these variables
acc_top_old = re.compile(
    r'<t t-set="resto_website" t-value="\(config\.website if \(config and config\.website\) else False\) or \'www\.restaurant\.com\'"/>\s*<t t-set="line_count".*?<div class="page single-page-invoice"[^>]*>',
    re.DOTALL
)
acc_replacement = f"""<t t-set="resto_website" t-value="(config.website if (config and config.website) else False) or 'www.restaurant.com'"/>
{make_dyn_vars('len(o.invoice_line_ids.filtered(lambda l: not l.display_type)) if o.invoice_line_ids else 1')}
                <div class="page single-page-invoice" style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #000000; background: #ffffff; padding: 6mm 10mm 4mm 10mm; position: relative; min-height: 250mm; max-height: 254mm; overflow: hidden; box-sizing: border-box; font-size: 10.5px; line-height: 1.45; page-break-inside: avoid; page-break-after: avoid;">"""
content = acc_top_old.sub(acc_replacement, content, count=1)

# Replace any old outer div max-height 275mm or 270mm with min-height: 250mm; max-height: 254mm
content = re.sub(
    r'style="font-family: \'Helvetica Neue\', Helvetica, Arial, sans-serif; color: #000000; background: #ffffff; padding: [^"]*max-height: 27[05]mm;[^"]*"',
    r'style="font-family: \'Helvetica Neue\', Helvetica, Arial, sans-serif; color: #000000; background: #ffffff; padding: 6mm 10mm 4mm 10mm; position: relative; min-height: 250mm; max-height: 254mm; overflow: hidden; box-sizing: border-box; font-size: 10.5px; line-height: 1.45; page-break-inside: avoid; page-break-after: avoid;"',
    content
)

with open(xml_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied complete dynamic scaling variables and 250mm min-height!")
