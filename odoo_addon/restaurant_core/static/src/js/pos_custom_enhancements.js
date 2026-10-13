/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { PaymentScreenStatus } from "@point_of_sale/app/screens/payment_screen/payment_status/payment_status";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { Navbar } from "@point_of_sale/app/navbar/navbar";
import { onMounted } from "@odoo/owl";

// 1. Améliorations de l'écran de vente (Recherche rapide et raccourcis)
patch(ProductScreen.prototype, {
    setup() {
        super.setup();

        onMounted(() => {
            this.enhancePosSearchAndDisplay();
        });
    },

    enhancePosSearchAndDisplay() {
        const updateSearchInput = () => {
            const searchInputs = document.querySelectorAll('.pos .search-bar input, .pos .input-container input');
            searchInputs.forEach(inp => {
                const targetPlaceholder = 'Rechercher un plat, boisson... (Nom ou /)';
                if (inp && inp.placeholder !== targetPlaceholder) {
                    inp.placeholder = targetPlaceholder;
                    inp.setAttribute('aria-label', 'Rechercher un plat');
                }
            });
        };

        updateSearchInput();
        setInterval(updateSearchInput, 1500);

        window.addEventListener('keydown', (e) => {
            if ((e.key === '/' || e.key === 'F3') && document.activeElement && document.activeElement.tagName !== 'INPUT') {
                const searchInput = document.querySelector('.pos .search-bar input, .pos .input-container input');
                if (searchInput) {
                    e.preventDefault();
                    searchInput.focus();
                    searchInput.select();
                }
            }
        });
    }
});

// 2. Améliorations de l'écran de paiement (Affichage en grand du montant saisi)
patch(PaymentScreenStatus.prototype, {
    get enteredAmountText() {
        const line = this.props.order.selected_paymentline || (this.props.order.paymentlines && this.props.order.paymentlines[0]);
        if (line) {
            return this.env.utils.formatCurrency(line.get_amount());
        }
        return this.env.utils.formatCurrency(0);
    },
    get enteredAmount() {
        const line = this.props.order.selected_paymentline || (this.props.order.paymentlines && this.props.order.paymentlines[0]);
        return line ? line.get_amount() : 0;
    }
});

// 3. Paiement simplifié en Espèces directes : Initialisation à 0 du grand champ sans aucun mélange
patch(PaymentScreen.prototype, {
    setup() {
        super.setup();
        onMounted(() => {
            if (this.currentOrder && this.payment_methods_from_config.length > 0) {
                if (this.currentOrder.paymentlines.length === 0) {
                    this.addNewPaymentLine(this.payment_methods_from_config[0]);
                }
                const selectedLine = this.currentOrder.selected_paymentline || this.currentOrder.paymentlines[0];
                if (selectedLine) {
                    // Remise à zéro pour que le grand champ soit strictement réservé à la saisie manuelle du gérant
                    selectedLine.set_amount(0);
                    this.numberBuffer.reset();
                }
            }
        });
    }
});

// 4. Redirection garantie vers Mes Ventes au clic
patch(Navbar.prototype, {
    goToMySales(ev) {
        if (ev) {
            ev.preventDefault();
            ev.stopPropagation();
        }
        window.location.assign("/web?db=restaurant_odoo#action=restaurant_core.action_restaurant_gerant_own_orders");
    }
});

// 5. Filet de sécurité supplémentaire : Capture globale immédiate du clic
if (typeof window !== "undefined") {
    window.addEventListener("click", function(ev) {
        const btn = ev.target && ev.target.closest && ev.target.closest(".pos-sales-nav-btn, .pos-home-nav-btn, [data-action='go-to-my-sales']");
        if (btn) {
            ev.preventDefault();
            ev.stopPropagation();
            window.location.assign("/web?db=restaurant_odoo#action=restaurant_core.action_restaurant_gerant_own_orders");
        }
    }, true);
}

