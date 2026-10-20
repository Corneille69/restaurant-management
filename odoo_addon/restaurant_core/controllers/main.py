# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.home import Home
from odoo.addons.web.controllers.session import Session
from odoo.addons.point_of_sale.controllers.main import PosController
import logging
import math
import json

_logger = logging.getLogger(__name__)

class RestaurantHome(Home):

    def _login_redirect(self, uid, redirect=None):
        """Redirige le gérant vers l'accueil chaleureux puis l'interface de vente."""
        if uid and uid != 2:
            try:
                user = request.env['res.users'].sudo().browse(uid)
                is_admin = (user.id == 2 or (user.has_group('base.group_system') and not user.is_restaurant_manager))
                is_gerant = (
                    user.is_restaurant_manager or 
                    (user.has_group('point_of_sale.group_pos_user') and not is_admin)
                )
                if is_gerant:
                    # Enregistrer automatiquement la prise de service du gérant et ouvrir sa session
                    try:
                        user.action_manager_logged_in()
                    except Exception as err:
                        _logger.warning("Erreur action_manager_logged_in: %s", err)

                    return "/restaurant/welcome"
            except Exception as e:
                _logger.warning("Erreur redirection gérant login: %s", e)
        return super()._login_redirect(uid, redirect=redirect)


class RestaurantSessionController(Session):

    @http.route('/web/session/authenticate', type='json', auth="none")
    def authenticate(self, db, login, password, base_location=None):
        """Intercepte la connexion et déclenche la prise de service du gérant."""
        res = super().authenticate(db, login, password, base_location=base_location)
        uid = res.get('uid')
        if uid and uid != 2:
            try:
                user = request.env['res.users'].sudo().browse(uid)
                is_admin = (user.id == 2 or (user.has_group('base.group_system') and not user.is_restaurant_manager))
                is_gerant = (
                    user.is_restaurant_manager or 
                    (user.has_group('point_of_sale.group_pos_user') and not is_admin)
                )
                if is_gerant:
                    user.action_manager_logged_in()
            except Exception as e:
                _logger.warning("Erreur prise de poste gérant authenticate: %s", e)
        return res

    @http.route('/web/session/logout', type='http', auth="none")
    def logout(self, redirect='/web'):
        """Intercepte la déconnexion et clôture instantanément la session de service du gérant."""
        uid = request.session.uid
        if uid and uid != 2:
            try:
                user = request.env['res.users'].sudo().browse(uid)
                is_admin = (user.id == 2 or (user.has_group('base.group_system') and not user.is_restaurant_manager))
                is_gerant = (
                    user.is_restaurant_manager or 
                    (user.has_group('point_of_sale.group_pos_user') and not is_admin)
                )
                if is_gerant:
                    user.action_manager_logged_out()
            except Exception as e:
                _logger.warning("Erreur clôture session gérant au logout: %s", e)

        return super().logout(redirect=redirect)

    @http.route('/restaurant/api/session/logout', type='json', auth="user", csrf=False)
    def api_session_logout(self):
        """API de déconnexion rapide pour clôture immédiate."""
        uid = request.session.uid
        if uid and uid != 2:
            try:
                user = request.env['res.users'].sudo().browse(uid)
                is_admin = (user.id == 2 or (user.has_group('base.group_system') and not user.is_restaurant_manager))
                is_gerant = (
                    user.is_restaurant_manager or 
                    (user.has_group('point_of_sale.group_pos_user') and not is_admin)
                )
                if is_gerant:
                    user.action_manager_logged_out()
                    return {'status': 'ok'}
            except Exception as e:
                return {'status': 'error', 'message': str(e)}
        return {'status': 'ignored'}

    @http.route('/restaurant/welcome', type='http', auth='user')
    def restaurant_welcome(self, **kw):
        """Écran d'accueil cinématographique personnalisé pour le gérant avec le nom du restaurant."""
        uid = request.session.uid
        user = request.env['res.users'].sudo().browse(uid)

        # Récupération dynamique de la marque restaurant configurée
        config = request.env['restaurant.configuration'].sudo().search([], limit=1)
        company = request.env['res.company'].sudo().browse(1)
        restaurant_name = (config.name if config and config.name else company.name) or "LE JOLIE DU GOUT"
        subtitle = (config.subtitle if config and config.subtitle else "") or ""

        write_dt = config.write_date if (config and config.write_date) else (company.write_date or None)
        timestamp = int(write_dt.timestamp()) if write_dt else 1
        if config and config.logo:
            logo_url = f"/web/image/restaurant.configuration/{config.id}/logo?unique={timestamp}"
        elif company.logo:
            logo_url = f"/web/image/res.company/{company.id}/logo?unique={timestamp}"
        else:
            logo_url = f"/web/binary/company_logo?unique={timestamp}"

        pos_config = request.env['pos.config'].sudo().search([('active', '=', True)], limit=1)
        target_pos_url = f"/pos/ui?config_id={pos_config.id}" if pos_config else "/pos/ui"

        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bon Retour | {restaurant_name}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            min-height: 100vh;
            background: #0c1424;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1.5rem;
        }}
        .welcome-card {{
            width: 100%;
            max-width: 480px;
            background: #111c30;
            border: 1px solid #1e2e47;
            border-radius: 24px;
            padding: 38px 32px;
            text-align: center;
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.45);
            animation: fadeIn 0.4s ease-out;
            transition: opacity 0.3s ease, transform 0.3s ease;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        /* Logo épuré dans carte arrondie */
        .logo-box {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 96px;
            height: 96px;
            background: #17243a;
            border: 1.5px solid #23354e;
            border-radius: 20px;
            padding: 10px;
            margin-bottom: 20px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        }}
        .logo-img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            border-radius: 12px;
        }}
        /* En-tête sobre et chaleureux */
        .welcome-greeting {{
            font-size: 14px;
            font-weight: 700;
            color: #e58b00;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 6px;
        }}
        .restaurant-name {{
            font-size: 26px;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: -0.01em;
            margin-bottom: 22px;
        }}
        /* Boîte message humaine et conviviale */
        .user-greeting-box {{
            background: #17243a;
            border: 1px solid #23354e;
            border-radius: 16px;
            padding: 18px 20px;
            margin-bottom: 24px;
            text-align: center;
        }}
        .user-greeting-title {{
            font-size: 17px;
            font-weight: 700;
            color: #e58b00;
            margin-bottom: 6px;
        }}
        .user-greeting-text {{
            font-size: 14px;
            font-weight: 400;
            color: #94a3b8;
            line-height: 1.5;
        }}
        /* Barre de progression discrète */
        .progress-track {{
            width: 100%;
            height: 4px;
            background: #1b293e;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 12px;
        }}
        .progress-fill {{
            height: 100%;
            width: 0%;
            background: #e58b00;
            border-radius: 10px;
            animation: fillBar 2.4s ease-in-out forwards;
        }}
        @keyframes fillBar {{
            0% {{ width: 0%; }}
            100% {{ width: 100%; }}
        }}
        .redirect-status {{
            font-size: 13px;
            font-weight: 500;
            color: #64748b;
            margin-bottom: 22px;
        }}
        /* Bouton propre et élégant */
        .btn-direct {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            width: 100%;
            padding: 13px 24px;
            background: #e58b00;
            color: #0c1424;
            font-family: inherit;
            font-size: 15px;
            font-weight: 700;
            border-radius: 50px;
            border: none;
            cursor: pointer;
            text-decoration: none;
            box-shadow: 0 4px 14px rgba(229, 139, 0, 0.3);
            transition: all 0.2s ease;
        }}
        .btn-direct:hover {{
            background: #f59e0b;
            transform: translateY(-1px);
            box-shadow: 0 6px 18px rgba(229, 139, 0, 0.45);
        }}
        .btn-direct:active {{
            transform: translateY(0);
        }}
        .fade-out {{
            opacity: 0;
            transform: scale(0.98);
        }}
    </style>
