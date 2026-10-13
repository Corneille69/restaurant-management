import re

xml_path = 'odoo_addon/restaurant_core/views/report_invoice.xml'
with open(xml_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix report_daily_invoice_template order row
daily_row_old = """                                    <tr>
                                        <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; vertical-align: middle;">
                                            <span style="font-weight: 700; color: #000000;" t-esc="order.pos_reference or order.name"/>
                                            <small t-if="order.user_id" style="display: block; font-weight: 400; color: #4b5563;">Gérant : <t t-esc="order.user_id.name"/></small>
                                        </td>
                                        <td style="border: 1px solid #000000; padding: 5px 6px; font-size: 9px; text-align: center; font-weight: 700; vertical-align: middle;" t-esc="len(order.lines) or 1"/>
                                        <td style="border: 1px solid #000000; padding: 5px 8px; font-size: 9px; text-align: right; font-weight: 700; vertical-align: middle;" t-esc="'{0:,.0f}'.format(order.amount_total).replace(',', ' ') + ' FCFA'"/>
                                        <td style="border: 1px solid #000000; padding: 5px 8px; font-size: 9px; text-align: right; font-weight: 700; vertical-align: middle;" t-esc="'{0:,.0f}'.format(order.amount_total).replace(',', ' ') + ' FCFA'"/>
                                    </tr>"""

daily_row_new = """                                    <tr>
                                        <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; vertical-align: middle;">
                                            <span style="font-weight: 700; color: #000000;" t-esc="order.pos_reference or order.name"/>
                                            <small t-if="order.user_id" style="display: block; font-weight: 400; color: #4b5563;">Gérant : <t t-esc="order.user_id.name"/></small>
                                        </td>
                                        <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; text-align: center; font-weight: 700; vertical-align: middle;" t-esc="len(order.lines) or 1"/>
                                        <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; text-align: right; font-weight: 700; vertical-align: middle;" t-esc="'{0:,.0f}'.format(order.amount_total).replace(',', ' ') + ' FCFA'"/>
                                        <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; text-align: right; font-weight: 800; vertical-align: middle;" t-esc="'{0:,.0f}'.format(order.amount_total).replace(',', ' ') + ' FCFA'"/>
                                    </tr>"""

content = content.replace(daily_row_old, daily_row_new)

# 2. Fix report_pos_order_invoice_template rows
pos_row_old = """                                <tr>
                                    <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; vertical-align: middle;">
                                        <span style="font-weight: 700; color: #000000;" t-esc="l.product_id.display_name or l.full_product_name"/>
                                    </td>
                                    <td style="border: 1px solid #000000; padding: 5px 6px; font-size: 9px; text-align: center; font-weight: 700; vertical-align: middle;" t-esc="'%g' % l.qty if l.qty else '0'"/>
                                    <td style="border: 1px solid #000000; padding: 5px 8px; font-size: 9px; text-align: right; font-weight: 700; vertical-align: middle;" t-esc="'{0:,.0f}'.format(l.price_unit).replace(',', ' ') + ' FCFA'"/>
                                    <td style="border: 1px solid #000000; padding: 5px 8px; font-size: 9px; text-align: right; font-weight: 700; vertical-align: middle;" t-esc="'{0:,.0f}'.format(l.price_subtotal_incl).replace(',', ' ') + ' FCFA'"/>
                                </tr>"""

pos_row_new = """                                <tr>
                                    <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; vertical-align: middle;">
                                        <span style="font-weight: 700; color: #000000;" t-esc="l.product_id.display_name or l.full_product_name"/>
                                    </td>
                                    <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; text-align: center; font-weight: 700; vertical-align: middle;" t-esc="'%g' % l.qty if l.qty else '0'"/>
                                    <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; text-align: right; font-weight: 700; vertical-align: middle;" t-esc="'{0:,.0f}'.format(l.price_unit).replace(',', ' ') + ' FCFA'"/>
                                    <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; text-align: right; font-weight: 800; vertical-align: middle;" t-esc="'{0:,.0f}'.format(l.price_subtotal_incl).replace(',', ' ') + ' FCFA'"/>
                                </tr>"""

content = content.replace(pos_row_old, pos_row_new)

# 3. Fix report_account_move_invoice_template rows
acc_row_old = """                                <tr>
                                    <td style="border: 1px solid #000000; padding: 5px 8px; font-size: 9px; vertical-align: middle;">
                                        <span style="font-weight: 700; color: #000000;" t-esc="l.name"/>
                                    </td>
                                    <td style="border: 1px solid #000000; padding: 5px 6px; font-size: 9px; text-align: center; font-weight: 700; vertical-align: middle;" t-esc="'%g' % l.quantity if l.quantity else '0'"/>
                                    <td style="border: 1px solid #000000; padding: 5px 8px; font-size: 9px; text-align: right; font-weight: 700; vertical-align: middle;" t-esc="'{0:,.0f}'.format(l.price_unit).replace(',', ' ') + ' FCFA'"/>
                                    <td style="border: 1px solid #000000; padding: 5px 8px; font-size: 9px; text-align: right; font-weight: 700; vertical-align: middle;" t-esc="'{0:,.0f}'.format(l.price_subtotal).replace(',', ' ') + ' FCFA'"/>
                                </tr>"""

acc_row_new = """                                <tr>
                                    <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; vertical-align: middle;">
                                        <span style="font-weight: 700; color: #000000;" t-esc="l.name"/>
                                    </td>
                                    <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; text-align: center; font-weight: 700; vertical-align: middle;" t-esc="'%g' % l.quantity if l.quantity else '0'"/>
                                    <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; text-align: right; font-weight: 700; vertical-align: middle;" t-esc="'{0:,.0f}'.format(l.price_unit).replace(',', ' ') + ' FCFA'"/>
                                    <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; text-align: right; font-weight: 800; vertical-align: middle;" t-esc="'{0:,.0f}'.format(l.price_subtotal).replace(',', ' ') + ' FCFA'"/>
                                </tr>"""

content = content.replace(acc_row_old, acc_row_new)

# Remove empty placeholder rows from report_account_move_invoice_template
acc_empty_rows = """                            <!-- Lignes vides pour conserver la disposition élégante du tableau comme sur l'image -->
                            <t t-if="len(lines) &lt; 5">
                                <t t-foreach="range(5 - len(lines))" t-as="empty_idx">
                                    <tr>
                                        <td style="border: 1px solid #000000; padding: 5px 8px; font-size: 9px; color: transparent;">-</td>
                                        <td style="border: 1px solid #000000; padding: 5px 6px; font-size: 9px; color: transparent;">-</td>
                                        <td style="border: 1px solid #000000; padding: 5px 8px; font-size: 9px; color: transparent;">-</td>
                                        <td style="border: 1px solid #000000; padding: 5px 8px; font-size: 9px; color: transparent;">-</td>
                                    </tr>
                                </t>
                            </t>"""
content = content.replace(acc_empty_rows, '')

# 4. Update Totals table in report_grand_marche_template & report_marche_dgi_template to use #{tot_pad}, #{tot_font}, #{tot_ttc_font}
# Let's inspect the totals table structure:
content = re.sub(
    r'<td colspan="2" style="border: 1px solid #000000; border-top: none; padding: 8px 10px; font-weight: 800; color: #000000; text-transform: uppercase;">\s*MONTANT HT\s*</td>\s*<td style="border: 1px solid #000000; border-top: none; padding: 8px 10px; text-align: right; font-weight: 700; color: #000000;"',
    r'<td colspan="2" t-attf-style="border: 1px solid #000000; border-top: none; padding: #{tot_pad}; font-size: #{tot_font}; font-weight: 800; color: #000000; text-transform: uppercase;">\n                                    MONTANT HT\n                                </td>\n                                <td t-attf-style="border: 1px solid #000000; border-top: none; padding: #{tot_pad}; font-size: #{tot_font}; text-align: right; font-weight: 700; color: #000000;"',
    content
)

content = re.sub(
    r'<td style="border: 1px solid #000000; padding: 5px 8px; font-size: 9px; font-weight: 800; color: #000000;">\s*TVA\s*</td>\s*<td style="border: 1px solid #000000; padding: 8px 6px; text-align: center; font-weight: 700; color: #000000; width: 45px;">\s*<span t-esc="o\.tax_rate"/>%\s*</td>\s*<td style="border: 1px solid #000000; padding: 5px 8px; font-size: 9px; text-align: right; font-weight: 700; color: #000000;"',
    r'<td t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_font}; font-weight: 800; color: #000000;">\n                                    TVA\n                                </td>\n                                <td t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_font}; text-align: center; font-weight: 700; color: #000000; width: 45px;">\n                                    <span t-esc="o.tax_rate"/>%\n                                </td>\n                                <td t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_font}; text-align: right; font-weight: 700; color: #000000;"',
    content
)

# Total TTC row:
content = re.sub(
    r'<td colspan="2" style="border: 1px solid #000000; padding: 5px 8px; font-size: 9px; font-weight: 900; font-size: 11\.5px; letter-spacing: 0\.5px; text-transform: uppercase;">\s*TOTAL TTC\s*</td>\s*<td style="border: 1px solid #000000; padding: 5px 8px; font-size: 9px; text-align: right; font-weight: 900; font-size: 12\.5px;"',
    r'<td colspan="2" t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_ttc_font}; font-weight: 900; letter-spacing: 0.5px; text-transform: uppercase;">\n                                    TOTAL TTC\n                                </td>\n                                <td t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_ttc_font}; text-align: right; font-weight: 900;"',
    content
)

with open(xml_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated all table cells with dynamic padding, font, line-height and tot_pad/tot_font!")
