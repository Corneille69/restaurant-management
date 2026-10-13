import re

xml_path = 'odoo_addon/restaurant_core/views/report_invoice.xml'
with open(xml_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add paperformat_id to action_report_marche_client_receipt
action_old = """    <record id="action_report_marche_client_receipt" model="ir.actions.report">
        <field name="name">🖨️ Reçu Client Grand Marché (PDF)</field>"""

action_new = """    <record id="action_report_marche_client_receipt" model="ir.actions.report">
        <field name="paperformat_id" ref="restaurant_core.paperformat_restaurant_single_page"/>
        <field name="name">🖨️ Reçu Client Grand Marché (PDF)</field>"""

content = content.replace(action_old, action_new)

# 2. Rewrite report_marche_client_receipt_template cleanly
receipt_template_new = """    <template id="report_marche_client_receipt_template">
        <t t-call="web.html_container">
            <t t-foreach="docs" t-as="o">
                <t t-set="config" t-value="env['restaurant.configuration'].sudo().search([], limit=1)"/>
                <t t-set="resto_name" t-value="(config.name if (config and config.name) else False) or (o.company_id.name if hasattr(o, 'company_id') else env.company.name) or 'RESTAURANT'"/>
                <t t-set="resto_sub" t-value="(config.subtitle if (config and config.subtitle) else False) or ''"/>
                <t t-set="resto_phone" t-value="(config.phone if (config and config.phone) else False) or (o.company_id.phone if hasattr(o, 'company_id') else env.company.phone) or '-'"/>
                <t t-set="resto_address" t-value="(config.address if (config and config.address) else False) or (o.company_id.street if hasattr(o, 'company_id') else env.company.street) or '-'"/>
                <t t-set="resto_email" t-value="(config.email if (config and config.email) else False) or (o.company_id.email if hasattr(o, 'company_id') else env.company.email) or ''"/>
                <t t-set="resto_website" t-value="(config.website if (config and config.website) else False) or (o.company_id.website if hasattr(o, 'company_id') else env.company.website) or ''"/>
                <t t-set="resto_rccm" t-value="(config.rccm if (config and config.rccm) else False) or ''"/>
                <t t-set="resto_ifu" t-value="(config.ifu if (config and config.ifu) else False) or ''"/>
                <t t-set="resto_legal" t-value="(config.legal_mention if (config and config.legal_mention) else False) or 'Facture normalisée certifiée conforme aux exigences de la DGI'"/>
                <t t-set="logo_src" t-value="image_data_uri(config.logo) if (config and config.logo) else (image_data_uri(env.company.logo) if env.company.logo else False)"/>
                <t t-set="line_count" t-value="len(o.line_ids) if o.line_ids else 1"/>
                <t t-set="dyn_font" t-value="'8.5px' if line_count &gt; 25 else '9.5px' if line_count &gt; 18 else '10px' if line_count &gt; 10 else '11px' if line_count &gt; 4 else '11.5px'"/>
                <t t-set="dyn_pad" t-value="'3px 6px' if line_count &gt; 25 else '4.5px 7px' if line_count &gt; 18 else '6px 8px' if line_count &gt; 10 else '8px 10px' if line_count &gt; 4 else '10px 12px'"/>
                <t t-set="dyn_line_height" t-value="'1.35' if line_count &gt; 25 else '1.4' if line_count &gt; 18 else '1.45' if line_count &gt; 10 else '1.5' if line_count &gt; 4 else '1.55'"/>
                <t t-set="sec_gap" t-value="'5px' if line_count &gt; 25 else '7px' if line_count &gt; 18 else '9px' if line_count &gt; 10 else '12px' if line_count &gt; 4 else '16px'"/>
                <t t-set="tot_font" t-value="'9px' if line_count &gt; 25 else '9.5px' if line_count &gt; 18 else '10px' if line_count &gt; 10 else '10.5px' if line_count &gt; 4 else '11px'"/>
                <t t-set="tot_pad" t-value="'3px 6px' if line_count &gt; 25 else '4px 6px' if line_count &gt; 18 else '5px 7px' if line_count &gt; 10 else '6px 8px' if line_count &gt; 4 else '7px 9px'"/>

                <div class="page single-page-invoice" style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #1e293b; background: #ffffff; padding: 5mm 10mm 4mm 10mm; position: relative; min-height: 250mm; max-height: 254mm; overflow: hidden; box-sizing: border-box; font-size: 10px; line-height: 1.45; page-break-inside: avoid; page-break-after: avoid;">
                    
                    <!-- EN-TÊTE ÉTABLISSEMENT -->
                    <div t-attf-style="display: table; width: 100%; margin-bottom: #{sec_gap}; border-bottom: 2.5px solid #064e3b; padding-bottom: 8px;">
                        <div style="display: table-cell; width: 62%; vertical-align: middle;">
                            <div style="display: table; width: 100%;">
                                <div style="display: table-cell; width: 65px; vertical-align: middle;">
                                    <img t-if="logo_src" t-att-src="logo_src" style="max-width: 60px; max-height: 60px; object-fit: contain;" alt="Logo"/>
                                    <div t-else="" style="width: 55px; height: 55px; background: #064e3b; color: #ffffff; border-radius: 6px; font-size: 26px; line-height: 55px; text-align: center;">🍽️</div>
                                </div>
                                <div style="display: table-cell; vertical-align: middle; padding-left: 10px;">
                                    <h2 style="font-size: 18px; font-weight: 900; color: #064e3b; margin: 0 0 2px 0; text-transform: uppercase;">
                                        <span t-esc="resto_name"/>
                                    </h2>
                                    <p t-if="resto_sub" style="font-size: 10.5px; color: #64748b; margin: 0 0 2px 0; font-weight: 600;">
                                        <span t-esc="resto_sub"/>
                                    </p>
                                    <div style="font-size: 10px; color: #475569; line-height: 1.35;">
                                        <span><strong t-esc="resto_address"/></span>
                                        <span t-if="resto_phone"> • Tél : <strong t-esc="resto_phone"/></span>
                                        <div t-if="resto_rccm or resto_ifu" style="margin-top: 1px; font-size: 9px; color: #64748b;">
                                            <span t-if="resto_rccm">RCCM : <strong t-esc="resto_rccm"/></span>
                                            <span t-if="resto_rccm and resto_ifu"> • </span>
                                            <span t-if="resto_ifu">IFU : <strong t-esc="resto_ifu"/></span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div style="display: table-cell; width: 38%; vertical-align: middle; text-align: right;">
                            <div style="background: #064e3b; color: #ffffff; display: inline-block; padding: 8px 16px; border-radius: 6px; border: 1.5px solid #d4af37; text-align: center;">
                                <div style="font-size: 13px; font-weight: 900; letter-spacing: 0.8px; color: #ffd700;">REÇU CLIENT</div>
                                <div style="font-size: 9.5px; font-weight: 700; color: #e2e8f0; margin-top: 1px;">COMMANDE GRAND MARCHÉ</div>
                                <div style="font-size: 12.5px; font-weight: 900; color: #ffffff; margin-top: 2px; font-family: monospace;">
                                    <span t-field="o.name"/>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- BLOCS CLIENT & INFORMATIONS DE COMMANDE -->
                    <div t-attf-style="display: table; width: 100%; margin-bottom: #{sec_gap};">
                        <div style="display: table-cell; width: 55%; vertical-align: top; padding-right: 10px;">
                            <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 7px 10px;">
                                <div style="font-size: 9.5px; font-weight: 800; color: #064e3b; text-transform: uppercase; margin-bottom: 2px;">
                                    Client / Donneur d'Ordre :
                                </div>
                                <div style="font-size: 12px; font-weight: 900; color: #0f172a; margin-bottom: 2px;">
                                    <span t-field="o.partner_name"/>
                                </div>
                                <div style="font-size: 9.5px; color: #334155; line-height: 1.35;">
                                    <div t-if="o.partner_phone"><strong>Téléphone :</strong> <span t-field="o.partner_phone"/></div>
                                    <div t-if="o.partner_address"><strong>Lieu d'Exécution :</strong> <span t-field="o.partner_address"/></div>
                                </div>
                            </div>
                        </div>
                        <div style="display: table-cell; width: 45%; vertical-align: top;">
                            <div style="background: #f0fdf4; border: 1px solid #86efac; border-radius: 6px; padding: 7px 10px;">
                                <div style="font-size: 9.5px; font-weight: 800; color: #166534; text-transform: uppercase; margin-bottom: 2px;">
                                    Détails du Reçu :
                                </div>
                                <table style="width: 100%; font-size: 9.5px; color: #1e293b; border-collapse: collapse;">
                                    <tr>
                                        <td style="padding: 1px 0; font-weight: 700; width: 45%;">Date :</td>
                                        <td style="padding: 1px 0; font-weight: 900;"><span t-field="o.date_invoice"/></td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 1px 0; font-weight: 700;">Gérant :</td>
                                        <td style="padding: 1px 0; font-weight: 800;"><span t-field="o.manager_id.name"/></td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 1px 0; font-weight: 700;">Mode Règlement :</td>
                                        <td style="padding: 1px 0; font-weight: 800;">
                                            <span t-if="o.payment_method == 'transfer'">Virement Bancaire</span>
                                            <span t-elif="o.payment_method == 'check'">Chèque Bancaire</span>
                                            <span t-elif="o.payment_method == 'cash'">Espèces</span>
                                            <span t-elif="o.payment_method == 'mobile'">Mobile Money</span>
                                            <span t-else="">À Terme (Bon de Commande)</span>
                                        </td>
                                    </tr>
                                </table>
                            </div>
                        </div>
                    </div>

                    <!-- OBJET DU MARCHÉ -->
                    <div t-attf-style="background: #0f172a; color: #ffffff; border-radius: 5px; padding: 5px 10px; margin-bottom: #{sec_gap}; border-left: 3.5px solid #d4af37;">
                        <span style="font-size: 9px; font-weight: 700; color: #94a3b8; text-transform: uppercase;">OBJET DE LA PRESTATION :</span>
                        <div style="font-size: 11.5px; font-weight: 900; color: #ffd700; margin-top: 1px;">
                            <span t-field="o.subject"/>
                        </div>
                    </div>

                    <!-- TABLEAU DES LIGNES -->
                    <table t-attf-style="width: 100%; border-collapse: collapse; margin-bottom: #{sec_gap}; font-size: #{dyn_font}; border: 1px solid #cbd5e1;">
                        <thead>
                            <tr style="background: #064e3b; color: #ffffff; text-align: left;">
                                <th t-attf-style="padding: #{dyn_pad}; width: 6%; text-align: center;">N°</th>
                                <th t-attf-style="padding: #{dyn_pad}; width: 14%;">Partie</th>
                                <th t-attf-style="padding: #{dyn_pad}; width: 44%;">Désignation &amp; Détails</th>
                                <th t-attf-style="padding: #{dyn_pad}; width: 10%; text-align: center;">Qté</th>
                                <th t-attf-style="padding: #{dyn_pad}; width: 13%; text-align: right;">Prix Unitaire</th>
                                <th t-attf-style="padding: #{dyn_pad}; width: 13%; text-align: right;">Sous-Total</th>
                            </tr>
                        </thead>
                        <tbody>
                            <t t-set="idx" t-value="1"/>
                            <t t-foreach="o.line_ids" t-as="l">
                                <tr style="border-bottom: 1px solid #e2e8f0;">
                                    <td t-attf-style="padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; text-align: center; font-weight: 700; color: #64748b;" t-esc="idx"/>
                                    <td t-attf-style="padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height};">
                                        <span t-if="l.item_type == 'repas'" style="background: #dcfce7; color: #166534; font-weight: 700; font-size: 9px; padding: 1.5px 5px; border-radius: 3px;">Repas</span>
                                        <span t-elif="l.item_type == 'boisson'" style="background: #fef3c7; color: #92400e; font-weight: 700; font-size: 9px; padding: 1.5px 5px; border-radius: 3px;">Boisson</span>
                                        <span t-elif="l.item_type == 'service'" style="background: #e0e7ff; color: #3730a3; font-weight: 700; font-size: 9px; padding: 1.5px 5px; border-radius: 3px;">Prestation</span>
                                        <span t-else="" style="background: #f1f5f9; color: #475569; font-weight: 700; font-size: 9px; padding: 1.5px 5px; border-radius: 3px;">Autre</span>
                                    </td>
                                    <td t-attf-style="padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height};">
                                        <strong style="color: #0f172a;"><span t-field="l.name"/></strong>
                                        <div t-if="l.notes" style="font-size: 8.5px; color: #64748b; font-style: italic; margin-top: 1px;">
                                            <span t-field="l.notes"/>
                                        </div>
                                    </td>
                                    <td t-attf-style="padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; text-align: center; font-weight: 800;"><span t-field="l.quantity"/></td>
                                    <td t-attf-style="padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; text-align: right; font-weight: 700;" t-esc="'{0:,.0f}'.format(l.price_unit).replace(',', ' ') + ' F'"/>
                                    <td t-attf-style="padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; text-align: right; font-weight: 900; color: #064e3b;" t-esc="'{0:,.0f}'.format(l.price_subtotal).replace(',', ' ') + ' F'"/>
                                </tr>
                                <t t-set="idx" t-value="idx + 1"/>
                            </t>
                        </tbody>
                    </table>

                    <!-- TOTAUX COMMERCIAUX DU REÇU -->
                    <div t-attf-style="display: table; width: 100%; margin-bottom: #{sec_gap};">
                        <div style="display: table-cell; width: 52%; vertical-align: top; padding-right: 12px;">
                            <div style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 5px; padding: 6px 10px; font-size: 9.5px;">
                                <div style="font-weight: 800; color: #0f172a; margin-bottom: 2px; text-transform: uppercase;">
                                    Conditions de la Prestation :
                                </div>
                                <div style="color: #475569; margin-bottom: 3px;"><span t-field="o.payment_terms"/></div>
                                <div t-if="o.notes" style="font-style: italic; color: #64748b; font-size: 9px;"><span t-field="o.notes"/></div>
                            </div>
                        </div>
                        <div style="display: table-cell; width: 48%; vertical-align: top;">
                            <table t-attf-style="width: 100%; border-collapse: collapse; font-size: #{tot_font};">
                                <tr style="border-bottom: 1px solid #e2e8f0;" t-if="o.amount_repas &gt; 0">
                                    <td t-attf-style="padding: #{tot_pad}; color: #475569;">Sous-total Plats &amp; Repas :</td>
                                    <td t-attf-style="padding: #{tot_pad}; text-align: right; font-weight: 700;" t-esc="'{0:,.0f}'.format(o.amount_repas).replace(',', ' ') + ' FCFA'"/>
                                </tr>
                                <tr style="border-bottom: 1px solid #e2e8f0;" t-if="o.amount_boissons &gt; 0">
                                    <td t-attf-style="padding: #{tot_pad}; color: #475569;">Sous-total Boissons :</td>
                                    <td t-attf-style="padding: #{tot_pad}; text-align: right; font-weight: 700;" t-esc="'{0:,.0f}'.format(o.amount_boissons).replace(',', ' ') + ' FCFA'"/>
                                </tr>
                                <tr style="border-bottom: 1px solid #e2e8f0;" t-if="o.amount_services &gt; 0">
                                    <td t-attf-style="padding: #{tot_pad}; color: #475569;">Sous-total Prestations Traiteur :</td>
                                    <td t-attf-style="padding: #{tot_pad}; text-align: right; font-weight: 700;" t-esc="'{0:,.0f}'.format(o.amount_services).replace(',', ' ') + ' FCFA'"/>
                                </tr>
                                <tr style="background: #064e3b; color: #ffffff; border-top: 2px solid #064e3b;">
                                    <td t-attf-style="padding: #{tot_pad}; font-weight: 900; font-size: 11px; letter-spacing: 0.5px;">TOTAL DE LA COMMANDE :</td>
                                    <td t-attf-style="padding: #{tot_pad}; text-align: right; font-weight: 900; font-size: 12.5px; color: #ffd700;" t-esc="'{0:,.0f}'.format(o.amount_untaxed).replace(',', ' ') + ' FCFA'"/>
                                </tr>
                                <tr t-if="o.amount_deposit &gt; 0" style="border-bottom: 1px solid #e2e8f0; background: #f0fdf4;">
                                    <td t-attf-style="padding: #{tot_pad}; font-weight: 700; color: #166534;">Moins Acompte Reçu :</td>
                                    <td t-attf-style="padding: #{tot_pad}; text-align: right; font-weight: 800; color: #166534;" t-esc="'- ' + '{0:,.0f}'.format(o.amount_deposit).replace(',', ' ') + ' FCFA'"/>
                                </tr>
                                <tr t-if="o.amount_deposit &gt; 0" style="border-bottom: 2px solid #b91c1c;">
                                    <td t-attf-style="padding: #{tot_pad}; font-weight: 900; color: #b91c1c; font-size: 11px;">SOLDE RESTANT À RÉGLER :</td>
                                    <td t-attf-style="padding: #{tot_pad}; text-align: right; font-weight: 900; color: #b91c1c; font-size: 12px;" t-esc="'{0:,.0f}'.format(max(0, o.amount_untaxed - o.amount_deposit)).replace(',', ' ') + ' FCFA'"/>
                                </tr>
                            </table>
                        </div>
                    </div>

                    <!-- PIED DE PAGE : INFORMATIONS CONFIGURÉES DANS L'ADMINISTRATION -->
                    <div style="position: absolute; bottom: 3mm; left: 10mm; right: 10mm; text-align: center; font-size: 8.5px; color: #475569; border-top: 1px solid #cbd5e1; padding-top: 4px; line-height: 1.35;">
                        <div t-if="resto_legal" style="font-weight: 600; color: #1e293b; margin-bottom: 2px;">
                            <span t-esc="resto_legal"/>
                        </div>
                        <div>
                            <span><strong><t t-esc="resto_name"/></strong></span>
                            <span t-if="resto_address"> • <t t-esc="resto_address"/></span>
                            <span t-if="resto_phone"> • Tél : <t t-esc="resto_phone"/></span>
                            <span t-if="resto_email"> • <t t-esc="resto_email"/></span>
                            <span t-if="resto_website"> • <t t-esc="resto_website"/></span>
                        </div>
                    </div>

                </div>
            </t>
        </t>
    </template>"""

# Replace the old template with the new template
pattern_template = re.compile(
    r'    <template id="report_marche_client_receipt_template">.*?</template>',
    re.DOTALL
)

content = pattern_template.sub(receipt_template_new, content)

with open(xml_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated report_marche_client_receipt_template cleanly!")
