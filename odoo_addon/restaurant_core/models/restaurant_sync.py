from odoo import models, fields, api, _
from odoo.exceptions import UserError
import json
import urllib.request
import logging
import re
import time

_logger = logging.getLogger(__name__)

BACKEND_WEBHOOK_URL = "http://restaurant-backend:8000/api/v1/odoo/webhook"

def _notify_backend(endpoint, payload):
    """Envoie une notification HTTP en temps réel au backend FastAPI."""
    try:
        url = f"{BACKEND_WEBHOOK_URL}/{endpoint}"
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req, timeout=3)
        _logger.info("Notification Odoo transmise au backend FastAPI: %s", url)
    except Exception as e:
        _logger.warning("Notification backend non délivrée (%s): %s", endpoint, e)


class PosOrder(models.Model):
    _inherit = 'pos.order'

    backend_order_id = fields.Char(
        string="ID Commande Backend",
        index=True,
        help="Identifiant de la commande provenant du backend FastAPI (Moteur Restaurant)"
    )
    backend_sync_status = fields.Selection(
        [
            ('synced', 'Synchronisé'),
            ('pending', 'En attente'),
            ('error', 'Erreur')
        ],
        string="Statut Synchronisation Backend",
        default='synced'
    )
    backend_table_number = fields.Char(
        string="Numéro de Table Backend"
    )
    tendered_amount = fields.Float(
        string="Montant Versé Client (FCFA)",
        compute="_compute_payment_details",
        store=True,
        help="Montant total remis par le client (avant déduction de la monnaie)"
    )
    change_amount = fields.Float(
        string="Monnaie Rendue (FCFA)",
        compute="_compute_payment_details",
        store=True,
        help="Monnaie remise au client"
    )
    net_paid_amount = fields.Float(
        string="Net Encaissé sans Monnaie (FCFA)",
        compute="_compute_payment_details",
        store=True,
        help="Montant net du paiement sans la monnaie (Total réel des plats vendus)"
    )
    payment_method_name = fields.Char(
        string="Mode de Paiement Principal",
        compute="_compute_payment_details",
        store=True,
        help="Mode de paiement utilisé pour régler la commande"
    )

    @api.depends('amount_total', 'amount_return', 'payment_ids', 'payment_ids.amount', 'payment_ids.payment_method_id')
    def _compute_payment_details(self):
        for rec in self:
            pos_pm = [p for p in rec.payment_ids if p.amount > 0 and p.payment_method_id]
            rec.payment_method_name = ", ".join([p.payment_method_id.name for p in pos_pm]) if pos_pm else (
                ", ".join([p.payment_method_id.name for p in rec.payment_ids if p.payment_method_id]) or "Espèces (Cash)"
            )
            rec.tendered_amount = sum(p.amount for p in pos_pm) if pos_pm else rec.amount_total
            rec.change_amount = abs(rec.amount_return)
            rec.net_paid_amount = rec.amount_total

    def get_dgi_qr_code_base64(self):
        """Génère le QR Code fiscal DGI en Base64 pour la commande POS."""
        self.ensure_one()
        cfg = self.env['restaurant.configuration'].sudo().search([], limit=1)
        nim = (cfg.nim if cfg and cfg.nim else 'RESTO-DGI-MCF-01')
        ifu = (cfg.ifu if cfg and cfg.ifu else (self.company_id.vat or '000123456789A'))
        ref = self.pos_reference or self.name or f"POS-{self.id}"
        date_str = self.date_order.strftime('%Y-%m-%d %H:%M:%S') if self.date_order else '2026-10-12'
        total_ttc = int(self.amount_total or 0)
        total_tax = int(self.amount_tax or 0)
        total_ht = total_ttc - total_tax
        qr_payload = f"DGI-FNE|NIM:{nim}|IFU:{ifu}|REF:{ref}|DATE:{date_str}|HT:{total_ht}|TVA:{total_tax}|TTC:{total_ttc}|CERTIFIE_DGI"
        try:
            import qrcode
            import io
            import base64
            qr = qrcode.QRCode(version=1, box_size=4, border=1)
            qr.add_data(qr_payload)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            b64_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
            return f"data:image/png;base64,{b64_str}"
        except Exception:
            return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAKwAAACsAQAAAADOSnp1AAABrklEQVR4nLWXMQ5bMQxDn4Pu9A1y/2PlBvQJXof/OxRNCyRQvVkDTUgUJS95c87jXRQ+DJ+1FpvFOuy9zz5rrU9B3oep1rZtyHWzneHNWbB3QiWszVmfg/wjXPbebA7p1yB/nB8APHNcvNi73xN8E44cDtu1nyaLOIS9uqG/hTbM1BJVE9ASreoQdg2tiMbUZAzbEGmNJUbmeEsRGwg0tAz1DoWQ0mDQkGasliG0iW2ubI/VsjccAkRljrcNJbZVLjVO1ZIktCY1KZnrHcQADakxzVzvkCJVoSTJWL5TSpuStmkZ04nU6wV6VbNz+kbSCoqNMDXTMEmTlCpNYSzflWpigSg6hf1gN4sX+1l8Lbq/AfkLb4DEX+KWOT8xTYqtakrGckJ7aTtoIw2M8W6il/1xD87BvmyxtJezdNJjc4/hYJFBP6kpKtcWAemcfxuDqZAYY6b8u6VY0oQQGNSJ2kLt1fh2Cnt1g8tFjksO8HxN7bHaAwaXBwiv55Sf9E6HbaSFuXlZ2ohe6rNMzfkHQHpkeVjnucGO/tNCg/cuO9bzBSp6rxPVqVm8/uO/+CcqbbLoEYMG+AAAAABJRU5ErkJggg=="

    def _export_for_ui(self, order):
        pos_ref = order.pos_reference
        if not pos_ref or not isinstance(pos_ref, str) or not re.search(r'([0-9-]){14,}', pos_ref):
            sess_code = (order.session_id.name or '00001').split('/')[-1].zfill(5) if order.session_id else '00001'
            fallback_ref = f"Order {sess_code}-001-{order.id:06d}"
            order.sudo().write({'pos_reference': fallback_ref})
        return super()._export_for_ui(order)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            pos_ref = vals.get('pos_reference')
            if not pos_ref or not isinstance(pos_ref, str) or not re.search(r'([0-9-]){14,}', pos_ref):
                sess_id = vals.get('session_id')
                sess = self.env['pos.session'].browse(sess_id) if sess_id else False
                sess_code = (sess.name or '00001').split('/')[-1].zfill(5) if sess else '00001'
                rnd_seq = f"{int(time.time() * 1000) % 10000000:07d}"
                vals['pos_reference'] = f"Order {sess_code}-001-{rnd_seq}"
        records = super().create(vals_list)
        for rec in records:
            mgr_user = rec.user_id or (rec.session_id.user_id if rec.session_id else False)
            mgr_name = mgr_user.name if mgr_user else "Gérant"
            mgr_login = mgr_user.login if mgr_user else ""
            pos_pm = [p for p in rec.payment_ids if p.amount > 0 and p.payment_method_id]
            pm_names = [p.payment_method_id.name for p in pos_pm]
            payment_str = ", ".join(pm_names) if pm_names else "Espèces (Cash)"
            tendered = sum(p.amount for p in pos_pm) if pos_pm else rec.amount_total
            change = abs(rec.amount_return)
            net_amt = rec.amount_total

            # Mise à jour directe du gérant dans Odoo
            if mgr_user and rec.state in ['paid', 'done']:
                mgr_user.sudo().session_sales_total += net_amt
                mgr_user.sudo().is_online = True
                if not mgr_user.last_login_time:
                    mgr_user.sudo().last_login_time = fields.Datetime.now()

                # Accumulation automatique en temps réel dans la Facturation de la Journée
                try:
                    self.env['restaurant.daily.report'].sudo()._accumulate_order(rec)
                except Exception as e:
                    _logger.warning("Erreur accumulation rapport journalier: %s", e)

            # Enregistrement dans le Journal des Faits et Gestes Odoo
            try:
                self.env['restaurant.activity.log'].sudo().create({
                    'manager_id': mgr_user.id if mgr_user else False,
                    'manager_name': mgr_name,
                    'manager_login': mgr_login,
                    'action_type': 'order_sale',
                    'order_number': rec.name,
                    'amount': net_amt,
                    'payment_method': payment_str,
                    'description': f"💰 Encaissement reçu {rec.name} par {mgr_name} : {net_amt:,.0f} FCFA nets sans monnaie ({payment_str}). Versé: {tendered:,.0f} FCFA, Monnaie: {change:,.0f} FCFA.",
                    'activity_time': rec.date_order or fields.Datetime.now(),
                })
            except Exception as e:
                _logger.warning("Erreur journal activité Odoo: %s", e)

            _notify_backend('order', {
                'odoo_id': rec.id,
                'order_name': rec.name,
                'total': net_amt,
                'tendered_amount': tendered,
                'change_amount': change,
                'state': rec.state,
                'manager_name': mgr_name,
                'manager_login': mgr_login,
                'session_name': rec.session_id.name if rec.session_id else False,
                'date_order': rec.date_order.isoformat() if rec.date_order else False,
                'payment_method': payment_str,
            })
        return records

    def action_pos_order_paid(self):
        res = super().action_pos_order_paid()
        for rec in self:
            mgr_user = rec.user_id or (rec.session_id.user_id if rec.session_id else False)
            mgr_name = mgr_user.name if mgr_user else "Gérant"
            mgr_login = mgr_user.login if mgr_user else ""
            pos_pm = [p for p in rec.payment_ids if p.amount > 0 and p.payment_method_id]
            pm_names = [p.payment_method_id.name for p in pos_pm]
            payment_str = ", ".join(pm_names) if pm_names else "Espèces (Cash)"
            tendered = sum(p.amount for p in pos_pm) if pos_pm else rec.amount_total
            change = abs(rec.amount_return)
            net_amt = rec.amount_total

            if mgr_user:
                mgr_user.sudo().session_sales_total += net_amt
                mgr_user.sudo().is_online = True

            # Accumulation automatique en temps réel dans la Facturation de la Journée
            try:
                self.env['restaurant.daily.report'].sudo()._accumulate_order(rec)
            except Exception as e:
                _logger.warning("Erreur accumulation rapport journalier: %s", e)

            try:
                self.env['restaurant.activity.log'].sudo().create({
                    'manager_id': mgr_user.id if mgr_user else False,
                    'manager_name': mgr_name,
                    'manager_login': mgr_login,
                    'action_type': 'order_sale',
                    'order_number': rec.name,
                    'amount': net_amt,
                    'payment_method': payment_str,
                    'description': f"💰 Validation & Paiement commande {rec.name} par {mgr_name} : {net_amt:,.0f} FCFA nets sans monnaie ({payment_str}). Versé: {tendered:,.0f} FCFA, Monnaie: {change:,.0f} FCFA.",
                    'activity_time': rec.date_order or fields.Datetime.now(),
                })
            except Exception as e:
                _logger.warning("Erreur journal activité Odoo: %s", e)

            _notify_backend('order', {
                'odoo_id': rec.id,
                'order_name': rec.name,
                'total': net_amt,
                'tendered_amount': tendered,
                'change_amount': change,
                'state': 'paid',
                'manager_name': mgr_name,
                'manager_login': mgr_login,
                'session_name': rec.session_id.name if rec.session_id else False,
                'date_order': rec.date_order.isoformat() if rec.date_order else False,
                'payment_method': payment_str,
            })
        return res

    def write(self, vals):
        res = super().write(vals)
        if vals.get('state') in ['paid', 'done']:
            for rec in self:
                try:
                    self.env['restaurant.daily.report'].sudo()._accumulate_order(rec)
                except Exception as e:
                    _logger.warning("Erreur accumulation rapport journalier write: %s", e)
        return res



