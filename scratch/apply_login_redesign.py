import re

# 1. Update backend/app/web/router.py
router_path = 'backend/app/web/router.py'
with open(router_path, 'r', encoding='utf-8') as f:
    router_code = f.read()

# CSS replacement in router.py
old_css_start = "/* Odoo Auth Screen Styling (Inspiré de l'image de référence) */"
old_css_end = ".odoo-footer-links span { font-weight: 600; }"

new_css = """/* =========================================================================
           LOGIN SCREEN : MODÈLE ORGANIQUE BLOB - BLEU MARINE & JAUNE OR
           ========================================================================= */
        body.auth-mode {
            background: #081326;
            background-image: 
                radial-gradient(circle at 18% 22%, rgba(245, 158, 11, 0.28) 0%, transparent 40%),
                radial-gradient(circle at 82% 78%, rgba(30, 58, 138, 0.5) 0%, transparent 45%),
                linear-gradient(135deg, #050d1a 0%, #0b192c 45%, #10243e 100%);
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            overflow-x: hidden;
            position: relative;
        }
        body.auth-mode header {
            display: none !important;
        }
        body.auth-mode .container {
            max-width: 480px;
            margin: auto;
            padding: 2rem 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .blob-login-container {
            position: relative;
            width: 440px;
            max-width: 94vw;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        /* Halo diffus d'ambiance */
        .blob-layer-back {
            position: absolute;
            inset: -14px -14px -10px -10px;
            border-radius: 52% 48% 68% 32% / 44% 56% 44% 56%;
            background: linear-gradient(135deg, #1e3a8a 0%, #0f2744 35%, #d97706 75%, #f59e0b 100%);
            opacity: 0.85;
            filter: blur(14px);
            z-index: 1;
        }

        /* Bordure liquide multi-tons visible en arrière-plan */
        .blob-layer-rim {
            position: absolute;
            inset: -6px -10px -6px -4px;
            border-radius: 46% 54% 34% 66% / 54% 46% 54% 46%;
            background: linear-gradient(145deg, #2563eb 0%, #1e3a8a 30%, #b45309 70%, #f59e0b 100%);
            box-shadow: 0 20px 45px rgba(0, 0, 0, 0.6);
            z-index: 2;
        }

        /* Carte principale forme organique liquide */
        .blob-card {
            position: relative;
            z-index: 3;
            width: 100%;
            padding: 2.75rem 2.25rem 2.5rem;
            border-radius: 45% 55% 63% 37% / 44% 42% 58% 56%;
            background: linear-gradient(150deg, #1b3864 0%, #224c80 30%, #466088 55%, #b2822a 82%, #d98e14 100%);
            box-shadow: 
                inset 0 2px 4px rgba(255, 255, 255, 0.4),
                inset 0 -2px 6px rgba(0, 0, 0, 0.3),
                0 25px 60px rgba(4, 11, 23, 0.7);
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        /* Médaillon Avatar Rond */
        .avatar-badge-wrap {
            position: relative;
            margin-top: -0.5rem;
            margin-bottom: 1.1rem;
        }
        .avatar-badge {
            width: 82px;
            height: 82px;
            border-radius: 50%;
            background: #ffffff;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3), 0 2px 6px rgba(0, 0, 0, 0.15);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .avatar-icon-svg {
            width: 48px;
            height: 48px;
        }

        /* Titre Sign In */
        .sign-in-title {
            color: #ffffff;
            font-size: 1.85rem;
            font-weight: 800;
            letter-spacing: 0.5px;
            margin-bottom: 1.6rem;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.35);
        }

        .blob-login-form {
            width: 100%;
            display: flex;
            flex-direction: column;
            gap: 1.15rem;
        }

        /* Rangée d'input avec Badge Squircle à gauche + Input Pillule */
        .blob-input-row {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            width: 100%;
        }

        .blob-input-badge {
            width: 44px;
            height: 44px;
            border-radius: 14px 6px 14px 6px;
            background: linear-gradient(135deg, #f59e0b 0%, #1e3a8a 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #ffffff;
            flex-shrink: 0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
            border: 1px solid rgba(255, 255, 255, 0.25);
        }

        .blob-input-pill {
            flex: 1;
            position: relative;
            background: rgba(255, 255, 255, 0.15);
            border: 1.5px solid rgba(255, 255, 255, 0.65);
            border-radius: 50px;
            padding: 0.65rem 1.15rem;
            display: flex;
            align-items: center;
            backdrop-filter: blur(8px);
            transition: all 0.25s ease;
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
        }
        .blob-input-pill:focus-within {
            border-color: #ffd700;
            background: rgba(255, 255, 255, 0.25);
            box-shadow: 0 0 16px rgba(245, 158, 11, 0.4), inset 0 1px 2px rgba(255, 255, 255, 0.3);
        }
        .blob-input-pill input {
            width: 100%;
            background: transparent;
            border: none;
            outline: none;
            color: #ffffff;
            font-size: 0.95rem;
            font-weight: 500;
        }
        .blob-input-pill input::placeholder {
            color: rgba(255, 255, 255, 0.72);
            font-weight: 400;
        }

        .eye-toggle-btn {
            background: none;
            border: none;
            color: rgba(255, 255, 255, 0.8);
            cursor: pointer;
            padding: 0 0.25rem;
            display: flex;
            align-items: center;
            transition: color 0.2s;
        }
        .eye-toggle-btn:hover {
            color: #ffd700;
        }

        /* Remember me & Forgot Password */
        .blob-options-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
            padding: 0 0.5rem;
            font-size: 0.78rem;
            color: rgba(255, 255, 255, 0.9);
            margin-top: -0.25rem;
        }
        .blob-remember-label {
            display: flex;
            align-items: center;
            gap: 0.4rem;
            cursor: pointer;
            user-select: none;
        }
        .blob-remember-label input[type="checkbox"] {
            accent-color: #f59e0b;
            cursor: pointer;
            width: 14px;
            height: 14px;
        }
        .blob-forgot-link {
            color: rgba(255, 255, 255, 0.85);
            text-decoration: none;
            transition: color 0.2s;
        }
        .blob-forgot-link:hover {
            color: #ffd700;
            text-decoration: underline;
        }

        /* Alerte Erreur */
        .blob-error-banner {
            background: rgba(185, 28, 28, 0.75);
            border: 1px solid rgba(254, 202, 202, 0.5);
            border-radius: 20px;
            color: #ffffff;
            font-size: 0.82rem;
            font-weight: 600;
            padding: 0.5rem 1rem;
            text-align: center;
            backdrop-filter: blur(4px);
        }

        /* Bouton LOGIN Pillule */
        .blob-btn-wrap {
            display: flex;
            justify-content: center;
            width: 100%;
            margin-top: 0.5rem;
        }
        .btn-login-pill {
            background: linear-gradient(90deg, #1e3a8a 0%, #2563eb 25%, #d97706 75%, #f59e0b 100%);
            border: none;
            border-radius: 50px;
            color: #ffffff;
            font-size: 1.05rem;
            font-weight: 800;
            letter-spacing: 1.5px;
            padding: 0.75rem 2.8rem;
            cursor: pointer;
            box-shadow: 0 8px 22px rgba(245, 158, 11, 0.45), 0 3px 8px rgba(0, 0, 0, 0.2);
            transition: all 0.25s ease;
            text-transform: uppercase;
        }
        .btn-login-pill:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 28px rgba(245, 158, 11, 0.6), 0 4px 10px rgba(0, 0, 0, 0.25);
            background: linear-gradient(90deg, #2563eb 0%, #3b82f6 25%, #f59e0b 75%, #fbbf24 100%);
        }
        .btn-login-pill:active {
            transform: translateY(1px);
        }

        /* Liens Sign up */
        .blob-signup-links {
            margin-top: 0.85rem;
            text-align: center;
            font-size: 0.82rem;
            color: rgba(255, 255, 255, 0.85);
        }
        .blob-signup-links a {
            color: #ffd700;
            font-weight: 700;
            text-decoration: none;
            margin-left: 0.25rem;
        }
        .blob-signup-links a:hover {
            text-decoration: underline;
        }

        /* Puces rôles rapides */
        .blob-role-chips {
            display: flex;
            justify-content: center;
            gap: 0.6rem;
            margin-top: 0.85rem;
        }
        .chip-btn {
            background: rgba(11, 25, 44, 0.55);
            border: 1px solid rgba(255, 215, 0, 0.4);
            border-radius: 20px;
            padding: 0.25rem 0.75rem;
            color: #ffd700;
            font-size: 0.75rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
        }
        .chip-btn:hover {
            background: rgba(245, 158, 11, 0.25);
            border-color: #ffd700;
            color: #ffffff;
        }"""

