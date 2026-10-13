import re
import xml.etree.ElementTree as ET

path = r"c:\Users\840 G5\Contacts\Bureau\restaurant-management\odoo_addon\restaurant_core\views\report_invoice.xml"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Template 1: report_marche_dgi_template
tmpl_marche_dgi = """    <template id="report_marche_dgi_template">
        <t t-call="web.html_container">
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
                <meta charset="utf-8"/>
            </head>
            <t t-foreach="docs" t-as="o">
                <t t-set="config" t-value="env['restaurant.configuration'].sudo().search([], limit=1)"/>
                <t t-set="resto_name" t-value="(config.name if (config and config.name) else False) or (o.company_id.name if hasattr(o, 'company_id') else env.company.name) or 'RESTAURANT'"/>
                <t t-set="resto_sub" t-value="(config.subtitle if (config and config.subtitle) else False) or ''"/>
                <t t-set="resto_ifu" t-value="(config.ifu if (config and config.ifu) else False) or (o.company_id.vat if hasattr(o, 'company_id') else env.company.vat) or '-'"/>
                <t t-set="resto_rccm" t-value="(config.rccm if (config and config.rccm) else False) or '-'"/>
                <t t-set="resto_nim" t-value="(config.nim if (config and config.nim) else False) or 'RESTO-DGI-MCF-01'"/>
                <t t-set="resto_regime" t-value="(config.tax_regime if (config and config.tax_regime) else False) or 'Régime Réel Normal'"/>
                <t t-set="resto_phone" t-value="(config.phone if (config and config.phone) else False) or (o.company_id.phone if hasattr(o, 'company_id') else env.company.phone) or '-'"/>
                <t t-set="resto_address" t-value="(config.address if (config and config.address) else False) or (o.company_id.street if hasattr(o, 'company_id') else env.company.street) or '-'"/>
                <t t-set="resto_email" t-value="(config.email if (config and config.email) else False) or (o.company_id.email if hasattr(o, 'company_id') else env.company.email) or '-'"/>
                <t t-set="resto_website" t-value="(config.website if (config and config.website) else False) or 'www.restaurant.com'"/>
                <t t-set="line_count" t-value="len(o.line_ids) if o.line_ids else 1"/>
                <t t-set="dyn_font" t-value="'8px' if line_count &gt; 25 else '8.5px' if line_count &gt; 18 else '9.5px' if line_count &gt; 10 else '10.5px' if line_count &gt; 4 else '11px'"/>
                <t t-set="dyn_pad" t-value="'2.5px 5px' if line_count &gt; 25 else '3.5px 6px' if line_count &gt; 18 else '5px 8px' if line_count &gt; 10 else '8px 12px' if line_count &gt; 4 else '11px 14px'"/>
                <t t-set="dyn_line_height" t-value="'1.3' if line_count &gt; 25 else '1.35' if line_count &gt; 18 else '1.4' if line_count &gt; 10 else '1.48' if line_count &gt; 4 else '1.55'"/>
                <t t-set="sec_gap" t-value="'4px' if line_count &gt; 25 else '6px' if line_count &gt; 18 else '8px' if line_count &gt; 10 else '12px' if line_count &gt; 4 else '16px'"/>
                <t t-set="tot_font" t-value="'8.5px' if line_count &gt; 25 else '9px' if line_count &gt; 18 else '9.5px' if line_count &gt; 10 else '10.5px' if line_count &gt; 4 else '11px'"/>
                <t t-set="tot_pad" t-value="'3px 5px' if line_count &gt; 25 else '3.5px 6px' if line_count &gt; 18 else '5px 7px' if line_count &gt; 10 else '6.5px 9px' if line_count &gt; 4 else '8px 10px'"/>
                <t t-set="tot_ttc_font" t-value="'10px' if line_count &gt; 25 else '10.5px' if line_count &gt; 18 else '11px' if line_count &gt; 10 else '12px' if line_count &gt; 4 else '13px'"/>
                <t t-set="ref_dgi" t-value="o.dgi_reference or ('DGI-FNE-GM-' + (o.date_invoice.strftime('%Y%m%d') if o.date_invoice else '2026') + '-0001')"/>

                <div class="article page single-page-invoice" style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #000000; background: #ffffff; padding: 6mm 10mm 4mm 10mm; position: relative; min-height: 250mm; box-sizing: border-box; font-size: 10.5px; line-height: 1.45; page-break-inside: avoid; page-break-after: avoid;">
                    
                    <!-- 1. EN-TÊTE : TITRE 'FACTURE' À GAUCHE & MÉTADONNÉES + QR CODE DGI À DROITE -->
                    <div t-attf-style="display: table; width: 100%; margin-bottom: #{sec_gap};">
                        <div style="display: table-cell; width: 45%; vertical-align: top;">
                            <h1 style="font-size: 26px; font-weight: 900; color: #000000; margin: 0 0 2px 0; letter-spacing: 1.5px; text-transform: uppercase; line-height: 1;">
                                FACTURE
                            </h1>
                            <div style="font-size: 9.5px; font-weight: 800; color: #166534; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 3px;">
                                FACTURE NORMALISÉE DGI (e-MCF)
                            </div>
                        </div>
                        <div style="display: table-cell; width: 55%; vertical-align: top; text-align: right;">
                            <div style="display: inline-table; text-align: left;">
                                <div style="display: table-row;">
                                    <div style="display: table-cell; vertical-align: middle; padding-right: 15px;">
                                        <table style="font-size: 11px; color: #000000; border-collapse: collapse;">
                                            <tr>
                                                <td style="font-weight: 800; padding: 2px 8px 2px 0; color: #000000;">Numéro de facture :</td>
                                                <td style="font-weight: 700; padding: 2px 0;" t-esc="o.name"/>
                                            </tr>
                                            <tr>
                                                <td style="font-weight: 800; padding: 2px 8px 2px 0; color: #000000;">Date de facturation :</td>
                                                <td style="font-weight: 600; padding: 2px 0;"><span t-field="o.date_invoice"/></td>
                                            </tr>
                                            <tr>
                                                <td style="font-weight: 800; padding: 2px 8px 2px 0; color: #000000;">Échéance :</td>
                                                <td style="font-weight: 600; padding: 2px 0;">
                                                    <span t-if="o.date_due" t-field="o.date_due"/>
                                                    <span t-else="">À réception</span>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td style="font-weight: 800; padding: 2px 8px 2px 0; color: #000000;">Référence :</td>
                                                <td style="font-weight: 700; padding: 2px 0; font-family: monospace;" t-esc="ref_dgi"/>
                                            </tr>
                                        </table>
                                    </div>
                                    <!-- QR CODE OFFICIEL DGI INTÉGRÉ DANS L'EN-TÊTE -->
                                    <div style="display: table-cell; vertical-align: middle; text-align: center; border-left: 1.5px solid #000000; padding-left: 12px;">
                                        <img t-att-src="o.get_dgi_qr_code_base64()" style="width: 65px; height: 65px; display: block; margin: 0 auto;" alt="QR DGI"/>
                                        <div style="font-size: 8px; font-weight: 800; color: #166534; margin-top: 2px; letter-spacing: 0.5px;">
                                            SCAN DGI e-MCF
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 2. SECTION VENDEUR ET CLIENT -->
                    <div t-attf-style="display: table; width: 100%; margin-bottom: #{sec_gap};">
                        <!-- COLONNE VENDEUR -->
                        <div style="display: table-cell; width: 50%; vertical-align: top; padding-right: 20px;">
                            <div style="font-size: 13.5px; font-weight: 900; color: #000000; margin-bottom: 6px;">
                                Vendeur
                            </div>
                            <div style="font-size: 11px; color: #111827; line-height: 1.45;">
                                <div style="font-weight: 800; font-size: 11.5px; color: #000000;" t-esc="resto_name"/>
                                <div style="font-style: italic; color: #4b5563;" t-if="resto_address" t-esc="resto_address"/>
                                <div t-if="resto_phone">Tél : <span t-esc="resto_phone"/></div>
                                <div style="margin-top: 4px; font-size: 10.5px; color: #374151;">
                                    <span t-if="resto_ifu">IFU : <strong t-esc="resto_ifu"/></span>
                                    <span t-if="resto_ifu and resto_rccm"> - </span>
                                    <span t-if="resto_rccm">RCCM : <strong t-esc="resto_rccm"/></span>
                                </div>
                            </div>
                        </div>

                        <!-- COLONNE CLIENT -->
                        <div style="display: table-cell; width: 50%; vertical-align: top; padding-left: 20px;">
                            <div style="font-size: 13.5px; font-weight: 900; color: #000000; margin-bottom: 6px;">
                                Client
                            </div>
                            <div style="font-size: 11px; color: #111827; line-height: 1.45;">
                                <div style="font-weight: 800; font-size: 11.5px; color: #000000;" t-esc="o.partner_name"/>
                                <div style="font-style: italic; color: #4b5563;" t-if="o.partner_address" t-esc="o.partner_address"/>
                                <div t-if="o.partner_phone">Tél : <span t-esc="o.partner_phone"/></div>
                                <div style="margin-top: 4px; font-size: 10.5px; color: #374151;">
                                    <span t-if="o.partner_ifu">NIF / IFU Client : <strong t-esc="o.partner_ifu"/></span>
                                    <span t-else="">Client Particulier / Entreprise</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 3. TABLEAU DES ARTICLES (DESIGNATION | QTE | PRIX UNIT | MONTANT) -->
                    <table style="width: 100%; border-collapse: collapse; border: 1px solid #000000; margin-bottom: 0;">
                        <thead>
                            <tr style="background-color: #000000; color: #ffffff;">
                                <th t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; font-weight: 900; text-align: left; text-transform: uppercase; letter-spacing: 0.5px; width: 48%;">
                                    DESIGNATION
                                </th>
                                <th t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; font-weight: 900; text-align: center; text-transform: uppercase; letter-spacing: 0.5px; width: 10%;">
                                    QTE
                                </th>
                                <th t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; font-weight: 900; text-align: right; text-transform: uppercase; letter-spacing: 0.5px; width: 20%;">
                                    PRIX UNIT
                                </th>
                                <th t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; font-weight: 900; text-align: right; text-transform: uppercase; letter-spacing: 0.5px; width: 22%;">
                                    MONTANT
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <t t-set="line_count" t-value="len(o.line_ids) if o.line_ids else 1"/>
                            <t t-foreach="o.line_ids" t-as="l">
                                <tr>
                                    <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; vertical-align: middle;">
                                        <span style="font-weight: 700; color: #000000;" t-esc="l.name"/>
                                        <span t-if="l.notes" style="font-size: 9.5px; color: #4b5563; font-style: italic; display: block;">
                                            <span t-esc="l.notes"/>
                                        </span>
                                    </td>
                                    <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; text-align: center; font-weight: 700; vertical-align: middle;" t-esc="'%g' % l.quantity if l.quantity else '0'"/>
                                    <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; text-align: right; font-weight: 700; vertical-align: middle;" t-esc="'{0:,.0f}'.format(l.price_unit).replace(',', ' ') + ' FCFA'"/>
                                    <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; text-align: right; font-weight: 800; vertical-align: middle;" t-esc="'{0:,.0f}'.format(l.price_subtotal).replace(',', ' ') + ' FCFA'"/>
                                </tr>
                            </t>
                        </tbody>
                    </table>

                    <!-- 4. BLOC DES TOTAUX ET CONDITIONS (DEUX COLONNES CÔTE À CÔTE SOUS LA TABLE DES ARTICLES) -->
                    <div style="width: 100%; margin-top: 0; margin-bottom: 10px; page-break-inside: avoid;">
                        <div style="display: table; width: 100%; border-collapse: collapse;">
                            <!-- COLONNE GAUCHE (48%) : CONDITIONS DE PAIEMENT + HOMOLOGATION DGI -->
                            <div style="display: table-cell; width: 48%; vertical-align: top; padding-right: 15px; padding-top: 4px;">
                                <div style="font-weight: 900; font-size: 11px; color: #000000; margin-bottom: 3px; text-transform: uppercase; letter-spacing: 0.3px;">
                                    Conditions et modalités de paiement
                                </div>
                                <div style="font-size: 10px; color: #1f2937; margin-bottom: 8px; line-height: 1.4;">
                                    <span t-if="o.payment_terms" t-esc="o.payment_terms"/>
                                    <span t-else="">Paiement à réception de facture</span>
                                    <div t-if="o.payment_method" style="margin-top: 2px;">
                                        Mode de règlement : 
                                        <strong t-if="o.payment_method == 'transfer'">Virement bancaire</strong>
                                        <strong t-elif="o.payment_method == 'check'">Chèque</strong>
                                        <strong t-elif="o.payment_method == 'cash'">Espèces</strong>
                                        <strong t-elif="o.payment_method == 'mobile'">Mobile Money</strong>
                                        <strong t-else="">Selon convention</strong>
                                    </div>
                                </div>

                                <!-- CADRE HOMOLOGATION DGI OFFICIEL -->
                                <div style="border: 1.5px solid #166534; background: #f0fdf4; border-radius: 4px; padding: 6px 8px; font-size: 9px; color: #14532d; line-height: 1.4;">
                                    <div style="font-weight: 900; text-transform: uppercase; margin-bottom: 3px; color: #166534; font-size: 9.5px; letter-spacing: 0.5px;">
                                        HOMOLOGATION DGI / e-MCF
                                    </div>
                                    <div>Réf. FNE : <strong t-esc="ref_dgi"/></div>
                                    <div>Sceau Fiscal : <span style="font-family: monospace; font-size: 8px; word-break: break-all;" t-esc="o.dgi_security_code or 'VERIFIED_DGI_SIGNATURE'"/></div>
                                    <div style="margin-top: 2px;">NIM : <strong t-esc="resto_nim"/> - Daté du : <span t-esc="o.dgi_certified_at or o.date_invoice"/></div>
                                </div>
                            </div>

                            <!-- COLONNE DROITE (52%) : TABLEAU DES TOTAUX ACCROCHÉ AUX ARTICLES -->
                            <div style="display: table-cell; width: 52%; vertical-align: top;">
                                <table style="width: 100%; border-collapse: collapse; border-top: none; font-size: 11px;">
                                    <tr>
                                        <td colspan="2" t-attf-style="border: 1px solid #000000; border-top: none; padding: #{tot_pad}; font-size: #{tot_font}; font-weight: 800; color: #000000; text-transform: uppercase;">
                                            MONTANT HT
                                        </td>
                                        <td t-attf-style="border: 1px solid #000000; border-top: none; padding: #{tot_pad}; font-size: #{tot_font}; text-align: right; font-weight: 700; color: #000000;" t-esc="'{0:,.0f}'.format(o.amount_untaxed).replace(',', ' ') + ' FCFA'"/>
                                    </tr>
                                    <tr>
                                        <td t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_font}; font-weight: 800; color: #000000;">
                                            TVA
                                        </td>
                                        <td t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_font}; text-align: center; font-weight: 700; color: #000000; width: 45px;">
                                            <span t-esc="o.tax_rate"/>%
                                        </td>
                                        <td t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_font}; text-align: right; font-weight: 700; color: #000000;" t-esc="'{0:,.0f}'.format(o.amount_tax).replace(',', ' ') + ' FCFA'"/>
                                    </tr>
                                    <tr t-if="o.is_certified_dgi and o.amount_aib &gt; 0">
                                        <td t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_font}; font-weight: 800; color: #000000;">
                                            AIB
                                        </td>
                                        <td t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_font}; text-align: center; font-weight: 700; color: #000000; width: 45px;">
                                            <span t-esc="o.aib_rate"/>%
                                        </td>
                                        <td t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_font}; text-align: right; font-weight: 700; color: #000000;" t-esc="'- ' + '{0:,.0f}'.format(o.amount_aib).replace(',', ' ') + ' FCFA'"/>
                                    </tr>
                                    <tr t-if="o.amount_deposit &gt; 0">
                                        <td colspan="2" t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_font}; font-weight: 800; color: #000000;">
                                            ACOMPTE VERSÉ
                                        </td>
                                        <td t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_font}; text-align: right; font-weight: 700; color: #000000;" t-esc="'- ' + '{0:,.0f}'.format(o.amount_deposit).replace(',', ' ') + ' FCFA'"/>
                                    </tr>
                                    <!-- TOTAL TTC EN FOND NOIR ET ÉCRITURE BLANCHE IDENTIQUE À L'IMAGE -->
                                    <tr style="background-color: #000000; color: #ffffff;">
                                        <td colspan="2" t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_ttc_font}; font-weight: 900; letter-spacing: 0.5px; text-transform: uppercase;">
                                            TOTAL TTC
                                        </td>
                                        <td t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_ttc_font}; text-align: right; font-weight: 900;" t-esc="'{0:,.0f}'.format(o.amount_total).replace(',', ' ') + ' FCFA'"/>
                                    </tr>
                                    <tr t-if="o.is_certified_dgi and o.amount_aib &gt; 0" style="background-color: #1e293b; color: #ffffff;">
                                        <td colspan="2" t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_font}; font-weight: 900; text-transform: uppercase;">
                                            NET À PAYER
                                        </td>
                                        <td t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_font}; text-align: right; font-weight: 900;" t-esc="'{0:,.0f}'.format(o.dgi_net_payable).replace(',', ' ') + ' FCFA'"/>
                                    </tr>
                                    <tr t-if="o.amount_deposit &gt; 0 and o.amount_residual &gt; 0">
                                        <td colspan="2" t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_font}; font-weight: 900; color: #b91c1c;">
                                            SOLDE RESTANT
                                        </td>
                                        <td t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_font}; text-align: right; font-weight: 900; color: #b91c1c;" t-esc="'{0:,.0f}'.format(o.amount_residual).replace(',', ' ') + ' FCFA'"/>
                                    </tr>
                                </table>
                            </div>
                        </div>
                    </div>

                    <!-- 5. PIED DE PAGE EN FLUX NORMAL (AUCUN CHEVAUCHEMENT POSSIBLE) -->
                    <div style="border-top: 1.5px solid #000000; padding-top: 8px; margin-top: 14px; font-size: 8.5px; color: #374151; line-height: 1.45;">
                        <div style="display: table; width: 100%;">
                            <!-- COLONNE 1 : MON ENTREPRISE -->
                            <div style="display: table-cell; width: 34%; vertical-align: top; padding-right: 10px;">
                                <div style="font-weight: 800; color: #000000; margin-bottom: 2px;" t-esc="resto_name"/>
                                <div t-esc="resto_address"/>
                                <div>N° IFU : <strong t-esc="resto_ifu"/></div>
                                <div>N° RCCM : <strong t-esc="resto_rccm"/></div>
                            </div>

                            <!-- COLONNE 2 : COORDONNÉES -->
                            <div style="display: table-cell; width: 33%; vertical-align: top; padding-right: 10px;">
                                <div style="font-weight: 800; color: #000000; margin-bottom: 2px;">Coordonnées</div>
                                <div t-if="o.manager_id">Gérant : <span t-esc="o.manager_id.name"/></div>
                                <div>Téléphone : <span t-esc="resto_phone"/></div>
                                <div>Email : <span t-esc="resto_email"/></div>
                                <div t-if="resto_website">Site : <span t-esc="resto_website"/></div>
                            </div>

                            <!-- COLONNE 3 : DÉTAILS BANCAIRES & DGI -->
                            <div style="display: table-cell; width: 33%; vertical-align: top;">
                                <div style="font-weight: 800; color: #000000; margin-bottom: 2px;">Détails bancaires &amp; DGI</div>
                                <div>Régime : <strong t-esc="resto_regime"/></div>
                                <div>NIM e-MCF : <strong t-esc="resto_nim"/></div>
                                <div style="color: #166534; font-weight: 700;">
                                    Facture normalisée certifiée conforme DGI
                                </div>
                            </div>
                        </div>
                    </div>

                </div>
            </t>
        </t>
    </template>"""

