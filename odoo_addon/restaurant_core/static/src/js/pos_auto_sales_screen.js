/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { FloorScreen } from "@pos_restaurant/app/floor_screen/floor_screen";
import { ReceiptScreen } from "@point_of_sale/app/screens/receipt_screen/receipt_screen";

// 1. Redirection automatique et permanente : INTERDICTION TOTALE DU FLOOR SCREEN (Plan de table)
patch(FloorScreen.prototype, {
    async onMounted() {
        super.onMounted();
        const tables = Object.values(this.pos.tables_by_id || {});
        const table1 = tables.find(t => String(t.name).trim() === '1') || tables[0];
        if (table1) {
            setTimeout(async () => {
                try {
                    await this.pos.setTable(table1);
                    if (!this.pos.get_order()) {
                        this.pos.add_new_order();
                    }
                    this.pos.showScreen("ProductScreen");
                } catch (e) {
                    console.warn("Auto-redirection vers ProductScreen:", e);
                }
            }, 30);
        }
    }
});

// 2. Écran de Reçu : Après validation d'un paiement ou clic sur "Nouvelle commande", retour direct sur la page de vente
patch(ReceiptScreen.prototype, {
    get nextScreen() {
        return { name: "ProductScreen" };
    },
    async orderDone() {
        const tables = Object.values(this.pos.tables_by_id || {});
        const table1 = this.pos.table || tables.find(t => String(t.name).trim() === '1') || tables[0];
        this.pos.removeOrder(this.currentOrder);
        if (table1) {
            await this.pos.setTable(table1);
        }
        this.pos.add_new_order();
        this.pos.resetProductScreenSearch();
        this.pos.showScreen("ProductScreen");
    }
});