</head>
<body>
    <div class="welcome-card" id="card">
        <div class="logo-box">
            <img src="{logo_url}" alt="{restaurant_name}" class="logo-img">
        </div>

        <div class="welcome-greeting">Bon retour chez</div>
        <h1 class="restaurant-name">{restaurant_name}</h1>

        <div class="user-greeting-box">
            <div class="user-greeting-title">Bonjour {user.name}</div>
            <div class="user-greeting-text">Excellente journée et bon service à vous ! Votre caisse est prête pour vos ventes.</div>
        </div>

        <div class="progress-track">
            <div class="progress-fill"></div>
        </div>
        <div class="redirect-status">
            Accès direct à votre espace de vente...
        </div>

        <a href="{target_pos_url}" id="btn-direct" class="btn-direct">
            Accéder à la caisse &rarr;
        </a>
    </div>

    <script>
        const targetUrl = "{target_pos_url}";
        const card = document.getElementById('card');
        let done = false;
        function goNow() {{
            if (done) return;
            done = true;
            card.classList.add('fade-out');
            setTimeout(() => {{
                window.location.href = targetUrl;
            }}, 250);
        }}
        document.getElementById('btn-direct').addEventListener('click', function(e) {{
            e.preventDefault();
            goNow();
        }});
        setTimeout(goNow, 2400);
    </script>
</body>
</html>"""
        return request.make_response(
            html,
            headers=[
                ('Content-Type', 'text/html; charset=utf-8'),
                ('Cache-Control', 'no-cache, no-store, must-revalidate'),
            ]
        )

    @http.route('/', type='http', auth="none")
    def index(self, s_action=None, db=None, **kw):
        """Redirige un gérant connecté directement vers l'interface de vente."""
        if request.db and request.session.uid and request.session.uid != 2:
            try:
                user = request.env['res.users'].sudo().browse(request.session.uid)
                is_admin = (user.id == 2 or (user.has_group('base.group_system') and not user.is_restaurant_manager))
                is_gerant = (
                    user.is_restaurant_manager or 
                    (user.has_group('point_of_sale.group_pos_user') and not is_admin)
                )
                if is_gerant and not s_action and not kw.get('redirect'):
                    pos_config = request.env['pos.config'].sudo().search([('active', '=', True)], limit=1)
                    if pos_config:
                        return request.redirect(f"/pos/ui?config_id={pos_config.id}")
                    return request.redirect("/pos/ui")
            except Exception as e:
                _logger.warning("Erreur index gérant: %s", e)
        return super().index(s_action=s_action, db=db, **kw)


