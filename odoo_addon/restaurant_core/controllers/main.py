# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.home import Home
import logging

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
                    pos_config = request.env['pos.config'].sudo().search([('active', '=', True)], limit=1)
                    if pos_config:
                        # Si aucune session n'est ouverte, ouvrir la caisse automatiquement pour le gérant
                        if not pos_config.current_session_id or pos_config.current_session_state not in ('opened', 'opening_control'):
                            try:
                                pos_config.with_user(uid).open_ui()
                            except Exception as session_err:
                                _logger.warning("Erreur ouverture auto session POS: %s", session_err)

                    # Rediriger vers l'accueil cinématographique chaleureux avec nom du restaurant
                    return "/restaurant/welcome"
            except Exception as e:
                _logger.warning("Erreur redirection gérant login: %s", e)
        return super()._login_redirect(uid, redirect=redirect)

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


class RestaurantBrandController(http.Controller):

    @http.route('/restaurant/api/brand', type='http', auth='none', cors='*', methods=['GET'], csrf=False)
    def get_restaurant_brand(self):
        """Retourne en temps réel les informations configurées du restaurant (Nom, Logo, Slogan)."""
        import json
        try:
            config = request.env['restaurant.configuration'].sudo().search([], limit=1)
            company = request.env['res.company'].sudo().browse(1)
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
