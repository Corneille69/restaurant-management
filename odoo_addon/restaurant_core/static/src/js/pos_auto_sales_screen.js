/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { FloorScreen } from "@pos_restaurant/app/floor_screen/floor_screen";
import { ReceiptScreen } from "@point_of_sale/app/screens/receipt_screen/receipt_screen";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { onMounted } from "@odoo/owl";

// 1. Démarrage direct et automatique sur l'écran de vente (ProductScreen)
patch(PosStore.prototype, {
    async setup() {
        await super.setup(...arguments);
        if (this.config && this.config.module_pos_restaurant) {
            try {
                const tables = Object.values(this.tables_by_id || {});
                const table1 = tables.find(t => String(t.name).trim() === '1') || tables[0];
                if (table1) {
                    await this.setTable(table1);
                    if (!this.get_order()) {
                        this.add_new_order();
                    }
                } else if (!this.get_order()) {
                    this.add_new_order();
                }
                this.showScreen("ProductScreen");
            } catch (err) {
                console.warn("Auto-redirection setup vers ProductScreen:", err);
            }
        }
    }
});

// 2. Filet de sécurité au cas où FloorScreen serait affiché
patch(FloorScreen.prototype, {
    setup() {
        super.setup();
        onMounted(() => {
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
        });
    }
});

// 3. Écran de Reçu : Après validation d'un paiement ou clic sur "Nouvelle commande", retour direct sur la page de vente
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
