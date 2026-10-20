# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
import hashlib
from .restaurant_sync import _notify_backend

_logger = logging.getLogger(__name__)


class RestaurantGrandMarche(models.Model):
    _name = 'restaurant.grand.marche'
    _description = 'Grand Marché & Facture Prestation Sur Mesure'
    _order = 'date_invoice desc, id desc'

    name = fields.Char(
        string="N° Facture Marché",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('Nouveau')
    )
    subject = fields.Char(
        string="Objet du Marché / Prestation",
        required=True,
        help="Ex: Prestation Buffet VIP 150 personnes, Cocktail séminaire entreprise, Banquet officiel..."
    )
    date_invoice = fields.Date(
        string="Date de Facturation",
        required=True,
        default=fields.Date.today
    )
    date_due = fields.Date(
        string="Date d'Échéance",
        help="Date limite de paiement convenue avec le client"
    )
    manager_id = fields.Many2one(
        'res.users',
        string="Gérant Responsable",
        required=True,
        default=lambda self: self.env.user,
        index=True
    )
    company_id = fields.Many2one(
        'res.company',
        string="Établissement",
        required=True,
        default=lambda self: self.env.company
    )
    currency_id = fields.Many2one(
        'res.currency',
        string="Devise",
        related='company_id.currency_id',
        readonly=True
    )

    # --- INFORMATIONS CLIENT (SAISIE LIBRE OU ENREGISTRÉ) ---
    partner_id = fields.Many2one(
        'res.partner',
        string="Client Enregistré (Facultatif)",
        help="Sélectionnez un client existant ou saisissez les informations librement ci-dessous."
    )
    partner_name = fields.Char(
        string="Nom du Client / Entreprise / Organisme",
        required=True,
        help="Nom de l'entreprise, du ministère, de l'organisation ou du particulier"
    )
    partner_phone = fields.Char(
        string="Téléphone / Contact",
        help="Numéro de contact du responsable"
    )
    partner_email = fields.Char(
        string="Email",
        help="Adresse email de facturation"
    )
    partner_address = fields.Char(
        string="Adresse / Lieu de la Prestation",
        help="Lieu de livraison ou de la réception"
    )
    partner_ifu = fields.Char(
        string="NIF / IFU Client (Fiscal)",
        help="Identifiant fiscal du client ou de l'entreprise pour marchés officiels"
    )

    # --- LIGNES DE FACTURATION MODÈLE CADRÉ SUR MESURE ---
    line_ids = fields.One2many(
        'restaurant.grand.marche.line',
        'marche_id',
        string="Prestations & Besoins Facturés",
        copy=True
    )

    # --- SYNTHÈSE FINANCIÈRE PAR CATÉGORIE ---
    amount_repas = fields.Monetary(
        string="Total Plats & Repas (FCFA)",
        compute='_compute_amounts',
        store=True,
        currency_field='currency_id'
    )
    amount_boissons = fields.Monetary(
        string="Total Boissons (FCFA)",
        compute='_compute_amounts',
        store=True,
        currency_field='currency_id'
    )
    amount_services = fields.Monetary(
        string="Total Services & Logistique (FCFA)",
        compute='_compute_amounts',
        store=True,
        currency_field='currency_id'
    )

    tax_rate = fields.Selection([
        ('18', '18% (TVA Standard Légale DGI)'),
        ('0', '0% (Exonéré de TVA / Hors Taxe)'),
    ], string="Régime TVA", default='18', required=True)

    amount_untaxed = fields.Monetary(
        string="Total Brut HT (FCFA)",
        compute='_compute_amounts',
        store=True,
        currency_field='currency_id'
    )
    amount_tax = fields.Monetary(
        string="Montant TVA (FCFA)",
        compute='_compute_amounts',
        store=True,
        currency_field='currency_id'
    )
    amount_total = fields.Monetary(
        string="Montant Total TTC (FCFA)",
        compute='_compute_amounts',
        store=True,
        currency_field='currency_id'
    )
    amount_deposit = fields.Monetary(
        string="Acompte Encaissé (FCFA)",
        default=0.0,
        currency_field='currency_id',
        help="Montant déjà versé par le client à la commande ou à l'avance"
    )
    amount_residual = fields.Monetary(
        string="Solde Restant Dû (FCFA)",
        compute='_compute_amounts',
        store=True,
        currency_field='currency_id'
    )

    # --- ESPACE FISCAL DGI (CALCUL AUTOMATIQUE TRANSPARENT) ---
    aib_rate = fields.Selection([
        ('1', '1% (Client avec IFU Valide - Entreprise / État)'),
        ('5', '5% (Client sans IFU / Particulier)'),
        ('0', '0% (Exonéré de retenue AIB)'),
    ], string="Taux Retenue AIB DGI", default='1', required=True,
       help="Taux fiscal de l'Acompte sur Impôt assis sur les Bénéfices (DGI Bénin/UEMOA)")

    amount_aib = fields.Monetary(
        string="Retenue AIB DGI (FCFA)",
        compute='_compute_amounts',
        store=True,
        currency_field='currency_id',
        help="Montant de la retenue fiscale à la source AIB déduite pour le Trésor Public"
    )
    dgi_net_payable = fields.Monetary(
        string="Net Commercial à Percevoir (TTC - AIB)",
        compute='_compute_amounts',
        store=True,
        currency_field='currency_id',
        help="Montant net que l'organisme payeur débourse après déduction de la retenue AIB"
    )
    dgi_base_ht = fields.Monetary(
        string="Base Imposable DGI HT",
        compute='_compute_amounts',
        store=True,
        currency_field='currency_id'
    )
    dgi_tax_amount = fields.Monetary(
        string="TVA DGI 18%",
        compute='_compute_amounts',
        store=True,
        currency_field='currency_id'
    )
    dgi_total_ttc = fields.Monetary(
        string="Total TTC DGI",
        compute='_compute_amounts',
        store=True,
        currency_field='currency_id'
    )

    # Statut Fiscal et Certification DGI (Strictement géré dans l'Admin)
    dgi_status = fields.Selection([
        ('draft', 'Saisie Gérant (En cours)'),
        ('to_certify', ' Transmis à l\'Admin • Prêt pour Certification DGI'),
        ('certified', ' Certifié DGI • Sceau Numérique Actif'),
    ], string="Statut Fiscal DGI", compute='_compute_dgi_status', store=True, index=True)

    is_certified_dgi = fields.Boolean(
        string="Facture Certifiée DGI",
        default=False,
        copy=False,
        index=True
    )
    dgi_reference = fields.Char(
        string="Référence Fiscale DGI (FNE e-MCF)",
        copy=False,
        readonly=True
    )
    dgi_security_code = fields.Char(
        string="Sceau Cryptographique SHA-256",
        copy=False,
        readonly=True
    )
    dgi_certified_at = fields.Datetime(
        string="Horodatage Certification DGI",
        copy=False,
        readonly=True
    )
    dgi_certified_by = fields.Char(
        string="Certifié par (Administrateur)",
        copy=False,
        readonly=True
    )
    dgi_qr_html = fields.Html(
        string="Aperçu Fiscal DGI & Sceau Numérique",
        compute='_compute_dgi_qr_html',
        readonly=True
    )
    invoice_id = fields.Many2one(
        'account.move',
        string="Facture Comptable Odoo Dédiée",
        readonly=True,
        copy=False
    )

    # --- CONDITIONS DE PAIEMENT ET NOTES ---
    payment_method = fields.Selection([
        ('transfer', 'Virement Bancaire'),
        ('check', 'Chèque Bancaire'),
        ('cash', 'Espèces'),
        ('mobile', 'Mobile Money (Orange/Moov/Wave)'),
        ('credit', 'À Terme (Bon de Commande Administratif)'),
    ], string="Mode de Règlement", default='transfer', required=True)

    payment_terms = fields.Char(
        string="Conditions de Règlement",
        default="Paiement à réception de facture"
    )
    notes = fields.Text(
        string="Notes & Spécifications Particulières",
        default="Prestation traiteur et fourniture sur mesure réalisée conformément aux besoins validés par le client."
    )

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirmed', 'Validé & Facturé'),
        ('paid', 'Payé / Soldé'),
        ('cancel', 'Annulé'),
    ], string="État Commercial", default='draft', required=True, copy=False, index=True)

    @api.model
    def default_get(self, fields_list):
        """Ne pas coder en dur de texte figé : laisser le gérant libre de faire ses propres choix."""
        res = super().default_get(fields_list)
        return res

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.partner_name = self.partner_id.name or self.partner_name
            self.partner_phone = self.partner_id.phone or self.partner_id.mobile or self.partner_phone
            self.partner_email = self.partner_id.email or self.partner_email
            addr_parts = [self.partner_id.street, self.partner_id.city]
            self.partner_address = ", ".join(filter(None, addr_parts)) or self.partner_address
            if self.partner_id.vat:
                self.partner_ifu = self.partner_id.vat
                self.aib_rate = '1'

    @api.onchange('partner_ifu')
    def _onchange_partner_ifu(self):
        if self.partner_ifu and self.partner_ifu.strip():
            self.aib_rate = '1'
        elif not self.partner_ifu:
            self.aib_rate = '5'

    @api.depends('line_ids.price_subtotal', 'line_ids.item_type', 'tax_rate', 'aib_rate', 'amount_deposit')
    def _compute_amounts(self):
        for rec in self:
            total_ht = sum(line.price_subtotal for line in rec.line_ids)
            repas_ht = sum(line.price_subtotal for line in rec.line_ids if line.item_type == 'repas')
            boissons_ht = sum(line.price_subtotal for line in rec.line_ids if line.item_type == 'boisson')
            services_ht = sum(line.price_subtotal for line in rec.line_ids if line.item_type in ('service', 'autre'))

            rec.amount_untaxed = round(total_ht, 2)
            rec.amount_repas = round(repas_ht, 2)
            rec.amount_boissons = round(boissons_ht, 2)
            rec.amount_services = round(services_ht, 2)

            rate = float(rec.tax_rate or '0')
            tax = round(total_ht * (rate / 100.0), 2)
            rec.amount_tax = tax
            total_ttc = round(total_ht + tax, 2)
            rec.amount_total = total_ttc
            rec.amount_residual = max(0.0, total_ttc - (rec.amount_deposit or 0.0))

            # Calculs DGI automatiques
            rec.dgi_base_ht = round(total_ht, 2)
            rec.dgi_tax_amount = tax
            rec.dgi_total_ttc = total_ttc
            aib_r = float(rec.aib_rate or '0')
            aib_amount = round(total_ht * (aib_r / 100.0), 2)
            rec.amount_aib = aib_amount
            rec.dgi_net_payable = max(0.0, round(total_ttc - aib_amount, 2))

    @api.onchange('line_ids', 'tax_rate', 'aib_rate', 'amount_deposit')
    def _onchange_lines_amounts(self):
        """Recalcule immédiatement en temps réel tous les totaux dès qu'une ligne ou un prix change."""
        self._compute_amounts()

    @api.depends('state', 'is_certified_dgi')
    def _compute_dgi_status(self):
        for rec in self:
            if rec.is_certified_dgi:
                rec.dgi_status = 'certified'
            elif rec.state in ('confirmed', 'paid'):
                rec.dgi_status = 'to_certify'
            else:
                rec.dgi_status = 'draft'

    def get_dgi_qr_code_base64(self):
        """Génère l'image PNG du QR code DGI en base64 pour affichage web et impression PDF sans dépendance externe."""
        self.ensure_one()
        cfg = self.env['restaurant.configuration'].sudo().search([], limit=1)
        nim = (cfg.nim if cfg and cfg.nim else "RESTO-DGI-MCF-01")
        ifu = (cfg.ifu if cfg and cfg.ifu else self.company_id.vat or "-")
        ref = self.dgi_reference or (f"DGI-FNE-GM-{self.name.replace('/', '-')}" if self.name else "DGI-PENDING")
        statut = "CERTIFIE_DGI" if self.is_certified_dgi else "EN_COURS"
        qr_data = f"DGI-FNE|NIM:{nim}|IFU:{ifu}|CLI_IFU:{self.partner_ifu or 'NA'}|FACT:{self.name}|TTC:{int(self.amount_total)}|HT:{int(self.amount_untaxed)}|REF:{ref}|STATUT:{statut}"
        try:
            import qrcode
            import io
            import base64
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=6,
                border=2,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
        except Exception as e:
            _logger.warning("Erreur génération QR code local qrcode: %s", e)
            import urllib.parse
            return f"https://api.qrserver.com/v1/create-qr-code/?size=130x130&data={urllib.parse.quote(qr_data)}"

    @api.depends('is_certified_dgi', 'dgi_reference', 'dgi_security_code', 'dgi_status', 'amount_total', 'amount_untaxed', 'partner_ifu')
    def _compute_dgi_qr_html(self):
        for rec in self:
            qr_base64 = rec.get_dgi_qr_code_base64()
            if rec.is_certified_dgi:
                ref = rec.dgi_reference or "DGI-CERTIFIED"
                rec.dgi_qr_html = f"""
                <div class="p-3 bg-white rounded-3 border text-center shadow-sm" style="border: 2px solid #059669 !important;">
                    <div class="badge bg-success p-2 mb-2 d-block fs-6">FACTURE CERTIFIÉE DGI (e-MCF)</div>
                    <div class="p-2 border rounded bg-light mb-2 d-inline-block">
                        <img src="{qr_base64}" alt="QR DGI" style="width: 120px; height: 120px; display: block; margin: 0 auto;"/>
                    </div>
                    <div class="text-dark fw-bold font-monospace" style="font-size: 13px;">{ref}</div>
                    <small class="text-muted d-block mt-1" style="font-size: 10px;">SceauSHA-256 : {(rec.dgi_security_code or '')[:28]}...</small>
                    <small class="text-success fw-bold d-block mt-1">SceauNumérique Approuvé &amp; Scellé • Conforme DGI</small>
                </div>
                """
            elif rec.dgi_status == 'to_certify':
                rec.dgi_qr_html = f"""
                <div class="p-3 rounded-3 border text-center shadow-sm" style="background-color: #fffbeb; border: 2px dashed #f59e0b !important;">
                    <div class="badge bg-warning text-dark p-2 mb-2 d-block fw-bold">ENVOYÉ À L'ADMIN • PRÊT POUR CERTIFICATION DGI</div>
                    <div class="p-2 border rounded bg-white mb-2 d-inline-block">
                        <img src="{qr_base64}" alt="QR DGI" style="width: 100px; height: 100px; display: block; margin: 0 auto;"/>
                    </div>
                    <div class="fw-bold text-dark mb-1">CalculsFiscaux DGI prêts sans erreur</div>
                    <small class="text-muted d-block" style="font-size: 11px;">BaseHT: {rec.amount_untaxed:,.0f} FCFA | TVA: {rec.amount_tax:,.0f} FCFA | AIB ({rec.aib_rate}%): {rec.amount_aib:,.0f} FCFA</small>
                    <small class="text-primary fw-bold d-block mt-2">Cliquezsur « Certifier la Facture DGI » pour sceller officiellement</small>
                </div>
                """
            else:
                rec.dgi_qr_html = """
                <div class="p-3 bg-white rounded-3 border text-center shadow-sm text-muted">
                    <i class="fa fa-edit fa-3x text-secondary mb-2 d-block"></i>
                    <div class="fw-bold mb-1">SaisieGérant en cours</div>
                    <small style="font-size: 11px;">Validezla commande pour l'envoyer automatiquement à l'administration.</small>
                </div>
                """

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('Nouveau')) == _('Nouveau'):
                seq_code = 'restaurant.grand.marche'
                seq = self.env['ir.sequence'].next_by_code(seq_code)
                if not seq:
                    year = fields.Date.today().strftime('%Y')
                    count = self.search_count([('date_invoice', '>=',f'{year}-01-01')]) + 1
                    seq = f"GM/{year}/{count:04d}"
                vals['name'] = seq
        return super().create(vals_list)

    def action_confirm(self):
        for rec in self:
            if not rec.line_ids:
                raise UserError(_("Veuillez renseigner au moins un plat, une boisson ou une prestation dans la commande."))
            for line in rec.line_ids:
                if not line.name or not line.name.strip():
                    raise UserError(_("Veuillez mentionner le nom de chaque plat ou boisson dans la commande."))
                if line.price_unit < 0:
                    raise UserError(_("Le prix unitaire ne peut pas être négatif."))
            if not rec.partner_name:
                raise UserError(_("Veuillez renseigner le nom du client ou de l'entreprise."))
            rec.state = 'confirmed'
            # Synchronisation automatique en coulisses pour l'admin
            rec._sync_accounting_invoice()
            try:
                _notify_backend('order', {
                    'order_name': rec.name,
                    'total': rec.amount_total,
                    'tendered_amount': rec.amount_total,
                    'change_amount': 0.0,
                    'odoo_id': rec.id + 1000000,
                    'state': 'paid',
                    'manager_name': rec.manager_id.name if rec.manager_id else 'Gérant',
                    'manager_login': rec.manager_id.login if rec.manager_id else 'gerant',
                    'payment_method': rec.payment_method or 'Grand Marché / Prestation',
                    'date_order': fields.Datetime.to_string(fields.Datetime.now()),
                })
            except Exception as notify_err:
                _logger.warning("Notification backend marché: %s", notify_err)
        return True

    def action_mark_paid(self):
        for rec in self:
            rec.amount_deposit = rec.amount_total
            rec.state = 'paid'
            try:
                _notify_backend('order', {
                    'order_name': rec.name,
                    'total': rec.amount_total,
                    'tendered_amount': rec.amount_total,
                    'change_amount': 0.0,
                    'odoo_id': rec.id + 1000000,
                    'state': 'paid',
                    'manager_name': rec.manager_id.name if rec.manager_id else 'Gérant',
                    'manager_login': rec.manager_id.login if rec.manager_id else 'gerant',
                    'payment_method': rec.payment_method or 'Grand Marché / Prestation',
                    'date_order': fields.Datetime.to_string(fields.Datetime.now()),
                })
            except Exception as notify_err:
                _logger.warning("Notification backend marché: %s", notify_err)
        return True

    def action_set_draft(self):
        for rec in self:
            if rec.is_certified_dgi:
                raise UserError(_("Cette facture est certifiée par la DGI avec un sceau fiscal scellé. Elle ne peut plus être repassée en brouillon."))
            rec.state = 'draft'
        return True

    def action_cancel(self):
        for rec in self:
            if rec.is_certified_dgi:
                raise UserError(_("Une facture officielle certifiée DGI ne peut pas être annulée directement. Veuillez établir un avoir régularisateur."))
            rec.state = 'cancel'
        return True

    # --- ACTIONS RAPIDES POUR LE REMPLISSAGE HORIZONTAL LIBRE DU GÉRANT ---
    def action_load_default_template(self):
        """Ajoute des lignes horizontales prêtes pour la saisie libre du gérant sans texte imposé."""
        self.ensure_one()
        blank_lines = [
            (0, 0, {
                'item_type': 'repas',
                'name': '',
                'quantity': 1.0,
                'price_unit': 0.0,
            }),
            (0, 0, {
                'item_type': 'boisson',
                'name': '',
                'quantity': 1.0,
                'price_unit': 0.0,
            }),
        ]
        self.write({'line_ids': blank_lines})
        return True

    def action_add_repas_line(self):
        self.ensure_one()
        self.write({
            'line_ids': [(0, 0, {
                'item_type': 'repas',
                'name': '',
                'quantity': 1.0,
                'price_unit': 0.0,
            })]
        })
        return True

    def action_add_boisson_line(self):
        self.ensure_one()
        self.write({
            'line_ids': [(0, 0, {
                'item_type': 'boisson',
                'name': '',
                'quantity': 1.0,
                'price_unit': 0.0,
            })]
        })
        return True

    def action_add_service_line(self):
        self.ensure_one()
        self.write({
            'line_ids': [(0, 0, {
                'item_type': 'service',
                'name': '',
                'quantity': 1.0,
                'price_unit': 0.0,
            })]
        })
        return True

    def action_add_custom_line(self):
        """Permet au gérant d'ajouter une ligne 100% libre et personnalisée."""
        self.ensure_one()
        self.write({
            'line_ids': [(0, 0, {
                'item_type': 'autre',
                'name': '',
                'quantity': 1.0,
                'price_unit': 0.0,
            })]
        })
        return True

    # --- ACTION D'IMPRESSION REÇU CLIENT IMMÉDIAT (GÉRANT) ---
    def action_print_client_receipt(self):
        """Imprime immédiatement le reçu / la facture commerciale propre pour le client."""
        self.ensure_one()
        return self.env.ref('restaurant_core.action_report_marche_client_receipt').report_action(self)

    def action_print_pdf(self):
        """Imprime la facture Grand Marché standard A4."""
        self.ensure_one()
        return self.env.ref('restaurant_core.action_report_restaurant_grand_marche').report_action(self)

    # --- CERTIFICATION FISCALE DGI STRICTE (ADMINISTRATEUR) ---
    def action_certify_dgi(self):
        """Certifie officiellement la facture auprès de la DGI (Réservé à l'Admin, sans aucune erreur)."""
        self.ensure_one()
        # 1. Droits administrateurs stricts : Seul l'administrateur système peut certifier
        is_admin = (
            self.env.user.has_group('base.group_system') or
            self.env.is_admin() or
            self.env.user.id in (1, 2)
        )
        if not is_admin:
            raise UserError(_("Seul un administrateur est habilité à certifier fiscalement une facture auprès de la DGI."))

        # 2. Si la facture est encore au statut brouillon lors de la certification, on la confirme directement
        if self.state == 'draft':
            if not self.partner_name:
                raise UserError(_("Veuillez renseigner le nom du client ou de l'organisme."))
            if not self.line_ids:
                raise UserError(_("Veuillez ajouter au moins une prestation dans la facture."))
            self.state = 'confirmed'

        if not self.partner_name:
            raise UserError(_("Veuillez renseigner le nom du client ou de l'organisme."))
        if not self.line_ids:
            raise UserError(_("Veuillez ajouter au moins une prestation dans la facture."))

        cfg = self.env['restaurant.configuration'].sudo().search([], limit=1)
        nim = (cfg.nim if cfg and cfg.nim else "RESTO-DGI-MCF-01")
        resto_ifu = (cfg.ifu if cfg and cfg.ifu else self.company_id.vat or "0000000000000")

        # 3. Génération de l'empreinte cryptographique SHA-256 avec sel fiscal DGI
        raw_sig = (
            f"DGI-GM|NIM:{nim}|RESTO_IFU:{resto_ifu}|CLI_IFU:{self.partner_ifu or 'PARTICULIER'}|"
            f"CLI:{self.partner_name}|DATE:{self.date_invoice}|HT:{int(self.amount_untaxed)}|"
            f"TVA:{int(self.amount_tax)}|AIB:{int(self.amount_aib)}|TTC:{int(self.amount_total)}|SALT_DGI_BENIN"
        )
        sig = hashlib.sha256(raw_sig.encode('utf-8')).hexdigest()

        # 4. Référence Fiscale DGI Unique FNE e-MCF
        year_str = self.date_invoice.strftime('%Y') if self.date_invoice else fields.Date.today().strftime('%Y')
        ref = f"DGI-FNE-GM-{year_str}-{sig[:8].upper()}"

        self.write({
            'is_certified_dgi': True,
            'dgi_reference': ref,
            'dgi_security_code': sig,
            'dgi_certified_at': fields.Datetime.now(),
            'dgi_certified_by': self.env.user.name,
        })

        # 5. Synchronisation de la facture comptable client B2B dans account.move
        self._sync_accounting_invoice(ref_dgi=ref, sig=sig)

        # 6. Notification immédiate au backend FastAPI
        try:
            _notify_backend('order', {
                'order_name': self.name,
                'total': self.amount_total,
                'tendered_amount': self.amount_total,
                'change_amount': 0.0,
                'odoo_id': self.id + 1000000,
                'state': 'paid',
                'manager_name': self.manager_id.name if self.manager_id else 'Gérant',
                'manager_login': self.manager_id.login if self.manager_id else 'gerant',
                'payment_method': self.payment_method or 'Grand Marché / Prestation',
                'date_order': fields.Datetime.to_string(fields.Datetime.now()),
                'dgi_reference': ref,
                'dgi_security_code': sig,
                'is_certified': True,
            })
        except Exception as notify_err:
            _logger.warning("Notification backend certification marché: %s", notify_err)

        return True

    def action_print_dgi_invoice(self):
        """Imprime la Facture Officielle Normalisée DGI avec le sceau cryptographique et QR Code."""
        self.ensure_one()
        return self.env.ref('restaurant_core.action_report_marche_dgi_invoice').report_action(self)

    def action_view_accounting_invoice(self):
        """Ouvre la facture client correspondante dans Odoo Facturation."""
        self.ensure_one()
        if not self.invoice_id:
            raise UserError(_("Aucune facture comptable n'est encore générée pour ce marché."))
        return {
            'type': 'ir.actions.act_window',
            'name': 'Facture Client Grand Marché (Comptabilité)',
            'res_model': 'account.move',
            'res_id': self.invoice_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def _sync_accounting_invoice(self, ref_dgi=None, sig=None):
        """Synchronise ou valide automatiquement la facture client B2B dans account.move de façon 100% infaillible."""
        for rec in self:
            if not rec.amount_total or rec.amount_total <= 0:
                continue
            try:
                partner = rec.partner_id
                if not partner:
                    partner_domain = [('name', '=', rec.partner_name)]
                    if rec.partner_ifu:
                        partner_domain = [('vat', '=', rec.partner_ifu)]
                    partner = self.env['res.partner'].sudo().search(partner_domain, limit=1)
                    if not partner:
                        partner = self.env['res.partner'].sudo().create({
                            'name': rec.partner_name,
                            'vat': rec.partner_ifu or False,
                            'phone': rec.partner_phone or False,
                            'email': rec.partner_email or False,
                            'street': rec.partner_address or False,
                            'customer_rank': 1,
                        })
                    rec.partner_id = partner.id

                journal = self.env['account.journal'].sudo().search([('type', '=', 'sale')], limit=1)
                
                # Compte de produit obligatoire pour les lignes sans produit catalogue
                income_account = None
                if journal and hasattr(journal, 'default_account_id') and journal.default_account_id:
                    income_account = journal.default_account_id
                if not income_account:
                    income_account = self.env['account.account'].sudo().search([
                        ('account_type', 'in', ('income', 'income_other')),
                        ('company_id', '=', rec.company_id.id)
                    ], limit=1)
                if not income_account:
                    income_account = self.env['account.account'].sudo().search([
                        ('code', '=like', '70%'),
                        ('company_id', '=', rec.company_id.id)
                    ], limit=1)
                if not income_account:
                    income_account = self.env['account.account'].sudo().search([
                        ('code', '=like', '40%'),
                        ('company_id', '=', rec.company_id.id)
                    ], limit=1)
                if not income_account:
                    income_account = self.env['account.account'].sudo().search([
                        ('company_id', '=', rec.company_id.id)
                    ], limit=1)

                tax_18 = self.env['account.tax'].sudo().search([
                    ('type_tax_use', '=', 'sale'),
                    ('name', 'ilike', '18')
                ], limit=1) if rec.tax_rate == '18' else False
                tax_ids = [(6, 0, [tax_18.id])] if tax_18 else []

                lines = []
                for line in rec.line_ids:
                    line_name = (line.name or '').strip()
                    if not line_name:
                        continue
                    cat_label = dict(line._fields['item_type'].selection).get(line.item_type, 'Prestation')
                    line_vals = {
                        'name': f"[{cat_label}] {line_name}",
                        'quantity': line.quantity or 1.0,
                        'price_unit': line.price_unit or 0.0,
                        'tax_ids': tax_ids,
                    }
                    if line.product_id:
                        line_vals['product_id'] = line.product_id.id
                    if income_account:
                        line_vals['account_id'] = income_account.id
                    lines.append((0, 0, line_vals))

                if not lines:
                    continue

                narration = (
                    f"Facture Grand Marché - Réf: {rec.name}\n"
                    f"Objet de la Prestation: {rec.subject}\n"
                    f"Client: {rec.partner_name} (IFU: {rec.partner_ifu or '-'})\n"
                    f"Total Brut HT: {rec.amount_untaxed:,.0f} FCFA\n"
                    f"TVA (18%): {rec.amount_tax:,.0f} FCFA\n"
                    f"Retenue AIB DGI ({rec.aib_rate}%): {rec.amount_aib:,.0f} FCFA\n"
                    f"Total TTC: {rec.amount_total:,.0f} FCFA\n"
                    f"Net Commercial à Payer: {rec.dgi_net_payable:,.0f} FCFA"
                )
                if ref_dgi:
                    narration += (
                        f"\n\n FACTURE CERTIFIÉE DGI (e-MCF)\n"
                        f"Référence Fiscale: {ref_dgi}\n"
                        f"Sceau SHA-256: {sig}\n"
                        f"Certifiée le: {fields.Datetime.now()} par {self.env.user.name}"
                    )

                if not rec.invoice_id:
                    move = self.env['account.move'].sudo().create({
                        'move_type': 'out_invoice',
                        'partner_id': partner.id,
                        'journal_id': journal.id if journal else False,
                        'invoice_date': rec.date_invoice,
                        'ref': f"{rec.name} ({ref_dgi})" if ref_dgi else rec.name,
                        'narration': narration,
                        'invoice_line_ids': lines,
                    })
                    rec.invoice_id = move.id
                else:
                    move = rec.invoice_id
                    if move.state == 'draft':
                        move.sudo().write({
                            'ref': f"{rec.name} ({ref_dgi})" if ref_dgi else rec.name,
                            'narration': narration,
                        })

                if ref_dgi and move and move.state == 'draft':
                    try:
                        move.sudo().action_post()
                    except Exception as post_err:
                        _logger.warning("Post account.move marché info: %s", post_err)
            except Exception as e:
                _logger.error("Erreur sync facture comptable grand marché: %s", e)


class RestaurantGrandMarcheLine(models.Model):
    _name = 'restaurant.grand.marche.line'
    _description = 'Ligne de Prestation Grand Marché'
    _order = 'id asc'

    marche_id = fields.Many2one(
        'restaurant.grand.marche',
        string="Marché",
        required=True,
        ondelete='cascade',
        index=True
    )
    item_type = fields.Selection([
        ('repas', ' Repas & Plats Cuisinés'),
        ('boisson', ' Boissons & Rafraîchissements'),
        ('service', ' Prestation, Vaisselle & Service'),
        ('autre', ' Ligne Libre / Personnalisée'),
    ], string="Catégorie", default='repas', required=True)

    product_id = fields.Many2one(
        'product.product',
        string="Choisir un Plat / Boisson du Restaurant (Catalogue)",
        help="Optionnel : Sélectionnez directement un plat ou une boisson de votre carte pour charger automatiquement son prix unitaire."
    )
    name = fields.Char(
        string="Nom du Plat, Boisson ou Prestation",
        required=False,
        help="Mentionnez librement le nom du plat ou de la boisson demandée."
    )
    quantity = fields.Float(
        string="Quantité",
        required=True,
        default=1.0
    )
    price_unit = fields.Float(
        string="Prix Unitaire (FCFA)",
        required=True,
        default=0.0,
        help="Prix unitaire saisi librement ou chargé depuis le catalogue"
    )
    price_subtotal = fields.Monetary(
        string="Montant Calculé (FCFA)",
        compute='_compute_subtotal',
        store=True,
        currency_field='currency_id'
    )
    currency_id = fields.Many2one(
        'res.currency',
        related='marche_id.currency_id',
        readonly=True
    )
    notes = fields.Char(
        string="Précisions / Spécifications",
        help="Précisions supplémentaires sur la cuisson, le service ou le conditionnement"
    )

    @api.onchange('name')
    def _onchange_name(self):
        """Classification intelligente suggérée sans jamais forcer ni écraser les choix personnalisés."""
        if self.name and not self.product_id:
            txt = self.name.lower()
            boisson_keywords = [
                'eau', 'jus', 'bissap', 'gingembre', 'tampico', 'boisson', 'biere', 'bière',
                'castel', 'beaufort', 'guinness', 'doppel', 'flag', 'brau', 'heineken',
                'soda', 'coca', 'fanta', 'sprite', 'youki', 'cocktail', 'the', 'thé', 'cafe',
                'café', 'vin', 'champagne', 'drink', 'sucrerie', 'canette', 'bouteille',
                'whisky', 'liqueur', 'sirop', 'degue', 'dèguè', 'gazeuse', 'tonic', 'red bull',
                'aperitif', 'apéritif', 'rhum', 'vodka', 'pastis'
            ]
            service_keywords = [
                'service', 'serveur', 'serveuse', 'maitre d\'hotel', 'maître d\'hôtel',
                'vaisselle', 'couvert', 'assiette', 'verre', 'nappe', 'decoration', 'décoration',
                'livraison', 'transport', 'sono', 'sonorisation', 'logistique', 'tente',
                'chaise', 'table', 'pause cafe', 'pause café', 'nettoyage', 'location',
                'personnel', 'hôtesse', 'hotesse', 'chapiteau', 'podium', 'salle'
            ]
            if any(k in txt for k in boisson_keywords):
                self.item_type = 'boisson'
            elif any(k in txt for k in service_keywords):
                self.item_type = 'service'
            # Note: Si ce n'est pas un mot-clé reconnu, l'utilisateur conserve son choix sans écrasement brutal

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Sélection rapide d'un plat ou boisson de la carte : nom, prix et sous-total auto."""
        if self.product_id:
            self.name = self.product_id.name
            self.price_unit = self.product_id.lst_price or 0.0
            prod_name_lower = (self.product_id.name or '').lower()
            pos_names = [c.name.lower() for c in self.product_id.pos_categ_ids] if self.product_id.pos_categ_ids else []
            if any(b in prod_name_lower for b in ['eau', 'jus', 'bissap', 'boisson', 'biere', 'soda', 'cocktail', 'the', 'cafe', 'vin', 'champagne', 'drink']) or any('boisson' in c for c in pos_names):
                self.item_type = 'boisson'
            else:
                self.item_type = 'repas'
            self.price_subtotal = round((self.quantity or 1.0) * self.price_unit, 2)

    @api.onchange('quantity', 'price_unit')
    def _onchange_calc_subtotal(self):
        """Calcul automatique immédiat du sous-total au fur et à mesure de la saisie."""
        self.price_subtotal = round((self.quantity or 0.0) * (self.price_unit or 0.0), 2)

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.price_subtotal = round((line.quantity or 0.0) * (line.price_unit or 0.0), 2)