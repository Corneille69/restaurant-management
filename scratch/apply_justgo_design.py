import re

# =========================================================================
# 1. Update backend/app/web/router.py
# =========================================================================
router_path = 'backend/app/web/router.py'
with open(router_path, 'r', encoding='utf-8') as f:
    router_code = f.read()

# Replace CSS in router.py
old_css_start = "/* ========================================================================="
# find login screen comment
start_idx = router_code.find("/* =========================================================================\n           LOGIN SCREEN :")
if start_idx == -1:
    start_idx = router_code.find("body.auth-mode {")

end_marker = "/* Admin Shell : Layout avec Sidebar Verticale à Gauche */"
end_idx = router_code.find(end_marker)

new_router_css = """/* =========================================================================
           LOGIN SCREEN : MODÈLE PREMIUM BLEU MARINE SOMBRE & JAUNE OR AMBRÉ
           Inspiré fidèlement du modèle de référence (Bon retour !)
           ========================================================================= */
        body.auth-mode {
            background-color: #0c1424;
            color: #ffffff;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            overflow-x: hidden;
            padding: 2rem 1rem;
        }
        body.auth-mode header {
            display: none !important;
        }
        body.auth-mode .container {
            max-width: 440px;
            margin: auto;
            padding: 0;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .justgo-login-container {
            width: 100%;
            max-width: 420px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        /* 1. Carte Logo au Sommet */
        .justgo-logo-card {
            width: 110px;
            height: 110px;
            background: #17243a;
            border: 1.5px solid #23354e;
            border-radius: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1.6rem;
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.45);
            padding: 12px;
            transition: transform 0.2s ease;
        }
        .justgo-logo-card:hover {
            transform: scale(1.03);
        }
        .justgo-logo-card img {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
            border-radius: 12px;
        }
        .justgo-logo-placeholder {
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.8rem;
        }

        /* 2. Titre & Sous-titre */
        .justgo-title {
            color: #e58b00;
            font-size: 1.85rem;
            font-weight: 800;
            text-align: center;
            margin-bottom: 0.4rem;
            letter-spacing: -0.01em;
        }
        .justgo-subtitle {
            color: #94a3b8;
            font-size: 0.88rem;
            text-align: center;
            margin-bottom: 2rem;
            line-height: 1.4;
        }

        /* 3. Formulaire */
        .justgo-form {
            width: 100%;
            display: flex;
            flex-direction: column;
        }

        /* Groupes d'inputs pillules sombres */
        .justgo-pill-group {
            width: 100%;
            background: #1b293e;
            border: 1.5px solid #273852;
            border-radius: 50px;
            padding: 0.85rem 1.4rem;
            display: flex;
            align-items: center;
            gap: 0.85rem;
            margin-bottom: 1.15rem;
            transition: all 0.25s ease;
        }
        .justgo-pill-group:focus-within {
            border-color: #e58b00;
            box-shadow: 0 0 18px rgba(229, 139, 0, 0.35);
            background: #203149;
        }
        .justgo-pill-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            color: #e58b00;
            font-size: 1.15rem;
            flex-shrink: 0;
        }
        .justgo-pill-input {
            flex: 1;
            background: transparent;
            border: none;
            outline: none;
            color: #ffffff;
            font-size: 0.98rem;
            font-weight: 500;
        }
        .justgo-pill-input::placeholder {
            color: #64748b;
            font-weight: 400;
        }
        .justgo-eye-btn {
            background: none;
            border: none;
            color: #64748b;
            font-size: 1.05rem;
            cursor: pointer;
            padding: 0 0.2rem;
            display: flex;
            align-items: center;
            transition: color 0.2s;
        }
        .justgo-eye-btn:hover {
            color: #e58b00;
        }

        /* Alerte Erreur */
        .justgo-error-banner {
            background: rgba(185, 28, 28, 0.25);
            border: 1px solid #dc2626;
            border-radius: 50px;
            color: #fca5a5;
            font-size: 0.84rem;
            font-weight: 600;
            padding: 0.6rem 1.25rem;
            text-align: center;
            margin-bottom: 1.15rem;
        }

        /* 4. Bouton Se Connecter */
        .btn-justgo-gold {
            width: 100%;
            background: #e58b00;
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            border: none;
            border-radius: 50px;
            color: #0c1424;
            font-size: 1.08rem;
            font-weight: 800;
            padding: 0.95rem;
            cursor: pointer;
            box-shadow: 0 8px 24px rgba(229, 139, 0, 0.4);
            transition: all 0.25s ease;
            text-align: center;
            margin-top: 0.4rem;
            margin-bottom: 1.25rem;
        }
        .btn-justgo-gold:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 28px rgba(229, 139, 0, 0.6);
            background: linear-gradient(135deg, #fbbf24 0%, #e58b00 100%);
        }
        .btn-justgo-gold:active {
            transform: translateY(1px);
        }

        /* 5. Se Souvenir de Moi */
        .justgo-remember-wrap {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.55rem;
            color: #94a3b8;
            font-size: 0.88rem;
            cursor: pointer;
            user-select: none;
            margin-bottom: 1.75rem;
        }
        .justgo-checkbox {
            width: 18px;
            height: 18px;
            border-radius: 6px;
            border: 1.5px solid #475569;
            background: #1b293e;
            accent-color: #e58b00;
            cursor: pointer;
        }

        /* 6. Liens Inférieurs */
        .justgo-footer-links {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.85rem;
            text-align: center;
            width: 100%;
        }
        .justgo-gold-link {
            color: #e58b00;
            font-size: 0.84rem;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.2s;
            cursor: pointer;
        }
        .justgo-gold-link:hover {
            color: #fbbf24;
            text-decoration: underline;
        }
        .justgo-signup-text {
            color: #94a3b8;
            font-size: 0.86rem;
        }
        .justgo-signup-text a {
            color: #e58b00;
            font-weight: 700;
            text-decoration: underline;
            margin-left: 0.25rem;
            cursor: pointer;
        }
        .justgo-signup-text a:hover {
            color: #fbbf24;
        }

        /* Rôles rapides Admin / Gérant */
        .justgo-role-chips {
            display: flex;
            justify-content: center;
            gap: 0.75rem;
            margin-top: 1.25rem;
        }
        .justgo-chip {
            background: #17243a;
            border: 1px solid #2a3d58;
            border-radius: 50px;
            padding: 0.35rem 0.95rem;
            color: #e58b00;
            font-size: 0.78rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
        }
        .justgo-chip:hover {
            background: #203149;
            border-color: #e58b00;
            color: #ffffff;
        }
        
        """