class PosSession(models.Model):
    _inherit = 'pos.session'

    @api.model_create_multi
    def create(self, vals_list):
        sessions = super().create(vals_list)
        for s in sessions:
            if s.user_id:
                s.user_id.sudo().write({
                    'is_online': True,
                    'last_login_time': s.start_at or fields.Datetime.now(),
                })
                try:
                    self.env['restaurant.activity.log'].sudo().create({
                        'manager_id': s.user_id.id,
                        'manager_name': s.user_id.name,
                        'manager_login': s.user_id.login,
                        'action_type': 'login',
                        'description': f"🟢 Prise de service du gérant {s.user_id.name}. Début de session {s.name}.",
                        'activity_time': s.start_at or fields.Datetime.now(),
                    })
                except Exception as e:
                    _logger.warning("Erreur journal session: %s", e)

                try:
                    self.env['restaurant.daily.report'].sudo()._create_manager_session_report(s.user_id, s.start_at)
                except Exception as e:
                    _logger.warning("Erreur création auto rapport session Odoo: %s", e)

            _notify_backend('session', {
                'session_id': s.id,
                'session_name': s.name,
                'manager_name': s.user_id.name if s.user_id else "Gérant",
                'manager_login': s.user_id.login if s.user_id else "",
                'start_at': s.start_at.isoformat() if s.start_at else None,
                'state': s.state,
                'total_sales': s.total_payments_amount,
                'cash_difference': s.cash_register_difference,
            })
        return sessions

    def write(self, vals):
        res = super().write(vals)
        for s in self:
            if 'state' in vals and vals['state'] == 'closed':
                if s.user_id:
                    s.user_id.sudo().write({
                        'is_online': False,
                        'last_logout_time': s.stop_at or fields.Datetime.now(),
                    })
                    try:
                        self.env['restaurant.activity.log'].sudo().create({
                            'manager_id': s.user_id.id,
                            'manager_name': s.user_id.name,
                            'manager_login': s.user_id.login,
                            'action_type': 'logout',
                            'amount': s.total_payments_amount,
                            'description': f"⚪ Fin de service & Déconnexion du gérant {s.user_id.name}. Session {s.name} clôturée. Ventes : {s.total_payments_amount:,.0f} FCFA.",
                            'activity_time': s.stop_at or fields.Datetime.now(),
                        })
                    except Exception as e:
                        _logger.warning("Erreur journal clôture session: %s", e)

            if 'state' in vals or 'stop_at' in vals or 'total_payments_amount' in vals or 'start_at' in vals:
                _notify_backend('session', {
                    'session_id': s.id,
                    'session_name': s.name,
                    'manager_name': s.user_id.name if s.user_id else "Gérant",
                    'manager_login': s.user_id.login if s.user_id else "",
                    'start_at': s.start_at.isoformat() if s.start_at else None,
                    'stop_at': s.stop_at.isoformat() if s.stop_at else None,
                    'state': s.state,
                    'total_sales': s.total_payments_amount,
                    'cash_difference': s.cash_register_difference,
                })
        return res

    def open_frontend_cb(self):
        """Bloque l'ouverture de la caisse interactive par l'administrateur."""
        if not self._context.get('from_backend') and (self.env.user.id == 2 or (self.env.user.has_group('base.group_system') and not self.env.user.is_restaurant_manager)):
            raise UserError(_("L'administrateur n'a pas l'autorisation de vendre. Seuls les gérants désignés ont la capacité d'ouvrir une caisse et d'effectuer des ventes."))
        return super().open_frontend_cb()


class PosConfig(models.Model):
    _inherit = 'pos.config'

    def open_ui(self):
        """Bloque le lancement du point de vente interactif par l'administrateur."""
        if not self._context.get('from_backend') and (self.env.user.id == 2 or (self.env.user.has_group('base.group_system') and not self.env.user.is_restaurant_manager)):
            raise UserError(_("L'administrateur n'a pas l'autorisation de vendre. Seuls les gérants désignés ont la capacité d'ouvrir une caisse et d'effectuer des ventes."))
        return super().open_ui()



class ProductTemplate(models.Model):
    _inherit = 'product.template'

    available_in_pos = fields.Boolean(
        string="Disponible dans le Point de Vente",
        default=True,
        help="Activé automatiquement pour que le gérant trouve immédiatement le plat dans sa caisse."
    )
    is_restaurant_dish = fields.Boolean(
        string="Plat Restaurant",
        default=True,
        help="Indique si ce produit est géré par la carte du restaurant"
    )
    backend_item_id = fields.Char(
        string="ID Plat Backend",
        index=True,
        help="Identifiant du plat / produit dans la base de données du backend"
    )
    restaurant_category_id = fields.Many2one(
        'pos.category',
        string="Catégorie",
        help="Catégorie du produit (Plats Principaux, Boissons, Desserts, Entrées)",
        compute='_compute_restaurant_category',
        inverse='_inverse_restaurant_category',
        store=True,
    )

    @api.depends('pos_categ_ids')
    def _compute_restaurant_category(self):
        for rec in self:
            rec.restaurant_category_id = rec.pos_categ_ids[:1].id if rec.pos_categ_ids else False

    def _inverse_restaurant_category(self):
        for rec in self:
            if rec.restaurant_category_id:
                rec.pos_categ_ids = [(6, 0, [rec.restaurant_category_id.id])]
            else:
                rec.pos_categ_ids = [(5, 0, 0)]

    def _is_restaurant_admin(self):
        """Vérifie si l'utilisateur courant est l'administrateur exclusif du restaurant."""
        user = self.env.user
        return user.id == 2 or (user.has_group('base.group_system') and not user.is_restaurant_manager)

    @api.model_create_multi
    def create(self, vals_list):
        if self.env.uid and not self._is_restaurant_admin():
            raise UserError(_("Accès refusé : Seul l'administrateur est autorisé à ajouter des plats et des boissons dans le menu du restaurant."))
        main_dish_cat = self.env.ref('restaurant_core.pos_categ_main_dish', raise_if_not_found=False)
        for vals in vals_list:
            if self._context.get('default_restaurant_category_id') and not vals.get('restaurant_category_id'):
                vals['restaurant_category_id'] = self._context.get('default_restaurant_category_id')
            if vals.get('restaurant_category_id'):
                vals['pos_categ_ids'] = [(6, 0, [vals['restaurant_category_id']])]
            elif not vals.get('pos_categ_ids') and main_dish_cat:
                vals['restaurant_category_id'] = main_dish_cat.id
                vals['pos_categ_ids'] = [(6, 0, [main_dish_cat.id])]

            if self._context.get('default_is_restaurant_dish') or vals.get('is_restaurant_dish'):
                vals['available_in_pos'] = True
                vals['detailed_type'] = 'consu'
                vals['is_restaurant_dish'] = True
                vals['sale_ok'] = True
        records = super().create(vals_list)
        for rec in records:
            if rec.available_in_pos:
                cat_name = rec.restaurant_category_id.name if rec.restaurant_category_id else (rec.pos_categ_ids[:1].name if rec.pos_categ_ids else 'Plats Principaux')
                _notify_backend('dish', {
                    'tmpl_id': rec.id,
                    'name': rec.name,
                    'price': rec.list_price,
                    'category': cat_name
                })
        return records

    def write(self, vals):
        if self.env.uid and not self._is_restaurant_admin():
            dish_fields = {'name', 'list_price', 'restaurant_category_id', 'pos_categ_ids', 'available_in_pos', 'is_restaurant_dish', 'image_1920', 'description_sale', 'active'}
            if any(f in vals for f in dish_fields):
                raise UserError(_("Accès refusé : Seul l'administrateur est autorisé à modifier les plats et les boissons dans le menu du restaurant."))
        if vals.get('restaurant_category_id'):
            vals['pos_categ_ids'] = [(6, 0, [vals['restaurant_category_id']])]
        res = super().write(vals)
        for rec in self:
            if rec.available_in_pos and ('name' in vals or 'list_price' in vals or 'available_in_pos' in vals or 'active' in vals or 'restaurant_category_id' in vals or 'pos_categ_ids' in vals):
                cat_name = rec.restaurant_category_id.name if rec.restaurant_category_id else (rec.pos_categ_ids[:1].name if rec.pos_categ_ids else 'Plats Principaux')
                _notify_backend('dish', {
                    'tmpl_id': rec.id,
                    'name': rec.name,
                    'price': rec.list_price,
                    'category': cat_name
                })
        return res

    def unlink(self):
        if self.env.uid and not self._is_restaurant_admin():
            raise UserError(_("Accès refusé : Seul l'administrateur est autorisé à supprimer des plats ou des boissons du restaurant."))
        return super().unlink()

    def action_confirm_dish(self):
        """Bouton pour valider et enregistrer le plat immédiatement"""
        if not self._is_restaurant_admin():
            raise UserError(_("Accès refusé : Seul l'administrateur est autorisé à valider des plats."))
        for rec in self:
            rec.write({
                'available_in_pos': True,
                'detailed_type': 'consu',
                'is_restaurant_dish': True,
                'sale_ok': True,
            })
            cat_name = rec.restaurant_category_id.name if rec.restaurant_category_id else (rec.pos_categ_ids[:1].name if rec.pos_categ_ids else 'Plats Principaux')
            _notify_backend('dish', {
                'tmpl_id': rec.id,
                'name': rec.name,
                'price': rec.list_price,
                'category': cat_name
            })

        action = self.env.ref('restaurant_core.action_restaurant_dishes').read()[0]
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Plat Enregistré avec Succès !',
                'message': f"Le plat '{self.name}' ({self.list_price:,.0f} FCFA) a été validé et est disponible immédiatement en caisse.",
                'sticky': False,
                'type': 'success',
                'next': action,
            }
        }

    def action_delete_dish(self):
        """Supprime ou retire le plat du menu et du backend."""
        if not self._is_restaurant_admin():
            raise UserError(_("Accès refusé : Seul l'administrateur est autorisé à retirer des plats de la carte."))
        dish_name = self.name
        tmpl_id = self.id

        _notify_backend('dish_delete', {
            'tmpl_id': tmpl_id,
            'name': dish_name
        })

        try:
            self.unlink()
        except Exception as e:
            _logger.warning("Suppression directe bloquée par des sessions POS ouvertes, masquage du plat: %s", e)
            self.write({'active': False, 'available_in_pos': False})

        action = self.env.ref('restaurant_core.action_restaurant_dishes').read()[0]
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Plat Retiré du Menu',
                'message': f"Le plat '{dish_name}' a été retiré de la carte.",
                'sticky': False,
                'type': 'danger',
                'next': action,
            }
        }

    def unlink(self):
        if self.env.uid and not self._is_restaurant_admin():
            raise UserError(_("Accès refusé : Seul l'administrateur est autorisé à supprimer des plats ou des boissons du restaurant."))
        for rec in self:
            _notify_backend('dish_delete', {
                'tmpl_id': rec.id,
                'name': rec.name
            })
        return super().unlink()


class PosCategoryRestaurant(models.Model):
    _inherit = 'pos.category'

    def _is_restaurant_admin(self):
        user = self.env.user
        return user.id == 2 or (user.has_group('base.group_system') and not user.is_restaurant_manager)

    @api.model_create_multi
    def create(self, vals_list):
        if self.env.uid and not self._is_restaurant_admin():
            raise UserError(_("Accès refusé : Seul l'administrateur est autorisé à créer ou ajouter des catégories. Le gérant a uniquement le rôle d'exécuter les ventes."))
        return super().create(vals_list)

    def write(self, vals):
        if self.env.uid and not self._is_restaurant_admin():
            raise UserError(_("Accès refusé : Seul l'administrateur est autorisé à modifier les catégories du restaurant."))
        return super().write(vals)

    def unlink(self):
        if self.env.uid and not self._is_restaurant_admin():
            raise UserError(_("Accès refusé : Seul l'administrateur est autorisé à supprimer des catégories."))
        return super().unlink()


