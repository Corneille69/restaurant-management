import re

filepath = 'odoo_addon/restaurant_core/views/report_invoice.xml'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update report_grand_marche_template
# Replace outer div of report_grand_marche_template to include min-height 250mm
gm_outer_old = '<div class="page single-page-invoice" style="font-family: \'Helvetica Neue\', Helvetica, Arial, sans-serif; color: #000000; background: #ffffff; padding: 7mm 11mm 5mm 11mm; position: relative; max-height: 275mm; overflow: hidden; box-sizing: border-box; font-size: 10px; page-break-inside: avoid; page-break-after: avoid;">'
gm_outer_new = '<div class="page single-page-invoice" style="font-family: \'Helvetica Neue\', Helvetica, Arial, sans-serif; color: #000000; background: #ffffff; padding: 6mm 10mm 4mm 10mm; position: relative; min-height: 250mm; max-height: 254mm; overflow: hidden; box-sizing: border-box; font-size: 10.5px; line-height: 1.45; page-break-inside: avoid; page-break-after: avoid;">'

content = content.replace(gm_outer_old, gm_outer_new)

# Let's define the adaptive variables block for grand marche
gm_vars_old = """                <t t-set="resto_website" t-value="(config.website if (config and config.website) else False) or 'www.restaurant.com'"/>"""

gm_vars_new = """                <t t-set="resto_website" t-value="(config.website if (config and config.website) else False) or 'www.restaurant.com'"/>
                <t t-set="line_count" t-value="len(o.line_ids) if o.line_ids else 1"/>
                <t t-set="dyn_font" t-value="'8.5px' if line_count &gt; 25 else '9.5px' if line_count &gt; 18 else '10.5px' if line_count &gt; 10 else '11px' if line_count &gt; 5 else '11.5px'"/>
                <t t-set="dyn_pad" t-value="'3px 6px' if line_count &gt; 25 else '4.5px 7px' if line_count &gt; 18 else '7px 9px' if line_count &gt; 10 else '9px 11px' if line_count &gt; 5 else '12px 12px'"/>
                <t t-set="dyn_line_height" t-value="'1.35' if line_count &gt; 25 else '1.4' if line_count &gt; 18 else '1.45' if line_count &gt; 10 else '1.5'"/>
                <t t-set="sec_gap" t-value="'6px' if line_count &gt; 25 else '8px' if line_count &gt; 18 else '12px' if line_count &gt; 10 else '16px' if line_count &gt; 5 else '20px'"/>"""

content = content.replace(gm_vars_old, gm_vars_new)

# 2. Update report_marche_dgi_template
mdgi_outer_old = """<template id="report_marche_dgi_template">
        <t t-call="web.html_container">
            <t t-foreach="docs" t-as="o">
                <t t-set="config" t-value="env['restaurant.configuration'].sudo().search([], limit=1)"/>
                <t t-set="resto_name" t-value="(config.name if (config and config.name) else False) or (o.company_id.name if hasattr(o, 'company_id') else env.company.name) or 'RESTAURANT'"/>
                <t t-set="resto_sub" t-value="(config.subtitle if (config and config.subtitle) else False) or ''"/>
                <t t-set="resto_ifu" t-value="(config.ifu if (config and config.ifu) else False) or (o.company_id.vat if hasattr(o, 'company_id') else env.company.vat) or '-'"/>
                <t t-set="resto_rccm" t-value="(config.rccm if (config and config.rccm) else False) or '-'"/>
                <t t-set="resto_regime" t-value="(config.tax_regime if (config and config.tax_regime) else False) or '-'"/>
                <t t-set="resto_nim" t-value="(config.nim if (config and config.nim) else False) or 'RESTO-DGI-MCF-01'"/>
                <t t-set="resto_phone" t-value="(config.phone if (config and config.phone) else False) or (o.company_id.phone if hasattr(o, 'company_id') else env.company.phone) or '-'"/>
                <t t-set="resto_address" t-value="(config.address if (config and config.address) else False) or (o.company_id.street if hasattr(o, 'company_id') else env.company.street) or '-'"/>
                <t t-set="resto_email" t-value="(config.email if (config and config.email) else False) or (o.company_id.email if hasattr(o, 'company_id') else env.company.email) or '-'"/>
                <t t-set="resto_website" t-value="(config.website if (config and config.website) else False) or 'www.restaurant.com'"/>
                <div class="page single-page-invoice" style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #000000; background: #ffffff; padding: 7mm 11mm 5mm 11mm; position: relative; max-height: 275mm; overflow: hidden; box-sizing: border-box; font-size: 10px; page-break-inside: avoid; page-break-after: avoid;">"""