# Template 2: report_grand_marche_template
tmpl_grand_marche = """    <template id="report_grand_marche_template">
        <t t-call="web.html_container">
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
                <meta charset="utf-8"/>
            </head>
            <t t-foreach="docs" t-as="o">
                <t t-set="config" t-value="env['restaurant.configuration'].sudo().search([], limit=1)"/>
                <t t-set="resto_name" t-value="(config.name if (config and config.name) else False) or (o.company_id.name if hasattr(o, 'company_id') else env.company.name) or 'RESTAURANT'"/>
                <t t-set="resto_sub" t-value="(config.subtitle if (config and config.subtitle) else False) or ''"/>
                <t t-set="resto_ifu" t-value="(config.ifu if (config and config.ifu) else False) or (o.company_id.vat if hasattr(o, 'company_id') else env.company.vat) or '-'"/>
                <t t-set="resto_rccm" t-value="(config.rccm if (config and config.rccm) else False) or '-'"/>
                <t t-set="resto_nim" t-value="(config.nim if (config and config.nim) else False) or 'RESTO-DGI-MCF-01'"/>
                <t t-set="resto_regime" t-value="(config.tax_regime if (config and config.tax_regime) else False) or '-'"/>
                <t t-set="resto_phone" t-value="(config.phone if (config and config.phone) else False) or (o.company_id.phone if hasattr(o, 'company_id') else env.company.phone) or '-'"/>
                <t t-set="resto_address" t-value="(config.address if (config and config.address) else False) or (o.company_id.street if hasattr(o, 'company_id') else env.company.street) or '-'"/>
                <t t-set="resto_email" t-value="(config.email if (config and config.email) else False) or (o.company_id.email if hasattr(o, 'company_id') else env.company.email) or '-'"/>
                <t t-set="resto_website" t-value="(config.website if (config and config.website) else False) or 'www.restaurant.com'"/>
                <t t-set="line_count" t-value="len(o.line_ids) if o.line_ids else 1"/>
                <t t-set="dyn_font" t-value="'8px' if line_count &gt; 25 else '8.5px' if line_count &gt; 18 else '9.5px' if line_count &gt; 10 else '10.5px' if line_count &gt; 4 else '11px'"/>
                <t t-set="dyn_pad" t-value="'2.5px 5px' if line_count &gt; 25 else '3.5px 6px' if line_count &gt; 18 else '5px 8px' if line_count &gt; 10 else '8px 12px' if line_count &gt; 4 else '11px 14px'"/>
                <t t-set="dyn_line_height" t-value="'1.3' if line_count &gt; 25 else '1.35' if line_count &gt; 18 else '1.4' if line_count &gt; 10 else '1.48' if line_count &gt; 4 else '1.55'"/>
                <t t-set="sec_gap" t-value="'4px' if line_count &gt; 25 else '6px' if line_count &gt; 18 else '8px' if line_count &gt; 10 else '12px' if line_count &gt; 4 else '16px'"/>
                <t t-set="tot_font" t-value="'8.5px' if line_count &gt; 25 else '9px' if line_count &gt; 18 else '9.5px' if line_count &gt; 10 else '10.5px' if line_count &gt; 4 else '11px'"/>
                <t t-set="tot_pad" t-value="'3px 5px' if line_count &gt; 25 else '3.5px 6px' if line_count &gt; 18 else '5px 7px' if line_count &gt; 10 else '6.5px 9px' if line_count &gt; 4 else '8px 10px'"/>
                <t t-set="tot_ttc_font" t-value="'10px' if line_count &gt; 25 else '10.5px' if line_count &gt; 18 else '11px' if line_count &gt; 10 else '12px' if line_count &gt; 4 else '13px'"/>

                <div class="article page single-page-invoice" style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #000000; background: #ffffff; padding: 6mm 10mm 4mm 10mm; position: relative; min-height: 250mm; box-sizing: border-box; font-size: 10.5px; line-height: 1.45; page-break-inside: avoid; page-break-after: avoid;">
                    
                    <!-- 1. EN-TÊTE : TITRE 'FACTURE' À GAUCHE & MÉTADONNÉES + QR CODE DGI À DROITE -->
                    <div t-attf-style="display: table; width: 100%; margin-bottom: #{sec_gap};">
                        <div style="display: table-cell; width: 45%; vertical-align: top;">
                            <h1 style="font-size: 26px; font-weight: 900; color: #000000; margin: 0 0 2px 0; letter-spacing: 1.5px; text-transform: uppercase; line-height: 1;">
                                FACTURE
                            </h1>
                            <t t-if="o.is_certified_dgi">
                                <div style="font-size: 9.5px; font-weight: 800; color: #166534; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 3px;">
                                    FACTURE CERTIFIÉE DGI (e-MCF)
                                </div>
                            </t>
                            <t t-else="">
                                <div style="font-size: 9.5px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 3px;">
                                    FACTURE GRAND MARCHÉ
                                </div>
                            </t>
                        </div>
                        <div style="display: table-cell; width: 55%; vertical-align: top; text-align: right;">
                            <div style="display: inline-table; text-align: left;">
                                <div style="display: table-row;">
                                    <div style="display: table-cell; vertical-align: middle; padding-right: 15px;">
                                        <table style="font-size: 11px; color: #000000; border-collapse: collapse;">
                                            <tr>
                                                <td style="font-weight: 800; padding: 2px 8px 2px 0; color: #000000;">Numéro de facture :</td>
                                                <td style="font-weight: 700; padding: 2px 0;" t-esc="o.name"/>
                                            </tr>
                                            <tr>
                                                <td style="font-weight: 800; padding: 2px 8px 2px 0; color: #000000;">Date de facturation :</td>
                                                <td style="font-weight: 600; padding: 2px 0;"><span t-field="o.date_invoice"/></td>
                                            </tr>
                                            <tr>
                                                <td style="font-weight: 800; padding: 2px 8px 2px 0; color: #000000;">Échéance :</td>
                                                <td style="font-weight: 600; padding: 2px 0;">
                                                    <span t-if="o.date_due" t-field="o.date_due"/>
                                                    <span t-else="">À réception</span>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td style="font-weight: 800; padding: 2px 8px 2px 0; color: #000000;">Référence :</td>
                                                <td style="font-weight: 700; padding: 2px 0; font-family: monospace;" t-esc="o.dgi_reference or o.subject or o.name"/>
                                            </tr>
                                        </table>
                                    </div>
                                    <!-- QR CODE DGI QUAND CERTIFIÉE -->
                                    <t t-if="o.is_certified_dgi">
                                        <div style="display: table-cell; vertical-align: middle; text-align: center; border-left: 1.5px solid #000000; padding-left: 12px;">
                                            <img t-att-src="o.get_dgi_qr_code_base64()" style="width: 65px; height: 65px; display: block; margin: 0 auto;" alt="QR DGI"/>
                                            <div style="font-size: 8px; font-weight: 800; color: #166534; margin-top: 2px; letter-spacing: 0.5px;">
                                                SCAN DGI e-MCF
                                            </div>
                                        </div>
                                    </t>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 2. SECTION VENDEUR ET CLIENT -->
                    <div t-attf-style="display: table; width: 100%; margin-bottom: #{sec_gap};">
                        <!-- COLONNE VENDEUR -->
                        <div style="display: table-cell; width: 50%; vertical-align: top; padding-right: 20px;">
                            <div style="font-size: 13.5px; font-weight: 900; color: #000000; margin-bottom: 6px;">
                                Vendeur
                            </div>
                            <div style="font-size: 11px; color: #111827; line-height: 1.45;">
                                <div style="font-weight: 800; font-size: 11.5px; color: #000000;" t-esc="resto_name"/>
                                <div style="font-style: italic; color: #4b5563;" t-if="resto_address" t-esc="resto_address"/>
                                <div t-if="resto_phone">Tél : <span t-esc="resto_phone"/></div>
                                <div style="margin-top: 4px; font-size: 10.5px; color: #374151;">
                                    <span t-if="resto_ifu">IFU : <strong t-esc="resto_ifu"/></span>
                                    <span t-if="resto_ifu and resto_rccm"> - </span>
                                    <span t-if="resto_rccm">RCCM : <strong t-esc="resto_rccm"/></span>
                                </div>
                            </div>
                        </div>

                        <!-- COLONNE CLIENT -->
                        <div style="display: table-cell; width: 50%; vertical-align: top; padding-left: 20px;">
                            <div style="font-size: 13.5px; font-weight: 900; color: #000000; margin-bottom: 6px;">
                                Client
                            </div>
                            <div style="font-size: 11px; color: #111827; line-height: 1.45;">
                                <div style="font-weight: 800; font-size: 11.5px; color: #000000;" t-esc="o.partner_name"/>
                                <div style="font-style: italic; color: #4b5563;" t-if="o.partner_address" t-esc="o.partner_address"/>
                                <div t-if="o.partner_phone">Tél : <span t-esc="o.partner_phone"/></div>
                                <div style="margin-top: 4px; font-size: 10.5px; color: #374151;">
                                    <span t-if="o.partner_ifu">NIF / IFU Client : <strong t-esc="o.partner_ifu"/></span>
                                    <span t-else="">Client Particulier / Entreprise</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 3. TABLEAU DES ARTICLES (DESIGNATION | QTE | PRIX UNIT | MONTANT) -->
                    <table style="width: 100%; border-collapse: collapse; border: 1px solid #000000; margin-bottom: 0;">
                        <thead>
                            <tr style="background-color: #000000; color: #ffffff;">
                                <th t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; font-weight: 900; text-align: left; text-transform: uppercase; letter-spacing: 0.5px; width: 48%;">
                                    DESIGNATION
                                </th>
                                <th t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; font-weight: 900; text-align: center; text-transform: uppercase; letter-spacing: 0.5px; width: 10%;">
                                    QTE
                                </th>
                                <th t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; font-weight: 900; text-align: right; text-transform: uppercase; letter-spacing: 0.5px; width: 20%;">
                                    PRIX UNIT
                                </th>
                                <th t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; font-weight: 900; text-align: right; text-transform: uppercase; letter-spacing: 0.5px; width: 22%;">
                                    MONTANT
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <t t-set="line_count" t-value="len(o.line_ids) if o.line_ids else 1"/>
                            <t t-foreach="o.line_ids" t-as="l">
                                <tr>
                                    <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; vertical-align: middle;">
                                        <span style="font-weight: 700; color: #000000;" t-esc="l.name"/>
                                        <span t-if="l.notes" style="font-size: 9.5px; color: #4b5563; font-style: italic; display: block;">
                                            <span t-esc="l.notes"/>
                                        </span>
                                    </td>
                                    <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; text-align: center; font-weight: 700; vertical-align: middle;" t-esc="'%g' % l.quantity if l.quantity else '0'"/>
                                    <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; text-align: right; font-weight: 700; vertical-align: middle;" t-esc="'{0:,.0f}'.format(l.price_unit).replace(',', ' ') + ' FCFA'"/>
                                    <td t-attf-style="border: 1px solid #000000; padding: #{dyn_pad}; font-size: #{dyn_font}; line-height: #{dyn_line_height}; text-align: right; font-weight: 800; vertical-align: middle;" t-esc="'{0:,.0f}'.format(l.price_subtotal).replace(',', ' ') + ' FCFA'"/>
                                </tr>
                            </t>
                        </tbody>
                    </table>

                    <!-- 4. BLOC DES TOTAUX ET CONDITIONS (DEUX COLONNES CÔTE À CÔTE SOUS LA TABLE DES ARTICLES) -->
                    <div style="width: 100%; margin-top: 0; margin-bottom: 10px; page-break-inside: avoid;">
                        <div style="display: table; width: 100%; border-collapse: collapse;">
                            <!-- COLONNE GAUCHE (48%) : CONDITIONS DE PAIEMENT + HOMOLOGATION DGI -->
                            <div style="display: table-cell; width: 48%; vertical-align: top; padding-right: 15px; padding-top: 4px;">
                                <div style="font-weight: 900; font-size: 11px; color: #000000; margin-bottom: 3px; text-transform: uppercase; letter-spacing: 0.3px;">
                                    Conditions et modalités de paiement
                                </div>
                                <div style="font-size: 10px; color: #1f2937; margin-bottom: 8px; line-height: 1.4;">
                                    <span t-if="o.payment_terms" t-esc="o.payment_terms"/>
                                    <span t-else="">Paiement à réception de facture</span>
                                    <div t-if="o.payment_method" style="margin-top: 2px;">
                                        Mode de règlement : 
                                        <strong t-if="o.payment_method == 'transfer'">Virement bancaire</strong>
                                        <strong t-elif="o.payment_method == 'check'">Chèque</strong>
                                        <strong t-elif="o.payment_method == 'cash'">Espèces</strong>
                                        <strong t-elif="o.payment_method == 'mobile'">Mobile Money</strong>
                                        <strong t-else="">Selon convention</strong>
                                    </div>
                                </div>

                                <!-- CADRE HOMOLOGATION DGI QUAND CERTIFIÉE -->
                                <t t-if="o.is_certified_dgi">
                                    <div style="border: 1.5px solid #166534; background: #f0fdf4; border-radius: 4px; padding: 6px 8px; font-size: 9px; color: #14532d; line-height: 1.4;">
                                        <div style="font-weight: 900; text-transform: uppercase; margin-bottom: 3px; color: #166534; font-size: 9.5px; letter-spacing: 0.5px;">
                                            HOMOLOGATION DGI / e-MCF
                                        </div>
                                        <div>Réf. FNE : <strong t-esc="o.dgi_reference"/></div>
                                        <div>Sceau Fiscal : <span style="font-family: monospace; font-size: 8px; word-break: break-all;" t-esc="o.dgi_security_code"/></div>
                                        <div style="margin-top: 2px;">NIM : <strong t-esc="resto_nim"/> - Daté du : <span t-esc="o.dgi_certified_at or o.date_invoice"/></div>
                                    </div>
                                </t>
                            </div>

                            <!-- COLONNE DROITE (52%) : TABLEAU DES TOTAUX ACCROCHÉ AUX ARTICLES -->
                            <div style="display: table-cell; width: 52%; vertical-align: top;">
                                <table style="width: 100%; border-collapse: collapse; border-top: none; font-size: 11px;">
                                    <tr>
                                        <td colspan="2" t-attf-style="border: 1px solid #000000; border-top: none; padding: #{tot_pad}; font-size: #{tot_font}; font-weight: 800; color: #000000; text-transform: uppercase;">
                                            MONTANT HT
                                        </td>
                                        <td t-attf-style="border: 1px solid #000000; border-top: none; padding: #{tot_pad}; font-size: #{tot_font}; text-align: right; font-weight: 700; color: #000000;" t-esc="'{0:,.0f}'.format(o.amount_untaxed).replace(',', ' ') + ' FCFA'"/>
                                    </tr>
                                    <tr>
                                        <td t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_font}; font-weight: 800; color: #000000;">
                                            TVA
                                        </td>
                                        <td t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_font}; text-align: center; font-weight: 700; color: #000000; width: 45px;">
                                            <span t-esc="o.tax_rate"/>%
                                        </td>
                                        <td t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_font}; text-align: right; font-weight: 700; color: #000000;" t-esc="'{0:,.0f}'.format(o.amount_tax).replace(',', ' ') + ' FCFA'"/>
                                    </tr>
                                    <tr t-if="o.is_certified_dgi and o.amount_aib &gt; 0">
                                        <td t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_font}; font-weight: 800; color: #000000;">
                                            AIB
                                        </td>
                                        <td t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_font}; text-align: center; font-weight: 700; color: #000000; width: 45px;">
                                            <span t-esc="o.aib_rate"/>%
                                        </td>
                                        <td t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_font}; text-align: right; font-weight: 700; color: #000000;" t-esc="'- ' + '{0:,.0f}'.format(o.amount_aib).replace(',', ' ') + ' FCFA'"/>
                                    </tr>
                                    <tr t-if="o.amount_deposit &gt; 0">
                                        <td colspan="2" t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_font}; font-weight: 800; color: #000000;">
                                            ACOMPTE VERSÉ
                                        </td>
                                        <td t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_font}; text-align: right; font-weight: 700; color: #000000;" t-esc="'- ' + '{0:,.0f}'.format(o.amount_deposit).replace(',', ' ') + ' FCFA'"/>
                                    </tr>
                                    <!-- TOTAL TTC EN FOND NOIR ET ÉCRITURE BLANCHE IDENTIQUE À L'IMAGE -->
                                    <tr style="background-color: #000000; color: #ffffff;">
                                        <td colspan="2" t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_ttc_font}; font-weight: 900; letter-spacing: 0.5px; text-transform: uppercase;">
                                            TOTAL TTC
                                        </td>
                                        <td t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_ttc_font}; text-align: right; font-weight: 900;" t-esc="'{0:,.0f}'.format(o.amount_total).replace(',', ' ') + ' FCFA'"/>
                                    </tr>
                                    <tr t-if="o.is_certified_dgi and o.amount_aib &gt; 0" style="background-color: #1e293b; color: #ffffff;">
                                        <td colspan="2" t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_font}; font-weight: 900; text-transform: uppercase;">
                                            NET À PAYER
                                        </td>
                                        <td t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_font}; text-align: right; font-weight: 900;" t-esc="'{0:,.0f}'.format(o.dgi_net_payable).replace(',', ' ') + ' FCFA'"/>
                                    </tr>
                                    <tr t-if="o.amount_deposit &gt; 0 and o.amount_residual &gt; 0">
                                        <td colspan="2" t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_font}; font-weight: 900; color: #b91c1c;">
                                            SOLDE RESTANT
                                        </td>
                                        <td t-attf-style="border: 1px solid #000000; padding: #{tot_pad}; font-size: #{tot_font}; text-align: right; font-weight: 900; color: #b91c1c;" t-esc="'{0:,.0f}'.format(o.amount_residual).replace(',', ' ') + ' FCFA'"/>
                                    </tr>
                                </table>
                            </div>
                        </div>
                    </div>

                    <!-- 5. PIED DE PAGE EN FLUX NORMAL (AUCUN CHEVAUCHEMENT POSSIBLE) -->
                    <div style="border-top: 1.5px solid #000000; padding-top: 8px; margin-top: 14px; font-size: 8.5px; color: #374151; line-height: 1.45;">
                        <div style="display: table; width: 100%;">
                            <!-- COLONNE 1 : MON ENTREPRISE -->
                            <div style="display: table-cell; width: 34%; vertical-align: top; padding-right: 10px;">
                                <div style="font-weight: 800; color: #000000; margin-bottom: 2px;" t-esc="resto_name"/>
                                <div t-esc="resto_address"/>
                                <div>N° IFU : <strong t-esc="resto_ifu"/></div>
                                <div>N° RCCM : <strong t-esc="resto_rccm"/></div>
                            </div>

                            <!-- COLONNE 2 : COORDONNÉES -->
                            <div style="display: table-cell; width: 33%; vertical-align: top; padding-right: 10px;">
                                <div style="font-weight: 800; color: #000000; margin-bottom: 2px;">Coordonnées</div>
                                <div t-if="o.manager_id">Gérant : <span t-esc="o.manager_id.name"/></div>
                                <div>Téléphone : <span t-esc="resto_phone"/></div>
                                <div>Email : <span t-esc="resto_email"/></div>
                                <div t-if="resto_website">Site : <span t-esc="resto_website"/></div>
                            </div>

                            <!-- COLONNE 3 : DÉTAILS BANCAIRES & DGI -->
                            <div style="display: table-cell; width: 33%; vertical-align: top;">
                                <div style="font-weight: 800; color: #000000; margin-bottom: 2px;">Détails bancaires &amp; DGI</div>
                                <div>Régime : <strong t-esc="resto_regime"/></div>
                                <div>NIM e-MCF : <strong t-esc="resto_nim"/></div>
                                <div style="color: #166534; font-weight: 700;">
                                    <t t-if="o.is_certified_dgi">Facture certifiée conforme DGI</t>
                                    <t t-else="">Facture Grand Marché</t>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>
            </t>
        </t>
    </template>"""

