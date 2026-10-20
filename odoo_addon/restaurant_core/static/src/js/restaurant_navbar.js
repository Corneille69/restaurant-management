/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { NavBar } from "@web/webclient/navbar/navbar";
import { onMounted, onPatched } from "@odoo/owl";

// Patch dynamique et réactif de la NavBar Odoo 17
patch(NavBar.prototype, {
    setup() {
        super.setup();

        onMounted(() => {
            this.syncRestaurantBrand();
        });

        onPatched(() => {
            this.syncRestaurantBrand();
        });
    },

    async onNavBarDropdownItemSelection(menu) {
        if (menu && menu.xmlid === "restaurant_core.menu_restaurant_orders") {
            try {
                await this.actionService.doAction("restaurant_core.action_restaurant_sales_monitoring", {
                    clearBreadcrumbs: true,
                });
                return;
            } catch (e) {
                window.location.href = "/web?db=restaurant_odoo#action=restaurant_core.action_restaurant_sales_monitoring";
                return;
            }
        }
        if (menu && (menu.xmlid === "restaurant_core.menu_restaurant_gerant_orders" || (menu.name && (menu.name.includes("Mes Ventes") || menu.name.includes("Reçus Caisse"))))) {
            try {
                await this.actionService.doAction("restaurant_core.action_restaurant_gerant_own_orders", {
                    clearBreadcrumbs: true,
                });
                return;
            } catch (e) {
                window.location.href = "/web?db=restaurant_odoo#action=restaurant_core.action_restaurant_gerant_own_orders";
                return;
            }
        }
        super.onNavBarDropdownItemSelection(menu);
    },

    async syncRestaurantBrand() {
        try {
            const res = await fetch("/restaurant/api/brand", { cache: "no-store" });
            const data = await res.json();
            if (!data) return;

            const isGerant = Boolean(data.is_gerant);
            if (isGerant) {
                document.documentElement.classList.add("o_resto_gerant_mode");
                document.body.classList.add("o_resto_gerant_mode");
            } else {
                document.documentElement.classList.remove("o_resto_gerant_mode");
                document.body.classList.remove("o_resto_gerant_mode");
            }
            localStorage.setItem("resto_is_gerant", isGerant ? "true" : "false");

            const navbar = this.root.el ? this.root.el.querySelector(".o_main_navbar") : document.querySelector(".o_main_navbar");
            if (!navbar) return;

            let brandContainer = navbar.querySelector(".o_restaurant_brand_container");
            if (!brandContainer) {
                brandContainer = document.createElement("div");
                brandContainer.className = "o_restaurant_brand_container";
                navbar.insertBefore(brandContainer, navbar.firstChild);
            }

            const logoUrl = data.logo_url || "/web/binary/company_logo";
            const name = data.name || "RESTAURANT";
            const subtitle = data.subtitle || "";

            if (isGerant) {
                brandContainer.innerHTML = `
                    <div class="o_restaurant_logo_card">
                        <img src="${logoUrl}" alt="Logo" class="o_restaurant_logo_img"/>
                    </div>
                    <div class="o_restaurant_brand_text_block">
                        <div class="o_restaurant_brand_name">${name}</div>
                        <div class="o_restaurant_brand_badge">ESPACE GÉRANT </div>
                    </div>
                `;
                brandContainer.onclick = () => {
                    this.actionService.doAction("restaurant_core.action_restaurant_gerant_own_orders", {
                        clearBreadcrumbs: true,
                    });
                };

                // Attachement direct sur l'onglet Mes Ventes pour garantir une action immédiate
                const salesTab = navbar.querySelector('[data-menu-xmlid="restaurant_core.menu_restaurant_gerant_orders"], .o_menu_sections [data-hotkey="1"]');
                if (salesTab) {
                    salesTab.style.pointerEvents = "auto";
                    salesTab.style.cursor = "pointer";
                    salesTab.onclick = (e) => {
                        e.preventDefault();
                        e.stopPropagation();
                        this.actionService.doAction("restaurant_core.action_restaurant_gerant_own_orders", {
                            clearBreadcrumbs: true,
                        });
                    };
                }

                // Bouton d'accès direct caisse
                const systray = navbar.querySelector(".o_menu_systray");
                let quickBtn = navbar.querySelector(".o_gerant_quick_pos_btn");
                if (!quickBtn) {
                    quickBtn = document.createElement("a");
                    quickBtn.className = "o_gerant_quick_pos_btn";
                    quickBtn.href = "/pos/ui?config_id="+ (data.pos_config_id || 2);
                    quickBtn.innerHTML = " Ouvrir la Caisse ";
                    if (systray) {
                        navbar.insertBefore(quickBtn, systray);
                    } else {
                        navbar.appendChild(quickBtn);
                    }
                }

                // Nettoyage de tout bouton redondant pour utiliser l'icône de messagerie native d'Odoo
                const oldChatBtn = navbar.querySelector(".o_resto_chat_btn");
                if (oldChatBtn) oldChatBtn.remove();
            } else {
                brandContainer.innerHTML = `
                    <div class="o_restaurant_logo_card">
                        <img src="${logoUrl}" alt="Logo" class="o_restaurant_logo_img"/>
                    </div>
                    <div class="o_restaurant_brand_name">${name}</div>
                    <div class="o_restaurant_brand_subtitle" style="display: ${subtitle ? 'block' : 'none'}">${subtitle}</div>
                `;
                brandContainer.onclick = () => {
                    window.location.hash = "#action=restaurant_core.action_restaurant_sales_dashboard";
                };

                const quickBtn = navbar.querySelector(".o_gerant_quick_pos_btn");
                if (quickBtn) quickBtn.remove();

                const oldChatBtn = navbar.querySelector(".o_resto_chat_btn");
                if (oldChatBtn) oldChatBtn.remove();
            }

            localStorage.setItem("resto_brand_name", name);
            localStorage.setItem("resto_brand_subtitle", subtitle);
            localStorage.setItem("resto_brand_logo", logoUrl);
        } catch (e) {
            // Silencieux si appel en cours
        }
    }
});

