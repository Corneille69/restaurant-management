import re
import py_compile

filepath = 'backend/app/web/router.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update .corporate-invoice-paper CSS to enforce min-height 250mm (85% of A4) and flex stretching
old_css_rule = r'\.corporate-invoice-paper\s*\{[^}]*\}'
new_css_rule = """.corporate-invoice-paper {
            background-color: #ffffff;
            color: #000000;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            padding: 8mm 12mm 8mm 12mm;
            border-radius: 4px;
            box-shadow: 0 20px 45px -10px rgba(0, 0, 0, 0.35);
            max-width: 820px;
            width: 100%;
            min-height: 250mm; /* Occupe 85% de la hauteur de la feuille A4 (297mm * 0.85 = 252.45mm) */
            margin: 0 auto;
            position: relative;
            border: 1px solid #000000;
            box-sizing: border-box;
            font-size: 11px;
            line-height: 1.5;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            page-break-inside: avoid;
            page-break-after: avoid;
        }"""

content = re.sub(old_css_rule, new_css_rule, content, count=1)

# 2. Update print CSS
old_print_rule = r'@page\s*\{[^}]*\}\s*@media print\s*\{.*?(?=\s*</style>)'
new_print_rule = """@page {
            size: A4 portrait;
            margin: 5mm 8mm 5mm 8mm;
        }
        @media print {
            html, body {
                height: 100% !important;
                margin: 0 !important;
                padding: 0 !important;
                background: #ffffff !important;
            }
            body * { visibility: hidden !important; }
            #invoiceModal:not(.hidden), #invoiceModal:not(.hidden) * { visibility: visible !important; }
            #modalGlobalInvoicePrint:not(.hidden), #modalGlobalInvoicePrint:not(.hidden) * { visibility: visible !important; }
            #dgiInvoiceModal:not(.hidden), #dgiInvoiceModal:not(.hidden) * { visibility: visible !important; }
            #receiptModal:not(.hidden), #receiptModal:not(.hidden) * { visibility: visible !important; }

            #invoiceModal:not(.hidden),
            #modalGlobalInvoicePrint:not(.hidden),
            #dgiInvoiceModal:not(.hidden) {
                position: absolute !important;
                left: 0 !important;
                top: 0 !important;
                width: 100% !important;
                background: white !important;
                padding: 0 !important;
                box-shadow: none !important;
                margin: 0 !important;
                page-break-after: avoid !important;
                page-break-inside: avoid !important;
            }
            .corporate-invoice-paper {
                border: none !important;
                box-shadow: none !important;
                padding: 4mm 6mm !important;
                background: #ffffff !important;
                max-width: 100% !important;
                width: 100% !important;
                height: 252mm !important; /* Occupe exactement 85% de la feuille A4 */
                min-height: 252mm !important;
                max-height: 254mm !important;
                display: flex !important;
                flex-direction: column !important;
                justify-content: space-between !important;
                overflow: hidden !important;
                page-break-inside: avoid !important;
                page-break-after: avoid !important;
                margin: 0 !important;
                box-sizing: border-box !important;
                line-height: 1.5 !important;
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }
            .corporate-inv-table th,
            .corporate-inv-totals-table tr.total-ttc-row,
            .corporate-inv-totals-table tr.total-ttc-row td {
                background-color: #000000 !important;
                color: #ffffff !important;
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }
            .modal-actions-bar { display: none !important; }
            #receiptModal:not(.hidden) { position: absolute !important; left: 50% !important; transform: translateX(-50%) !important; top: 0 !important; width: 340px !important; background: white !important; padding: 10px !important; }
            button { display: none !important; }
        }"""

content = re.sub(old_print_rule, new_print_rule, content, flags=re.DOTALL)