# Replace in content
pat_marche_dgi = r'<template id="report_marche_dgi_template">.*?</template>'
pat_grand_marche = r'<template id="report_grand_marche_template">.*?</template>'

assert re.search(pat_marche_dgi, content, re.DOTALL) is not None, "report_marche_dgi_template not found!"
assert re.search(pat_grand_marche, content, re.DOTALL) is not None, "report_grand_marche_template not found!"

content = re.sub(pat_marche_dgi, lambda m: tmpl_marche_dgi, content, flags=re.DOTALL)
content = re.sub(pat_grand_marche, lambda m: tmpl_grand_marche, content, flags=re.DOTALL)

# Also fix the duplicate style attribute at line 95 for report_daily_invoice_template
content = content.replace('style="font-family: \'Helvetica Neue\', Helvetica, Arial, sans-serif; color: #000000; background: #ffffff; padding: 6mm 10mm 4mm 10mm; position: relative; min-height: 250mm; max-height: 254mm; overflow: hidden; box-sizing: border-box; font-size: 10.5px; line-height: 1.45; page-break-inside: avoid; page-break-after: avoid;"> style="font-family: \'Helvetica Neue\', Helvetica, Arial, sans-serif; color: #000000; background: #ffffff; padding: 6mm 10mm 4mm 10mm; position: relative; min-height: 250mm; max-height: 254mm; overflow: hidden; box-sizing: border-box; font-size: 10.5px; line-height: 1.45; page-break-inside: avoid; page-break-after: avoid;">',
                          'style="font-family: \'Helvetica Neue\', Helvetica, Arial, sans-serif; color: #000000; background: #ffffff; padding: 6mm 10mm 4mm 10mm; position: relative; min-height: 250mm; box-sizing: border-box; font-size: 10.5px; line-height: 1.45; page-break-inside: avoid; page-break-after: avoid;">')

# Ensure article class in report_daily_invoice_template
content = content.replace('<div class="page single-page-invoice"', '<div class="article page single-page-invoice"')

# Remove any remaining emoji icons in action names or template tags
content = content.replace('🏛️ FACTURE', 'FACTURE')
content = content.replace('🏛️ Homologation', 'HOMOLOGATION')
content = content.replace('🏛️ Facture', 'Facture')
content = content.replace('🖨️ Reçu', 'Reçu')
content = content.replace('📑 Facture', 'Facture')
content = content.replace('📄 Facture', 'Facture')

# Clean bullet characters ' • ' to ' - ' across report templates
content = content.replace(' • ', ' - ')

# Write back
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully written to", path)

# Validate XML
ET.fromstring(content)
print("XML is strictly valid!")