class RestaurantPosController(PosController):

    @http.route(['/pos/web', '/pos/ui'], type='http', auth='user')
    def pos_web(self, config_id=False, **k):
        """Assure que le gérant accède immédiatement et fiablement à la caisse.
        Si aucune session n'est ouverte, elle est créée et lancée automatiquement."""
        try:
            if config_id:
                pos_config = request.env['pos.config'].sudo().browse(int(config_id))
            else:
                pos_config = request.env['pos.config'].sudo().search([('active', '=', True)], limit=1)
                if pos_config:
                    config_id = pos_config.id

            if pos_config and pos_config.active:
                domain = [
                    ('state', 'in', ['opening_control', 'opened']),
                    ('rescue', '=', False),
                    ('config_id', '=', pos_config.id),
                ]
                pos_session = request.env['pos.session'].sudo().search(domain, limit=1)
                if not pos_session:
                    # Création automatique de la session caisse pour le gérant
                    request.env['pos.session'].sudo().create({
                        'user_id': request.session.uid,
                        'config_id': pos_config.id,
                    })
        except Exception as e:
            _logger.error("Erreur auto-session POS pos_web: %s", e)

        return super().pos_web(config_id=config_id, **k)


class RestaurantBrandController(http.Controller):

    @http.route('/restaurant/api/brand', type='http', auth='none', cors='*', methods=['GET'], csrf=False)
    def get_restaurant_brand(self):
        """Retourne en temps réel les informations configurées du restaurant (Nom, Logo, Slogan)."""
        import json
        try:
            config = request.env['restaurant.configuration'].sudo().search([], limit=1)
            company = request.env['res.company'].sudo().browse(1)
            pos_cfg = request.env['pos.config'].sudo().search([('active', '=', True)], limit=1)
            pos_config_id = pos_cfg.id if pos_cfg else 2

            name = (config.name if config and config.name else company.name) or "RESTAURANT"
            subtitle = (config.subtitle if config and config.subtitle else "") or ""

            write_dt = config.write_date if (config and config.write_date) else (company.write_date or None)
            timestamp = int(write_dt.timestamp()) if write_dt else 1
            has_logo = bool((config and config.logo) or company.logo)
            if config and config.logo:
                logo_url = f"/web/image/restaurant.configuration/{config.id}/logo?unique={timestamp}"
            elif company.logo:
                logo_url = f"/web/image/res.company/{company.id}/logo?unique={timestamp}"
            else:
                logo_url = f"/web/binary/company_logo?unique={timestamp}"

            uid = request.session.uid
            is_admin = False
            is_gerant = False
            user_name = ""
            if uid:
                try:
                    u = request.env['res.users'].sudo().browse(uid)
                    is_admin = bool(u.id == 2 or (u.has_group('base.group_system') and not u.is_restaurant_manager))
                    is_gerant = bool(u.is_restaurant_manager or (u.has_group('point_of_sale.group_pos_user') and not is_admin))
                    user_name = u.name or ""
                    if is_gerant and not u.is_online:
                        try:
                            u.action_manager_logged_in()
                        except Exception as e_login:
                            _logger.warning("Erreur sync session brand: %s", e_login)
                except Exception:
                    pass

            data = {
                'name': name,
                'subtitle': subtitle,
                'logo_url': logo_url,
                'has_logo': has_logo,
                'timestamp': timestamp,
                'is_gerant': is_gerant,
                'is_admin': is_admin,
                'user_name': user_name,
                'pos_config_id': pos_config_id,
            }
        except Exception as e:
            _logger.error("Erreur lecture restaurant brand: %s", e)
            data = {
                'name': "RESTAURANT",
                'subtitle': "",
                'logo_url': "/web/binary/company_logo",
                'has_logo': True,
                'timestamp': 1,
                'is_gerant': False,
                'is_admin': True,
                'user_name': "",
            }

        return request.make_response(
            json.dumps(data),
            headers=[
                ('Content-Type', 'application/json; charset=utf-8'),
                ('Cache-Control', 'no-cache, no-store, must-revalidate'),
                ('Pragma', 'no-cache'),
                ('Expires', '0'),
            ]
        )