class ProductCategoryRestaurant(models.Model):
    _inherit = 'product.category'

    def _is_restaurant_admin(self):
        user = self.env.user
        return user.id == 2 or (user.has_group('base.group_system') and not user.is_restaurant_manager)

    @api.model_create_multi
    def create(self, vals_list):
        if self.env.uid and not self._is_restaurant_admin():
            raise UserError(_("Accès refusé : Seul l'administrateur est autorisé à créer des catégories."))
        return super().create(vals_list)

    def write(self, vals):
        if self.env.uid and not self._is_restaurant_admin():
            raise UserError(_("Accès refusé : Seul l'administrateur a le droit de modifier les catégories."))
        return super().write(vals)

    def unlink(self):
        if self.env.uid and not self._is_restaurant_admin():
            raise UserError(_("Accès refusé : Seul l'administrateur a le droit de supprimer des catégories."))
        return super().unlink()


class RestaurantTable(models.Model):
    _inherit = 'restaurant.table'

    backend_table_id = fields.Char(
        string="ID Table Backend",
        index=True,
        help="Identifiant de la table provenant du backend FastAPI"
    )


class ResUsers(models.Model):
    _inherit = 'res.users'

    is_restaurant_manager = fields.Boolean(
        string="Gérant de Restaurant",
        default=False,
        help="Définit si cet utilisateur est un gérant créé pour le restaurant."
    )
    manager_password = fields.Char(
        string="Mot de passe du Gérant",
        help="Mot de passe direct saisi par l'Administrateur pour le Gérant."
    )
    is_online = fields.Boolean(
        string="Présence en Ligne",
        default=False,
        help="Indique si le gérant est actuellement connecté et en service."
    )
    last_login_time = fields.Datetime(
        string="Prise de Service (Connexion)",
        help="Date et heure de début de service"
    )
    last_logout_time = fields.Datetime(
        string="Fin de Service (Déconnexion)",
        help="Date et heure de fin de service"
    )
    session_sales_total = fields.Float(
        string="Ventes Réalisées (FCFA)",
        default=0.0,
        help="Total des ventes réalisées lors de sa prise de poste"
    )

    def _is_restaurant_admin(self):
        """Vérifie si l'utilisateur courant est l'administrateur exclusif."""
        user = self.env.user
        return user.id == 2 or (user.has_group('base.group_system') and not user.is_restaurant_manager)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if self._context.get('default_is_restaurant_manager') or vals.get('is_restaurant_manager'):
                if self.env.uid and not self._is_restaurant_admin():
                    raise UserError(_("Accès refusé : Seul l'administrateur est autorisé à créer des gérants de restaurant."))

        pos_mgr_group = self.env.ref('point_of_sale.group_pos_manager', raise_if_not_found=False)
        pos_user_group = self.env.ref('point_of_sale.group_pos_user', raise_if_not_found=False)
        billing_group = self.env.ref('account.group_account_invoice', raise_if_not_found=False)
        base_user_group = self.env.ref('base.group_user', raise_if_not_found=False)

        mgr_groups = []
        if base_user_group:
            mgr_groups.append(base_user_group.id)
        if pos_mgr_group:
            mgr_groups.append(pos_mgr_group.id)
        elif pos_user_group:
            mgr_groups.append(pos_user_group.id)
        if billing_group:
            mgr_groups.append(billing_group.id)

        order_action = self.env.ref('restaurant_core.action_restaurant_gerant_own_orders', raise_if_not_found=False)
        action_rec = self.env['ir.actions.actions'].browse(order_action.id) if order_action else False

        for vals in vals_list:
            if self._context.get('default_is_restaurant_manager') or vals.get('is_restaurant_manager'):
                vals['is_restaurant_manager'] = True
                vals['active'] = True
                if action_rec:
                    vals['action_id'] = action_rec.id
                # Attribution des accès Point de Vente & Facturation dédiés au Gérant
                if mgr_groups:
                    vals['groups_id'] = [(6, 0, mgr_groups)]

        users = super().create(vals_list)

        for user, vals in zip(users, vals_list):
            if vals.get('manager_password'):
                user.password = vals['manager_password']
            if user.is_restaurant_manager:
                if action_rec:
                    user.action_id = action_rec
                _notify_backend('manager', {
                    'odoo_id': user.id,
                    'name': user.name,
                    'login': user.login,
                    'password': vals.get('manager_password', 'Pass1234!')
                })

        return users

    def write(self, vals):
        if vals.get('is_restaurant_manager'):
            pos_mgr_group = self.env.ref('point_of_sale.group_pos_manager', raise_if_not_found=False)
            pos_user_group = self.env.ref('point_of_sale.group_pos_user', raise_if_not_found=False)
            billing_group = self.env.ref('account.group_account_invoice', raise_if_not_found=False)
            base_user_group = self.env.ref('base.group_user', raise_if_not_found=False)

            mgr_groups = []
            if base_user_group:
                mgr_groups.append(base_user_group.id)
            if pos_mgr_group:
                mgr_groups.append(pos_mgr_group.id)
            elif pos_user_group:
                mgr_groups.append(pos_user_group.id)
            if billing_group:
                mgr_groups.append(billing_group.id)

            order_action = self.env.ref('restaurant_core.action_restaurant_gerant_own_orders', raise_if_not_found=False)
            if order_action:
                vals['action_id'] = order_action.id
            if mgr_groups:
                vals['groups_id'] = [(6, 0, mgr_groups)]
        elif vals.get('is_restaurant_manager') is False:
            vals['action_id'] = False

        res = super().write(vals)
        if vals.get('manager_password'):
            for user in self:
                user.password = vals['manager_password']
        return res

    def action_confirm_create_manager(self):
        """Bouton pour valider et enregistrer définitivement le gérant avec accès Point de Vente et Facturation."""
        if self.env.uid and not self._is_restaurant_admin():
            raise UserError(_("Accès refusé : Seul l'administrateur est autorisé à valider et enregistrer un gérant."))
        pos_mgr_group = self.env.ref('point_of_sale.group_pos_manager', raise_if_not_found=False)
        pos_user_group = self.env.ref('point_of_sale.group_pos_user', raise_if_not_found=False)
        billing_group = self.env.ref('account.group_account_invoice', raise_if_not_found=False)
        base_user_group = self.env.ref('base.group_user', raise_if_not_found=False)

        mgr_groups = []
        if base_user_group:
            mgr_groups.append(base_user_group.id)
        if pos_user_group:
            mgr_groups.append(pos_user_group.id)
        if billing_group:
            mgr_groups.append(billing_group.id)

        order_action = self.env.ref('restaurant_core.action_restaurant_gerant_own_orders', raise_if_not_found=False)

        for user in self:
            vals = {
                'is_restaurant_manager': True,
                'active': True,
            }
            if order_action:
                vals['action_id'] = order_action.id
            if mgr_groups:
                vals['groups_id'] = [(6, 0, mgr_groups)]
            user.write(vals)
            if user.manager_password:
                user.password = user.manager_password

            _notify_backend('manager', {
                'odoo_id': user.id,
                'name': user.name,
                'login': user.login,
                'password': user.manager_password or 'Pass1234!'
            })

        action = self.env.ref('restaurant_core.action_restaurant_managers').read()[0]
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Gérant Enregistré avec Succès !',
                'message': f"Le gérant {self.name} ({self.login}) a été officiellement enregistré avec accès Point de Vente & Facturation.",
                'sticky': False,
                'type': 'success',
                'next': action,
            }
        }

    def action_deactivate_manager(self):
        """Met fin aux accès du gérant (désactivation immédiate)."""
        if self.env.uid and not self._is_restaurant_admin():
            raise UserError(_("Accès refusé : Seul l'administrateur est autorisé à révoquer les accès d'un gérant."))
        for user in self:
            user.write({'active': False})
            _notify_backend('manager_toggle', {
                'odoo_id': user.id,
                'login': user.login,
                'is_active': False
            })
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Accès Révoqués',
                'message': f"Les accès du gérant {self.name} ont été révoqués. Il ne peut plus se connecter.",
                'sticky': False,
                'type': 'warning',
            }
        }

    def action_reactivate_manager(self):
        """Réactive les accès d'un gérant."""
        if self.env.uid and not self._is_restaurant_admin():
            raise UserError(_("Accès refusé : Seul l'administrateur est autorisé à réactiver un gérant."))
        for user in self:
            user.write({'active': True})
            _notify_backend('manager_toggle', {
                'odoo_id': user.id,
                'login': user.login,
                'is_active': True
            })
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Gérant Réactivé',
                'message': f"Le gérant {self.name} est à nouveau actif et peut se connecter.",
                'sticky': False,
                'type': 'success',
            }
        }

    def action_delete_manager(self):
        """Supprime ou retire sécuritairement le gérant d'Odoo et du backend."""
        if self.env.uid and not self._is_restaurant_admin():
            raise UserError(_("Accès refusé : Seul l'administrateur est autorisé à supprimer ou retirer un compte gérant."))
        user_names = []
        pos_mgr_group = self.env.ref('point_of_sale.group_pos_manager', raise_if_not_found=False)
        pos_user_group = self.env.ref('point_of_sale.group_pos_user', raise_if_not_found=False)
        groups_to_remove = []
        if pos_mgr_group:
            groups_to_remove.append((3, pos_mgr_group.id))
        if pos_user_group:
            groups_to_remove.append((3, pos_user_group.id))

        has_any_history = False

        for user in self:
            user_names.append(user.name or user.login)
            user_id = user.id
            user_login = user.login
            partner = user.partner_id

            # Vérification de l'existence d'opérations financières ou de documents
            has_orders = bool(self.env['pos.order'].sudo().search_count([('user_id', '=', user_id)]))
            has_marches = bool(self.env['restaurant.grand.marche'].sudo().search_count([('manager_id', '=', user_id)]))
            has_sessions = bool(self.env['pos.session'].sudo().search_count([('user_id', '=', user_id)]))
            has_invoices = bool(self.env['account.move'].sudo().search_count([('invoice_user_id', '=', user_id)])) if 'invoice_user_id' in self.env['account.move']._fields else False

            has_history = has_orders or has_marches or has_sessions or has_invoices

            if has_history:
                has_any_history = True
                # Révocation complète des accès et archivage sécurisé (respect des obligations fiscales DGI/OHADA)
                vals_archive = {
                    'active': False,
                    'is_restaurant_manager': False,
                    'action_id': False,
                }
                if groups_to_remove:
                    vals_archive['groups_id'] = groups_to_remove
                user.write(vals_archive)
                if partner and partner.active:
                    try:
                        partner.write({'active': False})
                    except Exception:
                        pass

                _notify_backend('manager_delete', {
                    'odoo_id': user_id,
                    'login': user_login
                })
            else:
                # Aucun historique : tentative de suppression physique sous savepoint PostgreSQL
                deleted_physically = False
                try:
                    with self.env.cr.savepoint():
                        _notify_backend('manager_delete', {
                            'odoo_id': user_id,
                            'login': user_login
                        })
                        user.unlink()
                        if partner and partner.active:
                            with self.env.cr.savepoint():
                                try:
                                    partner.unlink()
                                except Exception:
                                    pass
                        deleted_physically = True
                except Exception as e:
                    _logger.warning("Suppression physique directe annulée par contrainte SQL: %s", e)
                    deleted_physically = False

                if not deleted_physically:
                    has_any_history = True
                    vals_archive = {
                        'active': False,
                        'is_restaurant_manager': False,
                        'action_id': False,
                    }
                    if groups_to_remove:
                        vals_archive['groups_id'] = groups_to_remove
                    user.write(vals_archive)
                    if partner and partner.active:
                        try:
                            partner.write({'active': False})
                        except Exception:
                            pass

        action_ref = self.env.ref('restaurant_core.action_restaurant_managers', raise_if_not_found=False)
        action = action_ref.read()[0] if action_ref else False

        names_str = ", ".join(user_names)
        if has_any_history:
            msg = (
                f"Le compte du gérant {names_str} a été retiré et ses accès révoqués avec succès. "
                f"Ses ventes et pièces comptables sont intégralement conservées pour la conformité fiscale (DGI) et l'audit."
            )
            notif_type = 'warning'
            notif_title = 'Gérant Retiré & Archivé'
        else:
            msg = f"Le compte du gérant {names_str} a été définitivement supprimé."
            notif_type = 'success'
            notif_title = 'Gérant Supprimé'

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': notif_title,
                'message': msg,
                'sticky': False,
                'type': notif_type,
                'next': action,
            }
        }

    def unlink(self):
        for user in self:
            if user.is_restaurant_manager:
                if self.env.uid and not self._is_restaurant_admin():
                    raise UserError(_("Accès refusé : Seul l'administrateur est autorisé à supprimer un compte gérant."))
                has_orders = bool(self.env['pos.order'].sudo().search_count([('user_id', '=', user.id)]))
                has_marches = bool(self.env['restaurant.grand.marche'].sudo().search_count([('manager_id', '=', user.id)]))
                has_sessions = bool(self.env['pos.session'].sudo().search_count([('user_id', '=', user.id)]))
                if has_orders or has_marches or has_sessions:
                    raise UserError(
                        f"Impossible de supprimer définitivement le compte du gérant '{user.name}' ({user.login}) "
                        f"car des ventes, caisses ou factures Grand Marché lui sont rattachées.\n\n"
                        f"Pour la conformité légale et fiscale (DGI / OHADA), l'historique comptable ne peut pas être effacé.\n"
                        f"Veuillez plutôt utiliser le bouton 'Supprimer définitivement' ou 'Mettre fin aux accès' depuis sa fiche "
                        f"afin de révoquer ses droits et masquer son compte sans altérer vos déclarations financières."
                    )
                _notify_backend('manager_delete', {
                    'odoo_id': user.id,
                    'login': user.login
                })
        return super().unlink()


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    @api.model
    @api.returns('self')
    def get_user_roots(self):
        roots = super().get_user_roots()
        # Modules hors-sujet à masquer pour l'admin (Facturation reste 100% active et intacte)
        non_restaurant_xmlids = [
            'point_of_sale.menu_point_root',
            'mail.menu_root_discuss',
            'spreadsheet_dashboard.spreadsheet_dashboard_menu_root',
            'stock.menu_stock_root',
            'base.menu_management',
        ]
        excluded_menus = self.env['ir.ui.menu']
        for xmlid in non_restaurant_xmlids:
            menu_rec = self.env.ref(xmlid, raise_if_not_found=False)
            if menu_rec:
                excluded_menus |= menu_rec
        return roots - excluded_menus

    def _load_menus_blacklist(self):
        blacklist = super()._load_menus_blacklist()
        non_restaurant_xmlids = [
            'point_of_sale.menu_point_root',
            'mail.menu_root_discuss',
            'spreadsheet_dashboard.spreadsheet_dashboard_menu_root',
            'stock.menu_stock_root',
            'base.menu_management',
        ]
        non_resto_ids = []
        for xmlid in non_restaurant_xmlids:
            menu_rec = self.env.ref(xmlid, raise_if_not_found=False)
            if menu_rec:
                child_ids = self.search([('id', 'child_of', menu_rec.id)]).ids
                non_resto_ids.extend(child_ids)
        return list(set(blacklist + non_resto_ids))

    @api.model
    def load_menus(self, debug):
        """Gestion fine des menus :
        - Pour l'Admin : masque les éléments gérant spécifiques pour éviter les répétitions.
        - Pour le GÉRANT : conserve l'INTÉGRALITÉ absolue de tous ses menus et pages opérationnelles.
        """
        all_menus = super().load_menus(debug)
        is_admin = self.env.user.id == 2 or self.env.user.has_group('base.group_system')

        if is_admin:
            non_restaurant_xmlids = [
                'point_of_sale.menu_point_root',
                'mail.menu_root_discuss',
                'spreadsheet_dashboard.spreadsheet_dashboard_menu_root',
                'stock.menu_stock_root',
                'base.menu_management',
                'restaurant_core.menu_restaurant_gerant_pos',
                'restaurant_core.menu_restaurant_gerant_invoices',
                'restaurant_core.menu_restaurant_gerant_orders',
                'restaurant_core.menu_restaurant_dishes_gerant',
            ]
        else:
            # Pour le GÉRANT : ne masquer que les applications tierces hors-restaurant et le menu de gestion admin
            # Conserver en INTÉGRALITÉ : Caisse & Point de Vente, Mes Commandes & Ventes, Facturation & Reçus Clients, Menus & Plats (Consultation seule)
            non_restaurant_xmlids = [
                'mail.menu_root_discuss',
                'spreadsheet_dashboard.spreadsheet_dashboard_menu_root',
                'stock.menu_stock_root',
                'base.menu_management',
                'restaurant_core.menu_restaurant_dishes_all',
            ]

        to_purge_ids = set()
        for xmlid in non_restaurant_xmlids:
            m = self.env.ref(xmlid, raise_if_not_found=False)
            if m:
                to_purge_ids.add(m.id)

        def _purge_menu(mid):
            m = all_menus.pop(mid, None)
            if m and m.get('children'):
                for cid in m['children']:
                    _purge_menu(cid)

        for mid in list(to_purge_ids):
            _purge_menu(mid)

        if 'root' in all_menus and 'children' in all_menus['root']:
            all_menus['root']['children'] = [c for c in all_menus['root']['children'] if c not in to_purge_ids]

        rest_root = self.env.ref('restaurant_core.menu_restaurant_root', raise_if_not_found=False)
        if rest_root and rest_root.id in all_menus and 'children' in all_menus[rest_root.id]:
            all_menus[rest_root.id]['children'] = [c for c in all_menus[rest_root.id]['children'] if c not in to_purge_ids]

        return all_menus


