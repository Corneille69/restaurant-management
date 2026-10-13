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
        if (menu && (menu.xmlid === "restaurant_core.menu_restaurant_gerant_orders" || (menu.name && menu.name.includes("Ventes")))) {
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
                        <div class="o_restaurant_brand_badge">✦ ESPACE GÉRANT ✦</div>
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
                    quickBtn.href = "/pos/ui?config_id=2";
                    quickBtn.innerHTML = "⚡ Ouvrir la Caisse ➔";
                    if (systray) {
                        navbar.insertBefore(quickBtn, systray);
                    } else {
                        navbar.appendChild(quickBtn);
                    }
                }

                // Bouton d'accès direct Messages & Appel Vidéo (Admin <-> Gérant)
                let chatBtn = navbar.querySelector(".o_resto_chat_btn");
                if (!chatBtn) {
                    chatBtn = document.createElement("a");
                    chatBtn.className = "o_resto_chat_btn";
                    chatBtn.href = "/web?db=restaurant_odoo#action=mail.action_discuss";
                    chatBtn.style.cssText = "background: linear-gradient(135deg, #f59e0b, #d97706); color: black; font-weight: 800; font-size: 0.82rem; padding: 0.4rem 0.85rem; border-radius: 8px; margin-right: 0.75rem; text-decoration: none; display: inline-flex; align-items: center; gap: 0.35rem; box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);";
                    chatBtn.innerHTML = "💬 SMS &amp; Appel Vidéo (Admin)";
                    if (systray) {
                        navbar.insertBefore(chatBtn, systray);
                    } else {
                        navbar.appendChild(chatBtn);
                    }
                }
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

                const systray = navbar.querySelector(".o_menu_systray");
                let chatBtn = navbar.querySelector(".o_resto_chat_btn");
                if (!chatBtn) {
                    chatBtn = document.createElement("a");
                    chatBtn.className = "o_resto_chat_btn";
                    chatBtn.href = "/web?db=restaurant_odoo#action=mail.action_discuss";
                    chatBtn.style.cssText = "background: linear-gradient(135deg, #10b981, #059669); color: white; font-weight: 800; font-size: 0.82rem; padding: 0.4rem 0.85rem; border-radius: 8px; margin-right: 0.75rem; text-decoration: none; display: inline-flex; align-items: center; gap: 0.35rem; box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);";
                    chatBtn.innerHTML = "💬 SMS &amp; Appel Vidéo (Gérants)";
                    if (systray) {
                        navbar.insertBefore(chatBtn, systray);
                    } else {
                        navbar.appendChild(chatBtn);
                    }
                }
            }

            localStorage.setItem("resto_brand_name", name);
            localStorage.setItem("resto_brand_subtitle", subtitle);
            localStorage.setItem("resto_brand_logo", logoUrl);
        } catch (e) {
            // Silencieux si appel en cours
        }
    }
});
