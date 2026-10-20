/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { PaymentScreenStatus } from "@point_of_sale/app/screens/payment_screen/payment_status/payment_status";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { Navbar } from "@point_of_sale/app/navbar/navbar";
import { ProductCard } from "@point_of_sale/app/generic_components/product_card/product_card";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { Orderline } from "@point_of_sale/app/store/models";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { _t } from "@web/core/l10n/translation";
import { onMounted } from "@odoo/owl";

// 1. Améliorations de l'écran de vente (Recherche rapide, raccourcis et synchronisation en direct des stocks)
patch(ProductScreen.prototype, {
    setup() {
        super.setup();

        onMounted(() => {
            this.enhancePosSearchAndDisplay();
            this.setupRealtimeStockSync();
        });
    },

    setupRealtimeStockSync() {
        if (window.__pos_stock_sync_interval) {
            clearInterval(window.__pos_stock_sync_interval);
        }
        const syncStocks = async () => {
            try {
                if (this.pos && this.pos.orm && this.pos.db) {
                    const stockMap = await this.pos.orm.call("pos.session", "get_realtime_dish_stocks", []);
                    if (stockMap && typeof stockMap === "object") {
                        if (!this.pos.productStocks) {
                            this.pos.productStocks = {};
                        }
                        for (const [prodId, qty] of Object.entries(stockMap)) {
                            const id = Number(prodId);
                            const numQty = Number(qty);
                            if (this.pos.productStocks[id] !== numQty) {
                                this.pos.productStocks[id] = numQty;
                            }
                            const prod = this.pos.db.get_product_by_id(id);
                            if (prod && prod.available_quantity !== numQty) {
                                prod.available_quantity = numQty;
                            }
                        }
                    }
                }
            } catch (err) {
                // Silencieux pour ne pas perturber l'expérience de caisse
            }
        };

        // Synchronisation initiale et périodique toutes les 2.5 secondes en temps réel
        syncStocks();
        window.__pos_stock_sync_interval = setInterval(syncStocks, 2500);
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

// 2. Carte Produit : Affichage dynamique réactif du stock et état de rupture
patch(ProductCard.prototype, {
    setup() {
        if (super.setup) {
            super.setup();
        }
        try {
            this.pos = usePos();
        } catch (e) {
            this.pos = null;
        }
    },
    get productObj() {
        if (this.pos && this.pos.db && this.props.productId) {
            return this.pos.db.get_product_by_id(this.props.productId);
        }
        return null;
    },
    get formattedPrice() {
        if (this.productObj && this.productObj.lst_price !== undefined) {
            return this.env.utils.formatCurrency(this.productObj.lst_price);
        }
        return this.props.price;
    },
    get stockQty() {
        if (this.pos && this.pos.productStocks && (this.props.productId in this.pos.productStocks)) {
            const val = this.pos.productStocks[this.props.productId];
            if (val !== undefined && val !== null) {
                return Math.max(0, Number(val));
            }
        }
        const p = this.productObj;
        if (p && p.available_quantity !== undefined && p.available_quantity !== null) {
            return Math.max(0, Number(p.available_quantity));
        }
        return 20;
    },
    get isOutOfStock() {
        return this.stockQty <= 0;
    }
});

// 3. PosStore : Initialisation réactive des stocks, blocage d'ajout pour produits en rupture (Stock 0)
patch(PosStore.prototype, {
    async setup() {
        await super.setup(...arguments);
        if (!this.productStocks) {
            this.productStocks = {};
        }
    },

    async _processData(loadedData) {
        await super._processData(...arguments);
        if (!this.productStocks) {
            this.productStocks = {};
        }
        if (this.db) {
            for (const prod of Object.values(this.db.product_by_id || {})) {
                if (prod && prod.id) {
                    const qty = (prod.available_quantity !== undefined && prod.available_quantity !== null)
                        ? Number(prod.available_quantity)
                        : 20;
                    this.productStocks[prod.id] = qty;
                    prod.available_quantity = qty;
                }
            }
        }
    },

    async addProductToCurrentOrder(product, options = {}) {
        if (Number.isInteger(product)) {
            product = this.db.get_product_by_id(product);
        }
        if (!product) {
            return;
        }

        const pId = product.id;
        const stock = (this.productStocks && this.productStocks[pId] !== undefined)
            ? Number(this.productStocks[pId])
            : ((product.available_quantity !== undefined && product.available_quantity !== null) ? Number(product.available_quantity) : 20);

        // Signalement de rupture totale uniquement si le stock est strictement à 0
        if (stock <= 0) {
            await this.env.services.popup.add(ErrorPopup, {
                title: _t("Rupture de Stock !"),
                body: _t("Le plat ou la boisson « %s » est actuellement en rupture de stock (0 présent dans le restaurant).\n\nImpossible de l'ajouter à la commande.\nDemandez à l'administrateur d'entrer de nouveaux stocks.", product.display_name),
                confirmText: _t("Compris"),
            });
            return;
        }

        // Vérifier si la quantité demandée dépasse le stock disponible
        const currentOrder = this.get_order();
        if (currentOrder) {
            const line = currentOrder.get_orderlines().find(l => l.product.id === product.id);
            const inCart = line ? line.get_quantity() : 0;
            const toAdd = (options && options.quantity) ? options.quantity : 1;
            if (inCart + toAdd > stock) {
                await this.env.services.popup.add(ErrorPopup, {
                    title: _t("Stock Insuffisant !"),
                    body: _t("Stock maximal disponible pour « %s » : %s unité(s).\n\nVous avez déjà %s unité(s) dans le panier.\nImpossible d'en ajouter davantage sans réapprovisionnement.", product.display_name, stock, inCart),
                    confirmText: _t("Compris"),
                });
                return;
            }
        }

        return super.addProductToCurrentOrder(product, options);
    }
});

// 4. Contrôle au pavé numérique lors de la modification directe de la quantité
patch(Orderline.prototype, {
    set_quantity(quantity, keep_price) {
        const quant = typeof quantity === "number" ? quantity : parseFloat(quantity || 0);
        if (quant > 0 && this.product) {
            const pId = this.product.id;
            const maxStock = (this.pos && this.pos.productStocks && this.pos.productStocks[pId] !== undefined)
                ? Number(this.pos.productStocks[pId])
                : ((this.product.available_quantity !== undefined && this.product.available_quantity !== null) ? Number(this.product.available_quantity) : null);
            if (maxStock !== null && quant > maxStock) {
                this.env.services.popup.add(ErrorPopup, {
                    title: _t("Quantité Supérieure au Stock !"),
                    body: _t("Stock maximal disponible pour « %s » : %s unité(s).\n\nVous ne pouvez pas commander %s unité(s).", this.product.display_name, maxStock, quant),
                    confirmText: _t("Compris"),
                });
                return false;
            }
        }
        return super.set_quantity(quantity, keep_price);
    }
});

// 5. Améliorations de l'écran de paiement (Affichage en grand du montant saisi et décrémentation directe du stock)
patch(PaymentScreenStatus.prototype, {
    get enteredAmountText() {
        const order = this.props && this.props.order;
        const line = order && (order.selected_paymentline || (order.paymentlines && order.paymentlines[0]));
        if (line) {
            return this.env.utils.formatCurrency(line.get_amount());
        }
        return this.env.utils.formatCurrency(0);
    },
    get enteredAmount() {
        const order = this.props && this.props.order;
        const line = order && (order.selected_paymentline || (order.paymentlines && order.paymentlines[0]));
        return line ? line.get_amount() : 0;
    }
});

// 6. Paiement simplifié en Espèces directes et décrémentation en temps réel des stocks vendus
patch(PaymentScreen.prototype, {
    setup() {
        super.setup();
        onMounted(() => {
            if (this.currentOrder && this.payment_methods_from_config.length >0) {
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
    },

    async _finalizeValidation() {
        // Décrémentation visuelle immédiate des stocks dès confirmation du paiement
        if (this.currentOrder) {
            for (const line of this.currentOrder.get_orderlines()) {
                const prod = line.product;
                if (prod) {
                    const pId = prod.id;
                    const cur = (this.pos && this.pos.productStocks && this.pos.productStocks[pId] !== undefined)
                        ? this.pos.productStocks[pId]
                        : (prod.available_quantity || 0);
                    const newQty = Math.max(0, Number(cur) - line.get_quantity());
                    if (this.pos && this.pos.productStocks) {
                        this.pos.productStocks[pId] = newQty;
                    }
                    prod.available_quantity = newQty;
                }
            }
        }
        return super._finalizeValidation();
    }
});

// 7. Redirection garantie vers Mes Ventes au clic sur Accueil
patch(Navbar.prototype, {
    goToMySales(ev) {
        if (ev) {
            ev.preventDefault();
            ev.stopPropagation();
        }
        window.location.assign("/web?db=restaurant_odoo#action=restaurant_core.action_restaurant_gerant_own_orders");
    }
});

// 8. Filet de sécurité supplémentaire : Capture globale immédiate du clic Accueil
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