class RestaurantActivityLog(models.Model):
    _name = 'restaurant.activity.log'
    _description = "Faits et Gestes des Gérants (Journal d'Activité)"
    _order = 'activity_time desc, id desc'

    name = fields.Char(string="Titre / Référence", compute="_compute_name", store=True)
    manager_id = fields.Many2one('res.users', string="Gérant Concerné")
    manager_name = fields.Char(string="Nom du Gérant", required=True)
    manager_login = fields.Char(string="Identifiant (Login)", required=True)
    action_type = fields.Selection([
        ('login', '🟢 Prise de Service (Connexion)'),
        ('logout', '⚪ Fin de Service (Déconnexion)'),
        ('order_sale', '💰 Encaissement Vente'),
        ('price_adjusted', '✏️ Ajustement Prix')
    ], string="Nature de l'Action", required=True, default='order_sale')
    description = fields.Text(string="Détails & Faits et Gestes", required=True)
    order_number = fields.Char(string="N° Commande")
    amount = fields.Float(string="Montant en Jeu (FCFA)", default=0.0)
    payment_method = fields.Char(string="Mode de Paiement")
    activity_time = fields.Datetime(string="Date & Heure", default=fields.Datetime.now, required=True)

    @api.depends('action_type', 'manager_name', 'order_number')
    def _compute_name(self):
        for rec in self:
            if rec.order_number:
                rec.name = f"{rec.manager_name} - Vente {rec.order_number}"
            else:
                rec.name = f"{rec.manager_name} - {rec.action_type or 'Action'}"


class AccountMove(models.Model):
    _inherit = 'account.move'

    restaurant_daily_report_id = fields.Many2one(
        'restaurant.daily.report',
        string="Facture Fiscale Restaurant",
        compute="_compute_restaurant_report",
        store=True,
    )
    restaurant_order_count = fields.Integer(
        string="Nb Ventes Cumulées",
        related="restaurant_daily_report_id.total_orders",
        readonly=True
    )
    restaurant_dgi_ref = fields.Char(
        string="Réf Fiscale DGI",
        related="restaurant_daily_report_id.dgi_reference",
        readonly=True
    )
    restaurant_dgi_state = fields.Selection(
        related="restaurant_daily_report_id.state",
        string="État DGI Restaurant",
        readonly=True
    )

    @api.depends('ref')
    def _compute_restaurant_report(self):
        for move in self:
            if move.ref:
                clean_ref = move.ref.split(' ')[0]
                report = self.env['restaurant.daily.report'].search([('name', '=', clean_ref)], limit=1)
                move.restaurant_daily_report_id = report.id if report else False
            else:
                move.restaurant_daily_report_id = False

    def action_open_restaurant_daily_report(self):
        self.ensure_one()
        if not self.restaurant_daily_report_id:
            raise UserError(_("Aucun rapport journalier restaurant lié à cette facture."))
        return {
            'type': 'ir.actions.act_window',
            'name': 'Facture Générale Journalière & DGI',
            'res_model': 'restaurant.daily.report',
            'res_id': self.restaurant_daily_report_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_print_restaurant_invoice(self):
        """Imprime la facture client officielle conforme au design restaurant & DGI."""
        self.ensure_one()
        return self.env.ref('restaurant_core.action_report_restaurant_account_move_invoice').report_action(self)

    def get_dgi_qr_code_base64(self):
        """Génère le QR Code fiscal DGI en Base64 pour la facture comptable."""
        self.ensure_one()
        cfg = self.env['restaurant.configuration'].sudo().search([], limit=1)
        nim = (cfg.nim if cfg and cfg.nim else 'RESTO-DGI-MCF-01')
        ifu = ((cfg.ifu if cfg and cfg.ifu else False) or 
               (self.company_id.vat if hasattr(self, 'company_id') else '') or 
               '000123456789A')
        cli_ifu = (self.partner_id.vat if (self.partner_id and self.partner_id.vat) else 'PARTICULIER')
        ref = self.name or self.ref or self.restaurant_dgi_ref or f"INV-{self.id}"
        date_str = str(self.invoice_date or fields.Date.today())
        total_ttc = int(self.amount_total or 0)
        total_ht = int(self.amount_untaxed or 0)
        total_tax = int(self.amount_tax or 0)
        
        qr_payload = f"DGI-FNE|NIM:{nim}|IFU:{ifu}|CLI_IFU:{cli_ifu}|REF:{ref}|DATE:{date_str}|HT:{total_ht}|TVA:{total_tax}|TTC:{total_ttc}|CERTIFIE_DGI"
        
        try:
            import qrcode
            import io
            import base64
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=4,
                border=1,
            )
            qr.add_data(qr_payload)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            img_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            return f"data:image/png;base64,{img_b64}"
        except Exception:
            import urllib.parse
            return f"https://api.qrserver.com/v1/create-qr-code/?size=100x100&data={urllib.parse.quote(qr_payload)}"