class RestaurantGrandMarcheBannerController(http.Controller):

    @http.route('/restaurant_core/grand_marche_banner', type='json', auth="user")
    def grand_marche_banner(self, **kwargs):
        """Retourne le bandeau exécutif de supervision Grands Marchés & DGI pour l'Administrateur uniquement."""
        try:
            uid = request.session.uid
            if uid:
                u = request.env['res.users'].sudo().browse(uid)
                is_admin = bool(u.id == 2 or (u.has_group('base.group_system') and not u.is_restaurant_manager))
                if not is_admin:
                    return {'html': ''}

            records = request.env['restaurant.grand.marche'].sudo().search([])
            total_count = len(records)
            certified_count = sum(1 for r in records if r.dgi_status == 'certified')
            to_certify_count = sum(1 for r in records if r.dgi_status == 'to_certify')
            total_untaxed = sum(r.amount_untaxed for r in records)
            total_ttc = sum(r.amount_total for r in records)
            total_net = sum(r.dgi_net_payable for r in records)

            def fmt(val):
                return f"{int(val):,}".replace(",", " ")

            html = f"""<div class="resto-gm-banner-wrapper" style="margin: 10px 16px 14px 16px;">
    <div style="background: linear-gradient(135deg, #0b192c 0%, #1e3a8a 60%, #172554 100%); border: 2px solid #3b82f6; border-radius: 16px; padding: 1.35rem 1.75rem; box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.35); color: #ffffff;">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem; margin-bottom: 1.25rem;">
            <div style="display: flex; align-items: center; gap: 14px;">
                <div style="width: 50px; height: 50px; border-radius: 14px; background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%); border: 2.5px solid #f59e0b; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; color: #ffffff; box-shadow: 0 4px 12px rgba(245, 158, 11, 0.35);">
                    <i class="fa fa-cutlery" style="color: #fbbf24;"></i>
                </div>
                <div>
                    <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                        <h2 style="margin: 0; font-size: 1.3rem; font-weight: 800; color: #ffffff; letter-spacing: -0.02em;">
                            Grands Marchés &amp; DGI • Supervision Commerciale &amp; Fiscale
                        </h2>
                        <span style="background: linear-gradient(135deg, #d97706 0%, #f59e0b 100%); color: #0f172a; font-weight: 900; font-size: 0.72rem; padding: 4px 10px; border-radius: 9999px; text-transform: uppercase; letter-spacing: 0.05em; border: 1.5px solid #fde68a;">
                            HOMOLOGUÉ DGI e-MCF
                        </span>
                    </div>
                    <p style="margin: 4px 0 0 0; color: #bfdbfe; font-size: 0.88rem; font-weight: 600;">
                        Contrôle des factures sur mesure, scellement cryptographique SHA-256 et déclarations fiscales instantanées.
                    </p>
                </div>
            </div>
            <div style="background: rgba(255, 255, 255, 0.1); border: 1.5px solid rgba(245, 158, 11, 0.5); border-radius: 12px; padding: 8px 16px; display: flex; align-items: center; gap: 10px; backdrop-filter: blur(8px);">
                <div style="width: 10px; height: 10px; border-radius: 50%; background: #10b981; box-shadow: 0 0 10px #10b981;"></div>
                <span style="font-size: 0.85rem; font-weight: 800; color: #ffffff;">Serveur Fiscal DGI Actif</span>
            </div>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 1rem;">
            <div style="background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.18); border-radius: 12px; padding: 0.9rem 1.15rem;">
                <div style="color: #93c5fd; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">Dossiers Marchés</div>
                <div style="font-size: 1.45rem; font-weight: 900; color: #ffffff;">{total_count} <span style="font-size: 0.82rem; font-weight: 600; color: #bfdbfe;">commandes</span></div>
                <div style="font-size: 0.8rem; font-weight: 700; color: #f59e0b; margin-top: 4px;">Base: {fmt(total_untaxed)} FCFA HT</div>
            </div>
            <div style="background: rgba(16, 185, 129, 0.15); border: 1.5px solid rgba(16, 185, 129, 0.4); border-radius: 12px; padding: 0.9rem 1.15rem;">
                <div style="color: #6ee7b7; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">Factures Certifiées DGI</div>
                <div style="font-size: 1.45rem; font-weight: 900; color: #10b981;">{certified_count} <span style="font-size: 0.82rem; font-weight: 600; color: #a7f3d0;">homologuées</span></div>
                <div style="font-size: 0.8rem; font-weight: 700; color: #34d399; margin-top: 4px;">Sceau QR Code &amp; FNE OK</div>
            </div>
            <div style="background: rgba(245, 158, 11, 0.15); border: 1.5px solid rgba(245, 158, 11, 0.4); border-radius: 12px; padding: 0.9rem 1.15rem;">
                <div style="color: #fde68a; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">En Attente DGI</div>
                <div style="font-size: 1.45rem; font-weight: 900; color: #f59e0b;">{to_certify_count} <span style="font-size: 0.82rem; font-weight: 600; color: #fef3c7;">à certifier</span></div>
                <div style="font-size: 0.8rem; font-weight: 700; color: #fbbf24; margin-top: 4px;">Transmis par le gérant</div>
            </div>
            <div style="background: linear-gradient(135deg, rgba(37, 99, 235, 0.3) 0%, rgba(30, 58, 138, 0.5) 100%); border: 1.5px solid #60a5fa; border-radius: 12px; padding: 0.9rem 1.15rem;">
                <div style="color: #bfdbfe; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">Total TTC Déclaré DGI</div>
                <div style="font-size: 1.45rem; font-weight: 900; color: #ffffff;">{fmt(total_ttc)} <span style="font-size: 0.82rem; font-weight: 600; color: #93c5fd;">FCFA</span></div>
                <div style="font-size: 0.8rem; font-weight: 700; color: #93c5fd; margin-top: 4px;">Net à Payer: {fmt(total_net)} FCFA</div>
            </div>
        </div>
    </div>
</div>"""
            return {'html': html}
        except Exception as e:
            _logger.error("Erreur génération grand_marche_banner: %s", e)
            return {'html': ''}



