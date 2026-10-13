/** @odoo-module **/

import { Composer } from "@mail/core/common/composer";
import { AttachmentList } from "@mail/core/common/attachment_list";
import { VoiceRecorder } from "@mail/discuss/voice_message/common/voice_recorder";
import { patch } from "@web/core/utils/patch";

// 1. Patch de AttachmentList pour gérer le clic sur "Envoyer le vocal"
patch(AttachmentList.prototype, {
    onClickSendVoice(ev) {
        if (ev) {
            ev.stopPropagation();
            ev.preventDefault();
        }
        // Trouver le bouton d'envoi du compositeur associé
        const composerEl = this.el ? this.el.closest(".o-mail-Composer") : null;
        const sendBtn = composerEl
            ? composerEl.querySelector(".o-mail-Composer-send")
            : document.querySelector(".o-mail-Composer-send");

        if (sendBtn && !sendBtn.disabled) {
            sendBtn.click();
        } else if (this.env && this.env.composer && this.env.composer.sendMessage) {
            this.env.composer.sendMessage();
        }
    },
});

// 2. Patch de VoiceRecorder pour redonner automatiquement le focus au champ texte
patch(VoiceRecorder.prototype, {
    cleanUp(options) {
        super.cleanUp(options);
        setTimeout(() => {
            const composerEl = this.el ? this.el.closest(".o-mail-Composer") : document;
            const input = composerEl.querySelector(".o-mail-Composer-input");
            if (input) {
                input.focus();
            }
        }, 150);
    },
});

// 3. Patch de Composer pour s'assurer que le bouton d'envoi s'active dès que le vocal est uploadé
patch(Composer.prototype, {
    get isSendButtonDisabled() {
        if (this.state.recording) {
            return true;
        }
        const attachments = this.props.composer.attachments || [];
        const hasReadyAttachment = attachments.length > 0 && attachments.every((a) => !a.uploading);
        const hasText = Boolean(this.props.composer.textInputContent && this.props.composer.textInputContent.trim());

        if (!this.state.active) {
            return true;
        }
        if (hasReadyAttachment || hasText) {
            return false;
        }
        return super.isSendButtonDisabled;
    },
});