mdgi_outer_new = """<template id="report_marche_dgi_template">
        <t t-call="web.html_container">
            <t t-foreach="docs" t-as="o">
                <t t-set="config" t-value="env['restaurant.configuration'].sudo().search([], limit=1)"/>
                <t t-set="resto_name" t-value="(config.name if (config and config.name) else False) or (o.company_id.name if hasattr(o, 'company_id') else env.company.name) or 'RESTAURANT'"/>
                <t t-set="resto_sub" t-value="(config.subtitle if (config and config.subtitle) else False) or ''"/>
                <t t-set="resto_ifu" t-value="(config.ifu if (config and config.ifu) else False) or (o.company_id.vat if hasattr(o, 'company_id') else env.company.vat) or '-'"/>
                <t t-set="resto_rccm" t-value="(config.rccm if (config and config.rccm) else False) or '-'"/>
                <t t-set="resto_regime" t-value="(config.tax_regime if (config and config.tax_regime) else False) or '-'"/>
                <t t-set="resto_nim" t-value="(config.nim if (config and config.nim) else False) or 'RESTO-DGI-MCF-01'"/>
                <t t-set="resto_phone" t-value="(config.phone if (config and config.phone) else False) or (o.company_id.phone if hasattr(o, 'company_id') else env.company.phone) or '-'"/>
                <t t-set="resto_address" t-value="(config.address if (config and config.address) else False) or (o.company_id.street if hasattr(o, 'company_id') else env.company.street) or '-'"/>
                <t t-set="resto_email" t-value="(config.email if (config and config.email) else False) or (o.company_id.email if hasattr(o, 'company_id') else env.company.email) or '-'"/>
                <t t-set="resto_website" t-value="(config.website if (config and config.website) else False) or 'www.restaurant.com'"/>
                <t t-set="line_count" t-value="len(o.line_ids) if o.line_ids else 1"/>
                <t t-set="dyn_font" t-value="'8.5px' if line_count &gt; 25 else '9.5px' if line_count &gt; 18 else '10.5px' if line_count &gt; 10 else '11px' if line_count &gt; 5 else '11.5px'"/>
                <t t-set="dyn_pad" t-value="'3px 6px' if line_count &gt; 25 else '4.5px 7px' if line_count &gt; 18 else '7px 9px' if line_count &gt; 10 else '9px 11px' if line_count &gt; 5 else '12px 12px'"/>
                <t t-set="dyn_line_height" t-value="'1.35' if line_count &gt; 25 else '1.4' if line_count &gt; 18 else '1.45' if line_count &gt; 10 else '1.5'"/>
                <t t-set="sec_gap" t-value="'6px' if line_count &gt; 25 else '8px' if line_count &gt; 18 else '12px' if line_count &gt; 10 else '16px' if line_count &gt; 5 else '20px'"/>
                <div class="page single-page-invoice" style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #000000; background: #ffffff; padding: 6mm 10mm 4mm 10mm; position: relative; min-height: 250mm; max-height: 254mm; overflow: hidden; box-sizing: border-box; font-size: 10.5px; line-height: 1.45; page-break-inside: avoid; page-break-after: avoid;">"""

content = content.replace(mdgi_outer_old, mdgi_outer_new)

