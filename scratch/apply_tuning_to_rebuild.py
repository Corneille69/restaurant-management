with open('scratch/rebuild_complete_report_xml.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace dyn definitions
old_dyn = """                <t t-set="dyn_font" t-value="'8px' if line_count &gt; 25 else '8.5px' if line_count &gt; 18 else '9.5px' if line_count &gt; 10 else '10.5px' if line_count &gt; 4 else '11px'"/>
                <t t-set="dyn_pad" t-value="'2.5px 5px' if line_count &gt; 25 else '3.5px 6px' if line_count &gt; 18 else '5px 8px' if line_count &gt; 10 else '8px 12px' if line_count &gt; 4 else '11px 14px'"/>
                <t t-set="dyn_line_height" t-value="'1.3' if line_count &gt; 25 else '1.35' if line_count &gt; 18 else '1.4' if line_count &gt; 10 else '1.48' if line_count &gt; 4 else '1.55'"/>
                <t t-set="sec_gap" t-value="'4px' if line_count &gt; 25 else '6px' if line_count &gt; 18 else '8px' if line_count &gt; 10 else '12px' if line_count &gt; 4 else '16px'"/>
                <t t-set="tot_font" t-value="'8.5px' if line_count &gt; 25 else '9px' if line_count &gt; 18 else '9.5px' if line_count &gt; 10 else '10.5px' if line_count &gt; 4 else '11px'"/>
                <t t-set="tot_pad" t-value="'3px 5px' if line_count &gt; 25 else '3.5px 6px' if line_count &gt; 18 else '5px 7px' if line_count &gt; 10 else '6.5px 9px' if line_count &gt; 4 else '8px 10px'"/>
                <t t-set="tot_ttc_font" t-value="'10px' if line_count &gt; 25 else '10.5px' if line_count &gt; 18 else '11px' if line_count &gt; 10 else '12px' if line_count &gt; 4 else '13px'"/>"""

old_dyn_marche = """                <t t-set="dyn_font" t-value="'8px' if line_count &gt; 25 else '8.5px' if line_count &gt; 18 else '9.5px' if line_count &gt; 10 else '11px' if line_count &gt; 4 else '11.5px'"/>
                <t t-set="dyn_pad" t-value="'2.5px 5px' if line_count &gt; 25 else '3.5px 6px' if line_count &gt; 18 else '6px 8px' if line_count &gt; 10 else '10.5px 14px' if line_count &gt; 4 else '15px 16px'"/>
                <t t-set="dyn_line_height" t-value="'1.3' if line_count &gt; 25 else '1.35' if line_count &gt; 18 else '1.4' if line_count &gt; 10 else '1.5' if line_count &gt; 4 else '1.6'"/>
                <t t-set="sec_gap" t-value="'4px' if line_count &gt; 25 else '6px' if line_count &gt; 18 else '8px' if line_count &gt; 10 else '16px' if line_count &gt; 4 else '20px'"/>
                <t t-set="tot_font" t-value="'8.5px' if line_count &gt; 25 else '9px' if line_count &gt; 18 else '9.5px' if line_count &gt; 10 else '11px' if line_count &gt; 4 else '11.5px'"/>
                <t t-set="tot_pad" t-value="'3px 5px' if line_count &gt; 25 else '3.5px 6px' if line_count &gt; 18 else '5px 7px' if line_count &gt; 10 else '8px 10px' if line_count &gt; 4 else '10px 12px'"/>
                <t t-set="tot_ttc_font" t-value="'10px' if line_count &gt; 25 else '10.5px' if line_count &gt; 18 else '11px' if line_count &gt; 10 else '13px' if line_count &gt; 4 else '13.5px'"/>"""

new_dyn = """                <t t-set="dyn_font" t-value="'8px' if line_count &gt; 25 else '8.5px' if line_count &gt; 18 else '9.5px' if line_count &gt; 10 else '11.5px' if line_count &gt; 4 else '12.5px'"/>
                <t t-set="dyn_pad" t-value="'2.5px 5px' if line_count &gt; 25 else '3.5px 6px' if line_count &gt; 18 else '6px 8px' if line_count &gt; 10 else '24px 14px' if line_count &gt; 4 else '32px 16px'"/>
                <t t-set="dyn_line_height" t-value="'1.3' if line_count &gt; 25 else '1.35' if line_count &gt; 18 else '1.4' if line_count &gt; 10 else '1.6' if line_count &gt; 4 else '1.7'"/>
                <t t-set="sec_gap" t-value="'4px' if line_count &gt; 25 else '6px' if line_count &gt; 18 else '8px' if line_count &gt; 10 else '26px' if line_count &gt; 4 else '34px'"/>
                <t t-set="tot_font" t-value="'8.5px' if line_count &gt; 25 else '9px' if line_count &gt; 18 else '9.5px' if line_count &gt; 10 else '11.5px' if line_count &gt; 4 else '12.5px'"/>
                <t t-set="tot_pad" t-value="'3px 5px' if line_count &gt; 25 else '3.5px 6px' if line_count &gt; 18 else '5px 7px' if line_count &gt; 10 else '14px 12px' if line_count &gt; 4 else '18px 14px'"/>
                <t t-set="tot_ttc_font" t-value="'10px' if line_count &gt; 25 else '10.5px' if line_count &gt; 18 else '11px' if line_count &gt; 10 else '14px' if line_count &gt; 4 else '15px'"/>"""

content = content.replace(old_dyn, new_dyn)
content = content.replace(old_dyn_marche, new_dyn)

# Container padding
content = content.replace(
    "padding: 6mm 10mm 4mm 10mm;",
    "padding: 8mm 12mm 6mm 12mm;"
)

# Footers
content = content.replace(
    'style="border-top: 1.5px solid #000000; padding-top: 8px; margin-top: 14px; font-size: 8.5px; color: #374151; line-height: 1.45;"',
    't-attf-style="border-top: 1.5px solid #000000; padding-top: 14px; margin-top: #{\'10px\' if line_count &gt; 25 else \'16px\' if line_count &gt; 18 else \'26px\' if line_count &gt; 10 else \'55px\'}; font-size: #{\'8px\' if line_count &gt; 25 else \'8.5px\' if line_count &gt; 18 else \'9.5px\' if line_count &gt; 10 else \'10px\'}; color: #374151; line-height: 1.45;"'
)
content = content.replace(
    'style="border-top: 1.5px solid #000000; padding-top: 10px; margin-top: 20px; font-size: 8.5px; color: #374151; line-height: 1.45;"',
    't-attf-style="border-top: 1.5px solid #000000; padding-top: 14px; margin-top: #{\'10px\' if line_count &gt; 25 else \'16px\' if line_count &gt; 18 else \'26px\' if line_count &gt; 10 else \'55px\'}; font-size: #{\'8px\' if line_count &gt; 25 else \'8.5px\' if line_count &gt; 18 else \'9.5px\' if line_count &gt; 10 else \'10px\'}; color: #374151; line-height: 1.45;"'
)
content = content.replace(
    'style="border-top: 1.5px solid #064e3b; padding-top: 8px; margin-top: 14px; text-align: center; font-size: 8.5px; color: #475569; line-height: 1.45;"',
    't-attf-style="border-top: 1.5px solid #064e3b; padding-top: 14px; margin-top: #{\'10px\' if line_count &gt; 25 else \'16px\' if line_count &gt; 18 else \'26px\' if line_count &gt; 10 else \'55px\'}; text-align: center; font-size: #{\'8px\' if line_count &gt; 25 else \'8.5px\' if line_count &gt; 18 else \'9.5px\' if line_count &gt; 10 else \'10px\'}; color: #475569; line-height: 1.45;"'
)

with open('scratch/rebuild_complete_report_xml.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated scratch/rebuild_complete_report_xml.py successfully")