# Find CSS block and replace
idx1 = router_code.find(old_css_start)
idx2 = router_code.find(old_css_end)
if idx1 != -1 and idx2 != -1:
    end_of_block = idx2 + len(old_css_end)
    router_code = router_code[:idx1] + new_css + router_code[end_of_block:]
    print("Replaced CSS in router.py!")
else:
    print("Could not find CSS markers:", idx1, idx2)

# HTML replacement in router.py
old_html_start = '<!-- 1. LOGIN SCREEN (STYLE ODOO ENTERPRISE PURPLE #714B67) -->'
old_html_end = '<!-- 2. ADMIN PORTAL (GESTION DU RESTAURANT & NAVIGATION VERTICALE À GAUCHE) -->'

new_html = """<!-- 1. LOGIN SCREEN (DESIGN ORGANIQUE BLOB - BLEU MARINE & JAUNE OR) -->
        <div id="authScreen" class="blob-login-container">
            <!-- Couches organiques pour l'effet de profondeur liquide -->
            <div class="blob-layer-back"></div>
            <div class="blob-layer-rim"></div>

            <div class="blob-card">
                <!-- Avatar Médaillon Rond au Sommet -->
                <div class="avatar-badge-wrap">
                    <div class="avatar-badge">
                        <svg class="avatar-icon-svg" viewBox="0 0 100 100">
                            <defs>
                                <linearGradient id="userGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                                    <stop offset="0%" stop-color="#1E3A8A" />
                                    <stop offset="50%" stop-color="#2563EB" />
                                    <stop offset="100%" stop-color="#F59E0B" />
                                </linearGradient>
                            </defs>
                            <circle cx="50" cy="34" r="17" fill="url(#userGrad)" />
                            <path d="M 22 78 C 22 56, 35 50, 50 50 C 65 50, 78 56, 78 78 Z" fill="url(#userGrad)" />
                        </svg>
                    </div>
                </div>

                <!-- Titre Sign In -->
                <h2 class="sign-in-title">Sign In</h2>

                <form onsubmit="handleLogin(event)" class="blob-login-form">
                    <!-- Champ Identifiant avec badge squircle à gauche -->
                    <div class="blob-input-row">
                        <div class="blob-input-badge" title="Identifiant / Username">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/>
                            </svg>
                        </div>
                        <div class="blob-input-pill">
                            <input id="loginUsername" type="text" placeholder="Username" value="admin" required autocomplete="username" />
                        </div>
                    </div>

                    <!-- Champ Mot de passe avec badge squircle à gauche et oeil à droite -->
                    <div class="blob-input-row">
                        <div class="blob-input-badge" title="Mot de passe / Password">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/>
                            </svg>
                        </div>
                        <div class="blob-input-pill">
                            <input id="loginPassword" type="password" placeholder="••••••••••••" value="admin123" required autocomplete="current-password" />
                            <button type="button" class="eye-toggle-btn" onclick="toggleAuthPasswordVisibility()" title="Afficher/Masquer le mot de passe">
                                <svg id="eyeToggleSvg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                                    <circle cx="12" cy="12" r="3"></circle>
                                </svg>
                            </button>
                        </div>
                    </div>

                    <!-- Options Remember me & Forgot password -->
                    <div class="blob-options-row">
                        <label class="blob-remember-label">
                            <input type="checkbox" id="rememberMeCheck" checked />
                            <span>Remember me</span>
                        </label>
                        <a href="javascript:void(0)" onclick="alert('Veuillez contacter votre administrateur pour réinitialiser votre mot de passe.')" class="blob-forgot-link">Forgot password?</a>
                    </div>

                    <!-- Alerte Erreur -->
                    <div id="loginError" class="blob-error-banner" style="display: none;">
                        Wrong login/password
                    </div>

                    <!-- Bouton LOGIN Arrondi Pillule -->
                    <div class="blob-btn-wrap">
                        <button type="submit" class="btn-login-pill">
                            LOGIN
                        </button>
                    </div>

                    <!-- Lien Sign up -->
                    <div class="blob-signup-links">
                        <span>Don't have account?</span>
                        <a href="javascript:void(0)" onclick="alert('Contactez votre administrateur pour obtenir un compte.')">Sign up!</a>
                    </div>

                    <!-- Raccourcis rôles démo : Admin / Gérant -->
                    <div class="blob-role-chips">
                        <button type="button" class="chip-btn" onclick="fillAdminCreds()" title="Connexion Administrateur">👑 Admin</button>
                        <button type="button" class="chip-btn" onclick="fillManagerCreds()" title="Connexion Gérant">🧑‍💼 Gérant</button>
                    </div>
                </form>
            </div>
        </div>

        <!-- 2. ADMIN PORTAL (GESTION DU RESTAURANT & NAVIGATION VERTICALE À GAUCHE) -->"""

h_idx1 = router_code.find(old_html_start)
h_idx2 = router_code.find(old_html_end)
if h_idx1 != -1 and h_idx2 != -1:
    end_of_html = h_idx2 + len(old_html_end)
    router_code = router_code[:h_idx1] + new_html + router_code[end_of_html:]
    print("Replaced HTML in router.py!")
else:
    print("Could not find HTML markers:", h_idx1, h_idx2)

# Add toggleAuthPasswordVisibility in JS
js_func = """
        function toggleAuthPasswordVisibility() {
            const p = document.getElementById('loginPassword');
            const eye = document.getElementById('eyeToggleSvg');
            if (!p || !eye) return;
            if (p.type === 'password') {
                p.type = 'text';
                eye.innerHTML = '<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line>';
            } else {
                p.type = 'password';
                eye.innerHTML = '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle>';
            }
        }
"""
if "function toggleAuthPasswordVisibility" not in router_code:
    router_code = router_code.replace("async function handleLogin(e) {", js_func + "\n        async function handleLogin(e) {")
    print("Added toggleAuthPasswordVisibility JS in router.py!")

with open(router_path, 'w', encoding='utf-8') as f:
    f.write(router_code)

print("Updated backend/app/web/router.py successfully!")