# 3. Update report_daily_invoice_template
daily_outer_old = """<template id="report_daily_invoice_template">
        <t t-call="web.html_container">
            <t t-foreach="docs" t-as="o">
                <t t-set="config" t-value="env['restaurant.configuration'].sudo().search([], limit=1)"/>
                <t t-set="resto_name" t-value="(config.name if (config and config.name) else False) or o.company_name or (o.company_id.name if hasattr(o, 'company_id') else env.company.name) or 'RESTAURANT'"/>
                <t t-set="resto_sub" t-value="(config.subtitle if (config and config.subtitle) else False) or (o.company_subtitle if hasattr(o, 'company_subtitle') else '')"/>
                <t t-set="resto_ifu" t-value="(config.ifu if (config and config.ifu) else False) or o.company_ifu or (o.company_id.vat if hasattr(o, 'company_id') else env.company.vat) or '-'"/>
                <t t-set="resto_rccm" t-value="(config.rccm if (config and config.rccm) else False) or o.company_rccm or '-'"/>
                <t t-set="resto_regime" t-value="(config.tax_regime if (config and config.tax_regime) else False) or o.company_tax_regime or '-'"/>
                <t t-set="resto_division" t-value="(config.fiscal_division if (config and config.fiscal_division) else False) or o.company_fiscal_division or '-'"/>
                <t t-set="resto_phone" t-value="(config.phone if (config and config.phone) else False) or o.company_phone or (o.company_id.phone if hasattr(o, 'company_id') else env.company.phone) or '-'"/>
                <t t-set="resto_address" t-value="(config.address if (config and config.address) else False) or o.company_address or (o.company_id.street if hasattr(o, 'company_id') else env.company.street) or '-'"/>
                <t t-set="resto_email" t-value="(config.email if (config and config.email) else False) or o.company_email or (o.company_id.email if hasattr(o, 'company_id') else env.company.email) or '-'"/>
                <t t-set="resto_website" t-value="(config.website if (config and config.website) else False) or (o.company_website if hasattr(o, 'company_website') else (o.company_id.website if hasattr(o, 'company_id') else env.company.website)) or '-'"/>
                <t t-set="resto_nim" t-value="(config.nim if (config and config.nim) else False) or (o.company_nim if hasattr(o, 'company_nim') else 'RESTO-DGI-MCF-01')"/>
                <t t-set="resto_legal" t-value="(config.legal_mention if (config and config.legal_mention) else False) or (o.company_legal_mention if hasattr(o, 'company_legal_mention') else 'Facture normalisée certifiée conforme aux exigences de la Direction Générale des Impôts (DGI / e-MCF).')"/>
                <t t-set="logo_src" t-value="image_data_uri(config.logo) if (config and config.logo) else (image_data_uri(env.company.logo) if env.company.logo else False)"/>
                
                <div class="page single-page-invoice" style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #000000; background: #ffffff; padding: 7mm 11mm 5mm 11mm; position: relative; max-height: 275mm; overflow: hidden; box-sizing: border-box; font-size: 10px; page-break-inside: avoid; page-break-after: avoid;">"""

daily_outer_new = """<template id="report_daily_invoice_template">
        <t t-call="web.html_container">
            <t t-foreach="docs" t-as="o">
                <t t-set="config" t-value="env['restaurant.configuration'].sudo().search([], limit=1)"/>
                <t t-set="resto_name" t-value="(config.name if (config and config.name) else False) or o.company_name or (o.company_id.name if hasattr(o, 'company_id') else env.company.name) or 'RESTAURANT'"/>
                <t t-set="resto_sub" t-value="(config.subtitle if (config and config.subtitle) else False) or (o.company_subtitle if hasattr(o, 'company_subtitle') else '')"/>
                <t t-set="resto_ifu" t-value="(config.ifu if (config and config.ifu) else False) or o.company_ifu or (o.company_id.vat if hasattr(o, 'company_id') else env.company.vat) or '-'"/>
                <t t-set="resto_rccm" t-value="(config.rccm if (config and config.rccm) else False) or o.company_rccm or '-'"/>
                <t t-set="resto_regime" t-value="(config.tax_regime if (config and config.tax_regime) else False) or o.company_tax_regime or '-'"/>
                <t t-set="resto_division" t-value="(config.fiscal_division if (config and config.fiscal_division) else False) or o.company_fiscal_division or '-'"/>
                <t t-set="resto_phone" t-value="(config.phone if (config and config.phone) else False) or o.company_phone or (o.company_id.phone if hasattr(o, 'company_id') else env.company.phone) or '-'"/>
                <t t-set="resto_address" t-value="(config.address if (config and config.address) else False) or o.company_address or (o.company_id.street if hasattr(o, 'company_id') else env.company.street) or '-'"/>
                <t t-set="resto_email" t-value="(config.email if (config and config.email) else False) or o.company_email or (o.company_id.email if hasattr(o, 'company_id') else env.company.email) or '-'"/>
                <t t-set="resto_website" t-value="(config.website if (config and config.website) else False) or (o.company_website if hasattr(o, 'company_website') else (o.company_id.website if hasattr(o, 'company_id') else env.company.website)) or '-'"/>
                <t t-set="resto_nim" t-value="(config.nim if (config and config.nim) else False) or (o.company_nim if hasattr(o, 'company_nim') else 'RESTO-DGI-MCF-01')"/>
                <t t-set="resto_legal" t-value="(config.legal_mention if (config and config.legal_mention) else False) or (o.company_legal_mention if hasattr(o, 'company_legal_mention') else 'Facture normalisée certifiée conforme aux exigences de la Direction Générale des Impôts (DGI / e-MCF).')"/>
                <t t-set="logo_src" t-value="image_data_uri(config.logo) if (config and config.logo) else (image_data_uri(env.company.logo) if env.company.logo else False)"/>
                <t t-set="line_count" t-value="len(o.order_ids) if o.order_ids else 1"/>
                <t t-set="dyn_font" t-value="'8.5px' if line_count &gt; 25 else '9.5px' if line_count &gt; 18 else '10.5px' if line_count &gt; 10 else '11px' if line_count &gt; 5 else '11.5px'"/>
                <t t-set="dyn_pad" t-value="'3px 6px' if line_count &gt; 25 else '4.5px 7px' if line_count &gt; 18 else '7px 9px' if line_count &gt; 10 else '9px 11px' if line_count &gt; 5 else '12px 12px'"/>
                <t t-set="dyn_line_height" t-value="'1.35' if line_count &gt; 25 else '1.4' if line_count &gt; 18 else '1.45' if line_count &gt; 10 else '1.5'"/>
                <t t-set="sec_gap" t-value="'6px' if line_count &gt; 25 else '8px' if line_count &gt; 18 else '12px' if line_count &gt; 10 else '16px' if line_count &gt; 5 else '20px'"/>
                <div class="page single-page-invoice" style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #000000; background: #ffffff; padding: 6mm 10mm 4mm 10mm; position: relative; min-height: 250mm; max-height: 254mm; overflow: hidden; box-sizing: border-box; font-size: 10.5px; line-height: 1.45; page-break-inside: avoid; page-break-after: avoid;">"""