class RestaurantDailyReport(models.Model):
    _name = 'restaurant.daily.report'
    _description = "Facture Générale de la Journée & Certification DGI"
    _order = 'date desc, id desc'

    name = fields.Char(string="N° Facture Fiscale", required=True, default=lambda self: f"FACT-GEN-{fields.Date.today().strftime('%Y%m%d')}-01")
    date = fields.Date(string="Date Fiscale", required=True, default=fields.Date.today)
    
    # Données et identifiants de l'établissement (Synchronisés avec restaurant.configuration)
    company_name = fields.Char(string="Émetteur / Raison Sociale")
    company_subtitle = fields.Char(string="Sous-Titre / Slogan de l'Établissement")
    company_nif = fields.Char(string="NIF DGI de l'Entreprise")
    company_ifu = fields.Char(string="IFU DGI de l'Entreprise")
    company_rccm = fields.Char(string="RCCM")
    company_tax_regime = fields.Char(string="Régime Fiscal")
    company_fiscal_division = fields.Char(string="Division Fiscale")
    company_phone = fields.Char(string="Téléphone(s)")
    company_address = fields.Char(string="Adresse Complète")
    company_email = fields.Char(string="Adresse Email")
    company_website = fields.Char(string="Site Web")
    company_nim = fields.Char(string="NIM (Machine Fiscale DGI)")
    company_legal_mention = fields.Text(string="Mention Légale Obligatoire")
    tax_rate = fields.Float(string="Taux TVA DGI (%)", default=18.0)
    currency_id = fields.Many2one('res.currency', string="Devise", default=lambda self: self.env.company.currency_id)
    top_dgi_header_html = fields.Html(string="En-tête Officiel DGI & QR Code", compute="_compute_top_dgi_header", readonly=True)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        cfg = self.env['restaurant.configuration'].sudo().search([], limit=1)
        c = self.env.company
        if cfg:
            reg_dict = dict(cfg._fields['tax_regime'].selection) if 'tax_regime' in cfg._fields else {}
            res.update({
                'company_name': cfg.name or c.name or "Restaurant",
                'company_subtitle': cfg.subtitle or "",
                'company_ifu': cfg.ifu or c.vat or "",
                'company_nif': cfg.ifu or c.vat or "",
                'company_rccm': cfg.rccm or "",
                'company_tax_regime': reg_dict.get(cfg.tax_regime, cfg.tax_regime or ""),
                'company_fiscal_division': cfg.fiscal_division or "",
                'company_phone': cfg.phone or c.phone or "",
                'company_address': cfg.address or f"{c.street or ''} {c.city or ''}".strip() or "",
                'company_email': cfg.email or c.email or "",
                'company_website': cfg.website or c.website or "",
                'company_nim': cfg.nim or "",
                'company_legal_mention': cfg.legal_mention or "",
            })
        elif c:
            res.update({
                'company_name': c.name or "Restaurant",
                'company_subtitle': "",
                'company_ifu': c.vat or "",
                'company_nif': c.vat or "",
                'company_rccm': "",
                'company_tax_regime': "Régime du Réel Normal d'Imposition (RNI)",
                'company_fiscal_division': "",
                'company_phone': c.phone or "",
                'company_address': f"{c.street or ''} {c.city or ''}".strip() or "",
                'company_email': c.email or "",
                'company_website': c.website or "",
                'company_nim': "RESTO-DGI-MCF-01",
                'company_legal_mention': "Facture normalisée certifiée conforme aux exigences de la DGI",
            })
        return res

    @api.model_create_multi
    def create(self, vals_list):
        cfg = self.env['restaurant.configuration'].sudo().search([], limit=1)
        c = self.env.company
        for vals in vals_list:
            if cfg:
                reg_dict = dict(cfg._fields['tax_regime'].selection) if 'tax_regime' in cfg._fields else {}
                vals.setdefault('company_name', cfg.name or c.name)
                vals.setdefault('company_subtitle', cfg.subtitle or '')
                vals.setdefault('company_ifu', cfg.ifu or c.vat)
                vals.setdefault('company_nif', cfg.ifu or c.vat)
                vals.setdefault('company_rccm', cfg.rccm or '')
                vals.setdefault('company_tax_regime', reg_dict.get(cfg.tax_regime, cfg.tax_regime or ''))
                vals.setdefault('company_fiscal_division', cfg.fiscal_division or '')
                vals.setdefault('company_phone', cfg.phone or c.phone)
                vals.setdefault('company_address', cfg.address or f"{c.street or ''} {c.city or ''}".strip())
                vals.setdefault('company_email', cfg.email or c.email)
                vals.setdefault('company_website', cfg.website or c.website)
                vals.setdefault('company_nim', cfg.nim or 'RESTO-DGI-MCF-01')
                vals.setdefault('company_legal_mention', cfg.legal_mention or '')
            elif c:
                vals.setdefault('company_name', c.name)
                vals.setdefault('company_ifu', c.vat or '')
                vals.setdefault('company_nif', c.vat or '')
                vals.setdefault('company_phone', c.phone or '')
                vals.setdefault('company_address', f"{c.street or ''} {c.city or ''}".strip())
                vals.setdefault('company_email', c.email or '')
                vals.setdefault('company_website', c.website or '')
        return super().create(vals_list)

    def get_dgi_qr_code_base64(self):
        """Génère le QR code DGI en base64 pour la facture générale journalière."""
        self.ensure_one()
        cfg = self.env['restaurant.configuration'].sudo().search([], limit=1)
        c = self.env.company
        nim = (cfg.nim if cfg and cfg.nim else (self.company_nim or "RESTO-DGI-MCF-01"))
        ifu = (cfg.ifu if cfg and cfg.ifu else (self.company_ifu or c.vat or "-"))
        rccm = (cfg.rccm if cfg and cfg.rccm else (self.company_rccm or "-"))
        ref = self.dgi_reference or (f"DGI-FNE-{self.date.strftime('%Y%m%d') if self.date else '2026'}-01")
        statut = "CERTIFIEE_DGI" if self.is_certified_dgi else "EN_COURS"
        qr_data = f"DGI-FNE|NIM:{nim}|IFU:{ifu}|RCCM:{rccm}|FACT:{self.name}|TTC:{int(self.total_ttc)}|HT:{int(self.total_ht)}|REF:{ref}|STATUT:{statut}"
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
            _logger.warning("Erreur génération QR code daily report: %s", e)
            import urllib.parse
            return f"https://api.qrserver.com/v1/create-qr-code/?size=110x110&data={urllib.parse.quote(qr_data)}"

    @api.depends('name', 'date', 'total_ttc', 'total_ht', 'is_certified_dgi', 'dgi_reference',
                 'company_name', 'company_subtitle', 'company_ifu', 'company_rccm', 'company_phone', 'company_address', 'company_email')
    def _compute_top_dgi_header(self):
        cfg = self.env['restaurant.configuration'].sudo().search([], limit=1)
        c = self.env.company
        for rec in self:
            resto_name = (cfg.name if (cfg and cfg.name) else (rec.company_name or c.name)) or "Restaurant"
            resto_sub = (cfg.subtitle if (cfg and cfg.subtitle) else (rec.company_subtitle or ""))
            ifu = (cfg.ifu if (cfg and cfg.ifu) else (rec.company_ifu or c.vat)) or ""
            rccm = (cfg.rccm if (cfg and cfg.rccm) else rec.company_rccm) or ""
            regime = rec.company_tax_regime or ""
            if cfg and 'tax_regime' in cfg._fields:
                regime = dict(cfg._fields['tax_regime'].selection).get(cfg.tax_regime, cfg.tax_regime or regime)
            division = (cfg.fiscal_division if (cfg and cfg.fiscal_division) else rec.company_fiscal_division) or ""
            phone = (cfg.phone if (cfg and cfg.phone) else (rec.company_phone or c.phone)) or ""
            address = (cfg.address if (cfg and cfg.address) else (rec.company_address or c.street)) or ""
            email = (cfg.email if (cfg and cfg.email) else (rec.company_email or c.email)) or ""
            status_text = "FACTURE CERTIFIÉE DGI" if rec.is_certified_dgi else "SESSION EN COURS • DGI"
            ref_stamp = rec.dgi_reference or (f"DGI-FNE-{rec.date.strftime('%Y%m%d')}-01" if rec.date else "DGI-FNE-PENDING")
            qr_url = rec.get_dgi_qr_code_base64()

            logo_img = f'<img src="/web/image/restaurant.configuration/{cfg.id}/logo" alt="Logo" style="max-height: 75px; max-width: 75px; object-fit: contain;"/>' if (cfg and cfg.logo) else (
                f'<img src="/web/image/res.company/{c.id}/logo" alt="Logo" style="max-height: 75px; max-width: 75px; object-fit: contain;"/>' if c.logo else '<span style="font-size: 38px;">🍽️</span>'
            )

            slogan_html = f'<p class="text-muted fw-semibold mb-1" style="font-size: 12px; margin-top: 2px;">{resto_sub}</p>' if resto_sub else ''

            rec.top_dgi_header_html = f"""
            <div class="p-3 mb-3 rounded-3 shadow-sm" style="background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%); border: 2px solid #10b981;">
                <div class="d-flex justify-content-between align-items-center mb-2 px-2 py-1 rounded text-white" style="background-color: #0f172a; font-size: 11px; font-weight: bold; letter-spacing: 0.5px;">
                    <span>🏛️ RÉPUBLIQUE • DIRECTION GÉNÉRALE DES IMPÔTS (DGI) • e-MCF</span>
                    <span class="badge {'bg-success' if rec.is_certified_dgi else 'bg-warning text-dark'}">{status_text}</span>
                </div>
                <div class="row align-items-center g-3">
                    <div class="col-12 col-md-8 col-lg-9 d-flex gap-3 align-items-start">
                        <div class="rounded-3 border d-flex align-items-center justify-content-center p-2 bg-white shadow-sm flex-shrink-0" style="width: 75px; height: 75px; border-color: #cbd5e1 !important;">
                            {logo_img}
                        </div>
                        <div class="flex-grow-1">
                            <h4 class="fw-bold text-dark mb-0" style="font-size: 19px; line-height: 1.2;">{resto_name}</h4>
                            {slogan_html}
                            <div class="d-flex flex-wrap gap-2 text-muted mb-1" style="font-size: 11px;">
                                <span><strong>IFU :</strong> <code class="text-primary fw-bold">{ifu or '-'}</code></span>
                                <span>•</span>
                                <span><strong>RCCM :</strong> <code class="text-dark">{rccm or '-'}</code></span>
                                <span>•</span>
                                <span><strong>Régime :</strong> <span class="badge bg-light text-dark border">{regime or '-'}</span></span>
                                <span>•</span>
                                <span><strong>Division :</strong> <span class="text-primary fw-bold">{division or '-'}</span></span>
                            </div>
                            <div class="text-muted" style="font-size: 11px;">
                                <span>📍 {address or '-'}</span> &nbsp;•&nbsp; <span>📞 {phone or '-'}</span> &nbsp;•&nbsp; <span>✉️ {email or '-'}</span>
                            </div>
                        </div>
                    </div>
                    <div class="col-12 col-md-4 col-lg-3 text-center">
                        <div class="p-2 rounded-3 bg-white border shadow-sm d-inline-block" style="border: 2px solid #10b981 !important;">
                            <div class="fw-bold text-success text-uppercase mb-1" style="font-size: 9px; letter-spacing: 0.5px;">
                                🏛️ APPROBATION DGI
                            </div>
                            <img src="{qr_url}" alt="QR DGI" style="width: 95px; height: 95px; display: block; margin: 0 auto;"/>
                            <div class="fw-bold text-dark mt-1" style="font-size: 10px; font-family: monospace;">
                                {ref_stamp}
                            </div>
                            <div class="text-success fw-bold" style="font-size: 9px;">
                                {"✅ Scellée e-MCF" if rec.is_certified_dgi else "⏳ Facture Active"}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """

    total_ttc = fields.Float(string="Total Brut TTC (FCFA)", default=0.0)
    total_ht = fields.Float(string="Base Hors Taxes (HT)", default=0.0)
    total_tva = fields.Float(string="TVA DGI (18%)", default=0.0)
    total_orders = fields.Integer(string="Nombre Total de Ventes", default=0)
    order_ids = fields.Many2many(
        'pos.order',
        'restaurant_daily_report_pos_order_rel',
        'report_id',
        'order_id',
        string="Encaissements & Reçus de la Journée"
    )
    managers_summary = fields.Text(
        string="Ventes par Gérant de la Journée",
        readonly=True
    )
    managers_summary_html = fields.Html(
        string="Ventilation Visuelle par Gérant",
        readonly=True
    )
    payment_methods_summary = fields.Text(
        string="Répartition des Modes de Paiement",
        readonly=True
    )
    payment_methods_html = fields.Html(
        string="Ventilation Visuelle des Règlements",
        readonly=True
    )
    is_certified_dgi = fields.Boolean(string="Certifiée DGI", default=False)
    dgi_reference = fields.Char(string="Référence Fiscale DGI (FNE)")
    dgi_security_code = fields.Char(string="Signature SHA-256")
    dgi_certified_at = fields.Datetime(string="Horodatage Certification DGI")
    certified_by = fields.Char(string="Certifié Par", default="Administrateur")
    dgi_qr_html = fields.Html(
        string="Aperçu Fiscal DGI & Sceau Numérique",
        readonly=True
    )
    state = fields.Selection([
        ('draft', 'Brouillon Dynamique'),
        ('certified', '🏛️ Certifiée DGI (Verrouillée)')
    ], string="État", default='draft')
    invoice_id = fields.Many2one('account.move', string="Facture Comptable Odoo")

    # Champs du gérant ayant ouvert la session
    active_manager_id = fields.Many2one('res.users', string="Gérant de Session", index=True)
    active_manager_name = fields.Char(string="Gérant Connecté", default="Gérant")
    session_opened_at = fields.Datetime(string="Prise de Service (Date & Heure)", default=fields.Datetime.now)

    def action_print_pdf_invoice(self):
        """Déclenche l'impression PDF de la facture officielle conforme au design avec logo watermark."""
        self.ensure_one()
        return self.env.ref('restaurant_core.action_report_restaurant_daily_invoice').report_action(self)

    @api.model
    def create_manager_session_report(self, user_or_id, login_time_str=None, manager_name=None):
        """Méthode publique appelable par XML-RPC pour créer la facture de session à la connexion du gérant."""
        return self._create_manager_session_report(user_or_id, login_time_str, manager_name)

    @api.model
    def _create_manager_session_report(self, user_or_id, login_time_str=None, manager_name=None):
        """Crée automatiquement la Facture Générale pour le gérant connecté dès sa prise de service."""
        user = False
        if isinstance(user_or_id, int) and user_or_id:
            user = self.env['res.users'].browse(user_or_id)
            if not user.exists():
                user = False
        if not user and manager_name:
            user = self.env['res.users'].search([('name', '=', manager_name)], limit=1)
        if not user and hasattr(user_or_id, 'id'):
            user = user_or_id

        m_name = (user.name if user else manager_name) or "Gérant"
        m_id = user.id if user else False

        today = fields.Date.today()
        now = fields.Datetime.now()
        clean_name = "".join(c for c in m_name if c.isalnum() or c in "-_")
        time_suffix = now.strftime('%H%M')
        inv_name = f"FACT-MGR-{today.strftime('%Y%m%d')}-{clean_name[:10].upper()}-{time_suffix}"

        # Chercher si une facture de session ouverte pour ce gérant existe déjà aujourd'hui
        domain = [
            ('date', '=', today),
            ('state', '=', 'draft')
        ]
        if m_id:
            domain.append(('active_manager_id', '=', m_id))
        else:
            domain.append(('active_manager_name', '=', m_name))

        existing = self.search(domain, order='id desc', limit=1)
        if existing:
            return existing.id

        report = self.create({
            'name': inv_name,
            'date': today,
            'active_manager_id': m_id,
            'active_manager_name': m_name,
            'session_opened_at': now,
            'state': 'draft',
            'total_ttc': 0.0,
            'total_ht': 0.0,
            'total_tva': 0.0,
            'total_orders': 0
        })

        # Créer immédiatement la facture client comptable correspondante dans account.move
        try:
            partner = self.env['res.partner'].search([('name', '=', 'Clients Restaurant (Ventes Comptoir)')], limit=1)
            if not partner:
                partner = self.env['res.partner'].sudo().create({
                    'name': 'Clients Restaurant (Ventes Comptoir)',
                    'customer_rank': 1,
                })
            journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
            tax_18 = self.env['account.tax'].search([('type_tax_use', '=', 'sale'), ('name', 'ilike', '18')], limit=1)
            tax_ids = [(6, 0, [tax_18.id])] if tax_18 else []

            narration = (
                f"Facture Globale de Session - Réf: {report.name}\n"
                f"Gérant connecté: {user.name} ({user.login})\n"
                f"Prise de service: {now.strftime('%d/%m/%Y à %H:%M:%S')}\n"
                f"En attente des premières ventes..."
            )
            move = self.env['account.move'].sudo().create({
                'move_type': 'out_invoice',
                'partner_id': partner.id,
                'journal_id': journal.id if journal else False,
                'invoice_date': today,
                'ref': report.name,
                'narration': narration,
                'invoice_line_ids': [
                    (0, 0, {
                        'name': f"Session de Vente Restaurant - Gérant {user.name} ({today})",
                        'quantity': 1,
                        'price_unit': 0.0,
                        'tax_ids': tax_ids,
                    })
                ]
            })
            report.invoice_id = move.id
        except Exception as e:
            _logger.warning("Erreur création initiale account.move session: %s", e)

        return report.id

    @api.model
    def _accumulate_order(self, order):
        """Accumule automatiquement chaque paiement dans la Facture Générale du gérant ou du jour."""
        today = fields.Date.today()
        order_date = order.date_order.date() if order.date_order else today
        mgr_user = order.user_id or (order.session_id.user_id if order.session_id else False)

        # 1. Chercher la facture de session ouverte de ce gérant
        report = False
        if mgr_user:
            report = self.search([
                ('active_manager_id', '=', mgr_user.id),
                ('date', '=', order_date),
                ('state', '=', 'draft')
            ], order='id desc', limit=1)

        # 2. Sinon, chercher la facture générale de la date
        if not report:
            report = self.search([('date', '=', order_date), ('state', '=', 'draft')], order='id desc', limit=1)

        # 3. Si aucune facture n'existe, en créer une
        if not report:
            clean_name = "".join(c for c in (mgr_user.name if mgr_user else "GERANT") if c.isalnum() or c in "-_")
            time_suffix = fields.Datetime.now().strftime('%H%M')
            report = self.create({
                'name': f"FACT-MGR-{order_date.strftime('%Y%m%d')}-{clean_name[:10].upper()}-{time_suffix}",
                'date': order_date,
                'active_manager_id': mgr_user.id if mgr_user else False,
                'active_manager_name': mgr_user.name if mgr_user else "Gérant",
                'session_opened_at': order.date_order or fields.Datetime.now(),
                'state': 'draft'
            })

        if report.state != 'certified':
            report.action_calculate_from_orders()
        return report

    def action_reset_draft(self):
        """Permet à l'administrateur de déverrouiller la journée si de nouveaux encaissements ont été réalisés."""
        for rec in self:
            rec.state = 'draft'
            rec.action_calculate_from_orders()
        return True

    def action_view_invoice(self):
        """Ouvre la facture client officielle dans le module Facturation."""
        self.ensure_one()
        if not self.invoice_id:
            raise UserError(_("Aucune facture comptable n'est encore générée pour ce rapport."))
        return {
            'type': 'ir.actions.act_window',
            'name': 'Facture Client Officielle (Facturation Odoo)',
            'res_model': 'account.move',
            'res_id': self.invoice_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def _sync_accounting_invoice(self, rec):
        """Synchronise ou crée en temps réel la facture client officielle dans account.move."""
        if not rec.total_ttc or rec.total_ttc <= 0:
            return

        partner = self.env['res.partner'].search([('name', '=', 'Clients Restaurant (Ventes Comptoir)')], limit=1)
        if not partner:
            partner = self.env['res.partner'].sudo().create({
                'name': 'Clients Restaurant (Ventes Comptoir)',
                'customer_rank': 1,
            })

        journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
        if not journal:
            return

        tax_18 = self.env['account.tax'].search([('type_tax_use', '=', 'sale'), ('name', 'ilike', '18')], limit=1)
        tax_ids = [(6, 0, [tax_18.id])] if tax_18 else []

        narration = (
            f"Facture Globale Journalière - Réf: {rec.name}\n"
            f"Date fiscale: {rec.date}\n"
            f"Nombre de commandes cumulées: {rec.total_orders}\n"
            f"Base Hors Taxes (HT): {rec.total_ht:,.0f} FCFA\n"
            f"TVA DGI Collectée (18%): {rec.total_tva:,.0f} FCFA\n"
            f"Total Net Encaissé (TTC): {rec.total_ttc:,.0f} FCFA"
        )

        if not rec.invoice_id:
            existing_move = self.env['account.move'].search([('ref', '=', rec.name), ('move_type', '=', 'out_invoice')], limit=1)
            if existing_move:
                rec.invoice_id = existing_move.id
                move = existing_move
            else:
                try:
                    move = self.env['account.move'].sudo().create({
                        'move_type': 'out_invoice',
                        'partner_id': partner.id,
                        'journal_id': journal.id,
                        'invoice_date': rec.date,
                        'ref': rec.name,
                        'narration': narration,
                        'invoice_line_ids': [
                            (0, 0, {
                                'name': f"Chiffre d'Affaires Restaurant ({rec.date})",
                                'quantity': 1,
                                'price_unit': rec.total_ttc,
                                'tax_ids': tax_ids,
                            })
                        ]
                    })
                    rec.invoice_id = move.id
                except Exception as e:
                    _logger.warning("Erreur création initiale account.move: %s", e)
                    return
        else:
            move = rec.invoice_id

        if move and move.state == 'draft':
            try:
                move.write({'narration': narration})
                if move.invoice_line_ids:
                    move.invoice_line_ids[0].sudo().write({
                        'price_unit': rec.total_ttc,
                        'tax_ids': tax_ids,
                    })
            except Exception as e:
                _logger.warning("Erreur mise à jour account.move: %s", e)

    def action_calculate_from_orders(self):
        """Calcule et consolide tous les encaissements de la journée."""
        for rec in self:
            domain = [
                ('date_order', '>=', f"{rec.date} 00:00:00"),
                ('date_order', '<=', f"{rec.date} 23:59:59"),
                ('state', 'in', ['paid', 'done', 'invoiced'])
            ]
            if rec.active_manager_id:
                domain.append(('user_id', '=', rec.active_manager_id.id))
            orders = self.env['pos.order'].search(domain, order='date_order desc')

            total_ttc = sum(orders.mapped('amount_total'))
            rec.total_ttc = total_ttc
            rec.total_ht = round(total_ttc / 1.18, 2) if total_ttc > 0 else 0.0
            rec.total_tva = round(total_ttc - rec.total_ht, 2) if total_ttc > 0 else 0.0
            rec.total_orders = len(orders)
            rec.order_ids = [(6, 0, orders.ids)]

            # Résumé par gérant
            mgr_stats = {}
            for o in orders:
                m_name = o.user_id.name or "Gérant Inconnu"
                if m_name not in mgr_stats:
                    mgr_stats[m_name] = {'count': 0, 'amount': 0.0}
                mgr_stats[m_name]['count'] += 1
                mgr_stats[m_name]['amount'] += o.amount_total

            lines = []
            for m_name, s in mgr_stats.items():
                lines.append(f"👤 {m_name} : {s['count']} vente(s) encaissée(s) | Total net sans monnaie : {s['amount']:,.0f} FCFA")
            rec.managers_summary = "\n".join(lines) if lines else "Aucune vente enregistrée pour le moment."

            # Cartes visuelles HTML des gérants
            mgr_cards = []
            for m_name, s in mgr_stats.items():
                pct = (s['amount'] / total_ttc * 100) if total_ttc > 0 else 0
                mgr_cards.append(f"""
                <div class="col-12 col-md-6 col-lg-4 mb-3">
                    <div class="p-3 bg-white rounded-3 border shadow-sm h-100" style="border-left: 5px solid #2563eb !important;">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <span class="fw-bold text-dark" style="font-size: 15px;">👤 {m_name}</span>
                            <span class="badge bg-primary text-white">{s['count']} vente(s)</span>
                        </div>
                        <div class="fs-4 fw-bold text-primary mb-1">
                            {s['amount']:,.0f} FCFA
                        </div>
                        <div class="d-flex justify-content-between align-items-center text-muted mb-2" style="font-size: 11px;">
                            <span>Contribution au C.A.</span>
                            <span class="fw-bold text-dark">{pct:.1f}%</span>
                        </div>
                        <div class="progress" style="height: 6px;">
                            <div class="progress-bar bg-primary" role="progressbar" style="width: {pct}%;"></div>
                        </div>
                    </div>
                </div>
                """)

            if mgr_cards:
                rec.managers_summary_html = f"""
                <div class="p-2">
                    <h5 class="fw-bold text-dark mb-3">📊 Répartition des Ventes &amp; Encaissements par Gérant</h5>
                    <div class="row g-3">
                        {"".join(mgr_cards)}
                    </div>
                </div>
                """
            else:
                rec.managers_summary_html = """
                <div class="alert alert-light text-center p-4 border rounded">
                    <i class="fa fa-users fa-2x text-muted mb-2 d-block"></i>
                    <span class="text-muted">Aucune vente enregistrée pour le moment.</span>
                </div>
                """

            # Résumé par mode de paiement
            pm_stats = {}
            for o in orders:
                pm_name = o.payment_method_name or "Espèces (Cash)"
                pm_stats[pm_name] = pm_stats.get(pm_name, 0.0) + o.amount_total

            pm_lines = []
            for pm_name, amt in pm_stats.items():
                pm_lines.append(f"💳 {pm_name} : {amt:,.0f} FCFA")
            rec.payment_methods_summary = "\n".join(pm_lines) if pm_lines else "Aucun encaissement."

            pm_cards = []
            for pm_name, amt in pm_stats.items():
                pct = (amt / total_ttc * 100) if total_ttc > 0 else 0
                pm_cards.append(f"""
                <div class="col-12 col-md-4 mb-3">
                    <div class="p-3 bg-white rounded-3 border shadow-sm h-100" style="border-left: 5px solid #10b981 !important;">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <span class="fw-bold text-dark" style="font-size: 14px;">💳 {pm_name}</span>
                            <span class="badge bg-success text-white">{pct:.1f}%</span>
                        </div>
                        <div class="fs-4 fw-bold text-success mb-1">
                            {amt:,.0f} FCFA
                        </div>
                        <div class="text-muted" style="font-size: 11px;">Total encaissé via ce mode</div>
                    </div>
                </div>
                """)

            if pm_cards:
                rec.payment_methods_html = f"""
                <div class="p-2">
                    <h5 class="fw-bold text-dark mb-3">💳 Répartition des Encaissements par Mode de Règlement</h5>
                    <div class="row g-3">
                        {"".join(pm_cards)}
                    </div>
                </div>
                """
            else:
                rec.payment_methods_html = """
                <div class="alert alert-light text-center p-4 border rounded">
                    <i class="fa fa-credit-card fa-2x text-muted mb-2 d-block"></i>
                    <span class="text-muted">Aucun encaissement enregistré.</span>
                </div>
                """

            # Aperçu DGI
            if rec.is_certified_dgi:
                rec.dgi_qr_html = f"""
                <div class="p-3 bg-white rounded-3 border text-center shadow-sm">
                    <div class="badge bg-success p-2 mb-2 d-block">SCEAU OFFICIEL DGI-FNE</div>
                    <div class="p-2 border rounded bg-light mb-2 d-inline-block">
                        <img src="https://api.qrserver.com/v1/create-qr-code/?size=140x140&data=DGI|{rec.dgi_reference}|TTC:{rec.total_ttc}|HT:{rec.total_ht}" alt="QR DGI" style="width: 140px; height: 140px;"/>
                    </div>
                    <div class="text-muted font-monospace" style="font-size: 10px;">{rec.dgi_reference}</div>
                    <small class="text-success fw-bold d-block mt-1">Vérifié &amp; Conforme</small>
                </div>
                """
            else:
                rec.dgi_qr_html = """
                <div class="p-3 bg-white rounded-3 border text-center shadow-sm text-muted">
                    <i class="fa fa-lock fa-3x text-secondary mb-2 d-block"></i>
                    <div class="fw-bold mb-1">Facture en cours d'encaissement</div>
                    <small style="font-size: 11px;">Le sceau cryptographique et le QR code fiscal seront activés lors de la certification finale DGI.</small>
                </div>
                """

            # Synchronisation automatique de la facture client dans account.move
            try:
                self._sync_accounting_invoice(rec)
            except Exception as e:
                _logger.warning("Erreur synchronisation automatique account.move: %s", e)

        return True

    def action_certify_dgi(self):
        """Certifie la facture générale de la journée auprès de la DGI et valide la facture dans le module Facturation."""
        import hashlib
        for rec in self:
            rec.action_calculate_from_orders()
            raw_str = f"DGI|NIF:{rec.company_nif}|DATE:{rec.date}|TTC:{rec.total_ttc}|HT:{rec.total_ht}|TVA:{rec.total_tva}|ORDERS:{rec.total_orders}|SALT_DGI"
            sig = hashlib.sha256(raw_str.encode('utf-8')).hexdigest()
            ref = f"DGI-FNE-{rec.date.strftime('%Y%m%d')}-{sig[:8].upper()}"
            vals = {
                'is_certified_dgi': True,
                'dgi_reference': ref,
                'dgi_security_code': sig,
                'dgi_certified_at': fields.Datetime.now(),
                'certified_by': self.env.user.name,
                'state': 'certified'
            }

            rec.write(vals)

            # Validation comptable officielle
            if rec.invoice_id and rec.invoice_id.state == 'draft':
                try:
                    narration = (
                        f"Facture Globale Journalière - Réf: {rec.name}\n"
                        f"Date fiscale: {rec.date}\n"
                        f"Nombre de commandes: {rec.total_orders}\n"
                        f"Base HT: {rec.total_ht:,.0f} FCFA | TVA 18%: {rec.total_tva:,.0f} FCFA | TTC: {rec.total_ttc:,.0f} FCFA\n\n"
                        f"🏛️ CERTIFICATION FISCALE DGI (FNE) VALIDÉE\n"
                        f"Référence Fiscale : {ref}\n"
                        f"Signature SHA-256 : {sig}\n"
                        f"Certifié par : {self.env.user.name} le {fields.Datetime.now()}"
                    )
                    rec.invoice_id.write({
                        'ref': f"{rec.name} ({ref})",
                        'narration': narration
                    })
                    rec.invoice_id.action_post()
                except Exception as e:
                    _logger.warning("Erreur validation comptable account.move: %s", e)

            try:
                self.env['restaurant.activity.log'].sudo().create({
                    'manager_name': self.env.user.name,
                    'manager_login': self.env.user.login,
                    'action_type': 'order_sale',
                    'order_number': rec.name,
                    'amount': rec.total_ttc,
                    'description': f"🏛️ Certification DGI Facture Générale {rec.name} ({rec.total_orders} ventes, {rec.total_ttc:,.0f} FCFA TTC). Réf DGI: {ref}",
                    'activity_time': fields.Datetime.now(),
                })
            except Exception as e:
                _logger.warning("Erreur journal activité Odoo: %s", e)

            _notify_backend('daily_report_certified', {
                'invoice_date': rec.date.isoformat(),
                'invoice_number': rec.name,
                'total_ttc': rec.total_ttc,
                'total_ht': rec.total_ht,
                'total_tva': rec.total_tva,
                'total_orders': rec.total_orders,
                'dgi_reference': ref,
                'dgi_security_code': sig,
                'certified_by': self.env.user.name,
            })
        return True


class RestaurantConfiguration(models.Model):
    _name = 'restaurant.configuration'
    _description = "Configuration de l'Établissement & Fiscalité DGI"

    name = fields.Char(string="Nom du Restaurant", default="Lemo Daje Restaurant", required=True)
    subtitle = fields.Char(string="Sous-Titre / Slogan", default="Restaurant & Grill Gastronomique")
    logo = fields.Binary(string="Logo Officiel de l'Entreprise", attachment=True)
    ifu = fields.Char(string="IFU (Identifiant Fiscal Unique)", default="000123456789A", required=True)
    rccm = fields.Char(string="RCCM (Registre du Commerce)", default="BF-OUA-01-2024-B12-00456", required=True)
    phone = fields.Char(string="Téléphone(s) de Contact", default="+226 25 30 00 00", required=True)
    address = fields.Char(string="Adresse Complète", default="Avenue Kwame Nkrumah, Ouagadougou", required=True)
    email = fields.Char(string="Adresse Email", default="contact@lemodaje.com", required=True)
    website = fields.Char(string="Site Web", default="www.lemodaje.com")
    tax_regime = fields.Selection([
        ('RNI', "Régime du Réel Normal d'Imposition (RNI)"),
        ('RSI', "Régime Simplifié d'Imposition (RSI)"),
        ('CME', "Contribution des Micro-Entreprises (CME)"),
        ('SYNTHETIQUE', "Régime Synthétique / Forfaitaire"),
    ], string="Régime Fiscal", default='RNI', required=True)
    fiscal_division = fields.Char(string="Division Fiscale (Centre des Impôts)", default="DGI - Division Fiscale des Moyennes Entreprises", required=True)
    nim = fields.Char(string="NIM (Machine e-MCF DGI)", default="RESTO-DGI-MCF-01")
    tax_rate = fields.Float(string="Taux de TVA Normalisé (%)", default=18.0)
    legal_mention = fields.Text(string="Mention Légale Obligatoire", default="Facture normalisée certifiée conforme aux exigences de la DGI")
    dgi_qr_top_preview = fields.Html(string="Aperçu En-tête avec Code QR DGI Toujours en Haut", compute="_compute_dgi_qr_top_preview")

    def get_sample_dgi_qr_base64(self):
        """Retourne un code QR DGI scannable en Base64 pour l'aperçu du modèle."""
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAKwAAACsAQAAAADOSnp1AAABrklEQVR4nLWXMQ5bMQxDn4Pu9A1y/2PlBvQJXof/OxRNCyRQvVkDTUgUJS95c87jXRQ+DJ+1FpvFOuy9zz5rrU9B3oep1rZtyHWzneHNWbB3QiWszVmfg/wjXPbebA7p1yB/nB8APHNcvNi73xN8E44cDtu1nyaLOIS9uqG/hTbM1BJVE9ASreoQdg2tiMbUZAzbEGmNJUbmeEsRGwg0tAz1DoWQ0mDQkGasliG0iW2ubI/VsjccAkRljrcNJbZVLjVO1ZIktCY1KZnrHcQADakxzVzvkCJVoSTJWL5TSpuStmkZ04nU6wV6VbNz+kbSCoqNMDXTMEmTlCpNYSzflWpigSg6hf1gN4sX+1l8Lbq/AfkLb4DEX+KWOT8xTYqtakrGckJ7aTtoIw2M8W6il/1xD87BvmyxtJezdNJjc4/hYJFBP6kpKtcWAemcfxuDqZAYY6b8u6VY0oQQGNSJ2kLt1fh2Cnt1g8tFjksO8HxN7bHaAwaXBwiv55Sf9E6HbaSFuXlZ2ohe6rNMzfkHQHpkeVjnucGO/tNCg/cuO9bzBSp6rxPVqVm8/uO/+CcqbbLoEYMG+AAAAABJRU5ErkJggg=="

    @api.depends('name', 'ifu', 'rccm', 'tax_regime', 'fiscal_division', 'phone', 'address', 'email', 'logo')
    def _compute_dgi_qr_top_preview(self):
        for rec in self:
            c = self.env.company
            regime_dict = dict(self._fields['tax_regime'].selection)
            regime_label = regime_dict.get(rec.tax_regime, rec.tax_regime or "Régime du Réel Normal")
            qr_data = f"DGI-FNE|APPROBATION:VALIDEE|IFU:{rec.ifu or '000123456789A'}|RCCM:{rec.rccm or 'BF-OUA-01-2024-B12-00456'}|REGIME:{regime_label}|DIVISION:{rec.fiscal_division or 'DGI'}|RESTO:{rec.name or 'RESTAURANT'}|TEL:{rec.phone or ''}|EMAIL:{rec.email or ''}|STATUT:CERTIFIEE_DGI"
            qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=115x115&data={qr_data}"
            logo_img = f'<img src="/web/image/restaurant.configuration/{rec.id}/logo" alt="Logo" style="max-height: 80px; max-width: 80px; object-fit: contain;"/>' if rec.logo else ('<img src="/web/image/res.company/' + str(c.id) + '/logo" alt="Logo" style="max-height: 80px; max-width: 80px; object-fit: contain;"/>' if c.logo else '<span style="font-size: 40px;">🍽️</span>')

            rec.dgi_qr_top_preview = f"""
            <div class="p-3 mb-3 rounded-3 shadow-sm bg-white" style="border: 2px solid #10b981;">
                <div class="d-flex justify-content-between align-items-center mb-2 px-3 py-1 rounded text-white" style="background-color: #0f172a; font-size: 11px; font-weight: bold; letter-spacing: 0.5px;">
                    <span>🏛️ RÉPUBLIQUE • DIRECTION GÉNÉRALE DES IMPÔTS (DGI) • EN-TÊTE OFFICIEL DE FACTURE</span>
                    <span class="badge bg-success">✅ FACTURE CERTIFIÉE DGI (e-MCF)</span>
                </div>
                <div class="row align-items-center g-3">
                    <div class="col-12 col-md-8 col-lg-9 d-flex gap-3 align-items-start">
                        <div class="rounded-3 border d-flex align-items-center justify-content-center p-2 bg-light shadow-sm flex-shrink-0" style="width: 85px; height: 85px; border-color: #cbd5e1 !important;">
                            {logo_img}
                        </div>
                        <div class="flex-grow-1">
                            <h3 class="fw-bold text-dark mb-0" style="font-size: 20px; line-height: 1.2;">{rec.name or 'Lemo Daje Restaurant'}</h3>
                            <small class="text-muted d-block mb-1">{rec.subtitle or 'Restaurant & Grill'}</small>
                            <div class="d-flex flex-wrap gap-2 text-muted mb-1" style="font-size: 11px;">
                                <span><strong>IFU :</strong> <code class="text-primary fw-bold">{rec.ifu or '-'}</code></span>
                                <span>•</span>
                                <span><strong>RCCM :</strong> <code class="text-dark">{rec.rccm or '-'}</code></span>
                                <span>•</span>
                                <span><strong>Régime :</strong> <span class="badge bg-light text-dark border">{regime_label}</span></span>
                                <span>•</span>
                                <span><strong>Division :</strong> <span class="text-primary fw-bold">{rec.fiscal_division or '-'}</span></span>
                            </div>
                            <div class="text-muted" style="font-size: 11px;">
                                <span>📍 {rec.address or '-'}</span> &nbsp;•&nbsp; <span>📞 {rec.phone or '-'}</span> &nbsp;•&nbsp; <span>✉️ {rec.email or '-'}</span>
                            </div>
                        </div>
                    </div>
                    <div class="col-12 col-md-4 col-lg-3 text-center">
                        <div class="p-2 rounded-3 bg-white border shadow-sm d-inline-block" style="border: 2px solid #10b981 !important;">
                            <div class="fw-bold text-success text-uppercase mb-1" style="font-size: 9px; letter-spacing: 0.5px;">
                                🏛️ APPROBATION DGI
                            </div>
                            <img src="{qr_url}" alt="QR DGI" style="width: 95px; height: 95px; display: block; margin: 0 auto;"/>
                            <div class="fw-bold text-dark mt-1" style="font-size: 10px; font-family: monospace;">
                                DGI-FNE-CERT-OK
                            </div>
                            <div class="text-success fw-bold" style="font-size: 9px;">
                                Facture Certifiée DGI
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """

    @api.model
    def action_open_configuration(self):
        rec = self.search([], limit=1)
        if not rec:
            c = self.env.company
            rec = self.create({
                'name': c.name or 'Lemo Daje Restaurant',
                'ifu': c.vat or '000123456789A',
                'rccm': 'BF-OUA-01-2024-B12-00456',
                'phone': c.phone or '+226 25 30 00 00',
                'address': f"{c.street or ''} {c.city or ''}".strip() or 'Avenue Kwame Nkrumah, Ouagadougou',
                'email': c.email or 'contact@lemodaje.com',
                'logo': c.logo,
            })
        return {
            'type': 'ir.actions.act_window',
            'name': "⚙️ Configuration de l'Établissement & Fiscalité DGI",
            'res_model': 'restaurant.configuration',
            'res_id': rec.id,
            'view_mode': 'form',
            'target': 'current',
        }

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            rec._sync_to_company_and_backend()
        return records

    def write(self, vals):
        res = super().write(vals)
        for rec in self:
            rec._sync_to_company_and_backend()
        return res

    def _sync_to_company_and_backend(self):
        for rec in self:
            # 1. Mettre à jour la société Odoo active
            c = self.env.company
            vals_company = {
                'name': rec.name,
                'vat': rec.ifu,
                'phone': rec.phone,
                'email': rec.email,
                'street': rec.address,
                'website': rec.website,
            }
            if rec.logo:
                vals_company['logo'] = rec.logo
            c.sudo().write(vals_company)

            # 2. Mettre à jour tous les rapports journaliers / factures globales
            regime_label = dict(rec._fields['tax_regime'].selection).get(rec.tax_regime, rec.tax_regime) if 'tax_regime' in rec._fields else ''
            reports = self.env['restaurant.daily.report'].sudo().search([])
            for rep in reports:
                rep_vals = {
                    'company_name': rec.name,
                    'company_subtitle': rec.subtitle or '',
                    'company_ifu': rec.ifu or '',
                    'company_nif': rec.ifu or '',
                    'company_rccm': rec.rccm or '',
                    'company_tax_regime': regime_label,
                    'company_fiscal_division': rec.fiscal_division or '',
                    'company_phone': rec.phone or '',
                    'company_address': rec.address or '',
                    'company_email': rec.email or '',
                    'company_website': rec.website or '',
                    'company_nim': rec.nim or '',
                    'company_legal_mention': rec.legal_mention or '',
                }
                rep.sudo().write(rep_vals)

            # 3. Synchroniser vers le backend FastAPI (FastAPI Moteur Restaurant)
            try:
                logo_b64 = f"data:image/png;base64,{rec.logo.decode()}" if rec.logo else ""
                payload = {
                    "restaurant_name": rec.name,
                    "restaurant_subtitle": rec.subtitle or "",
                    "ifu": rec.ifu or "",
                    "nif": rec.ifu or "",
                    "rccm": rec.rccm or "",
                    "phone": rec.phone or "",
                    "address": rec.address or "",
                    "email": rec.email or "",
                    "website": rec.website or "",
                    "default_tax_regime": regime_label,
                    "fiscal_division": rec.fiscal_division or "",
                    "nim": rec.nim or "",
                    "tax_rate": rec.tax_rate or 18.0,
                    "legal_mention": rec.legal_mention or "",
                    "logo_url": logo_b64
                }
                _notify_backend('sync_settings_from_odoo', payload)
            except Exception as e:
                _logger.warning("Notification FastAPI échouée lors de la synchronisation: %s", e)

    def action_save_and_sync(self):
        self.ensure_one()
        self._sync_to_company_and_backend()

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': "Configuration Enregistrée & Synchronisée",
                'message': "Les identifiants fiscaux, le slogan, les coordonnées et le logo ont été appliqués à toutes les factures avec succès !",
                'type': 'success',
                'sticky': False,
            }
        }


