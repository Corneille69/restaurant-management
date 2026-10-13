/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { MessagingMenu } from "@mail/core/web/messaging_menu";

// Désactivation complète d'OdooBot dans le menu de messagerie
// Seuls les vrais messages des gérants du restaurant sont comptabilisés
patch(MessagingMenu.prototype, {
    get canPromptToInstall() {
        return false;
    },
    get shouldAskPushPermission() {
        return false;
    },
    get installationRequest() {
        return { isShown: false };
    },
    get notificationRequest() {
        return { isShown: false };
    },
    get counter() {
        // Ne compter que les messages non lus légitimes (gérants du restaurant)
        // en ignorant tout artifice de prompt OdooBot
        const unreadThreads = Object.values(this.store.Thread.records).filter(
            (thread) => thread.is_pinned && thread.message_unread_counter > 0 &&
            (!thread.displayName || !thread.displayName.toLowerCase().includes('odoobot'))
        ).length;
        const inboxCounter = this.store.discuss?.inbox?.counter || 0;
        return unreadThreads + inboxCounter;
    },
    getThreads() {
        const threads = super.getThreads();
        // Masquer complètement tout fil de discussion résiduel avec OdooBot
        return threads.filter(thread => {
            if (thread.displayName && thread.displayName.toLowerCase().includes('odoobot')) {
                return false;
            }
            return true;
        });
    }
});