content = content.replace(daily_outer_old, daily_outer_new)

# Update all table rows in grand marche and marche dgi so that all 4 td use #{dyn_pad}, #{dyn_font}, and #{dyn_line_height}
# In report_grand_marche_template:
gm_table_row_old = """                                    <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; vertical-align: middle;">
                                        <span style="font-weight: 700; color: #000000;" t-esc="l.name"/>
                                        <span t-if="l.notes" style="font-size: 9.5px; color: #4b5563; font-style: italic; display: block;">
                                            <span t-esc="l.notes"/>
                                        </span>
                                    </td>
                                    <td style="border: 1px solid #000000; padding: 5px 6px; font-size: 9px; text-align: center; font-weight: 700; vertical-align: middle;" t-esc="'%g' % l.quantity if l.quantity else '0'"/>
                                    <td style="border: 1px solid #000000; padding: 5px 8px; font-size: 9px; text-align: right; font-weight: 700; vertical-align: middle;" t-esc="'{0:,.0f}'.format(l.price_unit).replace(',', ' ') + ' FCFA'"/>
                                    <td style="border: 1px solid #000000; padding: 5px 8px; font-size: 9px; text-align: right; font-weight: 700; vertical-align: middle;" t-esc="'{0:,.0f}'.format(l.price_subtotal).replace(',', ' ') + ' FCFA'"/>"""

gm_table_row_new = """                                    <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; vertical-align: middle;">
                                        <span style="font-weight: 700; color: #000000;" t-esc="l.name"/>
                                        <span t-if="l.notes" style="font-size: 9.5px; color: #4b5563; font-style: italic; display: block;">
                                            <span t-esc="l.notes"/>
                                        </span>
                                    </td>
                                    <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; text-align: center; font-weight: 700; vertical-align: middle;" t-esc="'%g' % l.quantity if l.quantity else '0'"/>
                                    <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; text-align: right; font-weight: 700; vertical-align: middle;" t-esc="'{0:,.0f}'.format(l.price_unit).replace(',', ' ') + ' FCFA'"/>
                                    <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; text-align: right; font-weight: 800; vertical-align: middle;" t-esc="'{0:,.0f}'.format(l.price_subtotal).replace(',', ' ') + ' FCFA'"/>"""

content = content.replace(gm_table_row_old, gm_table_row_new)

# In report_daily_invoice_template table rows:
daily_row_old = """                                        <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; vertical-align: middle;">
                                            <span style="font-weight: 700; color: #000000;" t-esc="order.pos_reference or order.name"/>
                                            <small t-if="order.user_id" style="display: block; font-weight: 400; color: #4b5563;">Gérant : <t t-esc="order.user_id.name"/></small>
                                        </td>
                                        <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; text-align: center; font-weight: 700; vertical-align: middle;" t-esc="len(order.lines) or 1"/>
                                        <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; text-align: right; font-weight: 700; vertical-align: middle;" t-esc="'{0:,.0f}'.format(order.amount_total).replace(',', ' ') + ' FCFA'"/>
                                        <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; text-align: right; font-weight: 700; vertical-align: middle;" t-esc="'{0:,.0f}'.format(order.amount_total).replace(',', ' ') + ' FCFA'"/>"""