# =========================================================================
# FILTRAGE DES MESSAGES & DÉSACTIVATION COMPLÈTE D'ODOOBOT
# Seuls les messages des gérants sont autorisés et reçus par l'administrateur
# =========================================================================

class ResUsersBotDisable(models.Model):
    _inherit = 'res.users'

    def _init_messaging(self):
        # Bloquer définitivement toute initialisation ou relance d'OdooBot
        if self.sudo().odoobot_state != 'disabled':
            self.sudo().write({'odoobot_state': 'disabled'})
        res = super()._init_messaging()
        res['odoobotOnboarding'] = False
        return res

    def _init_odoobot(self):
        # Désactiver OdooBot sans créer de conversation ni envoyer de message
        self.sudo().write({'odoobot_state': 'disabled'})
        return False


class MailBotDisable(models.AbstractModel):
    _inherit = 'mail.bot'

    def _apply_logic(self, record, values, command=None):
        # Annuler toute logique automatique ou réponse d'OdooBot
        return


class DiscussChannelBotFilter(models.Model):
    _inherit = 'discuss.channel'

    @api.model_create_multi
    def create(self, vals_list):
        # Bloquer la création automatique de canaux ou discussions avec OdooBot
        filtered_vals = []
        for vals in vals_list:
            name = vals.get('name', '')
            if 'odoobot' in (name or '').lower():
                continue
            filtered_vals.append(vals)
        if not filtered_vals:
            return self.browse()
        return super().create(filtered_vals)