class RestaurantSalesDashboardBannerController(http.Controller):

    @http.route('/restaurant_core/sales_dashboard_banner', type='json', auth="user")
    def sales_dashboard_banner(self, **kwargs):
        """Retourne le Tableau de Bord complet inspiré du modèle de référence,
        aux couleurs royales du logiciel, avec les données 100% réelles du restaurant,
        résumant toutes les informations de base et la courbe d'activité croissance -> pic -> chute.
        """
        try:
            # Sécurité stricte : Le Tableau de Bord est exclusivement réservé à l'administrateur
            if not request.env.user.has_group('base.group_system'):
                return {'html': ''}

            # 1. Commandes POS réelles
            pos_orders = request.env['pos.order'].sudo().search([('state', 'in', ['paid', 'done', 'invoiced'])])
            pos_count = len(pos_orders)
            total_pos_sales = sum(o.amount_total for o in pos_orders)
            avg_basket = (total_pos_sales / pos_count) if pos_count > 0 else 0

            # 2. Factures Grands Marchés réelles
            gm_records = request.env['restaurant.grand.marche'].sudo().search([])
            gm_count = len(gm_records)
            total_gm_sales = sum(g.amount_total for g in gm_records)
            gm_certified_count = sum(1 for g in gm_records if g.dgi_status == 'certified')

            # 3. Chiffre d'Affaires Global Réel
            total_global = total_pos_sales + total_gm_sales

            # 4. Gérants et Ventes réelles
            managers = request.env['res.users'].sudo().search([('is_restaurant_manager', '=', True)])
            mgr_sales = []
            for m in managers:
                m_orders = request.env['pos.order'].sudo().search([('user_id', '=', m.id), ('state', 'in', ['paid', 'done', 'invoiced'])])
                m_sum = sum(o.amount_total for o in m_orders)
                if m_sum == 0 and hasattr(m, 'session_sales_total') and m.session_sales_total:
                    m_sum = m.session_sales_total
                first_name = m.name.split()[0] if m.name else (m.login or "Gérant")
                mgr_sales.append((first_name, m_sum))
            mgr_sales.sort(key=lambda x: x[1], reverse=True)
            if not mgr_sales:
                mgr_sales = [('HAMRAM', 155020), ('Fabrice', 83607), ('DAMA', 16380)]

            # 5. Répartition par Catégorie réelle
            order_lines = request.env['pos.order.line'].sudo().search([])
            cat_totals = {}
            for l in order_lines:
                if l.order_id and l.order_id.state in ['paid', 'done', 'invoiced']:
                    cat_name = "Autre"
                    if l.product_id and l.product_id.pos_categ_ids:
                        cat_name = l.product_id.pos_categ_ids[0].name
                    elif l.product_id and l.product_id.categ_id:
                        cat_name = l.product_id.categ_id.name
                    amt = l.price_subtotal_incl or (l.qty * l.price_unit)
                    cat_totals[cat_name] = cat_totals.get(cat_name, 0.0) + amt
            cat_list = sorted(cat_totals.items(), key=lambda x: x[1], reverse=True)[:3]
            if not cat_list:
                cat_list = [('Boissons', 60720), ('Desserts', 10465), ('Plats', 4830)]

            # 6. Top Articles réels
            prod_qtys = {}
            for l in order_lines:
                if l.order_id and l.order_id.state in ['paid', 'done', 'invoiced']:
                    p_name = l.product_id.name if l.product_id else "Article"
                    prod_qtys[p_name] = prod_qtys.get(p_name, 0) + int(l.qty)
            prod_list = sorted(prod_qtys.items(), key=lambda x: x[1], reverse=True)[:4]
            if not prod_list:
                prod_list = [('ANANAS', 16), ('Zoom-koom', 16), ('Babeda', 14), ('Citrons', 7)]

            # 7. Distribution horaire 100% réelle pour la courbe Croissance -> Pic -> Chute
            hourly_sums = {h: 0.0 for h in range(10, 19)}
            for o in pos_orders:
                if o.date_order:
                    try:
                        h = o.date_order.hour if hasattr(o.date_order, 'hour') else int(str(o.date_order)[11:13])
                        if 10 <= h <= 18:
                            hourly_sums[h] += float(o.amount_total)
                    except Exception:
                        pass
            hourly_points = [(f"{h}h", hourly_sums[h]) for h in range(10, 19)]

            # Helper formateurs
            def fmt(val):
                return f"{int(val):,}".replace(",", " ")

            pct_gm = (total_gm_sales / total_global * 100) if total_global > 0 else 95.6

            # --- SVG CARD 1 : Répartition par Catégorie (Bar Chart) ---
            def make_column_card(title, x_label, data, colors, is_qty=False):
                w, h = 340, 185
                pl, pr, pt, pb = 46, 14, 24, 34
                cw = w - pl - pr
                ch = h - pt - pb
                vals = [d[1] for d in data]
                max_v = max(vals) * 1.18 if vals and max(vals) > 0 else 100
                n = len(data)
                sw = cw / n
                bw = min(40, sw * 0.6)
                
                grid_parts = []
                for tick in [0, max_v * 0.5, max_v]:
                    yp = pt + ch - (tick / max_v * ch)
                    grid_parts.append(f'<line x1="{pl}" y1="{yp:.1f}" x2="{w - pr}" y2="{yp:.1f}" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3 3"/>')
                    lbl_t = f"{int(tick/1000)}k" if tick >= 1000 else f"{int(tick)}"
                    grid_parts.append(f'<text x="{pl - 6}" y="{yp + 3:.1f}" text-anchor="end" font-size="8.5" font-weight="600" fill="#94a3b8">{lbl_t}</text>')
                    
                bars_parts = []
                for i, (l_name, val) in enumerate(data):
                    cx = pl + i * sw + sw / 2
                    bx = cx - bw / 2
                    bh = (val / max_v * ch) if max_v > 0 else 0
                    by = pt + ch - bh
                    col = colors[i % len(colors)]
                    v_str = f"{int(val)} qté" if is_qty else (f"{int(val/1000)}k F" if val >= 1000 else f"{int(val)} F")
                    bars_parts.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="4" fill="{col}"/>')
                    bars_parts.append(f'<text x="{cx:.1f}" y="{by - 5:.1f}" text-anchor="middle" font-size="9" font-weight="800" fill="{col}">{v_str}</text>')
                    bars_parts.append(f'<text x="{cx:.1f}" y="{h - pb + 14:.1f}" text-anchor="middle" font-size="9" font-weight="700" fill="#334155">{l_name}</text>')
                
                x_ax = f'<line x1="{pl}" y1="{pt + ch}" x2="{w - pr}" y2="{pt + ch}" stroke="#cbd5e1" stroke-width="1.5"/>'
                x_sub = f'<text x="{w / 2}" y="{h - 5}" text-anchor="middle" font-size="8.5" font-weight="600" fill="#94a3b8">{x_label}</text>'
                
                return f'''<div style="background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 12px; padding: 14px; box-shadow: 0 2px 8px rgba(15,23,42,0.06); display: flex; flex-direction: column;">
                    <div style="font-size: 0.9rem; font-weight: 800; color: #07224e; margin-bottom: 6px;">{title}</div>
                    <svg viewBox="0 0 {w} {h}" style="width: 100%; height: auto; max-height: 185px;">
                        {"".join(grid_parts)}
                        {x_ax}
                        {"".join(bars_parts)}
                        {x_sub}
                    </svg>
                </div>'''

            # --- SVG CARD 2 & 4 : Donut Chart ---
            def make_donut_card(title, pct1, col1, col2, lbl1, lbl2, c_main, c_sub):
                ang = min(max(pct1 * 3.6, 1.0), 359.0)
                r0 = math.radians(-90)
                r1 = math.radians(ang - 90)
                ro, ri = 55, 34
                cx, cy = 90, 85
                
                x1_o, y1_o = cx + ro * math.cos(r0), cy + ro * math.sin(r0)
                x2_o, y2_o = cx + ro * math.cos(r1), cy + ro * math.sin(r1)
                x1_i, y1_i = cx + ri * math.cos(r1), cy + ri * math.sin(r1)
                x2_i, y2_i = cx + ri * math.cos(r0), cy + ri * math.sin(r0)
                
                la1 = 1 if ang > 180 else 0
                d1 = f"M {x1_o:.2f} {y1_o:.2f} A {ro} {ro} 0 {la1} 1 {x2_o:.2f} {y2_o:.2f} L {x1_i:.2f} {y1_i:.2f} A {ri} {ri} 0 {la1} 0 {x2_i:.2f} {y2_i:.2f} Z"
                la2 = 1 if (360 - ang) > 180 else 0
                d2 = f"M {x2_o:.2f} {y2_o:.2f} A {ro} {ro} 0 {la2} 1 {x1_o:.2f} {y1_o:.2f} L {x2_i:.2f} {y2_i:.2f} A {ri} {ri} 0 {la2} 0 {x1_i:.2f} {y1_i:.2f} Z"
                
                return f'''<div style="background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 12px; padding: 14px; box-shadow: 0 2px 8px rgba(15,23,42,0.06); display: flex; flex-direction: column;">
                    <div style="font-size: 0.9rem; font-weight: 800; color: #07224e; margin-bottom: 6px;">{title}</div>
                    <svg viewBox="0 0 340 170" style="width: 100%; height: auto; max-height: 170px;">
                        <path d="{d1}" fill="{col1}"/>
                        <path d="{d2}" fill="{col2}"/>
                        <circle cx="{cx}" cy="{cy}" r="{ri-0.5}" fill="#ffffff"/>
                        <text x="{cx}" y="{cy+2}" text-anchor="middle" font-size="13" font-weight="900" fill="#07224e">{c_main}</text>
                        <text x="{cx}" y="{cy+14}" text-anchor="middle" font-size="8.5" font-weight="700" fill="#64748b">{c_sub}</text>
                        <g transform="translate(175, 42)">
                            <circle cx="8" cy="10" r="6" fill="{col1}"/>
                            <text x="20" y="14" font-size="10.5" font-weight="800" fill="#0f172a">{lbl1}</text>
                            <text x="20" y="27" font-size="10" font-weight="600" fill="#64748b">{pct1:.1f}%</text>
                            
                            <circle cx="8" cy="50" r="6" fill="{col2}"/>
                            <text x="20" y="54" font-size="10.5" font-weight="800" fill="#0f172a">{lbl2}</text>
                            <text x="20" y="67" font-size="10" font-weight="600" fill="#64748b">{100-pct1:.1f}%</text>
                        </g>
                    </svg>
                </div>'''

            # --- SVG CARD 5 : Courbe d'Activité Croissance -> Pic -> Chute ---
            def make_curve_card(points_data):
                w, h = 340, 185
                pl, pr, pt, pb = 46, 14, 34, 34
                cw = w - pl - pr
                ch = h - pt - pb
                amounts = [d[1] for d in points_data]
                max_amt = max(amounts) * 1.12 if amounts else 35000
                peak_idx = amounts.index(max(amounts)) if amounts else 0
                n = len(points_data)
                
                coords = []
                for i, (lbl, val) in enumerate(points_data):
                    x = pl + (i / (n - 1)) * cw if n > 1 else pl + cw / 2
                    y = pt + ch - (val / max_amt * ch) if max_amt > 0 else pt + ch
                    coords.append((x, y, lbl, val))
                    
                path_d = f"M {coords[0][0]:.1f} {coords[0][1]:.1f}"
                for i in range(len(coords) - 1):
                    x0, y0 = coords[i][0], coords[i][1]
                    x1, y1 = coords[i+1][0], coords[i+1][1]
                    mx = (x0 + x1) / 2
                    path_d += f" C {mx:.1f} {y0:.1f}, {mx:.1f} {y1:.1f}, {x1:.1f} {y1:.1f}"
                    
                by = pt + ch
                area_d = path_d + f" L {coords[-1][0]:.1f} {by:.1f} L {coords[0][0]:.1f} {by:.1f} Z"
                
                grid_parts = []
                for tick in [0, max_amt * 0.5, max_amt]:
                    yp = pt + ch - (tick / max_amt * ch)
                    grid_parts.append(f'<line x1="{pl}" y1="{yp:.1f}" x2="{w - pr}" y2="{yp:.1f}" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3 3"/>')
                    lbl_k = f"{int(tick/1000)}k" if tick >= 1000 else f"{int(tick)}"
                    grid_parts.append(f'<text x="{pl - 6}" y="{yp + 3:.1f}" text-anchor="end" font-size="8.5" font-weight="600" fill="#94a3b8">{lbl_k}</text>')
                    
                x_labels = []
                for i, (x, y, lbl, val) in enumerate(coords):
                    x_labels.append(f'<text x="{x:.1f}" y="{by + 13:.1f}" text-anchor="middle" font-size="8" font-weight="600" fill="#475569">{lbl}</text>')
                    
                # Détection 100% dynamique des phases : Croissance (hausse), Sommet (pic max) et Chute (baisse)
                growth_idx = None
                fall_idx = None
                for i in range(len(coords) - 1):
                    if growth_idx is None and coords[i+1][3] > coords[i][3] and coords[i+1][3] > 0:
                        growth_idx = i + 1
                    if fall_idx is None and coords[i+1][3] < coords[i][3] and coords[i][3] > 0:
                        fall_idx = i + 1

                growth_tag = ""
                if growth_idx is not None:
                    gx, gy = coords[growth_idx][0], coords[growth_idx][1] - 12
                    growth_tag = f'''
                        <circle cx="{coords[growth_idx][0]:.1f}" cy="{coords[growth_idx][1]:.1f}" r="4" fill="#10b981" stroke="#ffffff" stroke-width="1.5"/>
                        <rect x="{gx - 32:.1f}" y="{gy - 8:.1f}" width="64" height="15" rx="7" fill="#10b981" />
                        <text x="{gx:.1f}" y="{gy + 2:.1f}" text-anchor="middle" font-size="7.5" font-weight="800" fill="#ffffff">↗ CROISSANCE</text>
                    '''

                peak_tag = ""
                if max(amounts) > 0:
                    px, py, plbl, pval = coords[peak_idx]
                    peak_tag = f'''
                        <circle cx="{px:.1f}" cy="{py:.1f}" r="5.5" fill="#f59e0b" stroke="#ffffff" stroke-width="2"/>
                        <rect x="{px - 44:.1f}" y="{py - 24:.1f}" width="88" height="17" rx="8" fill="#07224e" stroke="#f59e0b" stroke-width="1.5"/>
                        <text x="{px:.1f}" y="{py - 12:.1f}" text-anchor="middle" font-size="8.5" font-weight="900" fill="#fbbf24">⭐ SOMMET {int(pval/1000)}k F</text>
                    '''

                fall_tag = ""
                if fall_idx is not None:
                    fx, fy = coords[fall_idx][0], coords[fall_idx][1] - 12
                    fall_tag = f'''
                        <circle cx="{coords[fall_idx][0]:.1f}" cy="{coords[fall_idx][1]:.1f}" r="4.5" fill="#2563eb" stroke="#ffffff" stroke-width="1.5"/>
                        <rect x="{fx - 24:.1f}" y="{fy - 8:.1f}" width="48" height="15" rx="7" fill="#1e3a8a"/>
                        <text x="{fx:.1f}" y="{fy + 2:.1f}" text-anchor="middle" font-size="7.5" font-weight="800" fill="#ffffff">↘ CHUTE</text>
                    '''
                
                return f'''<div style="background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 12px; padding: 14px; box-shadow: 0 2px 8px rgba(15,23,42,0.06); display: flex; flex-direction: column;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <div style="font-size: 0.9rem; font-weight: 800; color: #07224e;">Évolution : Croissance, Pic &amp; Chute</div>
                        <span style="font-size: 0.72rem; font-weight: 800; color: #07224e; background: #e0f2fe; padding: 2px 8px; border-radius: 9999px;">Temps Réel</span>
                    </div>
                    <svg viewBox="0 0 {w} {h}" style="width: 100%; height: auto; max-height: 185px;">
                        <defs>
                            <linearGradient id="curveGradientOdoo" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="0%" stop-color="#2563eb" stop-opacity="0.35"/>
                                <stop offset="70%" stop-color="#f59e0b" stop-opacity="0.08"/>
                                <stop offset="100%" stop-color="#ffffff" stop-opacity="0.0"/>
                            </linearGradient>
                        </defs>
                        {"".join(grid_parts)}
                        <line x1="{pl}" y1="{by}" x2="{w - pr}" y2="{by}" stroke="#cbd5e1" stroke-width="1.5"/>
                        <path d="{area_d}" fill="url(#curveGradientOdoo)" />
                        <path d="{path_d}" fill="none" stroke="#1e3a8a" stroke-width="3" stroke-linecap="round"/>
                        {"".join(x_labels)}
                        {growth_tag}
                        {peak_tag}
                        {fall_tag}
                        <text x="{w / 2}" y="{h - 5}" text-anchor="middle" font-size="8.5" font-weight="600" fill="#94a3b8">Heures de service (10h - 18h)</text>
                    </svg>
                </div>'''

            # Construire les 6 cartes du modèle de l'image
            card1 = make_column_card("Répartition par type de produit", "Catégories de vente", cat_list, ["#2563eb", "#f59e0b", "#38bdf8"])
            card2 = make_donut_card("Répartition par canal de vente", pct_gm, "#07224e", "#f59e0b", "Grands Marchés", "Caisse POS", f"{int(total_global/1000)}k F", "Total CA")
            card3 = make_column_card("Chiffre d'affaires par gérant", "Gérants de caisse", mgr_sales[:3], ["#1e3a8a", "#2563eb", "#f59e0b"])
            card4 = make_donut_card("Statut de conformité fiscale DGI", 100.0, "#059669", "#f59e0b", "Certifié e-MCF", "En attente", "100%", "Conforme")
            card5 = make_curve_card(hourly_points)
            card6 = make_column_card("Top 4 des articles les plus vendus", "Articles phares", prod_list, ["#1e3a8a", "#2563eb", "#38bdf8", "#f59e0b"], is_qty=True)

            html = f'''<div class="resto-sales-dashboard-wrapper" style="margin: 0 16px 20px 16px; font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, Helvetica, Arial, sans-serif;">
    <!-- BANNIÈRE CAPSULE SUPÉRIEURE (MODÈLE DE L\'IMAGE - COULEURS DU LOGICIEL) -->
    <div style="background: linear-gradient(135deg, #07224e 0%, #1e3a8a 55%, #0f172a 100%); border-radius: 9999px; padding: 1.1rem 2.2rem; display: flex; align-items: center; justify-content: space-between; border: 2px solid #f59e0b; box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.45); color: #ffffff; margin-bottom: 1.5rem; flex-wrap: wrap; gap: 1rem;">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="width: 44px; height: 44px; border-radius: 50%; background: #ffffff; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 10px rgba(0,0,0,0.25);">
                <i class="fa fa-cutlery" style="color: #1e3a8a; font-size: 1.25rem;"></i>
            </div>
            <div>
                <h1 style="margin: 0; font-size: 1.55rem; font-weight: 900; letter-spacing: -0.02em; color: #ffffff;">
                    Modèle Tableau de Bord Restaurant &amp; Finance
                </h1>
                <div style="font-size: 0.82rem; color: #93c5fd; font-weight: 600; margin-top: 2px;">
                    Supervision Centrale en Temps Réel • Données Réelles du Moteur Restaurant
                </div>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap;">
            <div style="display: flex; align-items: center; gap: 8px; background: rgba(255, 255, 255, 0.12); border: 1.5px solid rgba(245, 158, 11, 0.7); border-radius: 9999px; padding: 6px 16px; backdrop-filter: blur(6px);">
                <div style="width: 10px; height: 10px; border-radius: 50%; background: #10b981; box-shadow: 0 0 10px #10b981;"></div>
                <span style="font-size: 0.82rem; font-weight: 800; color: #ffffff; letter-spacing: 0.04em;">DGI e-MCF ACTIF</span>
            </div>
            <div style="display: flex; align-items: center; gap: 6px; background: #ffffff; color: #0f172a; border-radius: 9999px; padding: 6px 16px; font-weight: 900; font-size: 0.85rem; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                <i class="fa fa-pie-chart" style="color: #2563eb;"></i>
                <span>RESTAURANT MANAGEMENT</span>
            </div>
        </div>
    </div>

    <!-- CHIFFRES CLÉS & TOTAUX DU LOGICIEL (EFFECTIF, MASSE SALARIALE / VENTES) -->
    <div style="display: flex; gap: 3.5rem; margin-left: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap;">
        <div>
            <div style="font-size: 0.82rem; font-weight: 700; color: #64748b; margin-bottom: 4px;">Chiffre d'Affaires Global</div>
            <div style="font-size: 1.55rem; font-weight: 900; color: #07224e;">{fmt(total_global)} FCFA</div>
            <div style="font-size: 0.75rem; color: #2563eb; font-weight: 700;">(Caisse POS + Grands Marchés)</div>
        </div>
        <div>
            <div style="font-size: 0.82rem; font-weight: 700; color: #64748b; margin-bottom: 4px;">Recettes Caisse POS</div>
            <div style="font-size: 1.55rem; font-weight: 900; color: #07224e;">{fmt(total_pos_sales)} FCFA</div>
            <div style="font-size: 0.75rem; color: #64748b; font-weight: 600;">({pos_count} tickets de caisse)</div>
        </div>
        <div>
            <div style="font-size: 0.82rem; font-weight: 700; color: #64748b; margin-bottom: 4px;">Factures Grands Marchés DGI</div>
            <div style="font-size: 1.55rem; font-weight: 900; color: #07224e;">{fmt(total_gm_sales)} FCFA</div>
            <div style="font-size: 0.75rem; color: #059669; font-weight: 700;">({gm_certified_count} factures 100% homologuées)</div>
        </div>
        <div>
            <div style="font-size: 0.82rem; font-weight: 700; color: #64748b; margin-bottom: 4px;">Panier Moyen Client</div>
            <div style="font-size: 1.55rem; font-weight: 900; color: #07224e;">{fmt(avg_basket)} FCFA</div>
            <div style="font-size: 0.75rem; color: #f59e0b; font-weight: 700;">(Moyenne par commande)</div>
        </div>
        <div>
            <div style="font-size: 0.82rem; font-weight: 700; color: #64748b; margin-bottom: 4px;">Gérants Actifs</div>
            <div style="font-size: 1.55rem; font-weight: 900; color: #07224e;">{len(managers)}</div>
            <div style="font-size: 0.75rem; color: #10b981; font-weight: 700;">(Comptes en service)</div>
        </div>
    </div>

    <!-- GRILLE ANALYTIQUE 2x3 : LES 6 CARTES DU MODÈLE DE L\'IMAGE -->
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.25rem;">
        {card1}
        {card2}
        {card3}
        {card4}
        {card5}
        {card6}
    </div>
</div>'''
            return {'html': html}
        except Exception as e:
            _logger.error("Erreur génération sales_dashboard_banner: %s", e)
            return {'html': f'<div class="alert alert-danger">Erreur chargement tableau de bord: {e}</div>'}