daily_row_new = """                                        <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; vertical-align: middle;">
                                            <span style="font-weight: 700; color: #000000;" t-esc="order.pos_reference or order.name"/>
                                            <small t-if="order.user_id" style="display: block; font-weight: 400; color: #4b5563;">Gérant : <t t-esc="order.user_id.name"/></small>
                                        </td>
                                        <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; text-align: center; font-weight: 700; vertical-align: middle;" t-esc="len(order.lines) or 1"/>
                                        <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; text-align: right; font-weight: 700; vertical-align: middle;" t-esc="'{0:,.0f}'.format(order.amount_total).replace(',', ' ') + ' FCFA'"/>
                                        <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; text-align: right; font-weight: 800; vertical-align: middle;" t-esc="'{0:,.0f}'.format(order.amount_total).replace(',', ' ') + ' FCFA'"/>"""

content = content.replace(daily_row_old, daily_row_new)

# In daily single summary row (fallback when no order_ids):
daily_fallback_old = """                                    <td style="border: 1px solid #000000; padding: 5px 8px; font-size: 9px; vertical-align: middle;">
                                        <span style="font-weight: 700; color: #000000;">Ventes Globales Restauration &amp; Boissons (Groupe B - Norme DGI)</span>
                                    </td>
                                    <td style="border: 1px solid #000000; padding: 5px 6px; font-size: 9px; text-align: center; font-weight: 700; vertical-align: middle;" t-esc="o.total_orders or 1"/>
                                    <td style="border: 1px solid #000000; padding: 5px 8px; font-size: 9px; text-align: right; font-weight: 700; vertical-align: middle;" t-esc="'{0:,.0f}'.format(o.total_ttc).replace(',', ' ') + ' FCFA'"/>
                                    <td style="border: 1px solid #000000; padding: 5px 8px; font-size: 9px; text-align: right; font-weight: 700; vertical-align: middle;" t-esc="'{0:,.0f}'.format(o.total_ttc).replace(',', ' ') + ' FCFA'"/>"""

daily_fallback_new = """                                    <td style="border: 1px solid #000000; padding: 12px 14px; font-size: 11.5px; line-height: 1.5; vertical-align: middle;">
                                        <span style="font-weight: 700; color: #000000;">Ventes Globales Restauration &amp; Boissons (Groupe B - Norme DGI)</span>
                                    </td>
                                    <td style="border: 1px solid #000000; padding: 12px 8px; font-size: 11.5px; line-height: 1.5; text-align: center; font-weight: 700; vertical-align: middle;" t-esc="o.total_orders or 1"/>
                                    <td style="border: 1px solid #000000; padding: 12px 10px; font-size: 11.5px; line-height: 1.5; text-align: right; font-weight: 700; vertical-align: middle;" t-esc="'{0:,.0f}'.format(o.total_ttc).replace(',', ' ') + ' FCFA'"/>
                                    <td style="border: 1px solid #000000; padding: 12px 14px; font-size: 11.5px; line-height: 1.5; text-align: right; font-weight: 800; vertical-align: middle;" t-esc="'{0:,.0f}'.format(o.total_ttc).replace(',', ' ') + ' FCFA'"/>"""

content = content.replace(daily_fallback_old, daily_fallback_new)

# Also update section gaps to #{sec_gap} in report_grand_marche_template
content = content.replace(
    '<!-- 1. EN-TÊTE : TITRE \'FACTURE\' À GAUCHE & MÉTADONNÉES + QR CODE DGI À DROITE -->\n                    <div style="display: table; width: 100%; margin-bottom: 12px;">',
    '<!-- 1. EN-TÊTE : TITRE \'FACTURE\' À GAUCHE & MÉTADONNÉES + QR CODE DGI À DROITE -->\n                    <div t-attf-style="display: table; width: 100%; margin-bottom: #{sec_gap};">'
)

content = content.replace(
    '<!-- 2. SECTION VENDEUR ET CLIENT (DEUX COLONNES NETTES EXACTEMENT COMME SUR L\'IMAGE) -->\n                    <div style="display: table; width: 100%; margin-bottom: 10px;">',
    '<!-- 2. SECTION VENDEUR ET CLIENT (DEUX COLONNES NETTES EXACTEMENT COMME SUR L\'IMAGE) -->\n                    <div t-attf-style="display: table; width: 100%; margin-bottom: #{sec_gap};">'
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated report_invoice.xml with 85% height stretch and adaptive clear typography!")