// =========================================================================
// GESTION PRIORITÉ FRANÇAIS (#1) & ANGLAIS (#2) DANS LES PRÉFÉRENCES
// =========================================================================
(function setupLanguagePriorityWatcher() {
    function reorderLanguageOptions() {
        const selects = document.querySelectorAll('select[name="lang"], select#lang, .modal select');
        selects.forEach(select => {
            if (!select) return;
            const options = Array.from(select.options);
            if (options.length <= 1) return;

            const hasLangOptions = options.some(opt => 
                (opt.value && (opt.value.includes('fr') || opt.value.includes('en'))) ||
                (opt.text && (opt.text.toLowerCase().includes('fran') || opt.text.toLowerCase().includes('engl')))
            );
            if (!hasLangOptions) return;

            // Classement : Français (fr_FR) en PREMIER (#1), puis autres français, puis Anglais (#2)
            const sorted = options.slice().sort((a, b) => {
                const valA = (a.value || '').toLowerCase();
                const textA = (a.text || '').toLowerCase();
                const valB = (b.value || '').toLowerCase();
                const textB = (b.text || '').toLowerCase();

                function getScore(val, text) {
                    if (val === 'fr_fr' || (text.includes('fran') && !text.includes('canada'))) return 1;
                    if (val.startsWith('fr') || text.includes('fran')) return 2;
                    if (val === 'en_us' || text.includes('engl') || text.includes('anglais')) return 3;
                    if (val.startsWith('en')) return 4;
                    return 10;
                }

                return getScore(valA, textA) - getScore(valB, textB);
            });

            let orderChanged = false;
            for (let i = 0; i < options.length; i++) {
                if (options[i] !== sorted[i]) {
                    orderChanged = true;
                    break;
                }
            }

            if (orderChanged) {
                const currentVal = select.value;
                select.innerHTML = '';
                sorted.forEach(opt => select.appendChild(opt));
                if (currentVal) {
                    select.value = currentVal;
                }
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', reorderLanguageOptions);
    } else {
        reorderLanguageOptions();
    }

    const observer = new MutationObserver(() => {
        reorderLanguageOptions();
    });

    observer.observe(document.documentElement, {
        childList: true,
        subtree: true
    });
})();