# 3. Update JavaScript openRestaurantInvoiceModal scaling logic
old_js_open = r'// 6\. Tableau des articles avec réduction progressive.*?// 7\. Totaux Financiers DGI'
new_js_open = """// 6. Tableau des articles avec adaptation dynamique à 85% de la feuille A4 (textes nets, sans chevauchement)
            const itemsTableBody = document.getElementById('invPaperItemsBody');
            const items = order.items || [];
            const itemCount = items.length || 1;

            // Barème dynamique : tire l'affiche vers le bas sur 85% de la feuille, grand confort de lecture, jamais superposé
            let rowFontSize = '12px';
            let rowPadding = '12px 14px';
            let thFontSize = '12px';
            let thPadding = '12px 14px';
            let secMargin = '1.75rem';
            let headerMargin = '1.75rem';
            let titleFontSize = '2.4rem';
            let qrSize = 78;
            let rowLineHeight = '1.55';

            if (itemCount > 25) {
                rowFontSize = '9px';
                rowPadding = '3px 6px';
                thFontSize = '9px';
                thPadding = '3.5px 6px';
                secMargin = '0.55rem';
                headerMargin = '0.65rem';
                titleFontSize = '1.75rem';
                qrSize = 58;
                rowLineHeight = '1.35';
            } else if (itemCount > 18) {
                rowFontSize = '9.5px';
                rowPadding = '4.5px 8px';
                thFontSize = '9.5px';
                thPadding = '5px 8px';
                secMargin = '0.85rem';
                headerMargin = '0.95rem';
                titleFontSize = '1.9rem';
                qrSize = 65;
                rowLineHeight = '1.4';
            } else if (itemCount > 10) {
                rowFontSize = '10.5px';
                rowPadding = '6.5px 10px';
                thFontSize = '10.5px';
                thPadding = '7.5px 10px';
                secMargin = '1.15rem';
                headerMargin = '1.25rem';
                titleFontSize = '2.1rem';
                qrSize = 70;
                rowLineHeight = '1.45';
            } else if (itemCount > 5) {
                rowFontSize = '11.5px';
                rowPadding = '9px 12px';
                thFontSize = '11.5px';
                thPadding = '10px 12px';
                secMargin = '1.45rem';
                headerMargin = '1.5rem';
                titleFontSize = '2.25rem';
                qrSize = 74;
                rowLineHeight = '1.5';
            }

            // Application dynamique aux conteneurs de la facture pour occuper 85% de la page
            const invModalPaper = document.querySelector('#invoiceModal .corporate-invoice-paper');
            if (invModalPaper) {
                invModalPaper.style.fontSize = (itemCount > 18 ? '9.5px' : (itemCount > 10 ? '10.5px' : '11.5px'));
                invModalPaper.style.minHeight = '250mm';
            }
            const invTitle = document.querySelector('#invoiceModal h1');
            if (invTitle) invTitle.style.fontSize = titleFontSize;
            
            const invHdrSec = document.getElementById('invPaperHeaderSec');
            if (invHdrSec) invHdrSec.style.marginBottom = headerMargin;
            const invVendorClientSec = document.getElementById('invPaperVendorClientSec');
            if (invVendorClientSec) invVendorClientSec.style.marginBottom = secMargin;
            const invTotalsSec = document.getElementById('invPaperTotalsSec');
            if (invTotalsSec) invTotalsSec.style.marginBottom = secMargin;
            const invCondSec = document.getElementById('invPaperCondBox');
            if (invCondSec) invCondSec.style.marginBottom = secMargin;

            const invHeaders = document.querySelectorAll('#invoiceModal .corporate-inv-table th');
            invHeaders.forEach(th => {
                th.style.fontSize = thFontSize;
                th.style.padding = thPadding;
                th.style.lineHeight = rowLineHeight;
            });
            const invTotalsCells = document.querySelectorAll('#invoiceModal .corporate-inv-totals-table td');
            invTotalsCells.forEach(td => {
                td.style.fontSize = (itemCount > 18 ? '9.5px' : '11.5px');
                td.style.padding = (itemCount > 18 ? '4.5px 7px' : (itemCount > 10 ? '7px 10px' : '10px 12px'));
                td.style.lineHeight = rowLineHeight;
            });

            // Re-génération du QR code avec taille adaptée
            const qrContainerScaled = document.getElementById('invPaperQrContainer');
            if (qrContainerScaled) {
                const qrTextScaled = encodeURIComponent(`DGI-FNE|IFU:${ifuVal}|RCCM:${rccmVal}|FACT:${invNum}|DATE:${formattedDate}|TTC:${Math.round(order.total_amount || 0)}|REF:${dgiRef}`);
                qrContainerScaled.innerHTML = `<img src="https://api.qrserver.com/v1/create-qr-code/?size=120x120&margin=1&data=${qrTextScaled}" style="width: ${qrSize}px; height: ${qrSize}px; display: block; margin: 0 auto;" alt="QR DGI" />`;
            }

            if (items.length === 0) {
                itemsTableBody.innerHTML = `
                    <tr>
                        <td style="border: 1px solid #000000; padding: 14px 14px; font-size: ${rowFontSize}; line-height: ${rowLineHeight}; font-weight: 700; color: #000000;">Consommations &amp; Ventes Restauration</td>
                        <td style="border: 1px solid #000000; padding: 14px 8px; font-size: ${rowFontSize}; line-height: ${rowLineHeight}; text-align: center; font-weight: 700;">1</td>
                        <td style="border: 1px solid #000000; padding: 14px 10px; font-size: ${rowFontSize}; line-height: ${rowLineHeight}; text-align: right; font-weight: 700;">${Math.round(order.total_amount).toLocaleString('fr-FR')} FCFA</td>
                        <td style="border: 1px solid #000000; padding: 14px 14px; font-size: ${rowFontSize}; line-height: ${rowLineHeight}; text-align: right; font-weight: 800;">${Math.round(order.total_amount).toLocaleString('fr-FR')} FCFA</td>
                    </tr>
                `;
            } else {
                itemsTableBody.innerHTML = items.map(it => {
                    const name = it.item_name || it.menu_item_name || (it.menu_item ? it.menu_item.name : ('Plat #' + it.menu_item_id));
                    const qty = it.quantity || 1;
                    const price = it.unit_price || 0;
                    const lineTotal = it.subtotal || (qty * price);
                    return `
                        <tr>
                            <td style="border: 1px solid #000000; padding: ${rowPadding}; font-size: ${rowFontSize}; line-height: ${rowLineHeight}; font-weight: 700; color: #000000;">${name}</td>
                            <td style="border: 1px solid #000000; padding: ${rowPadding}; font-size: ${rowFontSize}; line-height: ${rowLineHeight}; text-align: center; font-weight: 700;">${qty}</td>
                            <td style="border: 1px solid #000000; padding: ${rowPadding}; font-size: ${rowFontSize}; line-height: ${rowLineHeight}; text-align: right; font-weight: 700;">${Math.round(price).toLocaleString('fr-FR')} FCFA</td>
                            <td style="border: 1px solid #000000; padding: ${rowPadding}; font-size: ${rowFontSize}; line-height: ${rowLineHeight}; text-align: right; font-weight: 800;">${Math.round(lineTotal).toLocaleString('fr-FR')} FCFA</td>
                        </tr>
                    `;
                }).join('');
            }

            // 7. Totaux Financiers DGI"""

content = re.sub(old_js_open, new_js_open, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

py_compile.compile(filepath, doraise=True)
print("Updated backend/app/web/router.py successfully!")