if start_idx != -1 and end_idx != -1:
    router_code = router_code[:start_idx] + new_router_css + router_code[end_idx:]
    print("Replaced CSS in router.py!")
else:
    print("Could not find CSS markers in router.py:", start_idx, end_idx)

# Replace HTML for authScreen in router.py
html_start_marker = "<!-- 1. LOGIN SCREEN"
html_start_idx = router_code.find(html_start_marker)
html_end_marker = "<!-- 2. ADMIN PORTAL (GESTION DU RESTAURANT & NAVIGATION VERTICALE À GAUCHE) -->"
html_end_idx = router_code.find(html_end_marker)

new_router_html = """<!-- 1. LOGIN SCREEN (MODÈLE FIDÈLE BLEU MARINE & JAUNE OR - BON RETOUR !) -->
        <div id="authScreen" class="justgo-login-container">
            <!-- 1. Logo du Restaurant dans la carte arrondie foncée -->
            <div class="justgo-logo-card">
                <img id="authBrandLogoImg" src="/restaurant/api/brand/logo" alt="Logo" onerror="this.onerror=null; this.src='https://cdn-icons-png.flaticon.com/512/857/857681.png';" />
            </div>

            <!-- 2. Titre & Sous-titre -->
            <h1 class="justgo-title">Bon retour !</h1>
            <p class="justgo-subtitle">Heureux de vous retrouver, veuillez vous connecter.</p>

            <!-- 3. Formulaire de connexion -->
            <form class="justgo-form" onsubmit="handleLogin(event)">
                <!-- Champ 1 : Identifiant / Téléphone -->
                <div class="justgo-pill-group">
                    <span class="justgo-pill-icon" title="Identifiant / Téléphone">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/>
                        </svg>
                    </span>
                    <input id="loginUsername" type="text" class="justgo-pill-input" placeholder="Téléphone ou Identifiant" value="admin" required autocomplete="username" />
                </div>

                <!-- Champ 2 : Mot de passe avec Cadenas Or et Oeil -->
                <div class="justgo-pill-group">
                    <span class="justgo-pill-icon" title="Mot de passe">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/>
                        </svg>
                    </span>
                    <input id="loginPassword" type="password" class="justgo-pill-input" placeholder="Mot de passe" value="admin123" required autocomplete="current-password" />
                    <button type="button" class="justgo-eye-btn" onclick="toggleAuthPasswordVisibility()" title="Afficher/Masquer le mot de passe">
                        <svg id="eyeToggleSvg" width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                            <circle cx="12" cy="12" r="3"></circle>
                        </svg>
                    </button>
                </div>

                <!-- Alerte Erreur -->
                <div id="loginError" class="justgo-error-banner" style="display: none;">
                    Identifiants incorrects
                </div>

                <!-- Bouton Se connecter en Or Ambré -->
                <button type="submit" class="btn-justgo-gold">
                    Se connecter
                </button>

                <!-- Se souvenir de moi -->
                <label class="justgo-remember-wrap">
                    <input type="checkbox" id="rememberMeCheck" class="justgo-checkbox" checked />
                    <span>Se souvenir de moi</span>
                </label>

                <!-- Liens Inférieurs -->
                <div class="justgo-footer-links">
                    <a href="javascript:void(0)" onclick="alert('Code de réinitialisation : veuillez contacter votre administrateur.')" class="justgo-gold-link">
                        Code SMS non reçu ou inscription incomplète ?
                    </a>

                    <div class="justgo-signup-text">
                        Vous n'avez pas de compte? <a href="javascript:void(0)" onclick="alert('Veuillez contacter le gérant pour activer votre compte.')">S'inscrire</a>
                    </div>

                    <a href="javascript:void(0)" onclick="alert('Conditions générales du service restaurant applicables.')" class="justgo-gold-link" style="text-decoration: underline;">
                        Conditions générales
                    </a>
                </div>

                <!-- Raccourcis de connexion rapide -->
                <div class="justgo-role-chips">
                    <button type="button" class="justgo-chip" onclick="fillAdminCreds()" title="Connexion Administrateur">👑 Admin</button>
                    <button type="button" class="justgo-chip" onclick="fillManagerCreds()" title="Connexion Gérant">🧑‍💼 Gérant</button>
                </div>
            </form>
        </div>

        """

if html_start_idx != -1 and html_end_idx != -1:
    router_code = router_code[:html_start_idx] + new_router_html + router_code[html_end_idx:]
    print("Replaced HTML in router.py!")
else:
    print("Could not find HTML markers in router.py:", html_start_idx, html_end_idx)

with open(router_path, 'w', encoding='utf-8') as f:
    f.write(router_code)

print("backend/app/web/router.py updated successfully!")