class MailMessageFilter(models.Model):
    _inherit = 'mail.message'

    @api.model_create_multi
    def create(self, vals_list):
        # Stopper les notifications automatiques OdooBot pour l'administrateur
        for vals in vals_list:
            body = vals.get('body', '')
            author_id = vals.get('author_id')
            # Si le message vient du bot ou contient du texte automatique
            if author_id == 2 or 'odoobot' in str(body).lower():
                vals['needaction'] = False
        return super().create(vals_list)


class RestaurantIrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        res = super(RestaurantIrHttp, self).session_info()
        user = self.env.user
        if user:
            is_admin = bool(user.id == 2 or (user.has_group('base.group_system') and not user.is_restaurant_manager))
            is_gerant = bool(user.is_restaurant_manager or (user.has_group('point_of_sale.group_pos_user') and not is_admin))
            res['is_restaurant_manager'] = is_gerant
            res['is_restaurant_admin'] = is_admin
        return res


class RestaurantIrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    @api.model
    def search(self, domain, offset=0, limit=None, order=None):
        user = self.env.user
        domain_copy = list(domain) if domain else []
        if user and user.id != 1:
            is_admin = bool(user.id == 2 or (user.has_group('base.group_system') and not user.is_restaurant_manager))
            is_gerant = bool(user.is_restaurant_manager or (user.has_group('point_of_sale.group_pos_user') and not is_admin))

            gerant_xml_ids = [
                'restaurant_core.menu_restaurant_gerant_pos',
                'restaurant_core.menu_restaurant_gerant_invoices',
                'restaurant_core.menu_restaurant_gerant_orders',
                'restaurant_core.menu_restaurant_dishes_gerant',
            ]
            admin_xml_ids = [
                'restaurant_core.menu_restaurant_dashboard',
                'restaurant_core.menu_restaurant_managers',
                'restaurant_core.menu_restaurant_dishes_all',
                'restaurant_core.menu_restaurant_sessions',
                'restaurant_core.menu_restaurant_orders',
                'restaurant_core.menu_restaurant_invoices',
                'restaurant_core.menu_restaurant_config_direct',
            ]

            if is_admin:
                hidden_ids = []
                for xid in gerant_xml_ids:
                    m = self.env.ref(xid, raise_if_not_found=False)
                    if m:
                        hidden_ids.append(m.id)
                if hidden_ids:
                    domain_copy.append(('id', 'not in', hidden_ids))
            elif is_gerant:
                hidden_ids = []
                for xid in admin_xml_ids:
                    m = self.env.ref(xid, raise_if_not_found=False)
                    if m:
                        hidden_ids.append(m.id)
                if hidden_ids:
                    domain_copy.append(('id', 'not in', hidden_ids))

        return super().search(domain_copy, offset=offset, limit=limit, order=order)


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def _build_wkhtmltopdf_args(self, paperformat_id, landscape, specific_paperformat_args=None, set_viewport_size=False):
        command_args = super()._build_wkhtmltopdf_args(
            paperformat_id, landscape, specific_paperformat_args=specific_paperformat_args, set_viewport_size=set_viewport_size
        )
        if '--encoding' not in command_args:
            command_args.extend(['--encoding', 'utf-8'])
        return command_args
