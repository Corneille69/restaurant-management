from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Portails Web Espaces"])

@router.get("/app", response_class=HTMLResponse)
def get_web_portal():
    return """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RestaurantEngine - Espaces Dédiés</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Caveat:wght@600;700&family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0b0f19;
            --surface: #131b2e;
            --surface-hover: #1c2742;
            --border: #23304e;
            --primary: #6366f1;
            --primary-hover: #4f46e5;
            --admin-accent: #f59e0b;
            --manager-accent: #10b981;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --danger: #ef4444;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', sans-serif; }
        body { background: var(--bg); color: var(--text-main); min-height: 100vh; display: flex; flex-direction: column; }
        header { background: rgba(19, 27, 46, 0.8); backdrop-filter: blur(12px); border-bottom: 1px solid var(--border); padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 100; }
        .logo { font-size: 1.25rem; font-weight: 800; display: flex; align-items: center; gap: 0.6rem; background: linear-gradient(135deg, #a5b4fc, #6366f1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .user-nav { display: flex; align-items: center; gap: 1rem; }
        .role-badge { padding: 0.35rem 0.8rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; }
        .role-admin { background: rgba(245, 158, 11, 0.15); color: var(--admin-accent); border: 1px solid rgba(245, 158, 11, 0.3); }
        .role-manager { background: rgba(16, 185, 129, 0.15); color: var(--manager-accent); border: 1px solid rgba(16, 185, 129, 0.3); }
        .btn { padding: 0.6rem 1.2rem; border-radius: 8px; font-weight: 600; font-size: 0.875rem; cursor: pointer; transition: all 0.2s ease; border: none; display: inline-flex; align-items: center; gap: 0.5rem; }
        .btn-primary { background: var(--primary); color: white; }
        .btn-primary:hover { background: var(--primary-hover); }
        .btn-danger { background: rgba(239, 68, 68, 0.15); color: var(--danger); border: 1px solid rgba(239, 68, 68, 0.3); }
        .btn-danger:hover { background: var(--danger); color: white; }
        .btn-secondary { background: var(--surface-hover); color: var(--text-main); border: 1px solid var(--border); }
        .btn-secondary:hover { background: var(--border); }

        .container { max-width: 1540px; margin: 1.5rem auto; padding: 0 1.5rem; width: 100%; flex: 1; }
        
        /* =========================================================================
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
        
        /* Admin Shell : Layout avec Sidebar Verticale à Gauche */
        .admin-shell {
            display: flex;
            gap: 1.75rem;
            align-items: flex-start;
            width: 100%;
        }
        .admin-sidebar {
            width: 285px;
            flex-shrink: 0;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1.5rem 1.15rem;
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
            position: sticky;
            top: 5rem;
            box-shadow: 0 15px 35px -5px rgba(0, 0, 0, 0.45);
        }
        .admin-sidebar-brand {
            display: flex;
            align-items: center;
            gap: 0.85rem;
            padding-bottom: 1.25rem;
            border-bottom: 1px solid var(--border);
        }
        .sidebar-brand-logo {
            width: 44px;
            height: 44px;
            border-radius: 12px;
            background: rgba(245, 158, 11, 0.15);
            border: 1.5px solid rgba(245, 158, 11, 0.35);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.4rem;
            overflow: hidden;
            flex-shrink: 0;
        }
        .sidebar-brand-logo img {
            width: 100%;
            height: 100%;
            object-fit: contain;
        }
        .sidebar-brand-meta {
            overflow: hidden;
        }
        .sidebar-brand-meta h4 {
            font-size: 1.05rem;
            font-weight: 800;
            color: #ffffff;
            line-height: 1.2;
            margin-bottom: 0.2rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .sidebar-brand-meta span {
            font-size: 0.72rem;
            color: #fbbf24;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            display: block;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .sidebar-group-label {
            font-size: 0.68rem;
            font-weight: 800;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            padding: 0 0.5rem;
            margin-bottom: 0.35rem;
        }
        .sidebar-menu-list {
            display: flex;
            flex-direction: column;
            gap: 0.4rem;
        }
        .sidebar-nav-item {
            width: 100%;
            text-align: left;
            background: transparent;
            border: 1px solid transparent;
            border-radius: 12px;
            padding: 0.75rem 0.9rem;
            color: #cbd5e1;
            display: flex;
            align-items: center;
            gap: 0.85rem;
            cursor: pointer;
            transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
            font-family: inherit;
            user-select: none;
        }
        .sidebar-nav-item:hover {
            background: var(--surface-hover);
            color: #ffffff;
            border-color: rgba(255, 255, 255, 0.08);
            transform: translateX(3px);
        }
        .sidebar-nav-item.active {
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.22), rgba(217, 119, 6, 0.12));
            border: 1px solid #f59e0b;
            border-left: 4px solid #f59e0b;
            color: #ffffff;
            box-shadow: 0 4px 15px rgba(245, 158, 11, 0.25);
        }
        .sidebar-icon {
            display: none !important;
        }
        .sidebar-item-content {
            display: flex;
            flex-direction: column;
            line-height: 1.2;
            overflow: hidden;
        }
        .sidebar-item-title {
            font-size: 0.88rem;
            font-weight: 700;
            color: inherit;
        }
        .sidebar-item-sub {
            font-size: 0.72rem;
            color: var(--text-muted);
            margin-top: 2px;
        }
        .sidebar-nav-item.active .sidebar-item-sub {
            color: #fde68a;
        }
        .sidebar-bottom-box {
            margin-top: auto;
            padding-top: 1rem;
            border-top: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }
        .sidebar-user-card {
            background: rgba(245, 158, 11, 0.1);
            border: 1px solid rgba(245, 158, 11, 0.25);
            border-radius: 10px;
            padding: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        .admin-main-area {
            flex: 1;
            min-width: 0;
        }
        @media (max-width: 992px) {
            .admin-shell {
                flex-direction: column;
            }
            .admin-sidebar {
                width: 100%;
                position: static;
            }
        }

        /* Generic form controls */
        .form-group { margin-bottom: 1.25rem; }
        .form-group label { display: block; font-size: 0.875rem; font-weight: 600; margin-bottom: 0.5rem; color: var(--text-muted); }
        .form-control { width: 100%; padding: 0.75rem 1rem; background: var(--bg); border: 1px solid var(--border); border-radius: 8px; color: white; font-size: 0.95rem; outline: none; transition: border-color 0.2s; }
        .form-control:focus { border-color: var(--primary); }

        /* Dashboard Common */
        .grid-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.25rem; margin-bottom: 2rem; }
        .stat-card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; }
        .stat-card .label { color: var(--text-muted); font-size: 0.85rem; font-weight: 500; margin-bottom: 0.5rem; }
        .stat-card .value { font-size: 1.85rem; font-weight: 800; color: white; }

        .content-panel { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 1.75rem; margin-bottom: 2rem; }
        .panel-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
        .panel-header h3 { font-size: 1.25rem; font-weight: 700; }

        /* Tables & Lists */
        table { width: 100%; border-collapse: collapse; text-align: left; }
        th { padding: 0.75rem 1rem; color: var(--text-muted); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1px solid var(--border); }
        td { padding: 1rem; border-bottom: 1px solid var(--border); font-size: 0.9rem; }
        tr:hover td { background: var(--surface-hover); }

        .badge { padding: 0.25rem 0.6rem; border-radius: 6px; font-size: 0.75rem; font-weight: 600; display: inline-block; }
        .badge-success { background: rgba(16, 185, 129, 0.2); color: #34d399; }
        .badge-warning { background: rgba(245, 158, 11, 0.2); color: #fbbf24; }
        .badge-danger { background: rgba(239, 68, 68, 0.2); color: #f87171; }

        .banner-role { padding: 1rem 1.5rem; border-radius: 12px; margin-bottom: 2rem; display: flex; align-items: center; gap: 1rem; font-size: 0.95rem; }
        .banner-admin { background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); color: #fcd34d; }
        .banner-manager { background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); color: #6ee7b7; }

        .hidden { display: none !important; }

        /* Navigation Tabs */
        .manager-nav-tabs { display: flex; gap: 0.6rem; margin-bottom: 1.5rem; border-bottom: 2px solid var(--border); padding-bottom: 0.85rem; overflow-x: auto; flex-wrap: wrap; }
        .mgr-tab-btn { padding: 0.7rem 1.25rem; background: var(--surface); border: 1px solid var(--border); color: var(--text-muted); border-radius: 10px; font-size: 0.88rem; font-weight: 700; cursor: pointer; transition: all 0.2s ease; display: inline-flex; align-items: center; gap: 0.5rem; user-select: none; }
        .mgr-tab-btn:hover { background: var(--surface-hover); color: white; border-color: var(--manager-accent); }
        .mgr-tab-btn.active { background: linear-gradient(135deg, #10b981, #059669); color: white; border-color: #10b981; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.35); }
        .adm-tab-btn.active { background: linear-gradient(135deg, #f59e0b, #d97706); color: white; border-color: #f59e0b; box-shadow: 0 4px 15px rgba(245, 158, 11, 0.35); }

        @keyframes recordingPulse {
            0% { transform: scale(0.9); opacity: 0.6; }
            100% { transform: scale(1.25); opacity: 1; }
        }
        .recording-pulse-dot {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #ef4444;
            box-shadow: 0 0 10px #ef4444;
            animation: recordingPulse 0.8s infinite alternate;
        }
        .badge-unread {
            background: #ef4444;
            color: white;
            border-radius: 9999px;
            font-size: 0.7rem;
            font-weight: 800;
            padding: 2px 7px;
        }

        /* FACTURE OFFICIELLE CORPORATE & MODÈLE MONOCHROME DE RÉFÉRENCE (FIDÈLE À L'IMAGE & SANS CODE EN DUR) */
        .corporate-invoice-paper {
            background-color: #ffffff;
            color: #000000;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            padding: 8mm 12mm 8mm 12mm;
            border-radius: 4px;
            box-shadow: 0 20px 45px -10px rgba(0, 0, 0, 0.35);
            max-width: 820px;
            width: 100%;
            min-height: 250mm; /* Occupe 85% de la hauteur de la feuille A4 (297mm * 0.85 = 252.45mm) */
            margin: 0 auto;
            position: relative;
            border: 1px solid #000000;
            box-sizing: border-box;
            font-size: 11px;
            line-height: 1.5;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            page-break-inside: avoid;
            page-break-after: avoid;
        }
        .corporate-inv-table {
            width: 100%;
            border-collapse: collapse;
            border: 1px solid #000000;
            margin-bottom: 0;
            position: relative;
            z-index: 2;
        }
        .corporate-inv-table th {
            background-color: #000000 !important;
            color: #ffffff !important;
            padding: 9px 12px;
            font-size: 11px;
            font-weight: 900;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            border: 1px solid #000000;
        }
        .corporate-inv-table td {
            padding: 8px 12px;
            font-size: 11px;
            color: #000000;
            border: 1px solid #000000;
            vertical-align: middle;
        }
        .corporate-inv-totals-table {
            width: 52%;
            margin-left: auto;
            border-collapse: collapse;
            border-top: none;
            font-size: 11px;
            margin-bottom: 1.75rem;
        }
        .corporate-inv-totals-table td {
            border: 1px solid #000000;
            padding: 7px 10px;
            font-size: 11px;
            color: #000000;
        }
        .corporate-inv-totals-table tr.total-ttc-row {
            background-color: #000000 !important;
            color: #ffffff !important;
        }
        .corporate-inv-totals-table tr.total-ttc-row td {
            color: #ffffff !important;
            font-weight: 900;
            border: 1px solid #000000;
        }

        @page {
            size: A4 portrait;
            margin: 5mm 8mm 5mm 8mm;
        }
        @media print {
            html, body {
                height: 100% !important;
                margin: 0 !important;
                padding: 0 !important;
                background: #ffffff !important;
            }
            body * { visibility: hidden !important; }
            #invoiceModal:not(.hidden), #invoiceModal:not(.hidden) * { visibility: visible !important; }
            #modalGlobalInvoicePrint:not(.hidden), #modalGlobalInvoicePrint:not(.hidden) * { visibility: visible !important; }
            #dgiInvoiceModal:not(.hidden), #dgiInvoiceModal:not(.hidden) * { visibility: visible !important; }
            #receiptModal:not(.hidden), #receiptModal:not(.hidden) * { visibility: visible !important; }

            #invoiceModal:not(.hidden),
            #modalGlobalInvoicePrint:not(.hidden),
            #dgiInvoiceModal:not(.hidden) {
                position: absolute !important;
                left: 0 !important;
                top: 0 !important;
                width: 100% !important;
                background: white !important;
                padding: 0 !important;
                box-shadow: none !important;
                margin: 0 !important;
                page-break-after: avoid !important;
                page-break-inside: avoid !important;
            }
            .corporate-invoice-paper {
                border: none !important;
                box-shadow: none !important;
                padding: 4mm 6mm !important;
                background: #ffffff !important;
                max-width: 100% !important;
                width: 100% !important;
                height: 252mm !important; /* Occupe exactement 85% de la feuille A4 */
                min-height: 252mm !important;
                max-height: 254mm !important;
                display: flex !important;
                flex-direction: column !important;
                justify-content: space-between !important;
                overflow: hidden !important;
                page-break-inside: avoid !important;
                page-break-after: avoid !important;
                margin: 0 !important;
                box-sizing: border-box !important;
                line-height: 1.5 !important;
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }
            .corporate-inv-table th,
            .corporate-inv-totals-table tr.total-ttc-row,
            .corporate-inv-totals-table tr.total-ttc-row td {
                background-color: #000000 !important;
                color: #ffffff !important;
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }
            .modal-actions-bar { display: none !important; }
            #receiptModal:not(.hidden) { position: absolute !important; left: 50% !important; transform: translateX(-50%) !important; top: 0 !important; width: 340px !important; background: white !important; padding: 10px !important; }
            button { display: none !important; }
        }

        /* =========================================================================
           GRILLE & CARTES DES PLATS ET MENUS : FORME SQUIRCLE 3D (RÉFÉRENCE)
           Design : Bleu Marine, Jaune Or et Blanc Pur
           ========================================================================= */
        .dish-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(155px, 1fr));
            gap: 1.1rem;
            padding: 0.75rem 0.25rem;
        }
        .dish-card {
            width: 100%;
            height: 165px;
            background: #ffffff;
            border-radius: 24px;
            border: 3.5px solid #f59e0b;
            box-shadow: 0 4px 0 #d97706, inset 0 0 0 1.5px #1e3a8a, 0 8px 18px rgba(30, 58, 138, 0.15);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            padding: 10px 8px;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            user-select: none;
            box-sizing: border-box;
            text-align: center;
        }
        .dish-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 7px 0 #d97706, inset 0 0 0 1.5px #1e3a8a, 0 14px 24px rgba(30, 58, 138, 0.25);
            border-color: #fbbf24;
        }
        .dish-card:active {
            transform: translateY(1px);
            box-shadow: 0 2px 0 #d97706, inset 0 0 0 1.5px #1e3a8a, 0 4px 10px rgba(30, 58, 138, 0.2);
        }
        .dish-card-header {
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 4px;
        }
        .dish-card-cat-badge {
            font-size: 0.68rem;
            font-weight: 700;
            padding: 2px 7px;
            background: #1e3a8a;
            color: #ffffff;
            border-radius: 8px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 80px;
        }
        .dish-card-stock-badge {
            font-size: 0.68rem;
            font-weight: 800;
            padding: 2px 6px;
            border-radius: 8px;
            white-space: nowrap;
        }
        .dish-card-stock-ok {
            background: #eff6ff;
            color: #1e40af;
            border: 1px solid #bfdbfe;
        }
        .dish-card-stock-warning {
            background: #fef3c7;
            color: #b45309;
            border: 1px solid #fde68a;
        }
        .dish-card-stock-empty {
            background: #fef2f2;
            color: #dc2626;
            border: 1px solid #fecaca;
        }
        .dish-card-title {
            font-size: 0.84rem;
            font-weight: 800;
            color: #0f172a;
            line-height: 1.25;
            text-transform: uppercase;
            letter-spacing: -0.2px;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            margin: auto 0;
            padding: 2px 4px;
        }
        .dish-card-footer {
            width: 100%;
            padding-top: 6px;
            border-top: 1px dashed #e2e8f0;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .dish-card-price-pill {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            color: #ffffff;
            font-size: 0.8rem;
            font-weight: 800;
            padding: 3px 10px;
            border-radius: 10px;
            box-shadow: 0 2px 6px rgba(245, 158, 11, 0.35);
            border: 1px solid #fbbf24;
            letter-spacing: 0.2px;
            white-space: nowrap;
        }
        .dish-card.out-of-stock {
            border: 3.5px dashed #ef4444 !important;
            background: #fff5f5 !important;
            box-shadow: 0 4px 0 #b91c1c, inset 0 0 0 1.5px #ef4444, 0 6px 14px rgba(239, 68, 68, 0.15) !important;
            opacity: 0.82;
            cursor: not-allowed;
        }
        .dish-card.out-of-stock:hover {
            transform: none !important;
            box-shadow: 0 4px 0 #b91c1c, inset 0 0 0 1.5px #ef4444, 0 6px 14px rgba(239, 68, 68, 0.15) !important;
        }
        .dish-card-stock-alert {
            font-size: 0.68rem;
            font-weight: 800;
            color: #dc2626;
            background: rgba(239, 68, 68, 0.15);
            border: 1px solid rgba(239, 68, 68, 0.4);
            border-radius: 6px;
            padding: 1px 5px;
            margin-top: 3px;
            display: inline-block;
            letter-spacing: -0.2px;
        }

        /* =========================================================================
           MODE ADMIN : DESIGN EXÉCUTIF "CONFIGURATION RESTAURANT & DGI"
           Style institutionnel haut de gamme : Fond blanc épuré & ardoise (#f1f5f9),
           Bleu royal profond (#1e3a8a, #2563eb), Vert émeraude (#059669),
           Accents or ambré (#f59e0b, #fbbf24), liserés décoratifs et typographie nette.
           ========================================================================= */
        body.admin-mode {
            background-color: #f1f5f9 !important;
            color: #0f172a !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        /* En-tête Header en mode Admin */
        body.admin-mode header {
            background: #ffffff !important;
            backdrop-filter: blur(8px);
            border-bottom: 2px solid #e2e8f0 !important;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05) !important;
        }
        body.admin-mode header .logo {
            background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            font-weight: 800 !important;
        }
        body.admin-mode #navUserName {
            color: #0f172a !important;
            font-weight: 700 !important;
        }
        body.admin-mode .role-admin {
            background: #fef3c7 !important;
            color: #92400e !important;
            border: 1.5px solid #f59e0b !important;
            font-weight: 800 !important;
        }
        body.admin-mode #btnHeaderConfig {
            background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%) !important;
            color: #ffffff !important;
            border: 1px solid #1e3a8a !important;
            box-shadow: 0 4px 12px rgba(30, 58, 138, 0.25) !important;
            font-weight: 700 !important;
        }
        body.admin-mode #btnHeaderDiscuss {
            background: #ffffff !important;
            border: 1.5px solid #cbd5e1 !important;
        }
        body.admin-mode #btnHeaderDiscuss svg path:first-child {
            fill: #1e3a8a !important;
        }
        body.admin-mode #btnHeaderDiscuss svg path:last-child {
            fill: #2563eb !important;
        }
        body.admin-mode header .btn-secondary {
            background: #ffffff !important;
            border: 1.5px solid #cbd5e1 !important;
            color: #1e293b !important;
            font-weight: 700 !important;
        }
        body.admin-mode header .btn-secondary:hover {
            background: #fee2e2 !important;
            border-color: #ef4444 !important;
            color: #dc2626 !important;
        }

        /* Shell et Sidebar Administrative Exécutive */
        body.admin-mode .admin-shell {
            padding-top: 0.25rem;
        }
        body.admin-mode .admin-sidebar {
            background: #ffffff !important;
            border: 1.5px solid #e2e8f0 !important;
            border-top: 4px solid #1e3a8a !important;
            border-radius: 18px !important;
            box-shadow: 0 10px 30px -5px rgba(15, 23, 42, 0.08) !important;
        }
        body.admin-mode .admin-sidebar-brand {
            border-bottom: 1.5px solid #e2e8f0 !important;
        }
        body.admin-mode #sideRestoName {
            color: #0a0f1d !important;
            font-weight: 800 !important;
        }
        body.admin-mode #sideRestoSub {
            color: #64748b !important;
            font-weight: 600 !important;
        }
        body.admin-mode .sidebar-brand-logo {
            background: #eff6ff !important;
            border: 1.5px solid #bfdbfe !important;
            color: #1e3a8a !important;
        }
        body.admin-mode .sidebar-group-label {
            color: #1e3a8a !important;
            font-weight: 800 !important;
            letter-spacing: 0.08em !important;
            font-size: 0.72rem !important;
        }
        body.admin-mode .sidebar-nav-item {
            background: #ffffff !important;
            border: 1.5px solid #e2e8f0 !important;
            color: #334155 !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03) !important;
            transition: all 0.2s ease !important;
        }
        body.admin-mode .sidebar-nav-item:hover {
            background: #f8fafc !important;
            border-color: #cbd5e1 !important;
            color: #1e3a8a !important;
            transform: translateX(3px) !important;
        }
        body.admin-mode .sidebar-nav-item.active {
            background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%) !important;
            border: 1.5px solid #1e3a8a !important;
            border-left: 5px solid #f59e0b !important;
            color: #ffffff !important;
            box-shadow: 0 6px 18px rgba(30, 58, 138, 0.28) !important;
        }
        body.admin-mode .sidebar-nav-item.active .sidebar-item-title {
            color: #ffffff !important;
            font-weight: 800 !important;
        }
        body.admin-mode .sidebar-nav-item.active .sidebar-item-sub {
            color: #fef3c7 !important;
            font-weight: 600 !important;
        }
        body.admin-mode .sidebar-nav-item:not(.active) .sidebar-item-title {
            color: #0f172a !important;
            font-weight: 700 !important;
        }
        body.admin-mode .sidebar-nav-item:not(.active) .sidebar-item-sub {
            color: #64748b !important;
        }
        body.admin-mode .sidebar-bottom-box {
            border-top: 1.5px solid #e2e8f0 !important;
        }
        body.admin-mode .sidebar-user-card {
            background: #eff6ff !important;
            border: 1.5px solid #bfdbfe !important;
        }
        body.admin-mode .sidebar-user-card div[style*="color: #fbbf24"],
        body.admin-mode .sidebar-user-card div[style*="color:#fbbf24"] {
            color: #1e3a8a !important;
            font-weight: 800 !important;
        }

        /* Panneaux de Contenu & Cartes Institutionnelles */
        body.admin-mode .content-panel {
            background: #ffffff !important;
            border: 1.5px solid #e2e8f0 !important;
            border-radius: 16px !important;
            color: #0f172a !important;
            box-shadow: 0 6px 20px -4px rgba(15, 23, 42, 0.06) !important;
            border-top: 4px solid #1e3a8a !important;
            position: relative;
        }
        body.admin-mode .panel-header h3 {
            color: #0a0f1d !important;
            font-weight: 800 !important;
        }
        body.admin-mode .panel-header h3 span {
            color: #1e3a8a !important;
        }

        /* KPIs et Cartes Statistiques */
        body.admin-mode .stat-card {
            background: #ffffff !important;
            border: 1.5px solid #e2e8f0 !important;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04) !important;
            border-radius: 12px !important;
        }
        body.admin-mode .stat-card .label {
            color: #475569 !important;
            font-weight: 700 !important;
            font-size: 0.8rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.04em !important;
        }
        body.admin-mode .stat-card .value {
            color: #0a0f1d !important;
            font-weight: 800 !important;
        }

        /* Bannière Exécutive Tableau de bord */
        body.admin-mode #admSectionOverview > .content-panel:first-child {
            background: linear-gradient(135deg, #eff6ff 0%, #ffffff 50%, #fffbeb 100%) !important;
            border: 1.5px solid #bfdbfe !important;
            border-left: 6px solid #1e3a8a !important;
            box-shadow: 0 8px 24px rgba(30, 58, 138, 0.08) !important;
        }
        body.admin-mode #admSectionOverview > .content-panel:first-child h2 {
            color: #0a0f1d !important;
            font-weight: 800 !important;
        }

        /* Bandeau Facture du jour & DGI sur l'accueil */
        body.admin-mode #admSectionOverview div[style*="background: linear-gradient(135deg, rgba(245, 158, 11, 0.18)"] {
            background: linear-gradient(135deg, #fffbeb 0%, #ffffff 55%, #eff6ff 100%) !important;
            border: 2px solid #f59e0b !important;
            border-left: 6px solid #f59e0b !important;
            box-shadow: 0 8px 24px rgba(245, 158, 11, 0.12) !important;
        }
        body.admin-mode #admSectionOverview div[style*="background: linear-gradient(135deg, rgba(245, 158, 11, 0.18)"] div[style*="color: #fbbf24"] {
            color: #92400e !important;
        }
        body.admin-mode #admSectionOverview div[style*="background: linear-gradient(135deg, rgba(245, 158, 11, 0.18)"] p {
            color: #334155 !important;
        }

        /* Hero Card Facture du Jour & Certification DGI */
        body.admin-mode #heroDailyInvoiceCard {
            background: linear-gradient(135deg, #ecfdf5 0%, #ffffff 50%, #eff6ff 100%) !important;
            border: 2px solid #10b981 !important;
            border-left: 6px solid #059669 !important;
            box-shadow: 0 10px 28px rgba(16, 185, 129, 0.12) !important;
        }
        body.admin-mode #heroDailyInvoiceCard h2 {
            color: #065f46 !important;
            font-weight: 800 !important;
        }
        body.admin-mode #heroDailyInvoiceCard div[style*="background: rgba(15, 23, 42, 0.7)"] {
            background: #ffffff !important;
            border: 1.5px solid #e2e8f0 !important;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04) !important;
        }
        body.admin-mode #heroDailyInvoiceCard div[style*="background: rgba(15, 23, 42, 0.7)"] #heroDailyDateText {
            color: #0a0f1d !important;
        }
        body.admin-mode #heroDailyInvoiceCard div[style*="background: rgba(15, 23, 42, 0.7)"] #heroDailyManagersText {
            color: #1e3a8a !important;
        }

        /* Panneau d'Agrégation Factures Globales */
        body.admin-mode #admSectionGlobalInvoices .content-panel[style*="border: 2px solid #f59e0b"] {
            background: linear-gradient(180deg, #fffbeb 0%, #ffffff 100%) !important;
            border: 2px solid #f59e0b !important;
            border-left: 6px solid #d97706 !important;
        }
        body.admin-mode #admSectionGlobalInvoices .content-panel[style*="border: 2px solid #f59e0b"] h3 {
            color: #92400e !important;
        }

        /* Bannière Financière Temps Réel dans Factures */
        body.admin-mode #admSectionInvoices .content-panel:first-child {
            background: linear-gradient(180deg, #eff6ff 0%, #ffffff 100%) !important;
            border: 2px solid #3b82f6 !important;
            border-left: 6px solid #1e3a8a !important;
        }
        body.admin-mode #admSectionInvoices .content-panel:first-child h3 {
            color: #1e3a8a !important;
        }

        /* Sous-blocs de la Configuration Restaurant & DGI */
        body.admin-mode #admSectionConfig div[style*="background: var(--bg)"] {
            background: #f8fafc !important;
            border: 1.5px solid #e2e8f0 !important;
            border-radius: 14px !important;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03) !important;
        }
        body.admin-mode #admSectionConfig h4 {
            color: #1e3a8a !important;
            font-weight: 800 !important;
            border-bottom: 2px solid #e2e8f0 !important;
            padding-bottom: 0.6rem !important;
        }
        body.admin-mode #cfgLogoPreviewBox {
            background: #ffffff !important;
            border: 2px dashed #cbd5e1 !important;
        }

        /* Section Chat & Communications */
        body.admin-mode #admSectionChat > div {
            background: #ffffff !important;
            border: 1.5px solid #e2e8f0 !important;
            border-top: 4px solid #1e3a8a !important;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06) !important;
        }
        body.admin-mode #admSectionChat h2 {
            color: #1e3a8a !important;
        }
        body.admin-mode #admSectionChat div[style*="background: rgba(11, 15, 25, 0.6)"] {
            background: #f8fafc !important;
            border: 1.5px solid #e2e8f0 !important;
        }
        body.admin-mode #admChatHeader {
            background: #ffffff !important;
            border-bottom: 1.5px solid #e2e8f0 !important;
        }
        body.admin-mode #admChatActiveName {
            color: #0a0f1d !important;
        }
        body.admin-mode #admChatMessagesContainer {
            background: #f1f5f9 !important;
        }
        body.admin-mode #admSectionChat div[style*="background: rgba(19, 27, 46, 0.5)"] {
            background: #ffffff !important;
            border-top: 1px solid #e2e8f0 !important;
        }

        /* Contrôles de Formulaire, Inputs et Sélections */
        body.admin-mode .form-control,
        body.admin-mode select.form-control,
        body.admin-mode input.form-control {
            background: #ffffff !important;
            border: 1.5px solid #cbd5e1 !important;
            color: #0f172a !important;
            font-weight: 500 !important;
            border-radius: 8px !important;
        }
        body.admin-mode .form-control:focus {
            border-color: #2563eb !important;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.16) !important;
        }
        body.admin-mode .form-group label {
            color: #1e293b !important;
            font-weight: 700 !important;
        }
        body.admin-mode label {
            color: #1e293b !important;
        }

        /* Tableaux et Listes Administratives */
        body.admin-mode table {
            background: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 10px !important;
            overflow: hidden !important;
        }
        body.admin-mode th {
            background: #f8fafc !important;
            color: #1e3a8a !important;
            font-weight: 800 !important;
            border-bottom: 2px solid #cbd5e1 !important;
            font-size: 0.82rem !important;
            letter-spacing: 0.04em !important;
        }
        body.admin-mode td {
            background: #ffffff !important;
            border-bottom: 1px solid #e2e8f0 !important;
            color: #1e293b !important;
            font-size: 0.9rem !important;
        }
        body.admin-mode tr:hover td {
            background: #f8fafc !important;
        }

        /* Boutons d'Action */
        body.admin-mode .btn-primary {
            background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%) !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            border: none !important;
            box-shadow: 0 4px 12px rgba(30, 58, 138, 0.25) !important;
        }
        body.admin-mode .btn-primary:hover {
            background: linear-gradient(135deg, #172554 0%, #1d4ed8 100%) !important;
            box-shadow: 0 6px 16px rgba(30, 58, 138, 0.35) !important;
            transform: translateY(-1px) !important;
        }
        body.admin-mode .btn-secondary {
            background: #ffffff !important;
            border: 1.5px solid #cbd5e1 !important;
            color: #1e293b !important;
            font-weight: 700 !important;
        }
        body.admin-mode .btn-secondary:hover {
            background: #f1f5f9 !important;
            border-color: #94a3b8 !important;
            color: #0f172a !important;
        }

        /* Boutons Spécifiques Or DGI */
        body.admin-mode button[style*="linear-gradient(135deg, #f59e0b, #d97706)"],
        body.admin-mode button[style*="linear-gradient(135deg,#f59e0b,#d97706)"] {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
            color: #0a0f1d !important;
            font-weight: 800 !important;
            box-shadow: 0 4px 14px rgba(245, 158, 11, 0.35) !important;
        }

        /* Badges de Statut en mode Admin */
        body.admin-mode .badge-success {
            background: #ecfdf5 !important;
            color: #065f46 !important;
            border: 1px solid #a7f3d0 !important;
            font-weight: 700 !important;
        }
        body.admin-mode .badge-warning {
            background: #fffbeb !important;
            color: #92400e !important;
            border: 1px solid #fde68a !important;
            font-weight: 700 !important;
        }
        body.admin-mode .badge-danger {
            background: #fef2f2 !important;
            color: #991b1b !important;
            border: 1px solid #fecaca !important;
            font-weight: 700 !important;
        }

        /* Correction des textes inline qui étaient blancs sur fond sombre */
        body.admin-mode .content-panel div > span[style*="color: white"],
        body.admin-mode .content-panel div > span[style*="color:white"],
        body.admin-mode .content-panel div > span[style*="color: #ffffff"],
        body.admin-mode .content-panel div > span[style*="color:#ffffff"] {
            color: #0f172a !important;
        }
        body.admin-mode #overviewTaxRegime { color: #d97706 !important; font-weight: 700; }
        body.admin-mode #overviewFiscalDivision { color: #1e3a8a !important; font-weight: 700; }
        body.admin-mode #overviewIfu { color: #0284c7 !important; font-weight: 800; }
        body.admin-mode #overviewNim { color: #059669 !important; font-weight: 700; }
    </style>
</head>
<body>
    <header>
        <div class="logo">
            <span id="headerBrandLogo"></span>
            <span id="headerBrandName" class="app-restaurant-name">RestaurantEngine</span>
        </div>
        <div id="userNav" class="user-nav hidden" style="display: flex; align-items: center; gap: 0.85rem;">
            <button id="btnHeaderConfig" class="btn btn-primary" onclick="switchAdminTab('config')" style="background: linear-gradient(135deg, #f59e0b, #d97706); color: black; font-weight: 800; font-size: 0.82rem; padding: 0.45rem 1rem; border-radius: 8px; box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4); display: none;">CONFIGURATION DU RESTAURANT &amp; DGI</button>
            <a href="javascript:void(0)" onclick="openDirectCommunicationChat()" id="btnHeaderDiscuss" title="Messagerie &amp; Appels (SMS, Vocaux &amp; Vidéo)" style="position: relative; display: inline-flex; align-items: center; justify-content: center; text-decoration: none; padding: 6px; border-radius: 8px; background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255, 255, 255, 0.12); cursor: pointer; transition: all 0.2s ease;">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                    <path d="M20 2H8c-1.1 0-2 .9-2 2v1h10c1.66 0 3 1.34 3 3v8h1c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z" fill="#94a3b8"/>
                    <path d="M15 6H4c-1.1 0-2 .9-2 2v8c0 1.1.9 2 2 2h2v3l3.5-3H15c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2z" fill="#f8fafc"/>
                </svg>
                <span id="headerChatBadge" style="position: absolute; top: -4px; right: -5px; background: #10b981; color: white; border-radius: 9999px; font-size: 0.68rem; font-weight: 800; min-width: 18px; height: 18px; display: none; align-items: center; justify-content: center; padding: 0 4px; box-shadow: 0 2px 6px rgba(0,0,0,0.5);">0</span>
            </a>
            <span id="navUserName" style="font-weight: 600;"></span>
            <span id="navUserBadge" class="role-badge"></span>
            <button class="btn btn-secondary" onclick="logout()">Déconnexion</button>
        </div>
    </header>

    <div class="container">
        <!-- 1. LOGIN SCREEN (MODÈLE FIDÈLE BLEU MARINE & JAUNE OR - BON RETOUR !) -->
        <div id="authScreen" class="justgo-login-container">
            <!-- 1. Logo du Restaurant dans la carte arrondie foncée -->
            <div class="justgo-logo-card">
                <img id="authBrandLogoImg" src="/restaurant/api/brand/logo" alt="Logo" onerror="this.onerror=null; this.src='https://cdn-icons-png.flaticon.com/512/857/857681.png';" />
            </div>

            <!-- 2. Titre & Sous-titre -->
            <h1 class="justgo-title">Bonretour !</h1>
            <p class="justgo-subtitle">Heureuxde vous retrouver, veuillez vous connecter.</p>

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
                    <span>Sesouvenir de moi</span>
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
                    <button type="button" class="justgo-chip" onclick="fillAdminCreds()" title="Connexion Administrateur">Admin</button>
                    <button type="button" class="justgo-chip" onclick="fillManagerCreds()" title="Connexion Gérant">Gérant</button>
                </div>
            </form>
        </div>

        <!-- 2. ADMIN PORTAL (GESTION DU RESTAURANT & NAVIGATION VERTICALE À GAUCHE) -->
        <div id="adminPortal" class="hidden">
            <div class="admin-shell">
                <!-- SIDEBAR VERTICALE À GAUCHE (ÉLÉMENTS BIEN DESIGNÉS ET ORGANISÉS VERTICALEMENT) -->
                <aside class="admin-sidebar">
                    <!-- Brand du Restaurant avec Logo et Nom dynamique -->
                    <div class="admin-sidebar-brand">
                        <div id="sideRestoLogo" class="sidebar-brand-logo"></div>
                        <div class="sidebar-brand-meta">
                            <h4 id="sideRestoName">LemoDaje Restaurant</h4>
                            <span id="sideRestoSub">SupervisionGénérale</span>
                        </div>
                    </div>

                    <!-- Groupe 1 : Pilotage & Gestion Centrale -->
                    <div class="sidebar-group-label">PILOTAGE &amp;GESTION</div>
                    <div class="sidebar-menu-list">
                        <button class="sidebar-nav-item active" id="admTabBtnOverview" onclick="switchAdminTab('overview')">
                            <span class="sidebar-icon"></span>
                            <div class="sidebar-item-content">
                                <span class="sidebar-item-title">GestionRestaurant</span>
                                <span class="sidebar-item-sub">Tableaude bord &amp; KPIs</span>
                            </div>
                        </button>

                        <button class="sidebar-nav-item" id="admTabBtnGlobalInvoices" onclick="switchAdminTab('globalInvoices')">
                            <span class="sidebar-icon"></span>
                            <div class="sidebar-item-content">
                                <span class="sidebar-item-title">Facture &amp;Certification</span>
                                <span class="sidebar-item-sub">Facturedu Jour &amp; DGI e-MCF</span>
                            </div>
                        </button>

                        <button class="sidebar-nav-item" id="admTabBtnInvoices" onclick="switchAdminTab('invoices')">
                            <span class="sidebar-icon"></span>
                            <div class="sidebar-item-content">
                                <span class="sidebar-item-title">FacturesClients (Détail)</span>
                                <span class="sidebar-item-sub">Reçusindividuels encaissés</span>
                            </div>
                        </button>
                    </div>

                    <!-- Groupe 2 : Équipe & Exploitation -->
                    <div class="sidebar-group-label" style="margin-top: 0.6rem;">ÉQUIPE &amp;EXPLOITATION</div>
                    <div class="sidebar-menu-list">
                        <button class="sidebar-nav-item" id="admTabBtnManagers" onclick="switchAdminTab('managers')">
                            <span class="sidebar-icon"></span>
                            <div class="sidebar-item-content">
                                <span class="sidebar-item-title">Gérants &amp;Sessions</span>
                                <span class="sidebar-item-sub">Prisesde service &amp; caisses</span>
                            </div>
                        </button>

                        <button class="sidebar-nav-item" id="admTabBtnMenu" onclick="switchAdminTab('menu')">
                            <span class="sidebar-icon"></span>
                            <div class="sidebar-item-content">
                                <span class="sidebar-item-title">Carte &amp;Produits</span>
                                <span class="sidebar-item-sub">TarifsFCFA &amp; plats</span>
                            </div>
                        </button>
                    </div>

                    <!-- Groupe 3 : Configuration Système -->
                    <div class="sidebar-group-label" style="margin-top: 0.6rem;">CONFIGURATIONSYSTÈME</div>
                    <div class="sidebar-menu-list">
                        <button class="sidebar-nav-item" id="admTabBtnConfig" onclick="switchAdminTab('config')">
                            <span class="sidebar-icon"></span>
                            <div class="sidebar-item-content">
                                <span class="sidebar-item-title">ConfigurationRestaurant</span>
                                <span class="sidebar-item-sub">Identité,IFU, Logo &amp; DGI</span>
                            </div>
                        </button>
                    </div>

                    <!-- Groupe 4 : Communication Directe -->
                    <div class="sidebar-group-label" style="margin-top: 0.6rem;">COMMUNICATIONDIRECTE</div>
                    <div class="sidebar-menu-list">
                        <button class="sidebar-nav-item" id="admTabBtnChat" onclick="switchAdminTab('chat')">
                            <span class="sidebar-icon"></span>
                            <div class="sidebar-item-content">
                                <div style="display: flex; align-items: center; justify-content: space-between;">
                                    <span class="sidebar-item-title">SMS &amp;Appel</span>
                                    <span id="admChatBadge" class="badge-unread hidden" style="background: #ef4444; color: white; border-radius: 9999px; font-size: 0.7rem; font-weight: 800; padding: 2px 7px; margin-left: 6px;">0</span>
                                </div>
                                <span class="sidebar-item-sub">Messages,Vocaux &amp; Appels</span>
                            </div>
                        </button>
                    </div>



                    <!-- Bas de Sidebar : Profil Admin & Déconnexion -->
                    <div class="sidebar-bottom-box">
                        <div class="sidebar-user-card">
                            <span style="font-size: 1.4rem;"></span>
                            <div style="flex: 1; line-height: 1.2;">
                                <div style="font-size: 0.85rem; font-weight: 700; color: #fbbf24;">Administrateur</div>
                                <div style="font-size: 0.72rem; color: var(--text-muted);">LePatron • DGI Conforme</div>
                            </div>
                        </div>
                        <button class="btn btn-secondary" onclick="logout()" style="width: 100%; justify-content: center; font-size: 0.82rem; padding: 0.55rem;">
                             Déconnexion
                        </button>
                    </div>
                </aside>

                <!-- ZONE CENTRALE DE CONTENU À DROITE DE LA SIDEBAR -->
                <main class="admin-main-area">
                    <!-- SECTION 1 : GESTION RESTAURANT (TABLEAU DE BORD CENTRAL) -->
                    <div id="admSectionOverview">
                        <!-- BANNIÈRE CAPSULE SUPÉRIEURE (MODÈLE DE L'IMAGE - COULEURS DU LOGICIEL) -->
                        <div style="background: linear-gradient(135deg, #07224e 0%, #1e3a8a 55%, #0f172a 100%); border-radius: 9999px; padding: 1.1rem 2.2rem; display: flex; align-items: center; justify-content: space-between; border: 2px solid #f59e0b; box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.45); color: #ffffff; margin-bottom: 1.5rem; flex-wrap: wrap; gap: 1rem;">
                            <div style="display: flex; align-items: center; gap: 1rem;">
                                <div style="width: 44px; height: 44px; border-radius: 50%; background: #ffffff; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 10px rgba(0,0,0,0.25);">
                                    <span style="color: #1e3a8a; font-size: 1.3rem;">🍽️</span>
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
                                    <span>📊 RESTAURANT MANAGEMENT</span>
                                </div>
                            </div>
                        </div>

                        <!-- CHIFFRES CLÉS & TOTAUX DU LOGICIEL (EFFECTIF, MASSE SALARIALE / VENTES) -->
                        <div style="display: flex; gap: 3.5rem; margin-left: 0.5rem; margin-bottom: 1.5rem; flex-wrap: wrap;">
                            <div>
                                <div style="font-size: 0.82rem; font-weight: 700; color: #94a3b8; margin-bottom: 4px;">Chiffre d'Affaires Global</div>
                                <div id="admOverviewGlobalRev" style="font-size: 1.55rem; font-weight: 900; color: #fbbf24;">1 748 330 FCFA</div>
                                <div style="font-size: 0.75rem; color: #38bdf8; font-weight: 700;">(Caisse POS + Grands Marchés)</div>
                            </div>
                            <div>
                                <div style="font-size: 0.82rem; font-weight: 700; color: #94a3b8; margin-bottom: 4px;">Recettes Caisse POS</div>
                                <div id="admStatRevenue" style="font-size: 1.55rem; font-weight: 900; color: #ffffff;">79 810 FCFA</div>
                                <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 600;">(14 tickets de caisse)</div>
                            </div>
                            <div>
                                <div style="font-size: 0.82rem; font-weight: 700; color: #94a3b8; margin-bottom: 4px;">Factures Grands Marchés DGI</div>
                                <div id="admOverviewGmRev" style="font-size: 1.55rem; font-weight: 900; color: #ffffff;">1 668 520 FCFA</div>
                                <div style="font-size: 0.75rem; color: #34d399; font-weight: 700;">(3 factures 100% homologuées)</div>
                            </div>
                            <div>
                                <div style="font-size: 0.82rem; font-weight: 700; color: #94a3b8; margin-bottom: 4px;">Panier Moyen Client</div>
                                <div id="admOverviewAvgBasket" style="font-size: 1.55rem; font-weight: 900; color: #ffffff;">5 700 FCFA</div>
                                <div style="font-size: 0.75rem; color: #f59e0b; font-weight: 700;">(Moyenne par commande)</div>
                            </div>
                            <div>
                                <div style="font-size: 0.82rem; font-weight: 700; color: #94a3b8; margin-bottom: 4px;">Gérants Actifs</div>
                                <div id="admStatManagers" style="font-size: 1.55rem; font-weight: 900; color: #ffffff;">3</div>
                                <div style="font-size: 0.75rem; color: #10b981; font-weight: 700;">(Comptes en service)</div>
                            </div>
                        </div>

                        <!-- GRILLE ANALYTIQUE 2x3 : LES 6 CARTES DU MODÈLE DE L'IMAGE -->
                        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.25rem; margin-bottom: 2rem;">
                            <!-- Carte 1 : Répartition par Catégorie -->
                            <div style="background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 12px; padding: 14px; box-shadow: 0 2px 8px rgba(15,23,42,0.06); display: flex; flex-direction: column;">
                                <div style="font-size: 0.9rem; font-weight: 800; color: #07224e; margin-bottom: 6px;">Répartition par type de produit</div>
                                <svg viewBox="0 0 340 185" style="width: 100%; height: auto; max-height: 185px;">
                                    <line x1="46" y1="151.0" x2="326" y2="151.0" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3 3"/>
                                    <text x="40" y="154.0" text-anchor="end" font-size="8.5" font-weight="600" fill="#94a3b8">0</text>
                                    <line x1="46" y1="87.5" x2="326" y2="87.5" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3 3"/>
                                    <text x="40" y="90.5" text-anchor="end" font-size="8.5" font-weight="600" fill="#94a3b8">38k</text>
                                    <line x1="46" y1="24.0" x2="326" y2="24.0" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3 3"/>
                                    <text x="40" y="27.0" text-anchor="end" font-size="8.5" font-weight="600" fill="#94a3b8">76k</text>
                                    <line x1="46" y1="151.0" x2="326" y2="151.0" stroke="#cbd5e1" stroke-width="1.5"/>
                                    <rect x="73.0" y="44.0" width="40.0" height="107.0" rx="4" fill="#2563eb"/>
                                    <text x="93.0" y="39.0" text-anchor="middle" font-size="9" font-weight="800" fill="#2563eb">64k F</text>
                                    <text x="93.0" y="165.0" text-anchor="middle" font-size="9" font-weight="700" fill="#334155">Boissons</text>
                                    <rect x="166.0" y="133.0" width="40.0" height="18.0" rx="4" fill="#f59e0b"/>
                                    <text x="186.0" y="128.0" text-anchor="middle" font-size="9" font-weight="800" fill="#f59e0b">10k F</text>
                                    <text x="186.0" y="165.0" text-anchor="middle" font-size="9" font-weight="700" fill="#334155">Desserts</text>
                                    <rect x="259.0" y="143.0" width="40.0" height="8.0" rx="4" fill="#38bdf8"/>
                                    <text x="279.0" y="138.0" text-anchor="middle" font-size="9" font-weight="800" fill="#38bdf8">4k F</text>
                                    <text x="279.0" y="165.0" text-anchor="middle" font-size="9" font-weight="700" fill="#334155">Plats</text>
                                    <text x="170" y="180" text-anchor="middle" font-size="8.5" font-weight="600" fill="#94a3b8">Catégories de vente</text>
                                </svg>
                            </div>

                            <!-- Carte 2 : Canal de Vente Donut -->
                            <div style="background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 12px; padding: 14px; box-shadow: 0 2px 8px rgba(15,23,42,0.06); display: flex; flex-direction: column;">
                                <div style="font-size: 0.9rem; font-weight: 800; color: #07224e; margin-bottom: 6px;">Répartition par canal de vente</div>
                                <svg viewBox="0 0 340 170" style="width: 100%; height: auto; max-height: 170px;">
                                    <path d="M 90.00 30.00 A 55 55 0 1 1 74.52 32.22 L 80.43 51.55 A 34 34 0 1 0 90.00 51.00 Z" fill="#07224e"/>
                                    <path d="M 74.52 32.22 A 55 55 0 0 1 90.00 30.00 L 90.00 51.00 A 34 34 0 0 0 80.43 51.55 Z" fill="#f59e0b"/>
                                    <circle cx="90" cy="85" r="33.5" fill="#ffffff"/>
                                    <text x="90" y="87" text-anchor="middle" font-size="13" font-weight="900" fill="#07224e">1748k F</text>
                                    <text x="90" y="99" text-anchor="middle" font-size="8.5" font-weight="700" fill="#64748b">Total CA</text>
                                    <g transform="translate(175, 42)">
                                        <circle cx="8" cy="10" r="6" fill="#07224e"/>
                                        <text x="20" y="14" font-size="10.5" font-weight="800" fill="#0f172a">Grands Marchés</text>
                                        <text x="20" y="27" font-size="10" font-weight="600" fill="#64748b">95.4%</text>
                                        <circle cx="8" cy="50" r="6" fill="#f59e0b"/>
                                        <text x="20" y="54" font-size="10.5" font-weight="800" fill="#0f172a">Caisse POS</text>
                                        <text x="20" y="67" font-size="10" font-weight="600" fill="#64748b">4.6%</text>
                                    </g>
                                </svg>
                            </div>

                            <!-- Carte 3 : Performance Gérants -->
                            <div style="background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 12px; padding: 14px; box-shadow: 0 2px 8px rgba(15,23,42,0.06); display: flex; flex-direction: column;">
                                <div style="font-size: 0.9rem; font-weight: 800; color: #07224e; margin-bottom: 6px;">Chiffre d'affaires par gérant</div>
                                <svg viewBox="0 0 340 185" style="width: 100%; height: auto; max-height: 185px;">
                                    <line x1="46" y1="151.0" x2="326" y2="151.0" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3 3"/>
                                    <text x="40" y="154.0" text-anchor="end" font-size="8.5" font-weight="600" fill="#94a3b8">0</text>
                                    <line x1="46" y1="87.5" x2="326" y2="87.5" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3 3"/>
                                    <text x="40" y="90.5" text-anchor="end" font-size="8.5" font-weight="600" fill="#94a3b8">37k</text>
                                    <line x1="46" y1="24.0" x2="326" y2="24.0" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3 3"/>
                                    <text x="40" y="27.0" text-anchor="end" font-size="8.5" font-weight="600" fill="#94a3b8">74k</text>
                                    <line x1="46" y1="151.0" x2="326" y2="151.0" stroke="#cbd5e1" stroke-width="1.5"/>
                                    <rect x="73.0" y="44.0" width="40.0" height="107.0" rx="4" fill="#1e3a8a"/>
                                    <text x="93.0" y="39.0" text-anchor="middle" font-size="9" font-weight="800" fill="#1e3a8a">62k F</text>
                                    <text x="93.0" y="165.0" text-anchor="middle" font-size="9" font-weight="700" fill="#334155">HAMRAM</text>
                                    <rect x="166.0" y="122.0" width="40.0" height="29.0" rx="4" fill="#2563eb"/>
                                    <text x="186.0" y="117.0" text-anchor="middle" font-size="9" font-weight="800" fill="#2563eb">17k F</text>
                                    <text x="186.0" y="165.0" text-anchor="middle" font-size="9" font-weight="700" fill="#334155">Fabrice</text>
                                    <rect x="259.0" y="123.0" width="40.0" height="28.0" rx="4" fill="#f59e0b"/>
                                    <text x="279.0" y="118.0" text-anchor="middle" font-size="9" font-weight="800" fill="#f59e0b">16k F</text>
                                    <text x="279.0" y="165.0" text-anchor="middle" font-size="9" font-weight="700" fill="#334155">DAMA</text>
                                    <text x="170" y="180" text-anchor="middle" font-size="8.5" font-weight="600" fill="#94a3b8">Gérants de caisse</text>
                                </svg>
                            </div>

                            <!-- Carte 4 : Conformité DGI Donut -->
                            <div style="background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 12px; padding: 14px; box-shadow: 0 2px 8px rgba(15,23,42,0.06); display: flex; flex-direction: column;">
                                <div style="font-size: 0.9rem; font-weight: 800; color: #07224e; margin-bottom: 6px;">Statut de conformité fiscale DGI</div>
                                <svg viewBox="0 0 340 170" style="width: 100%; height: auto; max-height: 170px;">
                                    <path d="M 90.00 30.00 A 55 55 0 1 1 89.04 30.01 L 89.41 51.01 A 34 34 0 1 0 90.00 51.00 Z" fill="#059669"/>
                                    <circle cx="90" cy="85" r="33.5" fill="#ffffff"/>
                                    <text x="90" y="87" text-anchor="middle" font-size="13" font-weight="900" fill="#07224e">100%</text>
                                    <text x="90" y="99" text-anchor="middle" font-size="8.5" font-weight="700" fill="#64748b">Conforme</text>
                                    <g transform="translate(175, 42)">
                                        <circle cx="8" cy="10" r="6" fill="#059669"/>
                                        <text x="20" y="14" font-size="10.5" font-weight="800" fill="#0f172a">Certifié e-MCF</text>
                                        <text x="20" y="27" font-size="10" font-weight="600" fill="#64748b">100.0%</text>
                                        <circle cx="8" cy="50" r="6" fill="#f59e0b"/>
                                        <text x="20" y="54" font-size="10.5" font-weight="800" fill="#0f172a">En attente</text>
                                        <text x="20" y="67" font-size="10" font-weight="600" fill="#64748b">0.0%</text>
                                    </g>
                                </svg>
                            </div>

                            <!-- Carte 5 : Évolution Croissance -> Pic -> Chute -->
                            <div style="background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 12px; padding: 14px; box-shadow: 0 2px 8px rgba(15,23,42,0.06); display: flex; flex-direction: column;">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                                    <div style="font-size: 0.9rem; font-weight: 800; color: #07224e;">Évolution : Croissance, Pic &amp; Chute</div>
                                    <span style="font-size: 0.72rem; font-weight: 800; color: #07224e; background: #e0f2fe; padding: 2px 8px; border-radius: 9999px;">Temps Réel</span>
                                </div>
                                <svg viewBox="0 0 340 185" style="width: 100%; height: auto; max-height: 185px;">
                                    <defs>
                                        <linearGradient id="curveGradientFastApi" x1="0" y1="0" x2="0" y2="1">
                                            <stop offset="0%" stop-color="#2563eb" stop-opacity="0.35"/>
                                            <stop offset="70%" stop-color="#f59e0b" stop-opacity="0.08"/>
                                            <stop offset="100%" stop-color="#ffffff" stop-opacity="0.0"/>
                                        </linearGradient>
                                    </defs>
                                    <line x1="46" y1="151.0" x2="326" y2="151.0" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3 3"/>
                                    <text x="40" y="154.0" text-anchor="end" font-size="8.5" font-weight="600" fill="#94a3b8">0</text>
                                    <line x1="46" y1="92.5" x2="326" y2="92.5" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3 3"/>
                                    <text x="40" y="95.5" text-anchor="end" font-size="8.5" font-weight="600" fill="#94a3b8">24k</text>
                                    <line x1="46" y1="34.0" x2="326" y2="34.0" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3 3"/>
                                    <text x="40" y="37.0" text-anchor="end" font-size="8.5" font-weight="600" fill="#94a3b8">48k</text>
                                    <line x1="46" y1="151.0" x2="326" y2="151.0" stroke="#cbd5e1" stroke-width="1.5"/>
                                    <path d="M 46.0 144.9 C 63.5 144.9, 63.5 129.3, 81.0 129.3 C 98.5 129.3, 98.5 106.3, 116.0 106.3 C 133.5 106.3, 133.5 67.0, 151.0 67.0 C 168.5 67.0, 168.5 121.5, 186.0 121.5 C 203.5 121.5, 203.5 142.6, 221.0 142.6 C 238.5 142.6, 238.5 147.3, 256.0 147.3 C 273.5 147.3, 273.5 91.8, 291.0 91.8 C 308.5 91.8, 308.5 149.3, 326.0 149.3 L 326.0 151.0 L 46.0 151.0 Z" fill="url(#curveGradientFastApi)"/>
                                    <path d="M 46.0 144.9 C 63.5 144.9, 63.5 129.3, 81.0 129.3 C 98.5 129.3, 98.5 106.3, 116.0 106.3 C 133.5 106.3, 133.5 67.0, 151.0 67.0 C 168.5 67.0, 168.5 121.5, 186.0 121.5 C 203.5 121.5, 203.5 142.6, 221.0 142.6 C 238.5 142.6, 238.5 147.3, 256.0 147.3 C 273.5 147.3, 273.5 91.8, 291.0 91.8 C 308.5 91.8, 308.5 149.3, 326.0 149.3" fill="none" stroke="#1e3a8a" stroke-width="3" stroke-linecap="round"/>
                                    <text x="46.0" y="164.0" text-anchor="middle" font-size="8" font-weight="600" fill="#475569">10h</text>
                                    <text x="81.0" y="164.0" text-anchor="middle" font-size="8" font-weight="600" fill="#475569">11h</text>
                                    <text x="116.0" y="164.0" text-anchor="middle" font-size="8" font-weight="600" fill="#475569">12h</text>
                                    <text x="151.0" y="164.0" text-anchor="middle" font-size="8" font-weight="600" fill="#475569">13h</text>
                                    <text x="186.0" y="164.0" text-anchor="middle" font-size="8" font-weight="600" fill="#475569">14h</text>
                                    <text x="221.0" y="164.0" text-anchor="middle" font-size="8" font-weight="600" fill="#475569">15h</text>
                                    <text x="256.0" y="164.0" text-anchor="middle" font-size="8" font-weight="600" fill="#475569">16h</text>
                                    <text x="291.0" y="164.0" text-anchor="middle" font-size="8" font-weight="600" fill="#475569">17h</text>
                                    <text x="326.0" y="164.0" text-anchor="middle" font-size="8" font-weight="600" fill="#475569">18h</text>
                                    <rect x="51.0" y="117.0" width="60" height="14" rx="7" fill="#10b981"/>
                                    <text x="81.0" y="127.0" text-anchor="middle" font-size="7.5" font-weight="800" fill="#ffffff">↗ CROISSANCE</text>
                                    <circle cx="291.0" cy="91.8" r="5.5" fill="#f59e0b" stroke="#ffffff" stroke-width="2"/>
                                    <rect x="247.0" y="67.8" width="88" height="17" rx="8" fill="#07224e" stroke="#f59e0b" stroke-width="1.5"/>
                                    <text x="291.0" y="80.0" text-anchor="middle" font-size="8.5" font-weight="900" fill="#fbbf24">⭐ SOMMET 43k F</text>
                                    <circle cx="186.0" cy="121.5" r="4.5" fill="#2563eb" stroke="#ffffff" stroke-width="1.5"/>
                                    <rect x="192.0" y="113.5" width="52" height="14" rx="7" fill="#1e3a8a"/>
                                    <text x="218.0" y="124.0" text-anchor="middle" font-size="7.5" font-weight="800" fill="#ffffff">↘ CHUTE</text>
                                    <text x="170" y="180" text-anchor="middle" font-size="8.5" font-weight="600" fill="#94a3b8">Heures de service (10h - 18h)</text>
                                </svg>
                            </div>

                            <!-- Carte 6 : Top Articles -->
                            <div style="background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 12px; padding: 14px; box-shadow: 0 2px 8px rgba(15,23,42,0.06); display: flex; flex-direction: column;">
                                <div style="font-size: 0.9rem; font-weight: 800; color: #07224e; margin-bottom: 6px;">Top 4 des articles les plus vendus</div>
                                <svg viewBox="0 0 340 185" style="width: 100%; height: auto; max-height: 185px;">
                                    <line x1="46" y1="151.0" x2="326" y2="151.0" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3 3"/>
                                    <text x="40" y="154.0" text-anchor="end" font-size="8.5" font-weight="600" fill="#94a3b8">0</text>
                                    <line x1="46" y1="87.5" x2="326" y2="87.5" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3 3"/>
                                    <text x="40" y="90.5" text-anchor="end" font-size="8.5" font-weight="600" fill="#94a3b8">10</text>
                                    <line x1="46" y1="24.0" x2="326" y2="24.0" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3 3"/>
                                    <text x="40" y="27.0" text-anchor="end" font-size="8.5" font-weight="600" fill="#94a3b8">20</text>
                                    <line x1="46" y1="151.0" x2="326" y2="151.0" stroke="#cbd5e1" stroke-width="1.5"/>
                                    <rect x="61.0" y="43.0" width="40.0" height="108.0" rx="4" fill="#1e3a8a"/>
                                    <text x="81.0" y="38.0" text-anchor="middle" font-size="9" font-weight="800" fill="#1e3a8a">17 qté</text>
                                    <text x="81.0" y="165.0" text-anchor="middle" font-size="9" font-weight="700" fill="#334155">ANANAS</text>
                                    <rect x="131.0" y="43.0" width="40.0" height="108.0" rx="4" fill="#2563eb"/>
                                    <text x="151.0" y="38.0" text-anchor="middle" font-size="9" font-weight="800" fill="#2563eb">17 qté</text>
                                    <text x="151.0" y="165.0" text-anchor="middle" font-size="9" font-weight="700" fill="#334155">Zoom-koom</text>
                                    <rect x="201.0" y="62.0" width="40.0" height="89.0" rx="4" fill="#38bdf8"/>
                                    <text x="221.0" y="57.0" text-anchor="middle" font-size="9" font-weight="800" fill="#38bdf8">14 qté</text>
                                    <text x="221.0" y="165.0" text-anchor="middle" font-size="9" font-weight="700" fill="#334155">Babeda</text>
                                    <rect x="271.0" y="106.0" width="40.0" height="45.0" rx="4" fill="#f59e0b"/>
                                    <text x="291.0" y="101.0" text-anchor="middle" font-size="9" font-weight="800" fill="#f59e0b">7 qté</text>
                                    <text x="291.0" y="165.0" text-anchor="middle" font-size="9" font-weight="700" fill="#334155">citrons</text>
                                    <text x="170" y="180" text-anchor="middle" font-size="8.5" font-weight="600" fill="#94a3b8">Articles phares</text>
                                </svg>
                            </div>
                        </div>

                        <!-- BANDEAU D'ACCÈS RAPIDE PROÉMINENT : FACTURE DU JOUR & CERTIFICATION DGI -->
                        <div style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.18), rgba(16, 185, 129, 0.12)); border: 2px solid #f59e0b; border-radius: 14px; padding: 1.35rem 1.75rem; margin-bottom: 2rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1.25rem; box-shadow: 0 8px 24px rgba(245, 158, 11, 0.18);">
                            <div style="display: flex; align-items: center; gap: 1.25rem; flex: 1; min-width: 320px;">
                                <div style="font-size: 2.4rem; background: rgba(245, 158, 11, 0.22); width: 64px; height: 64px; border-radius: 14px; display: flex; align-items: center; justify-content: center; border: 1.5px solid rgba(245, 158, 11, 0.45); flex-shrink: 0;">
                                    
                                </div>
                                <div>
                                    <div style="font-size: 1.25rem; font-weight: 800; color: #fbbf24; display: flex; align-items: center; gap: 0.6rem; flex-wrap: wrap;">
                                        <span>Facturedu Jour &amp; Certification Fiscale DGI</span>
                                        <span class="badge" style="background: rgba(16, 185, 129, 0.25); color: #34d399; font-size: 0.78rem; font-weight: 800; border: 1px solid rgba(16, 185, 129, 0.4);">e-MCFAutomatique</span>
                                    </div>
                                    <p style="font-size: 0.88rem; color: #cbd5e1; margin-top: 0.35rem; line-height: 1.5;">
                                        Toutes les ventes des gérants sont automatiquement collectées, stockées et calculées selon les règles de la DGI (Base HT, TVA 18%, Total TTC). L'administrateur valide et certifie ici directement.
                                    </p>
                                </div>
                            </div>
                            <div style="display: flex; gap: 0.75rem; align-items: center;">
                                <button class="btn btn-primary" onclick="switchAdminTab('globalInvoices')" style="background: linear-gradient(135deg, #f59e0b, #d97706); color: #000; font-weight: 800; font-size: 0.95rem; padding: 0.85rem 1.6rem; box-shadow: 0 4px 15px rgba(245, 158, 11, 0.35); border-radius: 10px; cursor: pointer;">
                                     Ouvrir la Facture &amp; Certifier
                                </button>
                            </div>
                        </div>

                        <!-- Grille 2 colonnes : Identité Légale/Fiscale + État Opérationnel Odoo -->
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 1.5rem; margin-bottom: 2rem;">
                            <!-- Colonne 1 : Identité & Fiscalité de l'Établissement -->
                            <div class="content-panel" style="margin: 0;">
                                <div class="panel-header">
                                    <h3>Identité &amp; Fiscalité de l'Établissement</h3>
                                    <button class="btn btn-secondary" onclick="switchAdminTab('config')" style="font-size: 0.75rem;">Modifier </button>
                                </div>
                                <div style="font-size: 0.9rem; line-height: 1.8; color: var(--text-muted);">
                                    <div><strong>Nomde l'Établissement :</strong> <span id="overviewRestoName" style="color: white; font-weight: bold;">-</span></div>
                                    <div><strong>IFU(Identifiant Fiscal Unique) :</strong> <span id="overviewIfu" style="color: #38bdf8; font-family: monospace; font-weight: bold;">-</span></div>
                                    <div><strong>RCCM :</strong> <span id="overviewRccm" style="color: white;">-</span></div>
                                    <div><strong>RégimeFiscal :</strong> <span id="overviewTaxRegime" style="color: #fbbf24; font-weight: 600;">-</span></div>
                                    <div><strong>DivisionFiscale :</strong> <span id="overviewFiscalDivision" style="color: #a5b4fc; font-weight: 600;">-</span></div>
                                    <div><strong>NIM(Machine e-MCF) :</strong> <span id="overviewNim" style="color: #6ee7b7; font-family: monospace;">-</span></div>
                                    <div><strong>TauxTVA :</strong> <span id="overviewTaxRate" style="color: white;">18%</span></div>
                                    <div><strong>Adresse :</strong> <span id="overviewAddress" style="color: white;">-</span></div>
                                    <div><strong>Téléphone :</strong> <span id="overviewPhone" style="color: white;">-</span></div>
                                    <div><strong>EmailProfessionnel :</strong> <span id="overviewEmail" style="color: white;">-</span></div>
                                    <div style="margin-top: 0.5rem; padding-top: 0.4rem; border-top: 1px dashed var(--border); font-size: 0.8rem; color: #34d399; font-weight: 700;">
                                         Approbation DGI Active • Code QR toujours positionné en haut des factures
                                    </div>
                                </div>
                            </div>

                            <!-- Colonne 2 : Connectivité Odoo ERP & Moteur Central -->
                            <div class="content-panel" style="margin: 0;">
                                <div class="panel-header">
                                    <h3>Système Moteur &amp; Synchronisation ERP</h3>
                                    <span class="badge badge-success">Connecté</span>
                                </div>
                                <div style="font-size: 0.9rem; line-height: 1.8; color: var(--text-muted);">
                                    <div><strong>Basede Données Odoo :</strong> <span style="color: #38bdf8; font-family: monospace; font-weight: 700;">restaurant_odoo</span></div>
                                    <div><strong>PortOdoo Web &amp; POS :</strong> <span style="color: white; font-family: monospace;">8070</span></div>
                                    <div><strong>BackendFastAPI :</strong> <span style="color: white; font-family: monospace;">8000</span></div>
                                    <div><strong>Synchronisationd'Arrière-Plan :</strong> <span style="color: #34d399; font-weight: 600;">Automatique(toutes les 8s)</span></div>
                                    <div><strong>FacturationNormalisée :</strong> <span style="color: #fbbf24; font-weight: 600;">AgrégationDGI e-MCF</span></div>
                                    <div style="margin-top: 1.25rem; display: flex; gap: 0.6rem; flex-wrap: wrap;">
                                        <a href="http://localhost:8070/web?db=restaurant_odoo" target="_blank" class="btn btn-secondary" style="font-size: 0.8rem; text-decoration: none;">
                                             Ouvrir Odoo ERP
                                        </a>
                                        <button class="btn btn-secondary" onclick="switchAdminTab('globalInvoices')" style="font-size: 0.8rem;">
                                             Factures Globales DGI
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Suivi des Prises de Poste & Gérants en Direct -->
                        <div class="content-panel" style="margin-bottom: 0;">
                            <div class="panel-header">
                                <h3>Prises de Service &amp; Activités des Gérants en Direct</h3>
                                <button class="btn btn-secondary" onclick="loadSessionsData()" style="font-size: 0.75rem;">Rafraîchir les sessions</button>
                            </div>
                            <div style="overflow-x: auto;">
                                <table>
                                    <thead>
                                        <tr>
                                            <th>Gérant</th>
                                            <th>Identifiant</th>
                                            <th>Statutde Service</th>
                                            <th>Débutde Prise</th>
                                            <th>Finde Prise</th>
                                            <th>VentesEffectuées</th>
                                            <th>MontantEncaissé</th>
                                            <th>Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody id="sessionsTableBody">
                                        <tr><td colspan="8" style="text-align: center; color: var(--text-muted);">Chargementdes prises de service...</td></tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        <!-- Panneau des Dernières Factures & Encaissements Clients en Direct (Vue Exécutive) -->
                        <div class="content-panel" style="margin-top: 1.5rem; margin-bottom: 0;">
                            <div class="panel-header" style="flex-wrap: wrap; gap: 0.8rem;">
                                <div>
                                    <h3 style="display: flex; align-items: center; gap: 0.5rem; color: #fbbf24;">
                                        <span></span>Dernières Factures Clients &amp; Ventes Encaissées
                                    </h3>
                                    <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.25rem;">
                                        Flux des factures émises en direct par les gérants (Caisse Web ou Odoo POS).
                                    </p>
                                </div>
                                <div style="display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap;">
                                    <button class="btn btn-primary" onclick="switchAdminTab('invoices')" style="font-size: 0.78rem; background: linear-gradient(135deg, #f59e0b, #d97706); color: black; font-weight: 700;">
                                        Ouvrir Registre Complet 
                                    </button>
                                    <button class="btn btn-secondary" onclick="loadAdminOrdersData()" style="font-size: 0.78rem;">
                                         Rafraîchir
                                    </button>
                                </div>
                            </div>
                            <div style="overflow-x: auto;">
                                <table>
                                    <thead>
                                        <tr>
                                            <th>N°Facture</th>
                                            <th>Date &amp;Heure</th>
                                            <th>Gérant(Caisse)</th>
                                            <th>Paiement</th>
                                            <th>MontantTTC</th>
                                            <th>StatutDGI</th>
                                            <th style="text-align: center;">Action</th>
                                        </tr>
                                    </thead>
                                    <tbody id="overviewRecentOrdersTableBody">
                                        <tr><td colspan="7" style="text-align: center; color: var(--text-muted);">Chargementdes factures...</td></tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>

            <!-- SECTION DÉDIÉE : FACTURATION GLOBALE DYNAMIQUE & CERTIFICATION DGI -->
            <div id="admSectionGlobalInvoices" class="hidden">
                <!-- HERO CARD PRESTIGIEUX : FACTURE DU JOUR & CERTIFICATION FISCALE DGI (EXIGENCE ADMIN) -->
                <div id="heroDailyInvoiceCard" class="content-panel" style="border: 2px solid #10b981; background: linear-gradient(135deg, rgba(16, 185, 129, 0.14) 0%, rgba(15, 23, 42, 0.98) 100%); margin-bottom: 1.75rem; box-shadow: 0 12px 35px rgba(0,0,0,0.45); border-radius: 16px; position: relative;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; border-bottom: 1px solid rgba(16, 185, 129, 0.25); padding-bottom: 1.15rem; margin-bottom: 1.25rem;">
                        <div style="display: flex; align-items: center; gap: 1rem;">
                            <div style="width: 54px; height: 54px; border-radius: 14px; background: linear-gradient(135deg, #10b981, #059669); display: flex; align-items: center; justify-content: center; font-size: 1.85rem; box-shadow: 0 4px 18px rgba(16, 185, 129, 0.4);">
                                
                            </div>
                            <div>
                                <div style="display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap;">
                                    <h2 style="font-size: 1.45rem; font-weight: 800; color: #34d399; margin: 0; letter-spacing: -0.01em;">
                                        Facture du Jour &amp; Certification Fiscale DGI
                                    </h2>
                                    <span id="heroDailyStatusBadge" class="badge" style="background: rgba(245, 158, 11, 0.25); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.5); font-weight: 800; font-size: 0.82rem;">
                                         Prête pour certification
                                    </span>
                                    <span id="heroDailyNumberBadge" class="badge" style="background: rgba(59, 130, 246, 0.2); color: #93c5fd; font-family: monospace; font-weight: 700;">
                                        FACT-GLOB-DU-JOUR
                                    </span>
                                </div>
                                <p style="font-size: 0.88rem; color: #94a3b8; margin: 0.3rem 0 0 0;">
                                    Toutes les ventes des gérants s'additionnent et se calculent automatiquement selon les normes fiscales DGI. L'administrateur valide en un clic sans aucune erreur.
                                </p>
                            </div>
                        </div>
                        <div style="display: flex; gap: 0.75rem; align-items: center; flex-wrap: wrap;">
                            <button class="btn btn-secondary" onclick="openTodayGlobalInvoiceDetail()" style="font-weight: 700; padding: 0.7rem 1.35rem; border: 1.5px solid #38bdf8; color: #38bdf8; background: rgba(56, 189, 248, 0.12); display: flex; align-items: center; gap: 0.5rem; font-size: 0.92rem;" title="Consulter la facture complète avec toutes les ventes déjà calculées">
                                <span></span>Consulter la Facture du Jour
                            </button>
                            <button id="heroBtnCertifyToday" class="btn btn-primary" onclick="certifyTodayInvoiceDirectly()" style="background: linear-gradient(135deg, #10b981, #059669); font-weight: 800; padding: 0.75rem 1.6rem; font-size: 0.95rem; box-shadow: 0 4px 18px rgba(16, 185, 129, 0.45); display: flex; align-items: center; gap: 0.5rem;" title="Certifier immédiatement auprès de la DGI">
                                <span></span>Certifier la Facture du Jour (DGI)
                            </button>
                        </div>
                    </div>

                    <!-- BANDEAU DATE & GÉRANTS EN SERVICE (DATE SEULEMENT, AUCUNE HEURE) -->
                    <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 1.25rem; margin-bottom: 1.35rem; background: rgba(15, 23, 42, 0.7); padding: 1.15rem 1.35rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08);">
                        <div>
                            <div style="font-size: 0.74rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; color: #fbbf24; margin-bottom: 0.35rem;">
                                 Date de la Facture
                            </div>
                            <div id="heroDailyDateText" style="font-size: 1.2rem; font-weight: 800; color: #ffffff;">
                                -
                            </div>
                        </div>
                        <div>
                            <div style="font-size: 0.74rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; color: #93c5fd; margin-bottom: 0.35rem;">
                                 Gérant(s) ayant réalisé les ventes
                            </div>
                            <div id="heroDailyManagersText" style="font-size: 1.2rem; font-weight: 800; color: #60a5fa;">
                                -
                            </div>
                        </div>
                    </div>

                    <!-- GRILLE DES 4 GRANDS COMPTEURS FINANCIERS DGI DU JOUR -->
                    <div class="grid-stats" style="margin-bottom: 0;">
                        <div class="stat-card" style="border-left: 4px solid #10b981; background: rgba(16, 185, 129, 0.08);">
                            <div class="label" style="color: #a7f3d0;">Chiffred'Affaires Brut TTC</div>
                            <div id="heroDailyTotalTTC" class="value" style="color: #34d399; font-size: 1.75rem;">0FCFA</div>
                            <div style="font-size: 0.74rem; color: #a7f3d0; margin-top: 0.25rem;">Totaldes encaissements clients</div>
                        </div>
                        <div class="stat-card" style="border-left: 4px solid #3b82f6; background: rgba(59, 130, 246, 0.08);">
                            <div class="label" style="color: #bfdbfe;">BaseImposable Hors Taxes (HT)</div>
                            <div id="heroDailyTotalHT" class="value" style="color: #93c5fd; font-size: 1.75rem;">0FCFA</div>
                            <div style="font-size: 0.74rem; color: #bfdbfe; margin-top: 0.25rem;">Montantnet après règles DGI</div>
                        </div>
                        <div class="stat-card" style="border-left: 4px solid #f59e0b; background: rgba(245, 158, 11, 0.08);">
                            <div class="label" style="color: #fde68a;">TVADGI Collectée (18%)</div>
                            <div id="heroDailyTotalTVA" class="value" style="color: #fbbf24; font-size: 1.75rem;">0FCFA</div>
                            <div style="font-size: 0.74rem; color: #fde68a; margin-top: 0.25rem;">Taxescalculées et ventilées</div>
                        </div>
                        <div class="stat-card" style="border-left: 4px solid #8b5cf6; background: rgba(139, 92, 246, 0.08);">
                            <div class="label" style="color: #ddd6fe;">Nombrede Ventes du Jour</div>
                            <div id="heroDailySalesCount" class="value" style="color: #ffffff; font-size: 1.75rem;">0vente</div>
                            <div id="heroDailyFiscRefText" style="font-size: 0.74rem; color: #ddd6fe; margin-top: 0.25rem;">Enattente de certification DGI</div>
                        </div>
                    </div>
                </div>

                <!-- PANNEAU SUPÉRIEUR ET EN-TÊTE D'AGRÉGATION -->
                <div class="content-panel" style="border: 2px solid #f59e0b; background: linear-gradient(180deg, rgba(245, 158, 11, 0.12) 0%, rgba(19, 27, 46, 0.98) 100%);">
                    <div class="panel-header" style="flex-wrap: wrap; gap: 1rem;">
                        <div>
                            <div style="display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap;">
                                <h3 style="color: #fbbf24; font-size: 1.4rem; display: flex; align-items: center; gap: 0.5rem;">
                                    <span></span>Factures Globales &amp; Agrégation Dynamique des Ventes (DGI)
                                </h3>
                                <span id="globBillingLiveBadge" class="badge" style="background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); padding: 0.35rem 0.75rem; font-size: 0.8rem;">
                                     Synchronisation temps réel active
                                </span>
                            </div>
                            <p style="font-size: 0.88rem; color: var(--text-muted); margin-top: 0.4rem; max-width: 900px; line-height: 1.5;">
                                Les ventes réalisées par tous les gérants sont <strong>automatiquementcollectées, agrégées et calculées</strong>selon les règles fiscales DGI configurées. La facture globale reste en brouillon/en cours et se met à jour en continu jusqu'à votre certification officielle.
                            </p>
                        </div>
                        <div style="display: flex; gap: 0.6rem; align-items: center; flex-wrap: wrap;">
                            <button class="btn btn-secondary" onclick="openBillingConfigModal()" title="Paramétrer la période de facturation (quotidienne, hebdomadaire, mensuelle)">
                                 Période : <span id="currentBillingFreqLabel" style="color: #fbbf24; font-weight: bold; margin-left: 4px;">Quotidienne</span>
                            </button>
                            <button class="btn btn-secondary" onclick="openTaxRulesModal()" style="border-color: #6366f1; color: #a5b4fc;">
                                 Règles Fiscales DGI
                            </button>
                            <button class="btn btn-primary" onclick="generateNewGlobalInvoice()" style="background: linear-gradient(135deg, #f59e0b, #d97706); color: black; font-weight: 700;">
                                 Facture Période en Cours
                            </button>
                            <button class="btn btn-secondary" onclick="loadGlobalInvoicesData()" title="Actualiser manuellement">
                                 Actualiser
                            </button>
                        </div>
                    </div>

                    <!-- GRILLE DES KPIS FINANCIERS GLOBAUX CUMULÉS -->
                    <div class="grid-stats" style="margin-top: 1.25rem; margin-bottom: 0;">
                        <div class="stat-card" style="border-left: 4px solid #10b981; background: rgba(16, 185, 129, 0.05);">
                            <div class="label">Chiffred'Affaires Global (TTC)</div>
                            <div id="globKpiRevenueTTC" class="value" style="color: #34d399;">0FCFA</div>
                            <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.25rem;">Montanttotal brut encaissé</div>
                        </div>
                        <div class="stat-card" style="border-left: 4px solid #3b82f6; background: rgba(59, 130, 246, 0.05);">
                            <div class="label">BaseImposable Hors Taxes (HT)</div>
                            <div id="globKpiBaseHT" class="value" style="color: #93c5fd;">0FCFA</div>
                            <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.25rem;">Montantnet après règles fiscales</div>
                        </div>
                        <div class="stat-card" style="border-left: 4px solid #f59e0b; background: rgba(245, 158, 11, 0.05);">
                            <div class="label">TVA &amp;Taxes DGI Cumulées</div>
                            <div id="globKpiTotalTaxes" class="value" style="color: #fbbf24;">0FCFA</div>
                            <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.25rem;">Taxescalculées automatiquement</div>
                        </div>
                        <div class="stat-card" style="border-left: 4px solid #8b5cf6;">
                            <div class="label">FacturesGlobales Émises</div>
                            <div id="globKpiInvoicesCount" class="value" style="color: white;">0</div>
                            <div id="globKpiInvoicesStatusBreakdown" style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.25rem;">0certifiées • 0 en cours</div>
                        </div>
                    </div>
                </div>

                <!-- TABLEAU DE BORD DU REGISTRE DES FACTURES GLOBALES (Exigence 2) -->
                <div class="content-panel">
                    <div class="panel-header" style="flex-wrap: wrap; gap: 1rem;">
                        <div>
                            <h3 style="display: flex; align-items: center; gap: 0.5rem;">
                                <span></span>Registre Officiel des Factures Globales
                            </h3>
                            <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.25rem;">
                                Chaque facture globale regroupe automatiquement l'ensemble des ventes des gérants pour sa période.
                            </p>
                        </div>
                        
                        <!-- FILTRES & RECHERCHE (Exigences 2 & 8) -->
                        <div style="display: flex; gap: 0.6rem; align-items: center; flex-wrap: wrap;">
                            <select id="globFilterStatus" class="form-control" style="width: auto; padding: 0.5rem 0.8rem;" onchange="filterGlobalInvoicesTable()">
                                <option value="">Tousles statuts</option>
                                <option value="ready_for_certification">Prête pour certification</option>
                                <option value="in_progress">En cours</option>
                                <option value="draft">Brouillon</option>
                                <option value="certified">Certifiée</option>
                                <option value="cancelled">Annulée</option>
                            </select>
                            <select id="globFilterPeriod" class="form-control" style="width: auto; padding: 0.5rem 0.8rem;" onchange="filterGlobalInvoicesTable()">
                                <option value="">Toutesles fréquences</option>
                                <option value="daily">Quotidienne (Jour)</option>
                                <option value="weekly">Hebdomadaire (Semaine)</option>
                                <option value="monthly">Mensuelle (Mois)</option>
                            </select>
                            <input id="globSearchInput" type="text" placeholder="Rechercher N°, période, admin..." class="form-control" style="width: 220px; padding: 0.5rem 0.8rem;" oninput="filterGlobalInvoicesTable()" />
                        </div>
                    </div>

                    <!-- TABLEAU PRINCIPAL DES FACTURES GLOBALES (EXIGENCE 2) -->
                    <div style="overflow-x: auto;">
                        <table>
                            <thead>
                                <tr>
                                    <th>N°Facture</th>
                                    <th>GérantConnecté</th>
                                    <th>Date</th>
                                    <th>Période /Date</th>
                                    <th style="text-align: center;">NbVentes</th>
                                    <th style="text-align: right;">TotalHT</th>
                                    <th style="text-align: right;">TaxesDGI (18%)</th>
                                    <th style="text-align: right;">TotalBrut TTC</th>
                                    <th>Statut</th>
                                    <th>RéfFiscale DGI</th>
                                    <th style="text-align: center;">Actions</th>
                                </tr>
                            </thead>
                            <tbody id="globalInvoicesTableBody">
                                <tr>
                                    <td colspan="11" style="text-align: center; color: var(--text-muted); padding: 2rem;">
                                        Chargement des factures globales...
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- SECTION 2 : FACTURES & VENTES EN DIRECT (CALCUL & CUMUL EN TEMPS RÉEL) -->
            <div id="admSectionInvoices" class="hidden">
                <!-- BANNIÈRE FINANCIÈRE DE CALCUL ACCUMULATIF EN DIRECT -->
                <div class="content-panel" style="border: 2px solid #f59e0b; background: linear-gradient(180deg, rgba(245, 158, 11, 0.08) 0%, rgba(19, 27, 46, 0.95) 100%);">
                    <div class="panel-header" style="flex-wrap: wrap; gap: 1rem;">
                        <div>
                            <h3 style="display: flex; align-items: center; gap: 0.6rem; color: #fbbf24;">
                                <span></span>Totaux Financiers Cumulés en Direct (Temps Réel)
                            </h3>
                            <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.25rem;">
                                Les montants de toutes les factures s'additionnent et se calculent au fur et à mesure que les gérants valident des encaissements.
                            </p>
                        </div>
                        <button class="btn btn-primary" onclick="loadAdminOrdersData()" style="background: linear-gradient(135deg, #f59e0b, #d97706); color: black; font-weight: 700;">
                             Actualiser les Factures
                        </button>
                    </div>

                    <div class="grid-stats" style="margin-bottom: 0;">
                        <div class="stat-card" style="border-left: 4px solid #10b981;">
                            <div class="label">TotalTTC Encaissé (Chiffre d'Affaires)</div>
                            <div id="admInvAccumulatedTTC" class="value" style="color: #34d399;">0FCFA</div>
                        </div>
                        <div class="stat-card">
                            <div class="label">BaseImposable Hors Taxes (HT)</div>
                            <div id="admInvAccumulatedHT" class="value" style="color: #93c5fd;">0FCFA</div>
                        </div>
                        <div class="stat-card" style="border-left: 4px solid #f59e0b;">
                            <div class="label">TVADGI Collectée (18%)</div>
                            <div id="admInvAccumulatedTVA" class="value" style="color: #fbbf24;">0FCFA</div>
                        </div>
                        <div class="stat-card">
                            <div class="label">TotalFactures Émises</div>
                            <div id="admInvAccumulatedCount" class="value" style="color: white;">0</div>
                        </div>
                        <div class="stat-card">
                            <div class="label">MonnaieTotale Rendue</div>
                            <div id="admInvAccumulatedChange" class="value" style="color: #f87171;">0FCFA</div>
                        </div>
                    </div>
                </div>

                <!-- TABLE DES FACTURES CENTRALISÉES AVEC VISUALISATION OFFICIELLE -->
                <div class="content-panel">
                    <div class="panel-header" style="flex-wrap: wrap; gap: 1rem;">
                        <div>
                            <h3>Registre Centralisé des Factures Clients</h3>
                            <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.25rem;">
                                Cliquez sur <strong>«Facture Officielle »</strong>sur n'importe quelle ligne pour ouvrir, visualiser et imprimer la facture conforme au modèle chic élégant.
                            </p>
                        </div>
                        <div style="display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap;">
                            <input id="admInvoiceSearch" type="text" placeholder="Rechercher (n°, gérant, date...)" class="form-control" style="width: 240px; padding: 0.5rem 0.8rem;" oninput="filterAdminInvoicesTable()" />
                        </div>
                    </div>

                    <table>
                        <thead>
                            <tr>
                                <th>N°Facture</th>
                                <th>Date</th>
                                <th>Gérant(Caisse)</th>
                                <th>ModeRèglement</th>
                                <th>BaseHT</th>
                                <th>TVA18%</th>
                                <th>TotalTTC</th>
                                <th>CertificationDGI</th>
                                <th>ActionFacture</th>
                            </tr>
                        </thead>
                        <tbody id="adminOrdersTableBody">
                            <tr><td colspan="9" style="text-align: center; color: var(--text-muted);">Chargementdes factures...</td></tr>
                        </tbody>
                    </table>
                </div>

                <!-- PANEL : BILAN JOURNALIER & CERTIFICATION DGI -->
                <div class="content-panel" style="border: 2px solid #6366f1;">
                    <div class="panel-header" style="flex-wrap: wrap; gap: 1rem;">
                        <div>
                            <h3 style="display: flex; align-items: center; gap: 0.5rem;">
                                <span></span>Facture Générale de la Journée &amp; Certification Fiscale DGI
                            </h3>
                            <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.25rem;">
                                Bilan récapitulatif fiscal journalier conforme e-MCF. L'administrateur peut certifier et sceller fiscalement les ventes auprès de la Direction Générale des Impôts.
                            </p>
                        </div>
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            <input id="reportDateInput" type="date" class="form-control" style="width: auto; padding: 0.4rem 0.8rem;" onchange="loadDailyReportData()" />
                            <button class="btn btn-secondary" onclick="loadDailyReportData()">Consulterla Date</button>
                        </div>
                    </div>

                    <!-- Statut de la Certification DGI -->
                    <div id="dgiStatusBanner" style="padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                    </div>

                    <!-- Grille Totaux Fiscaux de la Journée -->
                    <div class="grid-stats" style="margin-bottom: 1.5rem;">
                        <div class="stat-card" style="border-left: 4px solid #10b981;">
                            <div class="label">TotalBrut de la Journée (TTC)</div>
                            <div id="reportTotalTTC" class="value" style="color: #34d399;">-FCFA</div>
                        </div>
                        <div class="stat-card">
                            <div class="label">BaseImposable Hors Taxes (HT)</div>
                            <div id="reportTotalHT" class="value">-FCFA</div>
                        </div>
                        <div class="stat-card" style="border-left: 4px solid #f59e0b;">
                            <div class="label">TVADGI (18%)</div>
                            <div id="reportTotalTVA" class="value" style="color: #fbbf24;">-FCFA</div>
                        </div>
                        <div class="stat-card">
                            <div class="label">NombreTotal de Commandes</div>
                            <div id="reportTotalOrders" class="value">-</div>
                        </div>
                    </div>

                    <!-- Répartitions Modes de Paiement & Gérants -->
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem; margin-bottom: 1.5rem;">
                        <div style="background: var(--bg); border: 1px solid var(--border); border-radius: 12px; padding: 1.25rem;">
                            <h4 style="font-size: 0.95rem; margin-bottom: 1rem; color: #a5b4fc;">Répartition par Mode de Paiement</h4>
                            <div id="reportPaymentList" style="display: flex; flex-direction: column; gap: 0.75rem;"></div>
                        </div>
                        <div style="background: var(--bg); border: 1px solid var(--border); border-radius: 12px; padding: 1.25rem;">
                            <h4 style="font-size: 0.95rem; margin-bottom: 1rem; color: #a5b4fc;">Ventes par Gérant de la Journée</h4>
                            <div id="reportManagerList" style="display: flex; flex-direction: column; gap: 0.75rem;"></div>
                        </div>
                    </div>

                    <!-- Actions -->
                    <div style="display: flex; gap: 1rem; flex-wrap: wrap; align-items: center; justify-content: flex-end; padding-top: 1rem; border-top: 1px solid var(--border);">
                        <button id="btnCertifyDGI" class="btn btn-primary" onclick="handleCertifyDGI()" style="background: linear-gradient(135deg, #4f46e5, #06b6d4); font-size: 0.95rem; padding: 0.75rem 1.5rem;">
                             Certifier la Journée avec la DGI
                        </button>
                        <button class="btn btn-secondary" onclick="printDailyInvoiceModal()" style="font-size: 0.95rem; padding: 0.75rem 1.5rem;">
                             Imprimer la Facture Normalisée DGI
                        </button>
                    </div>
                </div>
            </div>

            <!-- SECTION 3 : GESTION DES GÉRANTS & TRAÇABILITÉ -->
            <div id="admSectionManagers" class="hidden">
                <!-- Panel: Créer un gérant -->
                <div class="content-panel">
                    <div class="panel-header">
                        <h3>Créer un Compte Gérant Dédié</h3>
                    </div>
                    <form id="createManagerForm" onsubmit="handleCreateManager(event)" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; align-items: flex-end;">
                        <div class="form-group" style="margin: 0;">
                            <label>Nomcomplet du Gérant</label>
                            <input id="mgrFullName" class="form-control" type="text" placeholder="ex: Jean Dupont" required />
                        </div>
                        <div class="form-group" style="margin: 0;">
                            <label>Nomd'utilisateur (Login)</label>
                            <input id="mgrUsername" class="form-control" type="text" placeholder="ex: gerant_jean" required />
                        </div>
                        <div class="form-group" style="margin: 0;">
                            <label>AdresseEmail</label>
                            <input id="mgrEmail" class="form-control" type="email" placeholder="ex: jean@restaurant.com" required />
                        </div>
                        <div class="form-group" style="margin: 0;">
                            <label>Motde passe dédié au Gérant</label>
                            <input id="mgrPassword" class="form-control" type="password" placeholder="Mot de passe distinct" required />
                        </div>
                        <div>
                            <button type="submit" class="btn btn-primary" style="height: 44px; width: 100%; justify-content: center;">
                                Créer le Gérant
                            </button>
                        </div>
                    </form>
                    <div id="mgrMsg" style="margin-top: 1rem; font-size: 0.875rem;"></div>
                </div>

                <!-- Panel: Liste des gérants -->
                <div class="content-panel">
                    <div class="panel-header">
                        <h3>Traitement &amp; Suivi des Gérants (Présence en Ligne &amp; Horaires)</h3>
                        <button class="btn btn-secondary" onclick="loadAdminData()">Rafraîchirles Gérants</button>
                    </div>
                    <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem;">
                        Gestion exclusive des gérants habilités : nom du gérant, identifiant de connexion et montant cumulé vendu en FCFA. L'administrateur peut désactiver ou supprimer un compte à tout moment.
                    </p>
                    <table>
                        <thead>
                            <tr>
                                <th>Nom du Gérant</th>
                                <th>Identifiant (Login)</th>
                                <th>Montant Vendu (FCFA)</th>
                                <th>Compte Actif</th>
                                <th style="text-align: right;">Actions</th>
                            </tr>
                        </thead>
                        <tbody id="managersTableBody">
                            <tr><td colspan="5" style="text-align: center; color: var(--text-muted);">Chargement des gérants...</td></tr>
                        </tbody>
                    </table>
                </div>

                <!-- Panel: Traçabilité des Sessions & Heures des Gérants -->
                <div class="content-panel">
                    <div class="panel-header">
                        <h3>Traçabilité des Prises de Poste, Horaires &amp; Argent Encaissé par Gérant</h3>
                        <button class="btn btn-secondary" onclick="loadSessionsData()">Rafraîchirles Sessions</button>
                    </div>
                    <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem;">
                        Traçabilité complète de chaque gérant : date et heure exacte de connexion (prise de service), date et heure de déconnexion (fin de service), montant total des ventes et argent liquide/monnaie encaissé.
                    </p>
                    <table>
                        <thead>
                            <tr>
                                <th>Gérant(Nom &amp; Login)</th>
                                <th>Statuten Direct</th>
                                <th>Prisede Service (Connexion)</th>
                                <th>Finde Service (Déconnexion)</th>
                                <th>NbVentes</th>
                                <th>TotalVentes (FCFA)</th>
                                <th>ArgentEncaissé</th>
                                <th>MonnaieRendue</th>
                            </tr>
                        </thead>
                        <tbody id="sessionsTableBody">
                            <tr><td colspan="8" style="text-align: center; color: var(--text-muted);">Chargementdes sessions...</td></tr>
                        </tbody>
                    </table>
                </div>

                <!-- Panel: Journal en Temps Réel des Faits et Gestes des Gérants -->
                <div class="content-panel" style="border-left: 4px solid #38bdf8;">
                    <div class="panel-header">
                        <h3>Journal en Temps Réel des Faits &amp; Gestes des Gérants (Audit &amp; Traçabilité)</h3>
                        <button class="btn btn-secondary" onclick="loadActivityLogsData()">Rafraîchirle Journal</button>
                    </div>
                    <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem;">
                        Toutes les actions et faits et gestes des gérants sont stockés et mentionnés ici sans aucune erreur : connexion, encaissement de commande, montants en FCFA, monnaie rendue, ajustements et déconnexion.
                    </p>
                    <table>
                        <thead>
                            <tr>
                                <th>Date &amp;Heure</th>
                                <th>Gérant</th>
                                <th>ActionRéalisée</th>
                                <th>Détails &amp;Montants en Jeu</th>
                            </tr>
                        </thead>
                        <tbody id="activityLogsTableBody">
                            <tr><td colspan="4" style="text-align: center; color: var(--text-muted);">Chargementdu journal d'activité...</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- SECTION 4 : CHARGEMENT DES PRODUITS / PLATS -->
            <div id="admSectionMenu" class="hidden">
                <div class="content-panel">
                    <div class="panel-header">
                        <h3>Chargement des Produits &amp; Plats du Restaurant (Tarification FCFA)</h3>
                        <button class="btn btn-secondary" onclick="loadAdminDishesData()">Rafraîchirles Plats</button>
                    </div>
                    <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1.25rem;">
                        L'administrateur charge les produits disponibles avec leurs prix. Ces produits apparaissent instantanément chez le gérant, classés par catégories sous forme de cartes tactiles.
                    </p>
                    <form id="createDishForm" onsubmit="handleCreateDish(event)" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; align-items: flex-end; margin-bottom: 1.5rem; background: var(--bg); padding: 1.25rem; border-radius: 12px; border: 1px solid var(--border);">
                        <div class="form-group" style="margin: 0;">
                            <label>Nomdu Plat / Produit</label>
                            <input id="dishName" class="form-control" type="text" placeholder="ex: Poulet Braisé, Bissap..." required />
                        </div>
                        <div class="form-group" style="margin: 0;">
                            <label>Prixde vente (FCFA)</label>
                            <input id="dishPrice" class="form-control" type="number" step="50" min="0" placeholder="ex: 3500" required />
                        </div>
                        <div class="form-group" style="margin: 0;">
                            <label>Catégorie</label>
                            <select id="dishCategorySelect" class="form-control" required>
                                <!-- Rempli dynamiquement -->
                            </select>
                        </div>
                        <div class="form-group" style="margin: 0;">
                            <label>Nombreprésent (Stock) *</label>
                            <input id="dishQuantity" class="form-control" type="number" min="0" value="0" placeholder="ex: 0" required style="font-weight: bold; color: #fbbf24; border-color: rgba(245, 158, 11, 0.5);" title="Nombre de produits disponibles à charger dans le restaurant" />
                        </div>
                        <div>
                            <button type="submit" class="btn btn-primary" style="height: 44px; width: 100%; justify-content: center; background: linear-gradient(135deg, #f59e0b, #d97706); color: black; font-weight: 700;">
                                 Enregistrer le Produit
                            </button>
                        </div>
                    </form>
                    <div id="dishMsg" style="margin-bottom: 0.75rem; font-size: 0.875rem;"></div>
                    <div id="stockAlertsBanner" style="display: none; margin-bottom: 1.25rem;"></div>

                    <table>
                        <thead>
                            <tr>
                                <th>Nomdu Produit</th>
                                <th>Catégorie</th>
                                <th>Prix(FCFA)</th>
                                <th style="min-width: 140px;">NombrePrésent (Stock)</th>
                                <th>Disponibilité</th>
                                <th>SynchronisationOdoo</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody id="dishesTableBody">
                            <tr><td colspan="7" style="text-align: center; color: var(--text-muted);">Chargementdes plats...</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- SECTION 5 : CONFIGURATION DU LOGICIEL & INFORMATIONS DGI -->
            <div id="admSectionConfig" class="hidden">
                <div class="content-panel" style="border-top: 4px solid #f59e0b;">
                    <div class="panel-header">
                        <div>
                            <h3 style="display: flex; align-items: center; gap: 0.5rem; color: #fbbf24;">
                                <span></span>Configuration de l'Entreprise &amp; du Restaurant
                            </h3>
                            <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.25rem;">
                                Configurez ici les paramètres officiels de votre entreprise (Identité, Logo, Identifiants fiscaux et Coordonnées). Ces informations s'appliquent automatiquement sur l'ensemble de votre logiciel, vos reçus et vos factures.
                            </p>
                        </div>
                    </div>

                    <form id="restaurantConfigForm" onsubmit="handleSaveSettings(event)">
                        <!-- BLOC 1 : IDENTITÉ ET LOGO DE L'ENTREPRISE -->
                        <div style="background: var(--bg); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem;">
                            <h4 style="font-size: 1.05rem; color: #fbbf24; margin-bottom: 1.25rem; display: flex; align-items: center; gap: 0.5rem;">
                                <span></span>Identité du Restaurant &amp; Logo de l'Entreprise
                            </h4>

                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.25rem; margin-bottom: 1.25rem;">
                                <div class="form-group" style="margin: 0;">
                                    <label>Nomdu Restaurant (Apparaît sur toutes les factures) *</label>
                                    <input id="cfgRestoName" class="form-control" type="text" placeholder="ex: Lemo Daje Restaurant" required oninput="updateConfigLivePreview()" />
                                </div>
                                <div class="form-group" style="margin: 0;">
                                    <label>Sous-Titre /Slogan de l'Établissement</label>
                                    <input id="cfgRestoSub" class="form-control" type="text" placeholder="ex: Restaurant &amp; Grill Gastronomique" oninput="updateConfigLivePreview()" />
                                </div>
                            </div>

                            <!-- Gestion Logo avec prévisualisation -->
                            <div style="display: grid; grid-template-columns: 1fr 180px; gap: 1.5rem; align-items: center; background: rgba(255,255,255,0.02); border: 1px dashed var(--border); border-radius: 10px; padding: 1.25rem;">
                                <div>
                                    <label style="font-size: 0.85rem; font-weight: 700; color: var(--text-main); display: block; margin-bottom: 0.4rem;">
                                        Logo Officiel de l'Entreprise
                                    </label>
                                    <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.85rem;">
                                        Téléversez un fichier image (PNG, JPG, SVG, WebP) ou collez une URL directe. Ce logo apparaîtra en haut à gauche de toutes les factures certifiées.
                                    </p>
                                    <div style="display: flex; gap: 0.75rem; align-items: center; flex-wrap: wrap;">
                                        <label class="btn btn-secondary" style="cursor: pointer; margin: 0; font-size: 0.85rem; background: #26334d; border-color: #3b82f6; color: #93c5fd;">
                                             Téléverser une Image...
                                            <input type="file" id="cfgLogoFileInput" accept="image/*" style="display: none;" onchange="handleLogoFileUpload(event)" />
                                        </label>
                                        <button type="button" class="btn btn-secondary" style="font-size: 0.8rem;" onclick="resetLogoToDefault()">
                                             Réinitialiser au Badge Rétro
                                        </button>
                                    </div>
                                    <div style="margin-top: 0.85rem;">
                                        <input id="cfgLogoUrl" class="form-control" type="text" placeholder="Ou collez l'URL web directe ou Data URL base64..." oninput="updateLogoPreview(); updateConfigLivePreview();" />
                                    </div>
                                </div>

                                <!-- Box Prévisualisation du Logo -->
                                <div style="text-align: center;">
                                    <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.4rem; font-weight: 600;">Aperçudu Logo :</div>
                                    <div id="cfgLogoPreviewBox" style="width: 130px; height: 130px; margin: 0 auto; background: #faf7f2; border: 2px dashed #bfa892; border-radius: 50%; display: flex; align-items: center; justify-content: center; overflow: hidden; padding: 6px;">
                                        <!-- Rempli dynamiquement -->
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- BLOC 2 : IDENTIFIANTS FISCAUX OBLIGATOIRES DGI (IFU, RCCM, RÉGIME FISCAL, DIVISION FISCALE) -->
                        <div style="background: var(--bg); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem;">
                            <h4 style="font-size: 1.05rem; color: #38bdf8; margin-bottom: 1.25rem; display: flex; align-items: center; gap: 0.5rem;">
                                <span></span>Identifiants Fiscaux Légaux Obligatoires (DGI e-MCF)
                            </h4>

                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.25rem; margin-bottom: 1.25rem;">
                                <div class="form-group" style="margin: 0;">
                                    <label>IFU(Identifiant Fiscal Unique) *</label>
                                    <input id="cfgIfu" class="form-control" type="text" placeholder="ex: 000123456789A" required oninput="updateConfigLivePreview()" />
                                    <input id="cfgNif" type="hidden" />
                                </div>
                                <div class="form-group" style="margin: 0;">
                                    <label>RCCM(Registre du Commerce et du Crédit Mobilier) *</label>
                                    <input id="cfgRccm" class="form-control" type="text" placeholder="ex: BF-OUA-01-2024-B12-00456" required oninput="updateConfigLivePreview()" />
                                </div>
                                <div class="form-group" style="margin: 0;">
                                    <label>RégimeFiscal du Restaurant *</label>
                                    <select id="cfgTaxRegime" class="form-control" onchange="updateConfigLivePreview()" style="font-weight: 600;">
                                        <option value="Régime du Réel Normal d'Imposition (RNI)">Régimedu Réel Normal d'Imposition (RNI)</option>
                                        <option value="Régime Simplifié d'Imposition (RSI)">RégimeSimplifié d'Imposition (RSI)</option>
                                        <option value="Contribution des Micro-Entreprises (CME)">Contributiondes Micro-Entreprises (CME)</option>
                                        <option value="Régime Synthétique / Forfaitaire">RégimeSynthétique / Forfaitaire</option>
                                    </select>
                                </div>
                                <div class="form-group" style="margin: 0;">
                                    <label>DivisionFiscale du Restaurant (Centre des Impôts) *</label>
                                    <input id="cfgFiscalDivision" class="form-control" type="text" placeholder="ex: DGI - Division Fiscale des Moyennes Entreprises" required oninput="updateConfigLivePreview()" />
                                    <input id="cfgTaxCenter" type="hidden" />
                                </div>
                                <div class="form-group" style="margin: 0;">
                                    <label>NIM(Numéro Machine e-MCF DGI)</label>
                                    <input id="cfgNim" class="form-control" type="text" placeholder="ex: RESTO-DGI-MCF-01" required oninput="updateConfigLivePreview()" />
                                </div>
                                <div class="form-group" style="margin: 0;">
                                    <label>Tauxde TVA Normalisé (%)</label>
                                    <input id="cfgTaxRate" class="form-control" type="number" step="0.1" min="0" max="100" placeholder="18" required oninput="updateConfigLivePreview()" />
                                </div>
                            </div>

                            <div class="form-group" style="margin: 0;">
                                <label>MentionLégale Obligatoire imprimée au bas des factures</label>
                                <input id="cfgLegalMention" class="form-control" type="text" placeholder="ex: Facture normalisée certifiée conforme aux exigences de la DGI" oninput="updateConfigLivePreview()" />
                            </div>
                        </div>

                        <!-- BLOC 3 : COORDONNÉES COMPLÈTES DE L'ÉTABLISSEMENT -->
                        <div style="background: var(--bg); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem;">
                            <h4 style="font-size: 1.05rem; color: #a5b4fc; margin-bottom: 1.25rem; display: flex; align-items: center; gap: 0.5rem;">
                                <span></span>Coordonnées &amp; Contacts de l'Établissement (Tel, Adresse, Email)
                            </h4>

                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.25rem;">
                                <div class="form-group" style="margin: 0;">
                                    <label>Téléphone(s)de Contact (tel) *</label>
                                    <input id="cfgPhone" class="form-control" type="text" placeholder="ex: +226 25 30 00 00 / +226 70 00 00 00" required oninput="updateConfigLivePreview()" />
                                </div>
                                <div class="form-group" style="margin: 0;">
                                    <label>AdressePhysique Complète (Adress) *</label>
                                    <input id="cfgAddress" class="form-control" type="text" placeholder="ex: Avenue Kwame Nkrumah, Ouagadougou" required oninput="updateConfigLivePreview()" />
                                </div>
                                <div class="form-group" style="margin: 0;">
                                    <label>AdresseEmail Professionnelle (Email) *</label>
                                    <input id="cfgEmail" class="form-control" type="email" placeholder="ex: contact@lemodaje.com" required oninput="updateConfigLivePreview()" />
                                </div>
                                <div class="form-group" style="margin: 0;">
                                    <label>SiteWeb Officiel</label>
                                    <input id="cfgWebsite" class="form-control" type="text" placeholder="ex: www.lemodaje.com" oninput="updateConfigLivePreview()" />
                                </div>
                            </div>
                        </div>

                        <!-- Bouton Sauvegarder & Notification -->
                        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                            <div id="cfgSaveMsg" style="font-size: 0.95rem; font-weight: 700;"></div>
                            <button type="submit" class="btn btn-primary" style="background: linear-gradient(135deg, #f59e0b, #d97706); color: black; font-weight: 800; font-size: 1.05rem; padding: 0.9rem 2.2rem; box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4);">
                                 Enregistrer la Configuration du Restaurant &amp; DGI
                            </button>
                        </div>
                    </form>
                </div>
            </div>

            <!-- SECTION 6 : COMMUNICATION ADMIN <->GÉRANTS (SMS, VOCAUX & APPELS) -->
            <div id="admSectionChat" class="hidden">
                <div style="background: linear-gradient(135deg, rgba(19, 27, 46, 0.95), rgba(15, 23, 42, 0.95)); border: 1px solid var(--border); border-radius: 16px; padding: 1.5rem; box-shadow: 0 10px 30px rgba(0,0,0,0.4);">
                    
                    <!-- En-tête de section -->
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; flex-wrap: wrap; gap: 1rem; border-bottom: 1px solid var(--border); padding-bottom: 1rem;">
                        <div>
                            <h2 style="font-size: 1.4rem; font-weight: 800; color: #fbbf24; display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.25rem;">
                                 <span>SMS,Vocaux &amp; Appels avec les Gérants</span>
                            </h2>
                            <p style="color: var(--text-muted); font-size: 0.85rem; margin: 0;">
                                Échangez directement par SMS instantané, notes vocales et appels audio/vidéo avec chacun de vos gérants.
                            </p>
                        </div>
                        <div style="display: flex; gap: 0.6rem; align-items: center;">
                            <button class="btn btn-secondary" onclick="loadCommunicationContacts()" style="font-size: 0.85rem;">
                                 Actualiser les Gérants
                            </button>
                        </div>
                    </div>

                    <!-- Interface 2 Colonnes : Contacts Gérants à gauche, Thread SMS, Vocaux & Vidéo à droite -->
                    <div style="display: grid; grid-template-columns: 320px 1fr; gap: 1.5rem; min-height: 580px;">
                        
                        <!-- Colonne Gauche : Liste des Gérants -->
                        <div style="background: rgba(11, 15, 25, 0.6); border: 1px solid var(--border); border-radius: 12px; padding: 1rem; display: flex; flex-direction: column;">
                            <div style="font-size: 0.78rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.75rem;">
                                Gérants du Restaurant (<span id="admChatManagersCount">0</span>)
                            </div>
                            <div id="admChatContactsList" style="display: flex; flex-direction: column; gap: 0.5rem; overflow-y: auto; flex: 1;">
                                <div style="text-align: center; color: var(--text-muted); padding: 2rem 0; font-size: 0.85rem;">Chargementdes gérants...</div>
                            </div>
                        </div>

                        <!-- Colonne Droite : Fil de discussion et Commandes Vocales / Vidéo -->
                        <div style="background: rgba(11, 15, 25, 0.6); border: 1px solid var(--border); border-radius: 12px; display: flex; flex-direction: column; overflow: hidden;">
                            
                            <!-- Header de l'interlocuteur sélectionné -->
                            <div id="admChatHeader" style="background: rgba(19, 27, 46, 0.8); border-bottom: 1px solid var(--border); padding: 0.85rem 1.25rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.75rem;">
                                <div style="display: flex; align-items: center; gap: 0.75rem;">
                                    <div id="admChatActiveAvatar" style="width: 40px; height: 40px; border-radius: 50%; background: #1e293b; border: 1.5px solid #f59e0b; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; font-weight: 800; color: #f59e0b;">
                                        
                                    </div>
                                    <div>
                                        <div id="admChatActiveName" style="font-weight: 700; font-size: 1rem; color: var(--text-main);">Sélectionnezun gérant</div>
                                        <div id="admChatActiveStatus" style="font-size: 0.75rem; color: var(--text-muted);">Enattente de sélection</div>
                                    </div>
                                </div>
                                <div id="admChatActionButtons" style="display: flex; gap: 0.6rem;">
                                    <button class="btn btn-primary" onclick="initiateWebRTCCall('video')" style="background: linear-gradient(135deg, #10b981, #059669); font-weight: 700; font-size: 0.85rem; padding: 0.5rem 1rem;">
                                         Appel Vidéo
                                    </button>
                                    <button class="btn btn-secondary" onclick="initiateWebRTCCall('audio')" style="font-weight: 700; font-size: 0.85rem; padding: 0.5rem 1rem;">
                                         Appel Audio
                                    </button>
                                </div>
                            </div>

                            <!-- Zone des bulles de messages (textes, vocaux, etc.) -->
                            <div id="admChatMessagesContainer" style="flex: 1; padding: 1.25rem; overflow-y: auto; display: flex; flex-direction: column; gap: 0.75rem; max-height: 400px; min-height: 340px; background: rgba(8, 12, 20, 0.4);">
                                <div style="margin: auto; text-align: center; color: var(--text-muted); font-size: 0.88rem;">
                                    Sélectionnez un gérant dans la liste pour commencer à échanger par SMS, envoyer une note vocale ou démarrer un appel.
                                </div>
                            </div>

                            <!-- Raccourcis de messages rapides (Chips) -->
                            <div style="padding: 0.5rem 1.25rem; background: rgba(19, 27, 46, 0.5); border-top: 1px solid rgba(255,255,255,0.05); display: flex; gap: 0.5rem; overflow-x: auto;">
                                <button type="button" class="btn btn-secondary" style="font-size: 0.75rem; padding: 0.25rem 0.6rem; border-radius: 9999px; white-space: nowrap;" onclick="insertQuickMessage('adm', 'Bonjour, tout se passe bien en caisse ?')">Bonjour, tout va bien ?</button>
                                <button type="button" class="btn btn-secondary" style="font-size: 0.75rem; padding: 0.25rem 0.6rem; border-radius: 9999px; white-space: nowrap;" onclick="insertQuickMessage('adm', 'Pouvez-vous clôturer la session de caisse ?')">Clôture caisse</button>
                                <button type="button" class="btn btn-secondary" style="font-size: 0.75rem; padding: 0.25rem 0.6rem; border-radius: 9999px; white-space: nowrap;" onclick="insertQuickMessage('adm', 'Rejoignez-moi en appel vidéo s\'il vous plaît.')">Appel vidéo demandé</button>
                                <button type="button" class="btn btn-secondary" style="font-size: 0.75rem; padding: 0.25rem 0.6rem; border-radius: 9999px; white-space: nowrap;" onclick="insertQuickMessage('adm', 'Facture validée avec succès.')">Facture validée</button>
                            </div>

                            <!-- Barre de saisie standard (Texte + Bouton Vocal) -->
                            <div id="admChatNormalBar" style="padding: 0.85rem 1.25rem; background: rgba(19, 27, 46, 0.8); border-top: 1px solid var(--border); display: flex; gap: 0.75rem; align-items: center;">
                                <input type="text" id="admChatInput" placeholder="Taper votre message SMS instantané..." class="form-control" style="flex: 1; padding: 0.65rem 1rem; font-size: 0.9rem;" onkeydown="handleChatInputKey(event, 'adm')" />
                                <button type="button" class="btn btn-secondary" onclick="startVoiceRecording('adm')" title="Enregistrer une note vocale pour ce gérant" style="display: flex; align-items: center; gap: 0.4rem; padding: 0.65rem 1rem; font-weight: 700; border-radius: 8px; background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.4); color: #f87171; white-space: nowrap;">
                                     Vocal
                                </button>
                                <button class="btn btn-primary" onclick="sendChatMessage('adm')" style="background: linear-gradient(135deg, #f59e0b, #d97706); color: black; font-weight: 800; padding: 0.65rem 1.4rem; white-space: nowrap;">
                                    Envoyer 
                                </button>
                            </div>

                            <!-- Barre d'enregistrement vocal en cours (Admin) -->
                            <div id="admChatVoiceBar" class="hidden" style="padding: 0.85rem 1.25rem; background: rgba(30, 20, 25, 0.95); border-top: 2px solid #ef4444; display: flex; justify-content: space-between; align-items: center; gap: 1rem;">
                                <div style="display: flex; align-items: center; gap: 0.75rem;">
                                    <span class="recording-pulse-dot"></span>
                                    <span style="font-weight: 700; color: #f87171; font-size: 0.9rem;">Enregistrementvocal en cours...</span>
                                    <span id="admVoiceTimer" style="background: rgba(239, 68, 68, 0.25); color: #fca5a5; padding: 2px 8px; border-radius: 6px; font-family: monospace; font-size: 0.95rem; font-weight: 800;">0:00</span>
                                </div>
                                <div style="display: flex; gap: 0.6rem; align-items: center;">
                                    <button type="button" class="btn btn-secondary" onclick="cancelVoiceRecording('adm')" style="font-size: 0.85rem; padding: 0.45rem 0.9rem; color: #cbd5e1;">
                                         Annuler
                                    </button>
                                    <button type="button" class="btn btn-primary" onclick="stopAndSendVoiceRecording('adm')" style="background: linear-gradient(135deg, #ef4444, #dc2626); color: white; font-weight: 800; font-size: 0.85rem; padding: 0.45rem 1.2rem; box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);">
                                         Envoyer le vocal
                                    </button>
                                </div>
                            </div>

                        </div>
                    </div>

                </div>
            </div>

            </main>
    </div>
</div>

        <!-- 3. MANAGER PORTAL -->
        <div id="managerPortal" class="hidden">
            <div class="banner-role banner-manager" style="justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <span style="font-size: 1.5rem;"></span>
                    <div>
                        <strong>EspaceGérant de Restaurant (Tarification FCFA)</strong><br>
                        Bienvenue dans votre espace opérationnel. Votre point de vente est indépendant pour chaque service.
                    </div>
                </div>
                <div style="display: flex; gap: 0.6rem; flex-wrap: wrap;">
                    <a href="http://localhost:8070/pos/ui?config_id=2" target="_blank" class="btn btn-primary" style="text-decoration: none; background: linear-gradient(135deg, #10b981, #059669); font-weight: 700;">
                         Caisse Plein Écran Odoo
                    </a>
                    <a href="http://localhost:8070/web?db=restaurant_odoo" target="_blank" class="btn btn-secondary" style="text-decoration: none; font-weight: 700;">
                         Odoo Menus &amp; Caisse
                    </a>
                </div>
            </div>

            <!-- BARRE D'ONGLETS DE NAVIGATION COMPLÈTE DE L'ESPACE GÉRANT -->
            <div class="manager-nav-tabs">
                <button class="mgr-tab-btn active" id="tabBtnPos" onclick="switchManagerTab('pos')">
                     Vente des Plats (Point de Vente)
                </button>
                <button class="mgr-tab-btn" id="tabBtnInvoices" onclick="switchManagerTab('invoices')">
                     Reçus de Caisse &amp; Tickets
                </button>
                <button class="mgr-tab-btn" id="tabBtnOrders" onclick="switchManagerTab('orders')">
                     Mes Ventes
                </button>
                <button class="mgr-tab-btn" id="tabBtnTables" onclick="switchManagerTab('tables')">
                     Gestion des Tables en Salle
                </button>
                <button class="mgr-tab-btn" id="tabBtnStats" onclick="switchManagerTab('stats')">
                     Statistiques du Service
                </button>
                <button class="mgr-tab-btn" id="tabBtnChat" onclick="switchManagerTab('chat')">
                     SMS &amp; Appel
                    <span id="mgrChatBadge" class="badge-unread hidden" style="background: #ef4444; color: white; border-radius: 9999px; font-size: 0.7rem; font-weight: 800; padding: 2px 7px; margin-left: 6px;">0</span>
                </button>
            </div>

            <!-- SECTION 1 : POINT DE VENTE (POS) INTÉGRÉ DU GÉRANT (ACTIF PAR DÉFAUT À LA CONNEXION) -->
            <div id="mgrSectionPos">
                <div style="display: grid; grid-template-columns: 1.4fr 1fr; gap: 1.5rem; margin-bottom: 2rem; align-items: flex-start;" id="posContainer">
                    
                    <!-- COLONNE GAUCHE : CATALOGUE DE PRODUITS PAR CATÉGORIES (CARTES CARRÉES) -->
                    <div class="content-panel" style="margin: 0;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; flex-wrap: wrap; gap: 0.75rem;">
                            <h3 style="font-size: 1.25rem; color: #34d399; display: flex; align-items: center; gap: 0.5rem; font-weight: 800;">
                                <span></span>Vente des Plats &amp; Menu du Restaurant
                            </h3>
                            <div style="display: flex; gap: 0.5rem; align-items: center;">
                                <div style="position: relative; width: 220px;">
                                    <input id="dishSearchInput" type="text" class="form-control" placeholder="Taper le nom d'un plat..." oninput="filterDishes()" style="font-size: 0.85rem;" />
                                </div>
                                <button class="btn btn-secondary" onclick="loadManagerPOSData()" title="Recharger immédiatement les stocks saisis par l'admin" style="font-size: 0.8rem; padding: 0.45rem 0.85rem; border-color: #3b82f6; color: #93c5fd; font-weight: 700; display: inline-flex; align-items: center; gap: 0.35rem;">
                                    <span></span>Stocks Live
                                </button>
                            </div>
                        </div>

                        <!-- Indicateur clair de synchronisation des stocks -->
                        <div style="font-size: 0.78rem; color: #94a3b8; margin-bottom: 0.85rem; padding: 0.45rem 0.85rem; background: rgba(30, 58, 138, 0.2); border-left: 3px solid #3b82f6; border-radius: 6px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.5rem;">
                            <span> <strong>StockCaisse en Direct :</strong>Le nombre affiché correspond au stock chargé par l'Admin et diminue en direct à chaque vente.</span>
                            <span id="posLiveStockStatus" style="color: #34d399; font-weight: 700; font-size: 0.75rem;">●En temps réel</span>
                        </div>

                        <!-- Onglets Catégories non mélangées (Plats principaux, Boissons, Desserts, etc.) -->
                        <div id="categoryTabsBar" class="category-tabs">
                            <!-- Dynamique -->
                        </div>

                        <!-- Grille de cartes carrées bien jolies -->
                        <div id="dishesSquareGrid" class="dish-grid">
                            <!-- Dynamique -->
                        </div>
                    </div>

                    <!-- COLONNE DROITE : PANIER, MODES DE PAIEMENT, CALCULATEUR AUTOMATIQUE & REÇU -->
                    <div class="content-panel" style="margin: 0; position: sticky; top: 5rem; border: 2px solid #10b981;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                            <h3 style="font-size: 1.15rem; color: #6ee7b7; display: flex; align-items: center; gap: 0.5rem;">
                                <span></span>Commande en Cours
                            </h3>
                            <button class="btn btn-secondary" style="padding: 0.3rem 0.6rem; font-size: 0.75rem;" onclick="clearCart()">Vider</button>
                        </div>

                        <!-- Destination / Table -->
                        <div style="margin-bottom: 1rem;">
                            <label style="font-size: 0.75rem; color: var(--text-muted); font-weight: 600;">Destination /Table :</label>
                            <select id="posTableSelect" class="form-control" style="font-size: 0.85rem; padding: 0.45rem;">
                                <option value="">ÀEmporter / Comptoir</option>
                            </select>
                        </div>

                        <!-- Liste des articles dans le panier avec prix modifiable par le gérant -->
                        <div id="cartItemsContainer" style="max-height: 250px; overflow-y: auto; margin-bottom: 1rem; border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); padding: 0.75rem 0;">
                            <div style="text-align: center; color: var(--text-muted); font-size: 0.85rem; padding: 1.5rem 0;">
                                Panier vide. Cliquez sur une carte carrée pour ajouter un plat.
                            </div>
                        </div>

                        <!-- TOTAL GÉNÉRAL CALCULÉ AUTOMATIQUEMENT -->
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; background: var(--bg); padding: 1rem; border-radius: 10px; border: 1px solid var(--border);">
                            <span style="font-size: 0.95rem; font-weight: 600; color: var(--text-muted);">TotalCommande :</span>
                            <strong id="posCartTotal" style="font-size: 1.6rem; color: #34d399; font-weight: 800;">0FCFA</strong>
                        </div>

                        <!-- MODES DE PAIEMENT SÉLECTIONNABLES -->
                        <div style="margin-bottom: 1rem;">
                            <label style="font-size: 0.8rem; font-weight: 600; color: var(--text-muted); display: block; margin-bottom: 0.5rem;">Modede Paiement :</label>
                            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem;">
                                <button type="button" class="pay-method-btn active" data-method="Espèces (Cash)" onclick="selectPaymentMethod('Espèces (Cash)', this)">
                                     Espèces
                                </button>
                                <button type="button" class="pay-method-btn" data-method="Mobile Money (Orange / Wave / Moov)" onclick="selectPaymentMethod('Mobile Money (Orange / Wave / Moov)', this)">
                                     Mobile
                                </button>
                                <button type="button" class="pay-method-btn" data-method="Carte Bancaire / TPE" onclick="selectPaymentMethod('Carte Bancaire / TPE', this)">
                                     Carte
                                </button>
                            </div>
                        </div>

                        <!-- SAISIE DU MONTANT REMIS PAR LE CLIENT & CALCUL AUTOMATIQUE -->
                        <div style="margin-bottom: 1.25rem; background: var(--bg); padding: 1rem; border-radius: 10px; border: 1px solid var(--border);">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                                <label style="font-size: 0.8rem; font-weight: 700; color: #a5b4fc;">MontantReçu / Donné par Client (FCFA) :</label>
                                <button type="button" onclick="setExactAmount()" style="background: none; border: none; color: #38bdf8; font-size: 0.75rem; cursor: pointer; text-decoration: underline;">CompteExact</button>
                            </div>
                            <input id="posAmountTendered" type="number" step="100" min="0" class="form-control" placeholder="Montant remis par le client..." oninput="calculateChangeLive()" style="font-size: 1.15rem; font-weight: bold; color: white; margin-bottom: 0.5rem;" />
                            
                            <!-- Raccourcis billets FCFA -->
                            <div style="display: flex; gap: 0.35rem; flex-wrap: wrap; margin-bottom: 0.75rem;">
                                <button type="button" class="chip-btn" onclick="addShortcutAmount(1000)">1000</button>
                                <button type="button" class="chip-btn" onclick="addShortcutAmount(2000)">2000</button>
                                <button type="button" class="chip-btn" onclick="addShortcutAmount(5000)">5000</button>
                                <button type="button" class="chip-btn" onclick="addShortcutAmount(10000)">10000</button>
                                <button type="button" class="chip-btn" onclick="addShortcutAmount(20000)">20000</button>
                            </div>

                            <!-- ZONE DU CALCUL AUTOMATIQUE DE MONNAIE OU ALERTE INSUFFISANT -->
                            <div id="posChangeIndicator" style="border-radius: 8px; padding: 0.75rem; text-align: center; font-size: 0.95rem; font-weight: 700;">
                                <span style="color: var(--text-muted); font-size: 0.85rem; font-weight: normal;">Saisissezle montant remis par le client</span>
                            </div>
                        </div>

                        <!-- BOUTON DE VALIDATION DE LA VENTE & ÉMISSION DU REÇU -->
                        <button id="btnValidateSale" class="btn btn-primary" onclick="handleValidateSale()" style="width: 100%; justify-content: center; padding: 0.9rem; font-size: 1rem; font-weight: 800; background: linear-gradient(135deg, #10b981, #059669); box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);" disabled>
                             Valider la Vente &amp; Imprimer le Reçu
                        </button>
                    </div>
                </div>
            </div>

            <!-- SECTION 2 : REÇUS DE CAISSE CLIENTS (GÉRANT) -->
            <div id="mgrSectionInvoices" class="hidden">
                <div class="grid-stats">
                    <div class="stat-card">
                        <div class="label">Total des Reçus Encaissés</div>
                        <div id="mgrInvTotalSales" class="value" style="color: var(--manager-accent);">0FCFA</div>
                    </div>
                    <div class="stat-card">
                        <div class="label">Reçus de Caisse Émis</div>
                        <div id="mgrInvCount" class="value">0</div>
                    </div>
                    <div class="stat-card">
                        <div class="label">MonnaieRemise aux Clients</div>
                        <div id="mgrInvTotalChange" class="value" style="color: var(--admin-accent);">0FCFA</div>
                    </div>
                    <div class="stat-card">
                        <div class="label">Règlementle Plus Utilisé</div>
                        <div id="mgrInvTopPayment" class="value" style="font-size: 1.15rem; color: #a5b4fc;">Espèces(Cash)</div>
                    </div>
                </div>

                <div class="content-panel">
                    <div class="panel-header">
                        <h3>Reçus de Caisse &amp; Tickets Clients</h3>
                        <button class="btn btn-secondary" onclick="loadManagerData()">Actualiser les Reçus</button>
                    </div>
                    <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1.25rem;">
                        Toutes les ventes et encaissements réalisés par vous sont stockés avec la date, l'heure exacte et le montant net sans monnaie. Vous pouvez réimprimer ou consulter n'importe quel reçu à tout moment.
                    </p>
                    <table>
                        <thead>
                            <tr>
                                <th>N° Reçu (Ticket)</th>
                                <th>Date &amp;Heure de Paiement</th>
                                <th>Table</th>
                                <th>Modede Règlement</th>
                                <th>NetEncaissé (FCFA)</th>
                                <th>MontantReçu</th>
                                <th>MonnaieRendue</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody id="managerInvoicesTableBody">
                            <tr><td colspan="8" style="text-align: center; color: var(--text-muted);">Chargement des reçus de caisse...</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- SECTION 3 : MES COMMANDES & VENTES (GÉRANT) -->
            <div id="mgrSectionOrders" class="hidden">
                <div class="content-panel">
                    <div class="panel-header">
                        <h3>Mes Commandes &amp; Ventes Récentes</h3>
                        <button class="btn btn-secondary" onclick="loadManagerData()">Actualiser</button>
                    </div>
                    <table>
                        <thead>
                            <tr>
                                <th>Numéro</th>
                                <th>Table</th>
                                <th>Gérant /Caisse</th>
                                <th>Statut</th>
                                <th>Total(FCFA)</th>
                                <th>SyncOdoo</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody id="ordersTableBody">
                            <tr><td colspan="7" style="text-align: center; color: var(--text-muted);">Chargementdes commandes...</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- SECTION 4 : GESTION DES TABLES EN SALLE (GÉRANT) -->
            <div id="mgrSectionTables" class="hidden">
                <div class="content-panel">
                    <div class="panel-header">
                        <h3>Gestion des Tables en Salle</h3>
                        <button class="btn btn-secondary" onclick="loadManagerData()">Actualiserles Tables</button>
                    </div>
                    <div id="tablesGrid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem;">
                        <!-- Tables loaded dynamically -->
                    </div>
                </div>
            </div>

            <!-- SECTION 5 : STATISTIQUES & TABLEAU DE BORD DU SERVICE -->
            <div id="mgrSectionStats" class="hidden">
                <div class="grid-stats">
                    <div class="stat-card">
                        <div class="label">TablesLibres</div>
                        <div id="mgrStatAvailableTables" class="value" style="color: var(--manager-accent);">-</div>
                    </div>
                    <div class="stat-card">
                        <div class="label">TablesOccupées / Réservées</div>
                        <div id="mgrStatOccupiedTables" class="value" style="color: var(--admin-accent);">-</div>
                    </div>
                    <div class="stat-card">
                        <div class="label">Commandesen Préparation</div>
                        <div id="mgrStatPendingOrders" class="value">-</div>
                    </div>
                    <div class="stat-card">
                        <div class="label">PlatsActifs sur la Carte</div>
                        <div id="mgrStatMenuCount" class="value">-</div>
                    </div>
                </div>
            </div>

            <!-- SECTION 6 : COMMUNICATION GÉRANT <->ADMIN (SMS, VOCAUX & APPELS) -->
            <div id="mgrSectionChat" class="hidden">
                <div style="background: linear-gradient(135deg, rgba(19, 27, 46, 0.95), rgba(15, 23, 42, 0.95)); border: 1px solid var(--border); border-radius: 16px; padding: 1.5rem; box-shadow: 0 10px 30px rgba(0,0,0,0.4);">
                    
                    <!-- En-tête de section -->
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; flex-wrap: wrap; gap: 1rem; border-bottom: 1px solid var(--border); padding-bottom: 1rem;">
                        <div>
                            <h2 style="font-size: 1.4rem; font-weight: 800; color: #34d399; display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.25rem;">
                                 <span>LiaisonDirecte Administrateur (SMS, Vocaux &amp; Appels)</span>
                            </h2>
                            <p style="color: var(--text-muted); font-size: 0.85rem; margin: 0;">
                                Échangez en direct avec l'Administrateur du restaurant par SMS, notes vocales enregistrées ou appels audio/vidéo.
                            </p>
                        </div>
                        <div style="display: flex; gap: 0.6rem; align-items: center;">
                            <button class="btn btn-primary" onclick="initiateWebRTCCall('video')" style="background: linear-gradient(135deg, #10b981, #059669); font-weight: 700; font-size: 0.85rem; padding: 0.5rem 1.1rem;">
                                 Appel Vidéo Direct Admin
                            </button>
                            <button class="btn btn-secondary" onclick="initiateWebRTCCall('audio')" style="font-weight: 700; font-size: 0.85rem; padding: 0.5rem 1rem;">
                                 Appel Audio
                            </button>
                        </div>
                    </div>

                    <!-- Fiche statut de l'Administrateur -->
                    <div style="background: rgba(11, 15, 25, 0.6); border: 1px solid var(--border); border-radius: 12px; padding: 1rem 1.25rem; margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.75rem;">
                        <div style="display: flex; align-items: center; gap: 0.85rem;">
                            <div style="width: 44px; height: 44px; border-radius: 50%; background: #1e293b; border: 2px solid #fbbf24; display: flex; align-items: center; justify-content: center; font-size: 1.3rem;">
                                
                            </div>
                            <div>
                                <div style="font-weight: 800; font-size: 1.05rem; color: #fbbf24;" id="mgrChatAdminName">AdministrateurGénéral</div>
                                <div style="font-size: 0.78rem; color: #34d399; display: flex; align-items: center; gap: 0.35rem;">
                                    <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #34d399;"></span>
                                    Canal sécurisé ouvert &amp; direct
                                </div>
                            </div>
                        </div>
                        <div style="font-size: 0.8rem; color: var(--text-muted);">
                            Notifications instantanées activées 
                        </div>
                    </div>

                    <!-- Zone des bulles de messages -->
                    <div style="background: rgba(11, 15, 25, 0.6); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; display: flex; flex-direction: column;">
                        
                        <div id="mgrChatMessagesContainer" style="flex: 1; padding: 1.25rem; overflow-y: auto; display: flex; flex-direction: column; gap: 0.75rem; max-height: 420px; min-height: 340px; background: rgba(8, 12, 20, 0.4);">
                            <div style="margin: auto; text-align: center; color: var(--text-muted); font-size: 0.88rem;">
                                Chargement des échanges avec l'Administrateur...
                            </div>
                        </div>

                        <!-- Raccourcis de messages rapides (Chips) -->
                        <div style="padding: 0.5rem 1.25rem; background: rgba(19, 27, 46, 0.5); border-top: 1px solid rgba(255,255,255,0.05); display: flex; gap: 0.5rem; overflow-x: auto;">
                            <button type="button" class="btn btn-secondary" style="font-size: 0.75rem; padding: 0.25rem 0.6rem; border-radius: 9999px; white-space: nowrap;" onclick="insertQuickMessage('mgr', 'Bonjour Monsieur l\'Administrateur, le service est ouvert.')">Service ouvert</button>
                            <button type="button" class="btn btn-secondary" style="font-size: 0.75rem; padding: 0.25rem 0.6rem; border-radius: 9999px; white-space: nowrap;" onclick="insertQuickMessage('mgr', 'J\'ai une question concernant une facture client.')">Question facture</button>
                            <button type="button" class="btn btn-secondary" style="font-size: 0.75rem; padding: 0.25rem 0.6rem; border-radius: 9999px; white-space: nowrap;" onclick="insertQuickMessage('mgr', 'Pouvez-vous vous connecter en appel vidéo pour une vérification ?')">Appel vidéo svp</button>
                            <button type="button" class="btn btn-secondary" style="font-size: 0.75rem; padding: 0.25rem 0.6rem; border-radius: 9999px; white-space: nowrap;" onclick="insertQuickMessage('mgr', 'Toutes les tables sont bien gérées, aucune anomalie.')">Tout est en ordre</button>
                        </div>

                        <!-- Barre de saisie standard (Texte + Bouton Vocal) -->
                        <div id="mgrChatNormalBar" style="padding: 0.85rem 1.25rem; background: rgba(19, 27, 46, 0.8); border-top: 1px solid var(--border); display: flex; gap: 0.75rem; align-items: center;">
                            <input type="text" id="mgrChatInput" placeholder="Écrire un message SMS instantané à l'Administrateur..." class="form-control" style="flex: 1; padding: 0.65rem 1rem; font-size: 0.9rem;" onkeydown="handleChatInputKey(event, 'mgr')" />
                            <button type="button" class="btn btn-secondary" onclick="startVoiceRecording('mgr')" title="Enregistrer une note vocale pour l'Administrateur" style="display: flex; align-items: center; gap: 0.4rem; padding: 0.65rem 1rem; font-weight: 700; border-radius: 8px; background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.4); color: #f87171; white-space: nowrap;">
                                 Vocal
                            </button>
                            <button class="btn btn-primary" onclick="sendChatMessage('mgr')" style="background: linear-gradient(135deg, #10b981, #059669); color: white; font-weight: 800; padding: 0.65rem 1.4rem; white-space: nowrap;">
                                Envoyer 
                            </button>
                        </div>

                        <!-- Barre d'enregistrement vocal en cours (Gérant) -->
                        <div id="mgrChatVoiceBar" class="hidden" style="padding: 0.85rem 1.25rem; background: rgba(30, 20, 25, 0.95); border-top: 2px solid #ef4444; display: flex; justify-content: space-between; align-items: center; gap: 1rem;">
                            <div style="display: flex; align-items: center; gap: 0.75rem;">
                                <span class="recording-pulse-dot"></span>
                                <span style="font-weight: 700; color: #f87171; font-size: 0.9rem;">Enregistrementvocal en cours...</span>
                                <span id="mgrVoiceTimer" style="background: rgba(239, 68, 68, 0.25); color: #fca5a5; padding: 2px 8px; border-radius: 6px; font-family: monospace; font-size: 0.95rem; font-weight: 800;">0:00</span>
                            </div>
                            <div style="display: flex; gap: 0.6rem; align-items: center;">
                                <button type="button" class="btn btn-secondary" onclick="cancelVoiceRecording('mgr')" style="font-size: 0.85rem; padding: 0.45rem 0.9rem; color: #cbd5e1;">
                                     Annuler
                                </button>
                                <button type="button" class="btn btn-primary" onclick="stopAndSendVoiceRecording('mgr')" style="background: linear-gradient(135deg, #ef4444, #dc2626); color: white; font-weight: 800; font-size: 0.85rem; padding: 0.45rem 1.2rem; box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);">
                                     Envoyer le vocal
                                </button>
                            </div>
                        </div>

                    </div>

                </div>
            </div>

            
        </div>
    </div>

    <script>
        let token = localStorage.getItem('token') || '';
        let currentUser = JSON.parse(localStorage.getItem('user') || 'null');

        window.onload = async () => {
            await loadRestaurantConfig();
            if (token && currentUser) {
                renderUserSession();
            } else {
                showAuthScreen();
            }
        };

        function showAuthScreen() {
            document.body.classList.remove('admin-mode');
            document.body.classList.add('auth-mode');
            document.getElementById('authScreen').classList.remove('hidden');
            document.getElementById('adminPortal').classList.add('hidden');
            document.getElementById('managerPortal').classList.add('hidden');
            document.getElementById('userNav').classList.add('hidden');
            const btnHdrCfg = document.getElementById('btnHeaderConfig');
            if (btnHdrCfg) btnHdrCfg.style.display = 'none';
        }

        function fillAdminCreds() {
            const u = document.getElementById('loginUsername');
            const p = document.getElementById('loginPassword');
            if (u) u.value = 'admin';
            if (p) p.value = 'admin123';
        }

        function fillManagerCreds() {
            const u = document.getElementById('loginUsername');
            const p = document.getElementById('loginPassword');
            if (u) u.value = 'gerant';
            if (p) p.value = 'gerant123';
        }

        
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

        async function handleLogin(e) {
            e.preventDefault();
            const username = document.getElementById('loginUsername').value;
            const password = document.getElementById('loginPassword').value;
            const errorDiv = document.getElementById('loginError');
            errorDiv.style.display = 'none';

            try {
                const res = await fetch('/api/v1/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, password })
                });
                const data = await res.json();
                if (!res.ok) {
                    throw new Error(data.detail || 'Identifiants invalides');
                }
                token = data.access_token;
                currentUser = data;
                localStorage.setItem('token', token);
                localStorage.setItem('user', JSON.stringify(currentUser));
                await loadRestaurantConfig();
                renderUserSession();
            } catch (err) {
                errorDiv.innerText = err.message;
                errorDiv.style.display = 'block';
            }
        }

        function renderUserSession() {
            document.body.classList.remove('auth-mode');
            document.getElementById('authScreen').classList.add('hidden');
            document.getElementById('userNav').classList.remove('hidden');
            document.getElementById('navUserName').innerText = currentUser.full_name;
            
            const badge = document.getElementById('navUserBadge');
            badge.innerText = currentUser.role === 'admin' ? 'Administrateur' : 'Gérant';
            badge.className = 'role-badge ' + (currentUser.role === 'admin' ? 'role-admin' : 'role-manager');

            const btnHdrCfg = document.getElementById('btnHeaderConfig');
            if (currentUser.role === 'admin') {
                document.body.classList.add('admin-mode');
                if (btnHdrCfg) btnHdrCfg.style.display = 'inline-flex';
                document.getElementById('adminPortal').classList.remove('hidden');
                document.getElementById('managerPortal').classList.add('hidden');
                switchAdminTab('overview');
                loadAdminData();
            } else {
                document.body.classList.remove('admin-mode');
                if (btnHdrCfg) btnHdrCfg.style.display = 'none';
                document.getElementById('managerPortal').classList.remove('hidden');
                document.getElementById('adminPortal').classList.add('hidden');
                switchManagerTab('pos');
                loadManagerData();
            }

            // Démarrer la surveillance des messages et signaux d'appel vidéo
            startCommunicationPoller();
        }

        async function logout() {
            document.body.classList.remove('admin-mode');
            stopCommunicationPoller();
            try {
                if (token) {
                    await fetch('/api/v1/auth/logout', {
                        method: 'POST',
                        headers: { 'Authorization': 'Bearer ' + token }
                    });
                }
            } catch (e) {
                console.error("Erreur lors de la déconnexion backend", e);
            }
            token = '';
            currentUser = null;
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            const btnHdrCfg = document.getElementById('btnHeaderConfig');
            if (btnHdrCfg) btnHdrCfg.style.display = 'none';
            showAuthScreen();
        }

        // --- ADMIN FUNCTIONS ---
        async function loadAdminData() {
            try {
                loadGlobalInvoicesData();
                startGlobalInvoicingRealtimePoller();

                // Dashboard stats
                const resStats = await fetch('/api/v1/admin/dashboard', {
                    headers: { 'Authorization': 'Bearer ' + token }
                });
                if (resStats.ok) {
                    const stats = await resStats.json();
                    document.getElementById('admStatManagers').innerHTML = `<span style="color: #34d399; font-weight: 800;">${stats.online_managers ||0} En Ligne</span> / ${stats.total_managers}Total`;
                    document.getElementById('admStatTables').innerText = stats.total_tables;
                    document.getElementById('admStatDishes').innerText = stats.total_menu_items;
                    document.getElementById('admStatRevenue').innerText = Math.round(stats.total_revenue).toLocaleString('fr-FR') + ' FCFA';
                    document.getElementById('admStatOdoo').innerHTML = stats.odoo_connected 
                        ? '<span class="badge badge-success">Connecté</span>' 
                        : '<span class="badge badge-danger">Horsligne</span>';
                }

                // Managers list
                const resMgrs = await fetch('/api/v1/admin/managers', {
                    headers: { 'Authorization': 'Bearer ' + token }
                });
                if (resMgrs.ok) {
                    const mgrs = await resMgrs.json();
                    const tbody = document.getElementById('managersTableBody');
                    if (mgrs.length === 0) {
                        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: var(--text-muted);">Aucun gérant créé pour le moment.</td></tr>';
                    } else {
                        tbody.innerHTML = mgrs.map(m => {
                            const salesFormatted = Math.round(m.total_sales_amount || 0).toLocaleString('fr-FR') + ' FCFA';
                            return `
                            <tr>
                                <td><strong style="color: #ffffff; font-size: 0.95rem;">${m.full_name}</strong></td>
                                <td><code style="color: #93c5fd; background: rgba(30, 58, 138, 0.3); border: 1px solid #3b82f6; padding: 3px 8px; border-radius: 6px; font-weight: 700;">${m.username}</code></td>
                                <td><span style="color: #34d399; font-weight: 900; font-size: 1rem;">${salesFormatted}</span></td>
                                <td>
                                    ${m.is_active ? '<span class="badge badge-success">Actif</span>' : '<span class="badge badge-danger">Désactivé</span>'}
                                    ${m.odoo_user_id ? '<span class="badge" style="background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); margin-left: 4px;">Odoo #' + m.odoo_user_id + '</span>' : ''}
                                </td>
                                <td style="text-align: right;">
                                    <button class="btn btn-secondary" style="padding: 0.35rem 0.75rem; font-size: 0.78rem; font-weight: 700;" onclick="toggleManager(${m.id})">
                                        ${m.is_active ? 'Désactiver' : 'Activer'}
                                    </button>
                                    <button class="btn btn-danger" style="padding: 0.35rem 0.75rem; font-size: 0.78rem; font-weight: 700; margin-left: 0.5rem;" onclick="deleteManager(${m.id})">
                                        Supprimer
                                    </button>
                                </td>
                            </tr>
                            `;
                        }).join('');
                    }
                }

                // Charger également les sessions de travail et prises de poste
                await loadSessionsData();
                // Charger le journal d'activité (faits et gestes des gérants)
                await loadActivityLogsData();
                // Charger la liste des plats admin
                await loadAdminDishesData();
                // Charger la centralisation des commandes
                await loadAdminOrdersData();
                // Charger la facture générale de la journée & certification DGI
                await loadDailyReportData();
                // Charger la configuration générale du restaurant & DGI
                await loadRestaurantConfig();
            } catch (err) {
                console.error(err);
            }
        }

        async function loadSessionsData() {
            try {
                const res = await fetch('/api/v1/admin/work-sessions', {
                    headers: { 'Authorization': 'Bearer ' + token }
                });
                const tbody = document.getElementById('sessionsTableBody');
                if (res.ok) {
                    const sessions = await res.json();
                    if (sessions.length === 0) {
                        tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; color: var(--text-muted);">Aucuneprise de service pour le moment. Dès qu\’un gérant se connecte, sa session et son argent encaissé s\’affichent ici en direct.</td></tr>';
                    } else {
                        tbody.innerHTML = sessions.map(s => {
                            const isOnline = s.is_online;
                            const statusBadge = isOnline 
                                ? '<span class="badge badge-success" style="box-shadow: 0 0 10px rgba(16, 185, 129, 0.4);">EN SERVICE (Actif)</span>' 
                                : '<span class="badge" style="background: rgba(148, 163, 184, 0.2); color: #94a3b8;">Clôturé (Déconnecté)</span>';
                            
                            const startDate = s.login_at ? new Date(s.login_at).toLocaleString('fr-FR', { dateStyle: 'short', timeStyle: 'short' }) : 'N/A';
                            const stopDate = s.logout_at ? new Date(s.logout_at).toLocaleString('fr-FR', { dateStyle: 'short', timeStyle: 'short' }) : (isOnline ? '<span style="color: #34d399; font-weight: 600;">Encours...</span>' : 'N/A');
                            const tendered = s.total_tendered_amount ? Math.round(s.total_tendered_amount).toLocaleString('fr-FR') + ' FCFA' : '-';
                            const change = s.total_change_amount ? Math.round(s.total_change_amount).toLocaleString('fr-FR') + ' FCFA' : '0 FCFA';

                            return `
                                <tr>
                                    <td><strong>${s.manager_name}</strong>(<code>${s.manager_login}</code>)</td>
                                    <td>${statusBadge}</td>
                                    <td>${startDate}</td>
                                    <td>${stopDate}</td>
                                    <td><span class="badge" style="background: var(--bg); border: 1px solid var(--border);">${s.total_orders_count}vente(s)</span></td>
                                    <td><strong style="color: #34d399; font-size: 0.95rem;">${Math.round(s.total_sales_amount).toLocaleString('fr-FR')}FCFA</strong></td>
                                    <td><strong>${tendered}</strong></td>
                                    <td><span style="color: #f59e0b;">${change}</span></td>
                                </tr>
                            `;
                        }).join('');
                    }
                }
            } catch (err) {
                console.error("Erreur chargement work-sessions", err);
            }
        }

        async function loadActivityLogsData() {
            try {
                const res = await fetch('/api/v1/admin/activity-logs', {
                    headers: { 'Authorization': 'Bearer ' + token }
                });
                const tbody = document.getElementById('activityLogsTableBody');
                if (res.ok) {
                    const logs = await res.json();
                    if (logs.length === 0) {
                        tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: var(--text-muted);">Aucuneaction enregistrée pour le moment. Toutes les actions des gérants apparaîtront ici.</td></tr>';
                    } else {
                        tbody.innerHTML = logs.map(l => {
                            let actionBadge = '<span class="badge badge-info">' +l.action_type + '</span>';
                            if (l.action_type === 'ORDER_SALE') {
                                actionBadge = '<span class="badge badge-success" style="box-shadow: 0 0 8px rgba(16,185,129,0.3);">ENCAISSEMENT VENTE</span>';
                            } else if (l.action_type === 'LOGIN') {
                                actionBadge = '<span class="badge badge-primary">CONNEXION (Début)</span>';
                            } else if (l.action_type === 'LOGOUT') {
                                actionBadge = '<span class="badge" style="background: rgba(148,163,184,0.2); color: #94a3b8;">DÉCONNEXION (Fin)</span>';
                            } else if (l.action_type === 'PRICE_ADJUSTED') {
                                actionBadge = '<span class="badge badge-warning">AJUSTEMENT PRIX</span>';
                            }

                            const logDate = l.created_at ? new Date(l.created_at).toLocaleString('fr-FR', { dateStyle: 'short', timeStyle: 'medium' }) : '-';

                            return `
                                <tr>
                                    <td><small style="color: var(--text-muted);">${logDate}</small></td>
                                    <td><strong>${l.manager_name}</strong>(<code>${l.manager_login}</code>)</td>
                                    <td>${actionBadge}</td>
                                    <td>${l.description}</td>
                                </tr>
                            `;
                        }).join('');
                    }
                }
            } catch (err) {
                console.error("Erreur chargement activity logs", err);
            }
        }

        async function handleCreateManager(e) {
            e.preventDefault();
            const msg = document.getElementById('mgrMsg');
            msg.innerText = '';

            const payload = {
                full_name: document.getElementById('mgrFullName').value,
                username: document.getElementById('mgrUsername').value,
                email: document.getElementById('mgrEmail').value,
                password: document.getElementById('mgrPassword').value
            };

            try {
                const res = await fetch('/api/v1/admin/managers', {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + token 
                    },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if (!res.ok) throw new Error(data.detail || 'Erreur lors de la création');

                msg.innerHTML = `
                    <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid var(--manager-accent); border-radius: 8px; padding: 1rem; color: #6ee7b7;">
                        <strong style="font-size: 1rem;">Compte Gérant créé et activé par l'Administrateur !</strong>
                        <p style="margin-top: 0.5rem; font-size: 0.85rem; color: white; line-height: 1.6;">
                            <strong>Fiched'accès à remettre au Gérant :</strong><br>
                            • Nom : <code>${payload.full_name}</code><br>
                            • Identifiant (Login) : <code>${payload.username}</code><br>
                            • Mot de passe : <code>${payload.password}</code><br>
                            • Accès Odoo : <a href="http://localhost:8070/web?db=restaurant_odoo" target="_blank" style="color: #6ee7b7; text-decoration: underline;">http://localhost:8070/web?db=restaurant_odoo</a><br>
                            • Accès Portail : <a href="/app" style="color: #6ee7b7; text-decoration: underline;">http://localhost:8000/app</a>
                        </p>
                    </div>
                `;
                document.getElementById('createManagerForm').reset();
                loadAdminData();
            } catch (err) {
                msg.innerHTML = '<span style="color: var(--danger);">' +err.message + '</span>';
            }
        }

        async function toggleManager(id) {
            await fetch(`/api/v1/admin/managers/${id}/toggle-status`, {
                method: 'PATCH',
                headers: { 'Authorization': 'Bearer ' + token }
            });
            loadAdminData();
        }

        async function deleteManager(id) {
            if (confirm("Voulez-vous vraiment supprimer ce gérant ?")) {
                await fetch(`/api/v1/admin/managers/${id}`, {
                    method: 'DELETE',
                    headers: { 'Authorization': 'Bearer ' + token }
                });
                loadAdminData();
            }
        }

        async function loadAdminDishesData() {
            try {
                // Charger les catégories pour le menu déroulant
                const resCats = await fetch('/api/v1/menu/categories');
                if (resCats.ok) {
                    allCategories = await resCats.json();
                    const select = document.getElementById('dishCategorySelect');
                    if (select) {
                        select.innerHTML = allCategories.map(c => `<option value="${c.id}">${c.name}</option>`).join('');
                    }
                }

                // Charger les plats
                const resItems = await fetch('/api/v1/menu/items');
                if (resItems.ok) {
                    allDishes = await resItems.json();
                    
                    // Signalement en temps réel des ruptures et manques de stocks
                    const outOfStockItems = allDishes.filter(d =>((d.available_quantity !== undefined && d.available_quantity !== null ? d.available_quantity : 0) <= 0) || !d.is_available);
                    const banner = document.getElementById('stockAlertsBanner');
                    if (banner) {
                        if (outOfStockItems.length >0) {
                            banner.style.display = 'block';
                            banner.innerHTML = `
                                <div style="background: rgba(239, 68, 68, 0.18); border: 2px solid #ef4444; border-radius: 12px; padding: 1rem 1.25rem; color: #ffffff; box-shadow: 0 4px 15px rgba(239, 68, 68, 0.25);">
                                    <div style="display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap;">
                                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                                            <span style="font-size: 1.6rem;"></span>
                                            <div>
                                                <strong style="color: #fca5a5; font-size: 1.05rem; text-transform: uppercase; letter-spacing: 0.5px;">AlerteManque de Stock en Temps Réel !</strong>
                                                <div style="color: #ffffff; font-size: 0.88rem; margin-top: 3px;">
                                                    <strong>${outOfStockItems.length}produit(s) en rupture totale (0 restant en cuisine / bar) :</strong> 
                                                    <span style="color: #fecaca; font-weight: 700;">${outOfStockItems.map(d =>d.name).join(', ')}</span>
                                                </div>
                                            </div>
                                        </div>
                                        <span class="badge" style="background: #dc2626; color: white; font-weight: 800; font-size: 0.82rem; padding: 6px 12px; border-radius: 20px;">
                                             Action Requise : Réapprovisionner
                                        </span>
                                    </div>
                                </div>
                            `;
                        } else {
                            banner.style.display = 'block';
                            banner.innerHTML = `
                                <div style="background: rgba(16, 185, 129, 0.12); border: 1.5px solid #10b981; border-radius: 10px; padding: 0.65rem 1.25rem; color: #6ee7b7; font-size: 0.85rem; display: flex; align-items: center; gap: 0.5rem;">
                                    <span></span>
                                    <strong>Tousles produits disposent de stock pour la vente en caisse.</strong>
                                </div>
                            `;
                        }
                    }

                    const tbody = document.getElementById('dishesTableBody');
                    if (tbody) {
                        if (allDishes.length === 0) {
                            tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; color: var(--text-muted);">Aucunplat dans le menu. Utilisez le formulaire ci-dessus pour en ajouter.</td></tr>';
                        } else {
                            const activeId = document.activeElement ? document.activeElement.id : null;
                            tbody.innerHTML = allDishes.map(item => {
                                const stock = item.available_quantity !== undefined && item.available_quantity !== null ? item.available_quantity : 0;
                                const isOut = stock <= 0 || !item.is_available;
                                const badgeHtml = isOut
                                    ? '<span class="badge" style="background: linear-gradient(135deg, #dc2626, #991b1b); color: white; font-weight: 900; font-size: 0.82rem; padding: 5px 10px; border-radius: 6px; box-shadow: 0 2px 8px rgba(220, 38, 38, 0.4);">MANQUE DE STOCK (0)</span>'
                                    : (stock <= 3 
                                        ? '<span class="badge" style="background: #d97706; color: white; font-weight: 800; font-size: 0.82rem; padding: 4px 8px; border-radius: 6px;">Stock Faible (' + stock + ')</span>' 
                                        : '<span class="badge badge-success" style="font-weight: 800; font-size: 0.82rem; padding: 4px 8px; border-radius: 6px;">●En stock (' + stock + ')</span>');

                                return `
                                <tr style="${isOut ? 'background: rgba(239, 68, 68, 0.05);' : ''}">
                                    <td><strong>${item.name}</strong></td>
                                    <td><span class="badge" style="background: rgba(99, 102, 241, 0.2); color: #a5b4fc;">${getCategoryName(item.category_id)}</span></td>
                                    <td><strong>${Math.round(item.price).toLocaleString('fr-FR')}FCFA</strong></td>
                                    <td>
                                        <div style="display: flex; align-items: center; gap: 0.35rem;">
                                            <input type="number" min="0" value="${stock}" id="dishStock_${item.id}"
                                                   style="width: 70px; padding: 0.35rem 0.5rem; font-size: 0.85rem; background: var(--bg); border: 2px solid ${!isOut ? '#10b981' : '#ef4444'}; border-radius: 6px; color: ${!isOut ? '#34d399' : '#f87171'}; font-weight: 800; text-align: center;"
                                                   onchange="quickUpdateDishStock(${item.id}, this.value)" title="Modifier directement le nombre disponible de ce produit" />
                                            <button class="btn btn-secondary" style="padding: 0.3rem 0.55rem; font-size: 0.75rem;" onclick="quickUpdateDishStock(${item.id}, document.getElementById('dishStock_${item.id}').value)" title="Enregistrer le stock">
                                                
                                            </button>
                                        </div>
                                    </td>
                                    <td>${badgeHtml}</td>
                                    <td>${item.odoo_product_id ? '<span class="badge badge-success">OdooSync #' + item.odoo_product_id + '</span>' : '<span class="badge badge-warning">Enattente</span>'}</td>
                                    <td>
                                        <button class="btn btn-danger" style="padding: 0.3rem 0.6rem; font-size: 0.75rem;" onclick="deleteDish(${item.id})">
                                             Supprimer
                                        </button>
                                    </td>
                                </tr>
                                `;
                            }).join('');

                            // Restaurer le focus si l'utilisateur modifiait un champ
                            if (activeId && document.getElementById(activeId)) {
                                document.getElementById(activeId).focus();
                            }
                        }
                    }
                }
            } catch (err) {
                console.error(err);
            }
        }

        async function quickUpdateDishStock(id, newQty) {
            const qty = Math.max(0, parseInt(newQty) || 0);
            const msg = document.getElementById('dishMsg');
            try {
                const headers = { 'Content-Type': 'application/json' };
                if (token) headers['Authorization'] = 'Bearer ' + token;
                const res = await fetch(`/api/v1/menu/items/${id}/stock`, {
                    method: 'PATCH',
                    headers: headers,
                    body: JSON.stringify({ available_quantity: qty })
                });
                const data = await res.json();
                if (!res.ok) throw new Error(data.detail || "Erreur lors de la mise à jour du stock");
                if (msg) {
                    msg.innerHTML = `<span style="color: #34d399; font-weight: 600;">Stock mis à jour : « ${data.name} » a maintenant <strong>${data.available_quantity}unité(s)</strong>disponible(s) dans le restaurant.</span>`;
                    setTimeout(() => {if (msg.innerHTML.includes(data.name)) msg.innerHTML = ''; }, 4500);
                }
                await loadAdminDishesData();
            } catch (err) {
                if (msg) msg.innerHTML = '<span style="color: var(--danger);">' +err.message + '</span>';
            }
        }

        async function handleCreateDish(e) {
            e.preventDefault();
            const msg = document.getElementById('dishMsg');
            msg.innerText = '';
            const qtyInput = document.getElementById('dishQuantity');
            const qty = qtyInput ? (parseInt(qtyInput.value) || 0) : 0;
            const payload = {
                name: document.getElementById('dishName').value.trim(),
                price: parseFloat(document.getElementById('dishPrice').value),
                category_id: parseInt(document.getElementById('dishCategorySelect').value),
                available_quantity: qty,
                is_available: qty >0
            };
            try {
                const headers = { 'Content-Type': 'application/json' };
                if (token) headers['Authorization'] = 'Bearer ' + token;
                const res = await fetch('/api/v1/menu/items', {
                    method: 'POST',
                    headers: headers,
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if (!res.ok) throw new Error(data.detail || 'Erreur lors de l\’ajout du plat');
                msg.innerHTML = `<span style="color: #34d399; font-weight: 600;">Produit « ${data.name} » (${Math.round(data.price).toLocaleString('fr-FR')} FCFA | Stock: ${data.available_quantity} dispo) enregistré et synchronisé avec succès !</span>`;
                document.getElementById('createDishForm').reset();
                if (document.getElementById('dishQuantity')) document.getElementById('dishQuantity').value = 0;
                await loadAdminDishesData();
                const resStats = await fetch('/api/v1/admin/dashboard', { headers: { 'Authorization': 'Bearer ' + token } });
                if (resStats.ok) {
                    const stats = await resStats.json();
                    document.getElementById('admStatDishes').innerText = stats.total_menu_items;
                }
            } catch (err) {
                msg.innerHTML = '<span style="color: var(--danger);">' +err.message + '</span>';
            }
        }

        async function deleteDish(id) {
            if (confirm("Voulez-vous vraiment supprimer ce plat du menu ?")) {
                const headers = {};
                if (token) headers['Authorization'] = 'Bearer ' + token;
                await fetch(`/api/v1/menu/items/${id}`, { method: 'DELETE', headers: headers });
                await loadAdminDishesData();
            }
        }

        // --- MANAGER FUNCTIONS ---
        async function loadManagerData() {
            try {
                // Stats
                const resStats = await fetch('/api/v1/manager/dashboard', {
                    headers: { 'Authorization': 'Bearer ' + token }
                });
                if (resStats.ok) {
                    const stats = await resStats.json();
                    document.getElementById('mgrStatAvailableTables').innerText = stats.available_tables;
                    document.getElementById('mgrStatOccupiedTables').innerText = stats.occupied_tables;
                    document.getElementById('mgrStatPendingOrders').innerText = stats.pending_orders;
                    document.getElementById('mgrStatMenuCount').innerText = stats.total_dishes_on_menu;
                }

                // Tables
                const resTables = await fetch('/api/v1/manager/tables', {
                    headers: { 'Authorization': 'Bearer ' + token }
                });
                if (resTables.ok) {
                    const tables = await resTables.json();
                    const grid = document.getElementById('tablesGrid');
                    grid.innerHTML = tables.map(t => {
                        const isAvail = t.status === 'available';
                        const isOcc = t.status === 'occupied';
                        const badgeClass = isAvail ? 'badge-success' : (isOcc ? 'badge-danger' : 'badge-warning');
                        const statusLabel = isAvail ? 'Libre' : (isOcc ? 'Occupée' : 'Réservée');
                        return `
                            <div style="background: var(--bg); border: 1px solid var(--border); border-radius: 12px; padding: 1.25rem;">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                                    <strong>${t.name}</strong>
                                    <span class="badge ${badgeClass}">${statusLabel}</span>
                                </div>
                                <div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem;">
                                    Capacité : ${t.capacity} places
                                </div>
                                <select onchange="updateTableStatus(${t.id}, this.value)" class="form-control" style="font-size: 0.8rem; padding: 0.4rem 0.6rem;">
                                    <option value="available" ${isAvail ? 'selected' : ''}>Libre</option>
                                    <option value="occupied" ${isOcc ? 'selected' : ''}>Occupée</option>
                                    <option value="reserved" ${t.status === 'reserved' ? 'selected' : ''}>Réservée</option>
                                </select>
                            </div>
                        `;
                    }).join('');
                }

                // Orders
                const resOrders = await fetch('/api/v1/manager/orders', {
                    headers: { 'Authorization': 'Bearer ' + token }
                });
                if (resOrders.ok) {
                    let orders = await resOrders.json();
                    if (currentUser && currentUser.username) {
                        const myLogin = currentUser.username.trim().toLowerCase();
                        const myName = (currentUser.full_name || '').trim().toLowerCase();
                        orders = orders.filter(o => {
                            const oLogin = (o.manager_login || '').trim().toLowerCase();
                            const oName = (o.manager_name || '').trim().toLowerCase();
                            return oLogin === myLogin || (myName && oName === myName);
                        });
                    }
                    currentManagerOrders = orders;
                    const tbody = document.getElementById('ordersTableBody');
                    if (tbody) {
                        if (orders.length === 0) {
                            tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; color: var(--text-muted);">Aucunecommande enregistrée.</td></tr>';
                        } else {
                            tbody.innerHTML = orders.map(o => `
                                <tr>
                                    <td><strong>${o.order_number}</strong></td>
                                    <td>Table #${o.table_id || 'Comptoir'}</td>
                                    <td>
                                        <span>${o.manager_name || 'Gérant'}</span>
                                        ${o.session_name ? '<br><small style="color: var(--text-muted);">' +o.session_name + '</small>' : ''}
                                    </td>
                                    <td><span class="badge badge-warning">${o.status}</span></td>
                                    <td><strong>${Math.round(o.total_amount).toLocaleString('fr-FR')}FCFA</strong></td>
                                    <td>${o.odoo_sync_status === 'synced' ? '<span class="badge badge-success">Synchronisé</span>' : '<span class="badge badge-warning">' +o.odoo_sync_status + '</span>'}</td>
                                    <td>
                                        <select onchange="updateOrderStatus(${o.id}, this.value)" class="form-control" style="padding: 0.25rem 0.5rem; font-size: 0.75rem; width: auto;">
                                            <option value="pending" ${o.status === 'pending' ? 'selected' : ''}>Enattente</option>
                                            <option value="cooking" ${o.status === 'cooking' ? 'selected' : ''}>Encuisine</option>
                                            <option value="served" ${o.status === 'served' ? 'selected' : ''}>Servi</option>
                                            <option value="paid" ${o.status === 'paid' ? 'selected' : ''}>Payé</option>
                                        </select>
                                    </td>
                                </tr>
                            `).join('');
                        }
                    }

                    // Peupler également la Facturation & Reçus Clients
                    const invTbody = document.getElementById('managerInvoicesTableBody');
                    if (invTbody) {
                        const paidOrders = orders.filter(o =>o.status === 'paid');
                        const totalSales = paidOrders.reduce((sum, o) =>sum + (o.total_amount || 0), 0);
                        const totalChange = paidOrders.reduce((sum, o) =>sum + (o.change_amount || 0), 0);
                        
                        const elSales = document.getElementById('mgrInvTotalSales');
                        if (elSales) elSales.innerText = Math.round(totalSales).toLocaleString('fr-FR') + ' FCFA';

                        const elCount = document.getElementById('mgrInvCount');
                        if (elCount) elCount.innerText = paidOrders.length + ' reçu(s)';

                        const elChange = document.getElementById('mgrInvTotalChange');
                        if (elChange) elChange.innerText = Math.round(totalChange).toLocaleString('fr-FR') + ' FCFA';

                        if (paidOrders.length >0) {
                            const methods = paidOrders.map(o =>o.payment_method || 'Espèces (Cash)');
                            const topMethod = methods.sort((a,b) =>
                                methods.filter(v =>v===a).length - methods.filter(v =>v===b).length
                            ).pop();
                            const elMethod = document.getElementById('mgrInvTopPayment');
                            if (elMethod) elMethod.innerText = topMethod;
                        }

                        if (paidOrders.length === 0) {
                            invTbody.innerHTML = '<tr><td colspan="8" style="text-align: center; color: var(--text-muted);">Aucun reçu enregistré pour le moment. Dès qu\’une vente est validée, son reçu s\’affiche ici avec le montant net et la monnaie.</td></tr>';
                        } else {
                            invTbody.innerHTML = paidOrders.map(o => {
                                const dateStr = o.created_at ? new Date(o.created_at).toLocaleDateString('fr-FR') : 'N/A';
                                const tendered = o.tendered_amount ? Math.round(o.tendered_amount).toLocaleString('fr-FR') + ' FCFA' : '-';
                                const change = o.change_amount ? Math.round(o.change_amount).toLocaleString('fr-FR') + ' FCFA' : '0 FCFA';
                                return `
                                    <tr>
                                        <td><strong>${o.order_number}</strong></td>
                                        <td><small style="color: var(--text-muted);">${dateStr}</small></td>
                                        <td>Table #${o.table_id || 'Comptoir'}</td>
                                        <td><span class="badge" style="background: rgba(99, 102, 241, 0.15); color: #a5b4fc;">${o.payment_method || 'Espèces(Cash)'}</span></td>
                                        <td><strong style="color: #34d399; font-size: 0.95rem;">${Math.round(o.total_amount).toLocaleString('fr-FR')}FCFA</strong></td>
                                        <td>${tendered}</td>
                                        <td><span style="color: #f59e0b;">${change}</span></td>
                                        <td>
                                            <button class="btn btn-secondary" style="padding: 0.35rem 0.75rem; font-size: 0.8rem; font-weight: 700;" onclick="reprintOrderReceipt(${o.id})">
                                                 Imprimer Reçu
                                            </button>
                                        </td>
                                    </tr>
                                `;
                            }).join('');
                        }
                    }
                }

                // Charger le Point de Vente Caisse
                await loadManagerPOSData();
            } catch (err) {
                console.error(err);
            }
        }

        function switchManagerTab(tab) {
            const tabs = ['pos', 'invoices', 'orders', 'tables', 'stats', 'chat'];
            tabs.forEach(t => {
                const btn = document.getElementById('tabBtn' + t.charAt(0).toUpperCase() + t.slice(1));
                const sec = document.getElementById('mgrSection' + t.charAt(0).toUpperCase() + t.slice(1));
                if (btn) btn.classList.toggle('active', t === tab);
                if (sec) sec.classList.toggle('hidden', t !== tab);
            });
            if (tab === 'pos') {
                loadManagerPOSData();
            }
            if (tab === 'chat') {
                initCommunicationChat('mgr');
            }
        }

        function reprintOrderReceipt(orderId) {
            const order = (currentManagerOrders || []).find(o =>o.id === orderId);
            if (!order) return;
            const items = (order.items || []).map(it =>({
                dish: { name: it.menu_item_name || ('Plat #' + it.menu_item_id) },
                quantity: it.quantity,
                unit_price: it.unit_price
            }));
            const tendered = order.tendered_amount || order.total_amount;
            const change = order.change_amount || 0;
            showReceiptModal(order, items, order.total_amount, tendered, change, order.payment_method || 'Espèces (Cash)');
        }

        async function updateTableStatus(id, newStatus) {
            await fetch(`/api/v1/manager/tables/${id}/status?status_value=${newStatus}`, {
                method: 'PATCH',
                headers: { 'Authorization': 'Bearer ' + token }
            });
            loadManagerData();
        }

        async function updateOrderStatus(id, newStatus) {
            await fetch(`/api/v1/manager/orders/${id}/status?new_status=${newStatus}`, {
                method: 'PATCH',
                headers: { 'Authorization': 'Bearer ' + token }
            });
            loadManagerData();
        }

        // --- VARIABLES & FONCTIONS DU POINT DE VENTE (POS) GÉRANT ---
        let currentManagerOrders = [];
        let allDishes = [];
        let allCategories = [];
        let currentCategoryFilter = 'all';
        let currentSearchQuery = '';
        let cart = [];
        let currentPaymentMethod = 'Espèces (Cash)';

        function getCategoryName(catId) {
            const c = allCategories.find(cat =>cat.id === catId);
            return c ? c.name : 'Plat';
        }

        function getCategoryIcon(catName) {
            const lower = (catName || '').toLowerCase();
            if (lower.includes('boisson')) return '';
            if (lower.includes('dessert')) return '';
            if (lower.includes('entree') || lower.includes('entrée')) return '';
            if (lower.includes('plat') || lower.includes('principal')) return '';
            return '';
        }

        async function loadManagerPOSData() {
            try {
                // 1. Récupérer les catégories
                const resCats = await fetch('/api/v1/menu/categories');
                if (resCats.ok) {
                    allCategories = await resCats.json();
                }

                // 2. Récupérer les plats
                const resItems = await fetch('/api/v1/menu/items');
                if (resItems.ok) {
                    allDishes = await resItems.json();
                }

                // 3. Charger les tables dans le select POS
                const resTables = await fetch('/api/v1/manager/tables', {
                    headers: { 'Authorization': 'Bearer ' + token }
                });
                if (resTables.ok) {
                    const tables = await resTables.json();
                    const tableSelect = document.getElementById('posTableSelect');
                    if (tableSelect) {
                        const currentVal = tableSelect.value;
                        tableSelect.innerHTML = '<option value="">ÀEmporter / Comptoir</option>' + 
                            tables.map(t => `<option value="${t.id}" ${t.status === 'occupied' ? 'style="color:#fbbf24;"' : ''}>Table #${t.name}(${t.status === 'available' ? 'Libre' : 'Occupée'})</option>`).join('');
                        tableSelect.value = currentVal;
                    }
                }

                // 4. Rendu de l'interface POS
                renderCategoryTabs();
                renderDishesGrid();
                renderCart();
                calculateChangeLive();
                startPOSStockAutoRefresh();
            } catch (err) {
                console.error("Erreur chargement POS:", err);
            }
        }

        let posStockAutoRefreshTimer = null;
        function startPOSStockAutoRefresh() {
            if (posStockAutoRefreshTimer) return;
            posStockAutoRefreshTimer = setInterval(async () => {
                const posSec = document.getElementById('mgrSectionPos');
                if (posSec && !posSec.classList.contains('hidden') && token) {
                    try {
                        const r = await fetch('/api/v1/menu/items');
                        if (r.ok) {
                            const latestDishes = await r.json();
                            allDishes = latestDishes;
                            renderDishesGrid();
                        }
                    } catch (_) {}
                }
            }, 6000);
        }

        function renderCategoryTabs() {
            const container = document.getElementById('categoryTabsBar');
            if (!container) return;

            const totalCount = allDishes.length;
            let html = `
                <button class="tab-btn ${currentCategoryFilter === 'all' ? 'active' : ''}" onclick="filterByCategory('all')">
                     Tous (${totalCount})
                </button>
            `;

            allCategories.forEach(cat => {
                const count = allDishes.filter(d =>d.category_id === cat.id).length;
                const icon = getCategoryIcon(cat.name);
                const isActive = currentCategoryFilter === String(cat.id);
                html += `
                    <button class="tab-btn ${isActive ? 'active' : ''}" onclick="filterByCategory('${cat.id}')">
                        ${icon} ${cat.name} (${count})
                    </button>
                `;
            });

            container.innerHTML = html;
        }

        function filterByCategory(catId) {
            currentCategoryFilter = String(catId);
            renderCategoryTabs();
            renderDishesGrid();
        }

        function filterDishes() {
            const searchInput = document.getElementById('dishSearchInput');
            currentSearchQuery = searchInput ? searchInput.value.trim().toLowerCase() : '';
            renderDishesGrid();
        }

        function renderDishesGrid() {
            const grid = document.getElementById('dishesSquareGrid');
            if (!grid) return;

            // Afficher tous les plats (y compris épuisés pour signaler la rupture)
            let filtered = allDishes.slice();

            if (currentCategoryFilter !== 'all') {
                filtered = filtered.filter(d =>String(d.category_id) === currentCategoryFilter);
            }

            if (currentSearchQuery) {
                filtered = filtered.filter(d =>d.name.toLowerCase().includes(currentSearchQuery));
            }

            if (filtered.length === 0) {
                grid.innerHTML = `
                    <div style="grid-column: 1 / -1; text-align: center; padding: 3rem 1rem; color: var(--text-muted); background: var(--bg); border-radius: 12px; border: 1px dashed var(--border);">
                        <span style="font-size: 2.5rem; display: block; margin-bottom: 0.5rem;"></span>
                        <strong>Aucunplat ne correspond à votre recherche.</strong><br>
                        <small>Vérifiezles catégories ou saisissez un autre nom.</small>
                    </div>
                `;
                return;
            }

            grid.innerHTML = filtered.map(dish => {
                const catName = getCategoryName(dish.category_id);
                const stock = (dish.available_quantity !== undefined && dish.available_quantity !== null) ? (parseInt(dish.available_quantity) || 0) : 0;
                const isOutOfStock = stock <= 0 || !dish.is_available;

                let stockBadgeClass = 'dish-card-stock-ok';
                let stockText = `${stock}`;
                let alertHtml = '';

                if (isOutOfStock) {
                    stockBadgeClass = 'dish-card-stock-empty';
                    stockText = '0';
                    alertHtml = `<div class="dish-card-stock-alert">MANQUE DE PRODUIT (0)</div>`;
                } else if (stock <= 3) {
                    stockBadgeClass = 'dish-card-stock-warning';
                    stockText = `${stock}`;
                }

                const cardClass = isOutOfStock ? 'dish-card out-of-stock' : 'dish-card';

                return `
                    <div class="${cardClass}" onclick="addToCart(${dish.id})" title="${isOutOfStock ? 'Produit en rupture de stock - Aucun disponible' : 'Cliquer pour ajouter à la vente'}">
                        <div class="dish-card-header">
                            <span class="dish-card-cat-badge">${catName}</span>
                            <span class="dish-card-stock-badge ${stockBadgeClass}">${stockText}</span>
                        </div>
                        <div style="margin: auto 0; text-align: center; width: 100%;">
                            <div class="dish-card-title">${dish.name}</div>
                            ${alertHtml}
                        </div>
                        <div class="dish-card-footer">
                            ${isOutOfStock 
                                ? `<div class="dish-card-price-pill" style="background: linear-gradient(135deg, #ef4444, #b91c1c); border-color: #f87171; box-shadow: 0 2px 6px rgba(239, 68, 68, 0.4);">Rupture</div>`
                                : `<div class="dish-card-price-pill">${Math.round(dish.price).toLocaleString('fr-FR')}FCFA</div>`
                            }
                        </div>
                    </div>
                `;
            }).join('');
        }

        function addToCart(dishId) {
            const dish = allDishes.find(d =>d.id === dishId);
            if (!dish) return;

            const stock = (dish.available_quantity !== undefined && dish.available_quantity !== null) ? (parseInt(dish.available_quantity) || 0) : 0;

            if (stock <= 0 || !dish.is_available) {
                alert(` MANQUE DE PRODUIT / RUPTURE DE STOCK !\n\nIl n'y a plus aucun plat, dessert ou boisson « ${dish.name} » disponible actuellement dans le restaurant.\n\nCe produit est entièrement épuisé (Stock: 0). L'administrateur doit entrer de nouveaux stocks pour permettre sa vente.`);
                return;
            }

            const existingIndex = cart.findIndex(item =>item.dish.id === dishId);
            const currentQty = existingIndex >=0 ? cart[existingIndex].quantity : 0;

            if (currentQty + 1 >stock) {
                alert(` STOCK INSUFFISANT !\n\nSeulement ${stock} « ${dish.name} » présent(s) dans le restaurant.\nVous en avez déjà ${currentQty} dans votre panier.`);
                return;
            }

            if (existingIndex >=0) {
                cart[existingIndex].quantity += 1;
            } else {
                cart.push({
                    dish: dish,
                    quantity: 1,
                    unit_price: dish.price
                });
            }

            renderCart();
            calculateChangeLive();
        }

        function updateCartQuantity(index, delta) {
            if (cart[index]) {
                const dish = cart[index].dish;
                const stock = (dish.available_quantity !== undefined && dish.available_quantity !== null) ? (parseInt(dish.available_quantity) || 0) : 0;
                if (delta >0 && cart[index].quantity + delta >stock) {
                    alert(` Stock maximal atteint pour « ${dish.name} » !\n\nIl n'y a que ${stock} unité(s) présente(s) dans le restaurant.`);
                    return;
                }
                cart[index].quantity += delta;
                if (cart[index].quantity <= 0) {
                    cart.splice(index, 1);
                }
                renderCart();
                calculateChangeLive();
            }
        }

        function updateCartItemPrice(index, newPrice) {
            if (cart[index]) {
                const parsed = parseFloat(newPrice);
                cart[index].unit_price = isNaN(parsed) || parsed < 0 ? 0 : parsed;
                renderCart();
                calculateChangeLive();
            }
        }

        function removeFromCart(index) {
            if (cart[index]) {
                cart.splice(index, 1);
                renderCart();
                calculateChangeLive();
            }
        }

        function clearCart() {
            cart = [];
            document.getElementById('posAmountTendered').value = '';
            renderCart();
            calculateChangeLive();
        }

        function calculateCartTotal() {
            return cart.reduce((sum, it) =>sum + (it.unit_price * it.quantity), 0);
        }

        function renderCart() {
            const container = document.getElementById('cartItemsContainer');
            const totalElem = document.getElementById('posCartTotal');
            if (!container || !totalElem) return;

            if (cart.length === 0) {
                container.innerHTML = `
                    <div style="text-align: center; color: var(--text-muted); font-size: 0.85rem; padding: 2rem 0;">
                        Panier vide.<br>Cliquezsur une carte carrée pour ajouter un plat.
                    </div>
                `;
                totalElem.innerText = '0 FCFA';
                return;
            }

            const total = calculateCartTotal();
            totalElem.innerText = Math.round(total).toLocaleString('fr-FR') + ' FCFA';

            container.innerHTML = cart.map((item, idx) => {
                const subtotal = item.unit_price * item.quantity;
                const maxStock = (item.dish.available_quantity !== undefined && item.dish.available_quantity !== null) ? parseInt(item.dish.available_quantity) : 0;
                return `
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.6rem 0; border-bottom: 1px solid rgba(255,255,255,0.05); gap: 0.5rem;">
                        <div style="flex: 1; min-width: 0;">
                            <div style="font-weight: 700; font-size: 0.85rem; color: white; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                                ${item.dish.name}
                            </div>
                            <div style="font-size: 0.7rem; color: #94a3b8; margin-top: 1px;">
                                Stock resto dispo : <strong style="color: ${maxStock <= 3 ? '#fbbf24' : '#34d399'};">${maxStock}</strong>
                            </div>
                            <div style="display: flex; align-items: center; gap: 0.35rem; margin-top: 0.25rem;">
                                <input type="number" step="50" min="0" value="${item.unit_price}" onchange="updateCartItemPrice(${idx}, this.value)" style="width: 80px; padding: 0.2rem 0.4rem; font-size: 0.75rem; background: var(--bg); border: 1px solid var(--border); border-radius: 4px; color: #34d399; font-weight: bold; text-align: right;" title="Prix unitaire modifiable par le gérant" />
                                <span style="font-size: 0.75rem; color: var(--text-muted);">FCFA</span>
                            </div>
                        </div>

                        <div style="display: flex; align-items: center; gap: 0.35rem;">
                            <button type="button" class="btn btn-secondary" style="padding: 0.2rem 0.5rem; font-size: 0.75rem;" onclick="updateCartQuantity(${idx}, -1)">-</button>
                            <span style="font-weight: bold; font-size: 0.85rem; min-width: 20px; text-align: center;">${item.quantity}</span>
                            <button type="button" class="btn btn-secondary" style="padding: 0.2rem 0.5rem; font-size: 0.75rem;" onclick="updateCartQuantity(${idx}, 1)">+</button>
                        </div>

                        <div style="text-align: right; min-width: 75px;">
                            <div style="font-weight: 800; font-size: 0.85rem; color: white;">
                                ${Math.round(subtotal).toLocaleString('fr-FR')} F
                            </div>
                            <button type="button" onclick="removeFromCart(${idx})" style="background: none; border: none; color: #f87171; font-size: 0.7rem; cursor: pointer;">Supprimer</button>
                        </div>
                    </div>
                `;
            }).join('');
        }

        function selectPaymentMethod(method, btnElem) {
            currentPaymentMethod = method;
            document.querySelectorAll('.pay-method-btn').forEach(b =>b.classList.remove('active'));
            if (btnElem) btnElem.classList.add('active');
            calculateChangeLive();
        }

        function setExactAmount() {
            const total = calculateCartTotal();
            const input = document.getElementById('posAmountTendered');
            if (input) {
                input.value = total >0 ? total : '';
                calculateChangeLive();
            }
        }

        function addShortcutAmount(amount) {
            const input = document.getElementById('posAmountTendered');
            if (input) {
                input.value = amount;
                calculateChangeLive();
            }
        }

        function calculateChangeLive() {
            const total = calculateCartTotal();
            const tenderedInput = document.getElementById('posAmountTendered');
            const tendered = parseFloat(tenderedInput ? tenderedInput.value : 0) || 0;
            const indicator = document.getElementById('posChangeIndicator');
            const btn = document.getElementById('btnValidateSale');
            if (!indicator || !btn) return;

            if (cart.length === 0) {
                indicator.innerHTML = '<span style="color: var(--text-muted); font-size: 0.85rem;">Paniervide. Ajoutez des plats.</span>';
                indicator.style.background = 'transparent';
                indicator.style.border = 'none';
                btn.disabled = true;
                return;
            }

            if (currentPaymentMethod !== 'Espèces (Cash)') {
                indicator.innerHTML = `<span style="color: #60a5fa; font-size: 0.95rem;">Règlement électronique (${currentPaymentMethod}) : <strong>${Math.round(total).toLocaleString('fr-FR')}FCFA</strong></span>`;
                indicator.style.background = 'rgba(59, 130, 246, 0.15)';
                indicator.style.border = '1px solid rgba(59, 130, 246, 0.4)';
                btn.disabled = false;
                return;
            }

            if (tendered === 0) {
                indicator.innerHTML = '<span style="color: var(--text-muted); font-size: 0.85rem;">Saisissezle montant remis par le client</span>';
                indicator.style.background = 'transparent';
                indicator.style.border = 'none';
                btn.disabled = true;
            } else if (tendered < total) {
                const diff = total - tendered;
                indicator.innerHTML = `<span style="color: #f87171; font-size: 0.95rem;">Montant insuffisant ! Reste à payer : <strong>${Math.round(diff).toLocaleString('fr-FR')}FCFA</strong></span>`;
                indicator.style.background = 'rgba(239, 68, 68, 0.2)';
                indicator.style.border = '1px solid rgba(239, 68, 68, 0.5)';
                btn.disabled = true;
            } else if (tendered === total) {
                indicator.innerHTML = `<span style="color: #34d399; font-size: 0.95rem;">Compte exact ! Aucune monnaie à rendre (0 FCFA)</span>`;
                indicator.style.background = 'rgba(16, 185, 129, 0.15)';
                indicator.style.border = '1px solid rgba(16, 185, 129, 0.4)';
                btn.disabled = false;
            } else {
                const change = tendered - total;
                indicator.innerHTML = `<span style="color: #34d399; font-size: 1.05rem;">Monnaie à rendre au client : <strong>${Math.round(change).toLocaleString('fr-FR')}FCFA</strong></span>`;
                indicator.style.background = 'rgba(16, 185, 129, 0.2)';
                indicator.style.border = '1px solid #10b981';
                btn.disabled = false;
            }
        }

        async function handleValidateSale() {
            if (cart.length === 0) return;
            const total = calculateCartTotal();
            const tendered = parseFloat(document.getElementById('posAmountTendered').value) || total;
            
            if (currentPaymentMethod === 'Espèces (Cash)' && tendered < total) {
                alert("Le montant remis par le client est insuffisant !");
                return;
            }

            const change = Math.max(0, tendered - total);
            const tableId = document.getElementById('posTableSelect').value || null;

            const payload = {
                table_id: tableId ? parseInt(tableId) : null,
                items: cart.map(it =>({
                    menu_item_id: it.dish.id,
                    quantity: it.quantity,
                    custom_price: it.unit_price,
                    notes: null
                })),
                manager_name: currentUser ? currentUser.full_name : "Gérant",
                manager_login: currentUser ? currentUser.username : "gerant",
                payment_method: currentPaymentMethod,
                tendered_amount: tendered,
                change_amount: change
            };

            const btn = document.getElementById('btnValidateSale');
            btn.disabled = true;
            btn.innerText = " Enregistrement & Synchronisation...";

            try {
                const res = await fetch('/api/v1/orders/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + token
                    },
                    body: JSON.stringify(payload)
                });
                const orderData = await res.json();
                if (!res.ok) {
                    throw new Error(orderData.detail || "Erreur lors de la validation");
                }

                // Décrémenter immédiatement le stock en direct pour un affichage instantané
                payload.items.forEach(sold => {
                    const dishObj = allDishes.find(d =>d.id === sold.menu_item_id);
                    if (dishObj) {
                        const curQty = (dishObj.available_quantity !== undefined && dishObj.available_quantity !== null) ? parseInt(dishObj.available_quantity) : 0;
                        dishObj.available_quantity = Math.max(0, curQty - sold.quantity);
                        if (dishObj.available_quantity <= 0) {
                            dishObj.is_available = false;
                        }
                    }
                });
                renderDishesGrid();

                // Afficher le Reçu de Caisse
                showReceiptModal(orderData, [...cart], total, tendered, change, currentPaymentMethod);

                // Réinitialiser le panier
                cart = [];
                document.getElementById('posAmountTendered').value = '';
                renderCart();
                calculateChangeLive();

                // Rafraîchir les commandes récentes et tables
                await loadManagerData();
            } catch (err) {
                alert("Erreur lors de l'encaissement : " + err.message);
            } finally {
                btn.disabled = false;
                btn.innerText = " Valider la Vente & Imprimer le Reçu";
            }
        }

        function showReceiptModal(order, savedCart, total, tendered, change, method) {
            // S'assurer que le nom, slogan, logo et coordonnées du restaurant sont à jour
            const rName = (restaurantConfig && restaurantConfig.restaurant_name) || "Lemo Daje Restaurant";
            const rSub = (restaurantConfig && restaurantConfig.restaurant_subtitle) || "TICKET DE CAISSE & REÇU CLIENT";
            const recName = document.getElementById('recRestoName');
            if (recName) recName.innerText = rName;
            const recSub = document.getElementById('recRestoSub');
            if (recSub) recSub.innerText = rSub;
            
            const recLogo = document.getElementById('recRestoLogoBox');
            if (recLogo) {
                if (restaurantConfig && restaurantConfig.logo_url) {
                    recLogo.innerHTML = `<img src="${restaurantConfig.logo_url}" style="max-height: 48px; max-width: 130px; object-fit: contain; margin-bottom: 4px;" alt="Logo" />`;
                } else {
                    recLogo.innerHTML = '';
                }
            }
            const recMeta = document.getElementById('recRestoMeta');
            if (recMeta && restaurantConfig) {
                const parts = [];
                if (restaurantConfig.ifu || restaurantConfig.nif) parts.push(`IFU: ${restaurantConfig.ifu || restaurantConfig.nif}`);
                if (restaurantConfig.rccm) parts.push(`RCCM: ${restaurantConfig.rccm}`);
                if (restaurantConfig.phone) parts.push(`Tél: ${restaurantConfig.phone}`);
                if (restaurantConfig.email) parts.push(`Email: ${restaurantConfig.email}`);
                if (restaurantConfig.address) parts.push(`Adresse: ${restaurantConfig.address}`);
                if (restaurantConfig.website) parts.push(`Site: ${restaurantConfig.website}`);
                recMeta.innerText = parts.join(' • ');
            }

            document.getElementById('recOrderNum').innerText = order.order_number;
            document.getElementById('recOrderDate').innerText = new Date(order.created_at || Date.now()).toLocaleDateString('fr-FR');
            document.getElementById('recManagerName').innerText = currentUser ? currentUser.full_name : 'Gérant';
            document.getElementById('recManagerLogin').innerText = currentUser ? currentUser.username : 'gerant';
            
            const tableSelect = document.getElementById('posTableSelect');
            const tableName = (tableSelect && tableSelect.selectedIndex >=0) ? tableSelect.options[tableSelect.selectedIndex].text : 'À Emporter';
            document.getElementById('recTableName').innerText = tableName;

            const itemsContainer = document.getElementById('recItemsList');
            itemsContainer.innerHTML = savedCart.map(it => `
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                    <span>${it.quantity}x ${it.dish.name}(@ ${Math.round(it.unit_price).toLocaleString('fr-FR')})</span>
                    <strong>${Math.round(it.unit_price *it.quantity).toLocaleString('fr-FR')} FCFA</strong>
                </div>
            `).join('');

            document.getElementById('recTotalAmount').innerText = Math.round(total).toLocaleString('fr-FR') + ' FCFA';
            document.getElementById('recPaymentMethod').innerText = method;
            document.getElementById('recAmountTendered').innerText = Math.round(tendered).toLocaleString('fr-FR') + ' FCFA';
            document.getElementById('recChangeAmount').innerText = Math.round(change).toLocaleString('fr-FR') + ' FCFA';

            document.getElementById('receiptModal').classList.remove('hidden');
        }

        function closeReceiptModal() {
            document.getElementById('receiptModal').classList.add('hidden');
        }

        // --- GESTION DE LA CONFIGURATION DU RESTAURANT & DGI (100% DYNAMIQUE DEPUIS LA BASE DE DONNÉES) ---
        let restaurantConfig = null;

        // Générateur d'URL QR Code Haute Définition
        function getDgiQrCodeUrl(dataStr, size = 130) {
            return `https://api.qrserver.com/v1/create-qr-code/?size=${size}x${size}&margin=2&data=` + encodeURIComponent(dataStr);
        }

        // Rendu officiel du sceau et QR Code DGI d'approbation
        function renderDgiQrCodeStamp(targetElementId, qrData, refCode) {
            const el = document.getElementById(targetElementId);
            if (!el) return;
            const url = getDgiQrCodeUrl(qrData, 140);
            el.innerHTML = `
                <img src="${url}" 
                     alt="QR Approbation DGI" 
                     style="width: 100%; height: 100%; object-fit: contain; display: block;" 
                     onerror="this.onerror=null; this.parentElement.innerHTML='<div style=\\'display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;font-size:0.65rem;color:#047857;text-align:center;font-weight:bold;line-height:1.2;\\'><span style=\\'font-size:1.3rem;\\'></span><span>APPROBATIONDGI</span><span style=\\'font-size:0.58rem;font-family:monospace;\\'>${refCode || 'CERTIFIÉE'}</span></div>';" 
                />
            `;
        }

        async function loadRestaurantConfig() {
            try {
                const url = (token && currentUser && currentUser.role === 'admin') 
                    ? '/api/v1/admin/settings' 
                    : '/api/v1/settings';
                const headers = token ? { 'Authorization': 'Bearer ' + token } : {};
                const res = await fetch(url, { headers });
                if (res.ok) {
                    restaurantConfig = await res.json();
                    applyRestaurantConfigUI();
                }
            } catch (e) {
                console.error("Erreur chargement configuration restaurant", e);
            }
        }

        // Prévisualisation en direct de l'en-tête officiel dans l'onglet Configuration
        function updateConfigLivePreview() {
            const rName = (document.getElementById('cfgRestoName') ? document.getElementById('cfgRestoName').value.trim() : '') || (restaurantConfig ? restaurantConfig.restaurant_name : '') || "ÉTABLISSEMENT";
            const rSub = (document.getElementById('cfgRestoSub') ? document.getElementById('cfgRestoSub').value.trim() : '') || (restaurantConfig ? restaurantConfig.restaurant_subtitle : '') || "";
            const ifu = (document.getElementById('cfgIfu') ? document.getElementById('cfgIfu').value.trim() : '') || (restaurantConfig ? (restaurantConfig.ifu || restaurantConfig.nif) : '') || "-";
            const rccm = (document.getElementById('cfgRccm') ? document.getElementById('cfgRccm').value.trim() : '') || (restaurantConfig ? restaurantConfig.rccm : '') || "-";
            const regime = (document.getElementById('cfgTaxRegime') ? document.getElementById('cfgTaxRegime').value.trim() : '') || (restaurantConfig ? restaurantConfig.default_tax_regime : '') || "-";
            const division = (document.getElementById('cfgFiscalDivision') ? document.getElementById('cfgFiscalDivision').value.trim() : '') || (restaurantConfig ? (restaurantConfig.fiscal_division || restaurantConfig.tax_center) : '') || "-";
            const phone = (document.getElementById('cfgPhone') ? document.getElementById('cfgPhone').value.trim() : '') || (restaurantConfig ? restaurantConfig.phone : '') || "-";
            const address = (document.getElementById('cfgAddress') ? document.getElementById('cfgAddress').value.trim() : '') || (restaurantConfig ? restaurantConfig.address : '') || "-";
            const email = (document.getElementById('cfgEmail') ? document.getElementById('cfgEmail').value.trim() : '') || (restaurantConfig ? restaurantConfig.email : '') || "-";
            const logoVal = (document.getElementById('cfgLogoUrl') ? document.getElementById('cfgLogoUrl').value.trim() : '') || (restaurantConfig ? restaurantConfig.logo_url : '');

            // Mettre à jour les champs de texte
            const prevRName = document.getElementById('prevRestoName');
            if (prevRName) prevRName.innerText = rName;
            const prevRSub = document.getElementById('prevRestoSub');
            if (prevRSub) prevRSub.innerText = rSub;
            const prevIfu = document.getElementById('prevIfu');
            if (prevIfu) prevIfu.innerText = ifu;
            const prevRccm = document.getElementById('prevRccm');
            if (prevRccm) prevRccm.innerText = rccm;
            const prevRegime = document.getElementById('prevRegime');
            if (prevRegime) prevRegime.innerText = regime;
            const prevDivision = document.getElementById('prevDivision');
            if (prevDivision) prevDivision.innerText = division;
            const prevPhone = document.getElementById('prevPhone');
            if (prevPhone) prevPhone.innerText = phone;
            const prevAddress = document.getElementById('prevAddress');
            if (prevAddress) prevAddress.innerText = address;
            const prevEmail = document.getElementById('prevEmail');
            if (prevEmail) prevEmail.innerText = email;

            // Logo dans l'aperçu
            const prevLogo = document.getElementById('prevLogoBox');
            if (prevLogo) {
                if (logoVal) {
                    prevLogo.innerHTML = `<img src="${logoVal}" style="max-width: 65px; max-height: 65px; object-fit: contain;" alt="Logo" onerror="this.onerror=null; this.parentElement.innerHTML='';" />`;
                } else {
                    prevLogo.innerHTML = `<span style="font-size: 1.8rem;"></span>`;
                }
            }

            // QR Code Toujours En Haut dans l'aperçu DGI
            const qrData = `DGI-FNE|APPROBATION:VALIDEE|IFU:${ifu}|RCCM:${rccm}|REGIME:${regime}|DIVISION:${division}|RESTO:${rName}|TEL:${phone}|EMAIL:${email}|STATUT:CERTIFIEE_DGI|SCEAU:SHA256_OFFICIEL_OK`;
            renderDgiQrCodeStamp('prevQrCodeBox', qrData, 'DGI-CERT-OK');
        }

        function applyRestaurantConfigUI() {
            if (!restaurantConfig) return;

            // Titre officiel de l'application
            if (restaurantConfig.restaurant_name) {
                document.title = restaurantConfig.restaurant_name + " - Gestion & Caisse";
            }

            // En-tête globale du logiciel (Logo + Nom du Restaurant)
            const headerName = document.getElementById('headerBrandName');
            if (headerName) headerName.innerText = restaurantConfig.restaurant_name || "Restaurant Engine";

            const headerLogo = document.getElementById('headerBrandLogo');
            if (headerLogo) {
                if (restaurantConfig.logo_url) {
                    headerLogo.innerHTML = `<img src="${restaurantConfig.logo_url}" style="height: 28px; width: auto; max-width: 45px; object-fit: contain; vertical-align: middle; border-radius: 4px;" alt="Logo" />`;
                } else {
                    headerLogo.innerHTML = ``;
                }
            }

            // Sidebar Navigation Admin (Gauche)
            const sideName = document.getElementById('sideRestoName');
            if (sideName) sideName.innerText = restaurantConfig.restaurant_name || "Lemo Daje Restaurant";
            const sideSub = document.getElementById('sideRestoSub');
            if (sideSub) sideSub.innerText = restaurantConfig.restaurant_subtitle || "Supervision Générale";
            const sideLogo = document.getElementById('sideRestoLogo');
            if (sideLogo) {
                if (restaurantConfig.logo_url) {
                    sideLogo.innerHTML = `<img src="${restaurantConfig.logo_url}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 9px;" alt="Logo" onerror="this.onerror=null; this.parentElement.innerHTML='';" />`;
                } else {
                    sideLogo.innerHTML = ``;
                }
            }

            // Ticket de Caisse Client (Modal Reçu)
            const recName = document.getElementById('recRestoName');
            if (recName) recName.innerText = restaurantConfig.restaurant_name || "Lemo Daje Restaurant";
            const recSub = document.getElementById('recRestoSub');
            if (recSub) recSub.innerText = restaurantConfig.restaurant_subtitle || "TICKET DE CAISSE & REÇU CLIENT";
            const recLogo = document.getElementById('recRestoLogoBox');
            if (recLogo) {
                if (restaurantConfig.logo_url) {
                    recLogo.innerHTML = `<img src="${restaurantConfig.logo_url}" style="max-height: 48px; max-width: 130px; object-fit: contain; margin-bottom: 4px;" alt="Logo" />`;
                } else {
                    recLogo.innerHTML = '';
                }
            }
            const recMeta = document.getElementById('recRestoMeta');
            if (recMeta) {
                const parts = [];
                if (restaurantConfig.ifu || restaurantConfig.nif) parts.push(`IFU: ${restaurantConfig.ifu || restaurantConfig.nif}`);
                if (restaurantConfig.rccm) parts.push(`RCCM: ${restaurantConfig.rccm}`);
                if (restaurantConfig.phone) parts.push(`Tél: ${restaurantConfig.phone}`);
                if (restaurantConfig.email) parts.push(`Email: ${restaurantConfig.email}`);
                if (restaurantConfig.address) parts.push(`Adresse: ${restaurantConfig.address}`);
                if (restaurantConfig.website) parts.push(`Site: ${restaurantConfig.website}`);
                recMeta.innerText = parts.join(' • ');
            }

            // Récapitulatif sur l'accueil Admin
            const ovName = document.getElementById('overviewRestoName');
            if (ovName) ovName.innerText = restaurantConfig.restaurant_name;
            const ovIfu = document.getElementById('overviewIfu');
            if (ovIfu) ovIfu.innerText = restaurantConfig.ifu || restaurantConfig.nif || '-';
            const ovNif = document.getElementById('overviewNif');
            if (ovNif) ovNif.innerText = restaurantConfig.ifu || restaurantConfig.nif || '-';
            const ovNim = document.getElementById('overviewNim');
            if (ovNim) ovNim.innerText = restaurantConfig.nim || '-';
            const ovRccm = document.getElementById('overviewRccm');
            if (ovRccm) ovRccm.innerText = restaurantConfig.rccm || '-';
            const ovRegime = document.getElementById('overviewTaxRegime');
            if (ovRegime) ovRegime.innerText = restaurantConfig.default_tax_regime || "Régime du Réel Normal d'Imposition (RNI)";
            const ovDivision = document.getElementById('overviewFiscalDivision');
            if (ovDivision) ovDivision.innerText = restaurantConfig.fiscal_division || restaurantConfig.tax_center || '-';
            const ovTaxCenter = document.getElementById('overviewTaxCenter');
            if (ovTaxCenter) ovTaxCenter.innerText = restaurantConfig.fiscal_division || restaurantConfig.tax_center || '-';
            const ovTaxRate = document.getElementById('overviewTaxRate');
            if (ovTaxRate) ovTaxRate.innerText = (restaurantConfig.tax_rate || 18) + '%';
            const ovAddress = document.getElementById('overviewAddress');
            if (ovAddress) ovAddress.innerText = restaurantConfig.address || '-';
            const ovPhone = document.getElementById('overviewPhone');
            if (ovPhone) ovPhone.innerText = restaurantConfig.phone || '-';
            const ovEmail = document.getElementById('overviewEmail');
            if (ovEmail) ovEmail.innerText = restaurantConfig.email || '-';


            // Formulaire de configuration Admin
            const inpName = document.getElementById('cfgRestoName');
            if (inpName) inpName.value = restaurantConfig.restaurant_name || '';
            const inpSub = document.getElementById('cfgRestoSub');
            if (inpSub) inpSub.value = restaurantConfig.restaurant_subtitle || '';
            const inpLogo = document.getElementById('cfgLogoUrl');
            if (inpLogo) inpLogo.value = restaurantConfig.logo_url || '';
            
            const inpIfu = document.getElementById('cfgIfu');
            if (inpIfu) inpIfu.value = restaurantConfig.ifu || restaurantConfig.nif || '';
            const inpNif = document.getElementById('cfgNif');
            if (inpNif) inpNif.value = restaurantConfig.nif || restaurantConfig.ifu || '';

            const inpRccm = document.getElementById('cfgRccm');
            if (inpRccm) inpRccm.value = restaurantConfig.rccm || '';
            
            const inpRegime = document.getElementById('cfgTaxRegime');
            if (inpRegime) inpRegime.value = restaurantConfig.default_tax_regime || "Régime du Réel Normal d'Imposition (RNI)";

            const inpDivision = document.getElementById('cfgFiscalDivision');
            if (inpDivision) inpDivision.value = restaurantConfig.fiscal_division || restaurantConfig.tax_center || '';
            const inpCenter = document.getElementById('cfgTaxCenter');
            if (inpCenter) inpCenter.value = restaurantConfig.tax_center || restaurantConfig.fiscal_division || '';

            const inpNim = document.getElementById('cfgNim');
            if (inpNim) inpNim.value = restaurantConfig.nim || '';
            const inpRate = document.getElementById('cfgTaxRate');
            if (inpRate) inpRate.value = restaurantConfig.tax_rate || 18;
            const inpLegal = document.getElementById('cfgLegalMention');
            if (inpLegal) inpLegal.value = restaurantConfig.legal_mention || '';
            const inpAddr = document.getElementById('cfgAddress');
            if (inpAddr) inpAddr.value = restaurantConfig.address || '';
            const inpPhone = document.getElementById('cfgPhone');
            if (inpPhone) inpPhone.value = restaurantConfig.phone || '';
            const inpEmail = document.getElementById('cfgEmail');
            if (inpEmail) inpEmail.value = restaurantConfig.email || '';
            const inpWeb = document.getElementById('cfgWebsite');
            if (inpWeb) inpWeb.value = restaurantConfig.website || '';

            updateLogoPreview();
            updateConfigLivePreview();
        }

        function updateLogoPreview() {
            const previewBox = document.getElementById('cfgLogoPreviewBox');
            if (!previewBox) return;
            const inputVal = (document.getElementById('cfgLogoUrl') ? document.getElementById('cfgLogoUrl').value.trim() : '') || (restaurantConfig ? restaurantConfig.logo_url : '');
            if (inputVal) {
                previewBox.innerHTML = `<img src="${inputVal}" style="max-width: 110px; max-height: 110px; object-fit: contain;" alt="Logo Preview" onerror="this.onerror=null; this.parentElement.innerHTML='<span style=\\'color:#ef4444; font-size:0.75rem;\\'>Imageinvalide</span>';" />`;
            } else {
                previewBox.innerHTML = `
                    <div style="text-align: center; color: #8a7561;">
                        <div style="font-size: 0.65rem; font-weight: 800; letter-spacing: 0.08em;">RESTO</div>
                        <div style="font-size: 1.6rem; line-height: 1.2;"></div>
                        <div style="font-size: 0.6rem; font-weight: 800;">EST.</div>
                    </div>
                `;
            }
        }

        function resetLogoToDefault() {
            const inp = document.getElementById('cfgLogoUrl');
            if (inp) inp.value = '';
            const fileInp = document.getElementById('cfgLogoFileInput');
            if (fileInp) fileInp.value = '';
            if (restaurantConfig) restaurantConfig.logo_url = '';
            updateLogoPreview();
            updateConfigLivePreview();
        }

        function handleLogoFileUpload(e) {
            const file = e.target.files[0];
            if (!file) return;
            if (file.size >3 * 1024 * 1024) {
                alert("L'image sélectionnée est trop volumineuse (maximum 3 Mo).");
                return;
            }
            const reader = new FileReader();
            reader.onload = function(evt) {
                const base64Data = evt.target.result;
                const urlInp = document.getElementById('cfgLogoUrl');
                if (urlInp) urlInp.value = base64Data;
                updateLogoPreview();
                updateConfigLivePreview();
            };
            reader.readAsDataURL(file);
        }

        async function handleSaveSettings(e) {
            e.preventDefault();
            const msg = document.getElementById('cfgSaveMsg');
            if (msg) msg.innerHTML = '<span style="color: var(--text-muted);">Enregistrementen cours...</span>';

            const ifuVal = (document.getElementById('cfgIfu') ? document.getElementById('cfgIfu').value.trim() : '') || (document.getElementById('cfgNif') ? document.getElementById('cfgNif').value.trim() : '');
            const divisionVal = (document.getElementById('cfgFiscalDivision') ? document.getElementById('cfgFiscalDivision').value.trim() : '') || (document.getElementById('cfgTaxCenter') ? document.getElementById('cfgTaxCenter').value.trim() : '');

            const payload = {
                restaurant_name: document.getElementById('cfgRestoName').value.trim(),
                restaurant_subtitle: document.getElementById('cfgRestoSub').value.trim(),
                logo_url: document.getElementById('cfgLogoUrl').value.trim(),
                ifu: ifuVal,
                nif: ifuVal,
                rccm: document.getElementById('cfgRccm').value.trim(),
                default_tax_regime: document.getElementById('cfgTaxRegime').value.trim(),
                fiscal_division: divisionVal,
                tax_center: divisionVal,
                nim: document.getElementById('cfgNim').value.trim(),
                tax_rate: parseFloat(document.getElementById('cfgTaxRate').value) || 18.0,
                legal_mention: document.getElementById('cfgLegalMention').value.trim(),
                address: document.getElementById('cfgAddress').value.trim(),
                phone: document.getElementById('cfgPhone').value.trim(),
                email: document.getElementById('cfgEmail').value.trim(),
                website: document.getElementById('cfgWebsite').value.trim()
            };

            try {
                const res = await fetch('/api/v1/admin/settings', {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + token
                    },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if (!res.ok) throw new Error(data.detail || "Erreur de sauvegarde");

                restaurantConfig = data;
                applyRestaurantConfigUI();
                if (msg) msg.innerHTML = '<span style="color: #34d399;">Configuration et Approbation DGI enregistrées avec succès ! En-têtes et Factures actualisés.</span>';
                setTimeout(() => {if (msg) msg.innerHTML = ''; }, 4500);
            } catch (err) {
                if (msg) msg.innerHTML = '<span style="color: var(--danger);">' +err.message + '</span>';
            }
        }


        function switchAdminTab(tab) {
            const tabs = ['overview', 'globalInvoices', 'invoices', 'managers', 'menu', 'config', 'chat'];
            tabs.forEach(t => {
                const btn = document.getElementById('admTabBtn' + t.charAt(0).toUpperCase() + t.slice(1));
                const sec = document.getElementById('admSection' + t.charAt(0).toUpperCase() + t.slice(1));
                if (btn) btn.classList.toggle('active', t === tab);
                if (sec) sec.classList.toggle('hidden', t !== tab);
            });
            if (tab === 'overview') {
                loadAdminData();
                loadSessionsData();
            } else if (tab === 'globalInvoices') {
                loadGlobalInvoicesData();
            } else if (tab === 'invoices') {
                loadAdminOrdersData();
            } else if (tab === 'managers') {
                loadAdminData();
                loadSessionsData();
                loadActivityLogsData();
            } else if (tab === 'menu') {
                loadAdminDishesData();
            } else if (tab === 'config') {
                loadRestaurantConfig();
            } else if (tab === 'chat') {
                initCommunicationChat('adm');
            }
        }

        // =========================================================================
        // MODULE : FACTURATION GLOBALE DYNAMIQUE & FISCALITÉ DGI (ADMIN)
        // =========================================================================
        let allGlobalInvoices = [];
        let currentDetailInvoice = null;
        let todayGlobalInvoice = null;
        let globalInvoicingPollerId = null;
        let activeDetInvoiceSubTab = 'lines';
        let lastLiveStatusHash = '';

        // Démarrer la surveillance en temps réel (Exigence 7)
        function startGlobalInvoicingRealtimePoller() {
            if (globalInvoicingPollerId) clearInterval(globalInvoicingPollerId);
            globalInvoicingPollerId = setInterval(async () => {
                if (!token) return;
                try {
                    const res = await fetch('/api/v1/billing/live-status', {
                        headers: { 'Authorization': 'Bearer ' + token }
                    });
                    if (!res.ok) return;
                    const live = await res.json();
                    const liveHash = `${live.current_invoice_id}_${live.current_invoice_sales_count}_${live.current_invoice_ttc}_${live.last_order_number}_${live.last_order_time}`;

                    if (!lastLiveStatusHash) {
                        lastLiveStatusHash = liveHash;
                    } else if (lastLiveStatusHash !== liveHash) {
                        lastLiveStatusHash = liveHash;
                        // Flasher le badge de synchronisation temps réel
                        const badge = document.getElementById('globBillingLiveBadge');
                        if (badge) {
                            badge.style.transform = 'scale(1.08)';
                            badge.style.background = 'rgba(16, 185, 129, 0.4)';
                            setTimeout(() => {
                                badge.style.transform = 'scale(1)';
                                badge.style.background = 'rgba(16, 185, 129, 0.2)';
                            }, 800);
                        }

                        // Actualiser la liste des factures globales et le registre des factures clients
                        loadGlobalInvoicesData();
                        loadAdminOrdersData();
                        loadAdminData();
                        loadSessionsData();

                        // Si le modal de la facture active est ouvert et non certifié, actualiser son contenu en temps réel
                        if (currentDetailInvoice && !currentDetailInvoice.is_certified && currentDetailInvoice.id === live.current_invoice_id) {
                            silentRefreshOpenGlobalInvoiceDetail(currentDetailInvoice.id);
                        }
                    }

                    // Rafraîchissement automatique des stocks en temps réel si l'administrateur est sur l'onglet Menu
                    const menuSec = document.getElementById('admSectionMenu');
                    if (menuSec && !menuSec.classList.contains('hidden')) {
                        await loadAdminDishesData();
                    }
                } catch(e) {
                    // Silencieux
                }
            }, 2500);
        }

        // Chargement des données de factures globales
        async function loadGlobalInvoicesData() {
            try {
                const res = await fetch('/api/v1/billing/global-invoices', {
                    headers: { 'Authorization': 'Bearer ' + token }
                });
                if (res.ok) {
                    allGlobalInvoices = await res.json();
                    renderGlobalInvoicesKPIs();
                    renderGlobalInvoicesTable();
                }

                // Récupérer la config pour le libellé de fréquence
                const resCfg = await fetch('/api/v1/billing/config', {
                    headers: { 'Authorization': 'Bearer ' + token }
                });
                if (resCfg.ok) {
                    const cfg = await resCfg.json();
                    const freqNames = { 'daily': 'Quotidienne (Jour)', 'weekly': 'Hebdomadaire (Semaine)', 'monthly': 'Mensuelle (Mois)' };
                    const lbl = document.getElementById('currentBillingFreqLabel');
                    if (lbl) lbl.innerText = freqNames[cfg.billing_frequency] || cfg.billing_frequency;
                }
            } catch (err) {
                console.error("Erreur chargement facturation globale:", err);
            }
        }

        // Rendu des KPIs du bandeau financier et de la Hero Card Facture du Jour
        function renderGlobalInvoicesKPIs() {
            let totalTTC = 0;
            let totalHT = 0;
            let totalTaxes = 0;
            let certCount = 0;
            let inProgCount = 0;

            allGlobalInvoices.forEach(inv => {
                totalTTC += inv.total_ttc || 0;
                totalHT += inv.total_ht || 0;
                totalTaxes += inv.total_taxes || 0;
                if (inv.is_certified) certCount++;
                else inProgCount++;
            });

            // Trouver la facture du jour (priorité à la facture active de la journée courante)
            const todayDateStr = new Date().toISOString().slice(0, 10);
            todayGlobalInvoice = allGlobalInvoices.find(inv => 
                inv.period_type === 'daily' && inv.period_start && inv.period_start.startsWith(todayDateStr)
            ) || allGlobalInvoices.find(inv =>inv.period_type === 'daily') || (allGlobalInvoices.length >0 ? allGlobalInvoices[0] : null);

            // Mettre à jour la Hero Card Facture du Jour & Certification DGI
            renderHeroDailyInvoiceCard(todayGlobalInvoice);

            const elRev = document.getElementById('globKpiRevenueTTC');
            if (elRev) elRev.innerText = Math.round(totalTTC).toLocaleString('fr-FR') + ' FCFA';
            const elHT = document.getElementById('globKpiBaseHT');
            if (elHT) elHT.innerText = Math.round(totalHT).toLocaleString('fr-FR') + ' FCFA';
            const elTax = document.getElementById('globKpiTotalTaxes');
            if (elTax) elTax.innerText = Math.round(totalTaxes).toLocaleString('fr-FR') + ' FCFA';
            const elCnt = document.getElementById('globKpiInvoicesCount');
            if (elCnt) elCnt.innerText = allGlobalInvoices.length;
            const elBrk = document.getElementById('globKpiInvoicesStatusBreakdown');
            if (elBrk) elBrk.innerText = `${certCount} certifiée(s) • ${inProgCount} en cours/prête(s)`;
        }

        // Rendu spécifique de la Hero Card Facture du Jour & Certification DGI (Exigence utilisateur)
        function renderHeroDailyInvoiceCard(inv) {
            const card = document.getElementById('heroDailyInvoiceCard');
            if (!card) return;

            const now = new Date();
            const dateStr = inv && (inv.opened_at || inv.period_start)
                ? new Date(inv.opened_at || inv.period_start).toLocaleDateString('fr-FR', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })
                : now.toLocaleDateString('fr-FR', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
            
            const mgrName = inv && inv.manager_name ? inv.manager_name : 'Gérant(s) en caisse';
            const num = inv ? inv.invoice_number : `FACT-GLOB-${now.getFullYear()}${String(now.getMonth()+1).padStart(2,'0')}${String(now.getDate()).padStart(2,'0')}`;
            const ttc = inv ? Math.round(inv.total_ttc || 0) : 0;
            const ht = inv ? Math.round(inv.total_ht || 0) : 0;
            const tva = inv ? Math.round(inv.total_taxes || 0) : 0;
            const salesCount = inv ? (inv.total_sales_count || 0) : 0;

            const elDate = document.getElementById('heroDailyDateText');
            if (elDate) elDate.innerText = dateStr.charAt(0).toUpperCase() + dateStr.slice(1);
            const elMgr = document.getElementById('heroDailyManagersText');
            if (elMgr) elMgr.innerText = mgrName;

            const elNum = document.getElementById('heroDailyNumberBadge');
            if (elNum) elNum.innerText = num;

            const elTTC = document.getElementById('heroDailyTotalTTC');
            if (elTTC) elTTC.innerText = ttc.toLocaleString('fr-FR') + ' FCFA';
            const elHT = document.getElementById('heroDailyTotalHT');
            if (elHT) elHT.innerText = ht.toLocaleString('fr-FR') + ' FCFA';
            const elTVA = document.getElementById('heroDailyTotalTVA');
            if (elTVA) elTVA.innerText = tva.toLocaleString('fr-FR') + ' FCFA';
            const elSales = document.getElementById('heroDailySalesCount');
            if (elSales) elSales.innerText = salesCount + (salesCount >1 ? ' ventes' : ' vente');

            const elBadge = document.getElementById('heroDailyStatusBadge');
            const elFisc = document.getElementById('heroDailyFiscRefText');
            const btnCertify = document.getElementById('heroBtnCertifyToday');

            if (inv && inv.is_certified) {
                if (elBadge) elBadge.innerHTML = '<span class="badge" style="background: rgba(16, 185, 129, 0.25); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.5); font-weight: 800;">FACTURE DÉJÀ CERTIFIÉE DGI</span>';
                if (elFisc) elFisc.innerHTML = `<span style="color: #34d399; font-weight: 700; font-family: monospace;">Réf : ${inv.dgi_fiscal_reference}</span>`;
                if (btnCertify) {
                    btnCertify.disabled = true;
                    btnCertify.style.opacity = '0.6';
                    btnCertify.innerHTML = '<span></span>Facture Déjà Certifiée';
                }
            } else if (salesCount === 0) {
                if (elBadge) elBadge.innerHTML = '<span class="badge" style="background: rgba(148, 163, 184, 0.25); color: #94a3b8; font-weight: 700;">En attente des premières ventes</span>';
                if (elFisc) elFisc.innerText = 'En attente des ventes des gérants';
                if (btnCertify) {
                    btnCertify.disabled = true;
                    btnCertify.style.opacity = '0.6';
                    btnCertify.innerHTML = '<span></span>En attente de ventes pour certifier';
                }
            } else {
                if (elBadge) elBadge.innerHTML = '<span class="badge" style="background: rgba(245, 158, 11, 0.25); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.5); font-weight: 800;">Prête pour certification DGI</span>';
                if (elFisc) elFisc.innerText = 'Tous les calculs DGI sont prêts et conformes';
                if (btnCertify) {
                    btnCertify.disabled = false;
                    btnCertify.style.opacity = '1';
                    btnCertify.innerHTML = '<span></span>Certifier la Facture du Jour (DGI)';
                }
            }
        }

        async function openTodayGlobalInvoiceDetail() {
            if (todayGlobalInvoice && todayGlobalInvoice.id) {
                await openGlobalInvoiceDetail(todayGlobalInvoice.id);
            } else {
                await generateNewGlobalInvoice();
                if (allGlobalInvoices.length >0) {
                    await openGlobalInvoiceDetail(allGlobalInvoices[0].id);
                }
            }
        }

        async function certifyTodayInvoiceDirectly() {
            if (todayGlobalInvoice && todayGlobalInvoice.id) {
                await openGlobalInvoiceDetail(todayGlobalInvoice.id);
                promptCertifyCurrentInvoice();
            } else {
                alert("Aucune vente enregistrée pour la journée. Dès que le gérant valide un encaissement, la facture est prête pour certification.");
            }
        }

        // Rendu du tableau des factures globales (Exigence 2)
        function renderGlobalInvoicesTable() {
            const tbody = document.getElementById('globalInvoicesTableBody');
            if (!tbody) return;

            const filterStatus = (document.getElementById('globFilterStatus')?.value || '').trim();
            const filterPeriod = (document.getElementById('globFilterPeriod')?.value || '').trim();
            const searchQ = (document.getElementById('globSearchInput')?.value || '').toLowerCase().trim();

            const filtered = allGlobalInvoices.filter(inv => {
                if (filterStatus && inv.status !== filterStatus) return false;
                if (filterPeriod && inv.period_type !== filterPeriod) return false;
                if (searchQ) {
                    const matchNum = (inv.invoice_number || '').toLowerCase().includes(searchQ);
                    const matchLabel = (inv.period_label || '').toLowerCase().includes(searchQ);
                    const matchAdmin = (inv.certified_by || '').toLowerCase().includes(searchQ);
                    const matchMgr = (inv.manager_name || '').toLowerCase().includes(searchQ) || (inv.manager_login || '').toLowerCase().includes(searchQ);
                    if (!matchNum && !matchLabel && !matchAdmin && !matchMgr) return false;
                }
                return true;
            });

            if (filtered.length === 0) {
                tbody.innerHTML = '<tr><td colspan="11" style="text-align: center; color: var(--text-muted); padding: 2.5rem;">Aucunefacture globale ne correspond aux filtres actuels.</td></tr>';
                return;
            }

            tbody.innerHTML = filtered.map(inv => {
                const statusBadge = getInvoiceStatusBadgeHTML(inv.status, inv.is_certified, inv.has_anomalies);
                const mgrBadge = inv.manager_name 
                    ? `<span class="badge" style="background: rgba(37, 99, 235, 0.2); color: #93c5fd; font-weight: 700; font-size: 0.85rem; border: 1px solid rgba(59, 130, 246, 0.3);"> ${inv.manager_name}</span>`
                    : `<span style="color: var(--text-muted); font-size: 0.85rem;">Global(Tous)</span>`;

                const openedAtStr = inv.opened_at 
                    ? new Date(inv.opened_at).toLocaleDateString('fr-FR')
                    : (inv.period_start ? new Date(inv.period_start).toLocaleDateString('fr-FR') : '-');

                const fiscRef = inv.dgi_fiscal_reference 
                    ? `<strong style="color: #34d399; font-family: monospace; font-size: 0.85rem;">${inv.dgi_fiscal_reference}</strong>`
                    : `<span style="color: var(--text-muted);">-</span>`;

                let taxesStr = 'TVA 18%';
                try {
                    const details = JSON.parse(inv.tax_details || '[]');
                    if (details.length >0) {
                        taxesStr = details.map(d => `${d.rule_name}(${d.rate}%)`).join(', ');
                    }
                } catch(e) {}

                return `
                    <tr>
                        <td>
                            <strong style="color: #fbbf24; font-family: monospace; font-size: 0.95rem;">${inv.invoice_number}</strong>
                        </td>
                        <td>${mgrBadge}</td>
                        <td style="font-size: 0.85rem; color: #cbd5e1;">${openedAtStr}</td>
                        <td>
                            <strong>${inv.period_label}</strong><br>
                            <small style="color: var(--text-muted); text-transform: capitalize;">Période ${inv.period_type}</small>
                        </td>
                        <td style="text-align: center;">
                            <span class="badge" style="background: rgba(99, 102, 241, 0.2); color: #a5b4fc; font-weight: 700; font-size: 0.85rem;">
                                ${inv.total_sales_count} ventes
                            </span>
                        </td>
                        <td style="text-align: right; font-weight: 600; color: #93c5fd;">
                            ${Math.round(inv.total_ht || 0).toLocaleString('fr-FR')} FCFA
                        </td>
                        <td style="text-align: right; color: #fbbf24;">
                            <div style="font-weight: 600;">${Math.round(inv.total_taxes ||0).toLocaleString('fr-FR')} FCFA</div>
                            <small style="color: var(--text-muted); font-size: 0.72rem;">${taxesStr}</small>
                        </td>
                        <td style="text-align: right;">
                            <strong style="color: #34d399; font-size: 1.05rem;">
                                ${Math.round(inv.total_ttc || 0).toLocaleString('fr-FR')} FCFA
                            </strong>
                        </td>
                        <td>${statusBadge}</td>
                        <td style="font-size: 0.85rem;">${fiscRef}</td>
                        <td style="text-align: center; white-space: nowrap;">
                            <button class="btn btn-secondary" onclick="openGlobalInvoiceDetail(${inv.id})" style="padding: 0.4rem 0.75rem; font-size: 0.8rem;" title="Consulter la facture détaillée">
                                 Ouvrir
                            </button>
                            <button class="btn btn-secondary" onclick="openGlobalInvoicePrintPreview(${inv.id})" style="padding: 0.4rem 0.75rem; font-size: 0.8rem; margin-left: 4px;" title="Aperçu officiel DGI">
                                 Aperçu
                            </button>
                            ${!inv.is_certified ? `
                                <button class="btn btn-primary" onclick="promptCertifyGlobalInvoice(${inv.id})" style="padding: 0.4rem 0.75rem; font-size: 0.8rem; margin-left: 4px; background: linear-gradient(135deg, #10b981, #059669); font-weight: bold;" title="Certifier avec la DGI">
                                     Certifier
                                </button>
                            ` : ''}
                        </td>
                    </tr>
                `;
            }).join('');
        }

        function filterGlobalInvoicesTable() {
            renderGlobalInvoicesTable();
        }

        function getInvoiceStatusBadgeHTML(status, isCertified, hasAnomalies) {
            if (isCertified || status === 'certified') {
                return '<span class="badge" style="background: rgba(16, 185, 129, 0.25); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.5); font-weight: 700;">Certifiée DGI</span>';
            }
            if (status === 'cancelled') {
                return '<span class="badge" style="background: rgba(239, 68, 68, 0.25); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.5);">Annulée</span>';
            }
            if (status === 'ready_for_certification') {
                return '<span class="badge" style="background: rgba(245, 158, 11, 0.25); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.5); font-weight: 700;">Prête pour certification</span>';
            }
            if (status === 'in_progress') {
                return '<span class="badge" style="background: rgba(59, 130, 246, 0.25); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.5);">En cours</span>';
            }
            return '<span class="badge" style="background: rgba(148, 163, 184, 0.25); color: #94a3b8; border: 1px solid rgba(148, 163, 184, 0.5);">Brouillon</span>';
        }

        // 2. Consultation détaillée de la facture globale (Exigences 3, 11, 12, 13, 14, 15, 16)
        async function openGlobalInvoiceDetail(invoiceId) {
            try {
                const res = await fetch(`/api/v1/billing/global-invoices/${invoiceId}`, {
                    headers: { 'Authorization': 'Bearer ' + token }
                });
                if (!res.ok) throw new Error("Impossible de charger le détail de la facture globale.");
                const inv = await res.json();
                currentDetailInvoice = inv;
                renderDetailModalContent(inv);
                document.getElementById('modalGlobalInvoiceDetail').classList.remove('hidden');
            } catch (err) {
                alert("Erreur: " + err.message);
            }
        }

        async function silentRefreshOpenGlobalInvoiceDetail(invoiceId) {
            try {
                const res = await fetch(`/api/v1/billing/global-invoices/${invoiceId}`, {
                    headers: { 'Authorization': 'Bearer ' + token }
                });
                if (res.ok) {
                    const inv = await res.json();
                    currentDetailInvoice = inv;
                    renderDetailModalContent(inv);
                }
            } catch(e) {}
        }

        function closeGlobalInvoiceDetailModal() {
            document.getElementById('modalGlobalInvoiceDetail').classList.add('hidden');
            currentDetailInvoice = null;
        }

        function switchDetInvoiceSubTab(subTab) {
            activeDetInvoiceSubTab = subTab;
            const tabs = ['lines', 'managers', 'taxes', 'audit'];
            tabs.forEach(t => {
                const btn = document.getElementById('detSubTabBtn' + t.charAt(0).toUpperCase() + t.slice(1));
                const sec = document.getElementById('detSubSec' + t.charAt(0).toUpperCase() + t.slice(1));
                if (btn) {
                    btn.classList.toggle('active', t === subTab);
                    if (t === subTab) {
                        btn.style.borderColor = '#f59e0b';
                        btn.style.color = '#fbbf24';
                    } else {
                        btn.style.borderColor = 'var(--border)';
                        btn.style.color = 'var(--text-main)';
                    }
                }
                if (sec) sec.classList.toggle('hidden', t !== subTab);
            });
        }

        // Rendu complet du contenu de la facture globale (Cases d'en-tête, Totaux, Lignes et Gérants)
        function renderDetailModalContent(inv) {
            // 0. Bandeau Date & Gérants en service (Exigence utilisateur : Date uniquement, aucune heure)
            const invDate = inv.opened_at || inv.period_start || inv.created_at;
            const elTopDate = document.getElementById('detTopInvoiceDate');
            if (elTopDate) {
                const dateText = invDate 
                    ? new Date(invDate).toLocaleDateString('fr-FR', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })
                    : new Date().toLocaleDateString('fr-FR', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
                elTopDate.innerText = dateText.charAt(0).toUpperCase() + dateText.slice(1);
            }
            const elTopMgr = document.getElementById('detTopInvoiceManagers');
            if (elTopMgr) {
                elTopMgr.innerText = inv.manager_name ? `${inv.manager_name} (${inv.manager_login || ''})` : 'Gérant(s) ayant effectué les ventes';
            }
            const elTopStatus = document.getElementById('detTopInvoiceStatusBadge');
            if (elTopStatus) {
                elTopStatus.innerHTML = getInvoiceStatusBadgeHTML(inv.status, inv.is_certified, inv.has_anomalies);
            }

            // 1. Cases d'En-tête & Mentions Légales
            const elNum = document.getElementById('detInvNumber');
            if (elNum) elNum.innerText = inv.invoice_number;
            
            const elPerLbl = document.getElementById('detInvPeriodLabel');
            if (elPerLbl) elPerLbl.innerText = inv.period_label;

            const dtStart = inv.period_start ? new Date(inv.period_start).toLocaleDateString('fr-FR') : '-';
            const dtEnd = inv.period_end ? new Date(inv.period_end).toLocaleDateString('fr-FR') : '-';
            const elDtStart = document.getElementById('detInvDateStart');
            if (elDtStart) elDtStart.innerText = dtStart;
            const elDtEnd = document.getElementById('detInvDateEnd');
            if (elDtEnd) elDtEnd.innerText = dtEnd;

            const elFreq = document.getElementById('detInvFrequencyBadge');
            if (elFreq) {
                const fMap = { 'daily': 'Quotidienne (Jour)', 'weekly': 'Hebdomadaire (Semaine)', 'monthly': 'Mensuelle (Mois)' };
                elFreq.innerText = fMap[inv.period_type] || inv.period_type;
            }

            const elMgr = document.getElementById('detInvManagerName');
            if (elMgr) elMgr.innerText = inv.manager_name ? `${inv.manager_name} (${inv.manager_login || ''})` : 'Global (Tous les gérants)';
            const elOpen = document.getElementById('detInvOpenedAt');
            if (elOpen) elOpen.innerText = inv.opened_at ? new Date(inv.opened_at).toLocaleDateString('fr-FR') : (inv.period_start ? new Date(inv.period_start).toLocaleDateString('fr-FR') : '-');

            const restoName = (restaurantConfig && restaurantConfig.restaurant_name) || "Lemo Daje Restaurant";
            const ifu = (restaurantConfig && (restaurantConfig.ifu || restaurantConfig.nif)) || "000123456789A";
            const nif = inv.dgi_nif || ifu;
            const nim = inv.dgi_nim || (restaurantConfig && restaurantConfig.nim) || "RESTO-DGI-MCF-01";
            const rccm = (restaurantConfig && restaurantConfig.rccm) || "BF-OUA-01-2024-B12-00456";
            const regime = (restaurantConfig && restaurantConfig.default_tax_regime) || "Régime du Réel Normal d'Imposition (RNI)";
            const division = (restaurantConfig && (restaurantConfig.fiscal_division || restaurantConfig.tax_center)) || "DGI - Division Fiscale des Moyennes Entreprises";
            const phone = (restaurantConfig && restaurantConfig.phone) || "+226 25 30 00 00";
            const address = (restaurantConfig && restaurantConfig.address) || "Avenue Kwame Nkrumah, Ouagadougou";
            const email = (restaurantConfig && restaurantConfig.email) || "contact@lemodaje.com";
            const logoUrl = restaurantConfig ? restaurantConfig.logo_url : "";

            // Mise à jour du bandeau supérieur officiel (Logo + Identifiants + QR DGI Toujours En Haut)
            const elLogoBox = document.getElementById('detInvLogoBox');
            if (elLogoBox) {
                if (logoUrl) {
                    elLogoBox.innerHTML = `<img src="${logoUrl}" style="max-width: 64px; max-height: 64px; object-fit: contain;" alt="Logo" onerror="this.onerror=null; this.parentElement.innerHTML='';" />`;
                } else {
                    elLogoBox.innerHTML = `<span style="font-size: 1.8rem;"></span>`;
                }
            }
            const elBrand = document.getElementById('detInvRestoBrand');
            if (elBrand) elBrand.innerText = restoName;
            const elSub = document.getElementById('detInvRestoSub');
            if (elSub) elSub.innerText = (restaurantConfig && restaurantConfig.restaurant_subtitle) || "Restaurant & Grill Gastronomique";
            const elHIfu = document.getElementById('detInvHeaderIfu');
            if (elHIfu) elHIfu.innerText = ifu;
            const elHRccm = document.getElementById('detInvHeaderRccm');
            if (elHRccm) elHRccm.innerText = rccm;
            const elHRegime = document.getElementById('detInvHeaderRegime');
            if (elHRegime) elHRegime.innerText = regime;
            const elHDiv = document.getElementById('detInvHeaderDivision');
            if (elHDiv) elHDiv.innerText = division;
            const elHPhone = document.getElementById('detInvHeaderPhone');
            if (elHPhone) elHPhone.innerText = " " + phone;
            const elHAddr = document.getElementById('detInvHeaderAddress');
            if (elHAddr) elHAddr.innerText = " " + address;
            const elHEmail = document.getElementById('detInvHeaderEmail');
            if (elHEmail) elHEmail.innerText = " " + email;

            // QR Code DGI Toujours En Haut
            const qrData = `DGI-FNE|IFU:${ifu}|RCCM:${rccm}|FACT:${inv.invoice_number}|PERIODE:${inv.period_label}|TTC:${Math.round(inv.total_ttc || 0)}|HT:${Math.round(inv.total_ht || 0)}|REF:${inv.dgi_fiscal_reference || 'DGI-CERT'}|STATUT:${inv.is_certified ? 'CERTIFIEE_DGI' : 'SESSION_ACTIVE'}`;
            renderDgiQrCodeStamp('detInvQrBox', qrData, inv.dgi_fiscal_reference);
            const elStampCode = document.getElementById('detInvStampCode');
            if (elStampCode) elStampCode.innerText = inv.dgi_fiscal_reference || (inv.is_certified ? 'DGI-CERTIFIÉE' : 'EN COURS');

            // Cases d'en-tête existantes
            const elResto = document.getElementById('detInvRestoName');
            if (elResto) elResto.innerText = restoName;
            const elNif = document.getElementById('detInvNif');
            if (elNif) elNif.innerText = nif;
            const elNim = document.getElementById('detInvNim');
            if (elNim) elNim.innerText = nim;

            const elFiscRef = document.getElementById('detInvFiscalRef');
            if (elFiscRef) elFiscRef.innerText = inv.dgi_fiscal_reference || (inv.is_certified ? 'DGI-CERTIFIÉE' : 'En attente de certification');

            const certDateStr = inv.certified_at ? new Date(inv.certified_at).toLocaleDateString('fr-FR') : 'Non certifiée';
            const elCertDate = document.getElementById('detInvCertDate');
            if (elCertDate) elCertDate.innerText = certDateStr;
            const elCertBy = document.getElementById('detInvCertBy');
            if (elCertBy) elCertBy.innerText = inv.certified_by || '-';

            const elStatus = document.getElementById('detInvStatusBadge');
            if (elStatus) elStatus.innerHTML = getInvoiceStatusBadgeHTML(inv.status, inv.is_certified, inv.has_anomalies);


            // 2. Grandes Cases de Totaux Financiers (Section 12 & Totaux)
            const elTTC = document.getElementById('detInvTotalTTC');
            if (elTTC) elTTC.innerText = Math.round(inv.total_ttc || 0).toLocaleString('fr-FR') + ' FCFA';
            const elHT = document.getElementById('detInvTotalHT');
            if (elHT) elHT.innerText = Math.round(inv.total_ht || 0).toLocaleString('fr-FR') + ' FCFA';
            const elTax = document.getElementById('detInvTotalTaxes');
            if (elTax) elTax.innerText = Math.round(inv.total_taxes || 0).toLocaleString('fr-FR') + ' FCFA';
            const elCnt = document.getElementById('detInvSalesCount');
            if (elCnt) elCnt.innerText = `${inv.total_sales_count} ventes`;

            // 3. Bannière d'anomalies (Exigence 15)
            const anomBanner = document.getElementById('detInvAnomaliesBanner');
            let anomaliesList = [];
            try { anomaliesList = JSON.parse(inv.anomalies || '[]'); } catch(e) {}

            if (anomaliesList.length >0) {
                const alertItems = anomaliesList.map(a => {
                    const color = a.severity === 'CRITICAL' ? '#ef4444' : (a.severity === 'WARNING' ? '#f59e0b' : '#3b82f6');
                    return `<li style="margin-bottom: 0.35rem; color: ${color}; font-size: 0.88rem;"><strong>[${a.type}]</strong> ${a.message}</li>`;
                }).join('');
                anomBanner.innerHTML = `
                    <div style="background: rgba(245, 158, 11, 0.12); border: 1.5px solid #f59e0b; border-radius: 12px; padding: 1.25rem;">
                        <div style="display: flex; align-items: center; gap: 0.5rem; color: #fbbf24; font-weight: bold; margin-bottom: 0.6rem;">
                            <span style="font-size: 1.2rem;"></span>Points d'Attention &amp; Anomalies Détectées (${anomaliesList.length}) :
                        </div>
                        <ul style="padding-left: 1.5rem; margin: 0;">${alertItems}</ul>
                    </div>
                `;
            } else {
                anomBanner.innerHTML = `
                    <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 10px; padding: 0.85rem 1.25rem; display: flex; align-items: center; gap: 0.6rem; color: #34d399; font-size: 0.9rem;">
                        <span></span> <strong>ConformitéFiscale DGI Validée :</strong>Toutes les ventes de la période sont intègres, pré-remplies et prêtes pour certification.
                    </div>
                `;
            }

            // 4. Boutons d'actions et verrouillage (Exigences 11 & 16)
            const btnCertify = document.getElementById('detBtnCertify');
            const btnRecalc = document.getElementById('detBtnRecalculate');
            const hasCritical = anomaliesList.some(a =>a.severity === 'CRITICAL');

            if (inv.is_certified) {
                btnCertify.disabled = true;
                btnCertify.style.opacity = '0.5';
                btnCertify.innerHTML = '<span></span>FACTURE DÉJÀ CERTIFIÉE (VERROUILLÉE)';
                btnRecalc.disabled = true;
                btnRecalc.style.opacity = '0.5';
            } else {
                btnRecalc.disabled = false;
                btnRecalc.style.opacity = '1';
                btnRecalc.innerHTML = '<span></span>RECALCULER';

                if (hasCritical || inv.total_sales_count === 0) {
                    btnCertify.disabled = true;
                    btnCertify.style.opacity = '0.5';
                    btnCertify.innerHTML = '<span></span>CERTIFICATION BLOQUÉE (ANOMALIES)';
                } else {
                    btnCertify.disabled = false;
                    btnCertify.style.opacity = '1';
                    btnCertify.innerHTML = '<span></span>CERTIFIER LA FACTURE';
                }
            }

            // 5. Tableau dynamique des lignes de vente pré-remplies (Exigences 3 & 12)
            const tbodyItems = document.getElementById('detInvItemsBody');
            const tfootItems = document.getElementById('detInvItemsFoot');
            const items = inv.items || [];

            if (items.length === 0) {
                tbodyItems.innerHTML = '<tr><td colspan="9" style="text-align: center; color: var(--text-muted); padding: 2.5rem; font-style: italic;">Aucunevente enregistrée pour cette période pour le moment. Dès qu’un gérant effectue une vente, elle apparaîtra ici automatiquement.</td></tr>';
            } else {
                tbodyItems.innerHTML = items.map((it, idx) => {
                    const dt = it.order_date ? new Date(it.order_date).toLocaleDateString('fr-FR') : '-';
                    const rowBg = idx % 2 === 0 ? 'rgba(30, 41, 59, 0.4)' : 'rgba(15, 23, 42, 0.6)';
                    return `
                        <tr style="background: ${rowBg}; border-bottom: 1px solid #334155; transition: background 0.15s ease;" onmouseover="this.style.background='rgba(51, 65, 85, 0.5)'" onmouseout="this.style.background='${rowBg}'">
                            <td style="padding: 0.85rem; border-right: 1px solid #334155;">
                                <strong style="color: #fbbf24; font-family: monospace; font-size: 0.92rem; background: rgba(245, 158, 11, 0.12); padding: 0.2rem 0.45rem; border-radius: 4px; border: 1px solid rgba(245, 158, 11, 0.3);">
                                    #${it.order_number}
                                </strong>
                            </td>
                            <td style="padding: 0.85rem; font-size: 0.85rem; color: #cbd5e1; border-right: 1px solid #334155; white-space: nowrap;">
                                ${dt}
                            </td>
                            <td style="padding: 0.85rem; border-right: 1px solid #334155;">
                                <strong style="color: white; font-size: 0.9rem;"> ${it.manager_name || 'Gérant'}</strong><br>
                                <small style="color: #94a3b8; font-size: 0.75rem;">Caisse: ${it.manager_login || 'caisse'} • ${it.payment_method || 'Espèces'}</small>
                            </td>
                            <td style="padding: 0.85rem; border-right: 1px solid #334155; color: #f1f5f9; font-size: 0.88rem;">
                                ${it.items_summary || 'Vente restaurant'}
                            </td>
                            <td style="padding: 0.85rem; text-align: center; font-weight: 800; font-size: 0.95rem; border-right: 1px solid #334155; color: white;">
                                <span style="background: rgba(148, 163, 184, 0.15); padding: 0.2rem 0.55rem; border-radius: 6px;">${it.total_items_count}</span>
                            </td>
                            <td style="padding: 0.85rem; text-align: right; color: #cbd5e1; border-right: 1px solid #334155; font-family: monospace; font-size: 0.9rem;">
                                ${Math.round(it.unit_price || 0).toLocaleString('fr-FR')} FCFA
                            </td>
                            <td style="padding: 0.85rem; text-align: right; color: #93c5fd; font-weight: 700; border-right: 1px solid #334155; font-family: monospace; font-size: 0.92rem;">
                                ${Math.round(it.amount_ht || 0).toLocaleString('fr-FR')} FCFA
                            </td>
                            <td style="padding: 0.85rem; text-align: right; color: #fbbf24; font-weight: 700; border-right: 1px solid #334155; font-family: monospace; font-size: 0.92rem;">
                                ${Math.round(it.amount_tax || 0).toLocaleString('fr-FR')} FCFA
                            </td>
                            <td style="padding: 0.85rem; text-align: right; font-family: monospace;">
                                <strong style="color: #34d399; font-size: 1.05rem; background: rgba(16, 185, 129, 0.1); padding: 0.2rem 0.5rem; border-radius: 6px; border: 1px solid rgba(16, 185, 129, 0.25);">
                                    ${Math.round(it.amount_ttc || 0).toLocaleString('fr-FR')} FCFA
                                </strong>
                            </td>
                        </tr>
                    `;
                }).join('');
            }

            // Pied de tableau avec les cases de totaux obligatoires bien visibles (Exigence 12)
            tfootItems.innerHTML = `
                <tr style="background: #1e293b; border-top: 3px solid #3b82f6; border-bottom: 2px solid #475569;">
                    <td colspan="6" style="padding: 1.25rem 1rem; text-align: right; font-weight: 900; text-transform: uppercase; letter-spacing: 0.05em; color: white; font-size: 0.95rem; border-right: 1px solid #334155;">
                         TOTAUX CALCULÉS DE LA FACTURE GLOBALE :
                    </td>
                    <td style="padding: 1.25rem 0.85rem; text-align: right; font-weight: 900; color: #93c5fd; font-size: 1.15rem; font-family: monospace; border-right: 1px solid #334155; background: rgba(59, 130, 246, 0.1);">
                        <div style="font-size: 0.7rem; color: #94a3b8; text-transform: uppercase; font-weight: 700;">TOTALHT</div>
                        ${Math.round(inv.total_ht || 0).toLocaleString('fr-FR')} FCFA
                    </td>
                    <td style="padding: 1.25rem 0.85rem; text-align: right; font-weight: 900; color: #fbbf24; font-size: 1.15rem; font-family: monospace; border-right: 1px solid #334155; background: rgba(245, 158, 11, 0.1);">
                        <div style="font-size: 0.7rem; color: #94a3b8; text-transform: uppercase; font-weight: 700;">TOTALTAXES (DGI)</div>
                        ${Math.round(inv.total_taxes || 0).toLocaleString('fr-FR')} FCFA
                    </td>
                    <td style="padding: 1.25rem 0.85rem; text-align: right; font-weight: 900; color: #34d399; font-size: 1.35rem; font-family: monospace; background: rgba(16, 185, 129, 0.15);">
                        <div style="font-size: 0.7rem; color: #a7f3d0; text-transform: uppercase; font-weight: 700;">TOTALTTC</div>
                        ${Math.round(inv.total_ttc || 0).toLocaleString('fr-FR')} FCFA
                    </td>
                </tr>
            `;

            // 6. Récapitulatif par gérant (Exigence 13)
            const mgrGrid = document.getElementById('detInvManagerCardsGrid');
            let mgrList = [];
            try { mgrList = JSON.parse(inv.manager_summary || '[]'); } catch(e) {}

            if (mgrList.length === 0) {
                mgrGrid.innerHTML = '<div style="color: var(--text-muted); font-size: 0.9rem; padding: 1.5rem; background: #1e293b; border-radius: 12px; border: 1px solid #334155;">Aucunevente de gérant rattachée.</div>';
            } else {
                const mgrCards = mgrList.map(m => `
                    <div style="background: #1e293b; border: 1.5px solid #334155; border-radius: 14px; padding: 1.35rem; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.85rem; border-bottom: 1px solid #334155; padding-bottom: 0.65rem;">
                            <div>
                                <strong style="font-size: 1.1rem; color: white;"> ${m.manager_name}</strong><br>
                                <small style="color: #94a3b8;">Caisse: <span style="font-family: monospace; color: #cbd5e1;">${m.manager_login || 'N/A'}</span></small>
                            </div>
                            <span class="badge" style="background: rgba(99, 102, 241, 0.25); color: #a5b4fc; font-weight: 800; font-size: 0.85rem; padding: 0.35rem 0.65rem;">
                                ${m.sales_count} ventes
                            </span>
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.65rem; margin-bottom: 0.75rem;">
                            <div style="background: #0f172a; padding: 0.6rem 0.75rem; border-radius: 8px; border: 1px solid #334155;">
                                <small style="color: #94a3b8; display: block; font-size: 0.72rem; text-transform: uppercase;">TotalHT</small>
                                <strong style="color: #93c5fd; font-family: monospace; font-size: 0.95rem;">${Math.round(m.total_ht ||0).toLocaleString('fr-FR')} FCFA</strong>
                            </div>
                            <div style="background: #0f172a; padding: 0.6rem 0.75rem; border-radius: 8px; border: 1px solid #334155;">
                                <small style="color: #94a3b8; display: block; font-size: 0.72rem; text-transform: uppercase;">TaxesDGI</small>
                                <strong style="color: #fbbf24; font-family: monospace; font-size: 0.95rem;">${Math.round(m.total_tax ||0).toLocaleString('fr-FR')} FCFA</strong>
                            </div>
                        </div>
                        <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 0.65rem 0.85rem; display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 0.82rem; font-weight: 700; color: #a7f3d0; text-transform: uppercase;">TotalEncaissé TTC</span>
                            <strong style="color: #34d399; font-size: 1.15rem; font-family: monospace;">${Math.round(m.total_ttc ||0).toLocaleString('fr-FR')} FCFA</strong>
                        </div>
                    </div>
                `).join('');

                // Carte Total Général Consolidé
                const grandTotalCard = `
                    <div style="background: linear-gradient(145deg, rgba(245, 158, 11, 0.12), rgba(245, 158, 11, 0.04)); border: 2px solid #f59e0b; border-radius: 14px; padding: 1.35rem; box-shadow: 0 4px 18px rgba(245, 158, 11, 0.2);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.85rem; border-bottom: 1px solid rgba(245, 158, 11, 0.3); padding-bottom: 0.65rem;">
                            <div>
                                <strong style="font-size: 1.15rem; color: #fbbf24;">Total Général Consolidé</strong><br>
                                <small style="color: #fde68a;">Tousgérants &amp; caisses confondus</small>
                            </div>
                            <span class="badge" style="background: rgba(245, 158, 11, 0.25); color: #fbbf24; font-weight: 800; font-size: 0.85rem; padding: 0.35rem 0.65rem;">
                                ${inv.total_sales_count} ventes
                            </span>
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.65rem; margin-bottom: 0.75rem;">
                            <div style="background: #0f172a; padding: 0.6rem 0.75rem; border-radius: 8px; border: 1px solid #334155;">
                                <small style="color: #94a3b8; display: block; font-size: 0.72rem; text-transform: uppercase;">TotalHT</small>
                                <strong style="color: #93c5fd; font-family: monospace; font-size: 0.95rem;">${Math.round(inv.total_ht ||0).toLocaleString('fr-FR')} FCFA</strong>
                            </div>
                            <div style="background: #0f172a; padding: 0.6rem 0.75rem; border-radius: 8px; border: 1px solid #334155;">
                                <small style="color: #94a3b8; display: block; font-size: 0.72rem; text-transform: uppercase;">TotalTaxes</small>
                                <strong style="color: #fbbf24; font-family: monospace; font-size: 0.95rem;">${Math.round(inv.total_taxes ||0).toLocaleString('fr-FR')} FCFA</strong>
                            </div>
                        </div>
                        <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 8px; padding: 0.65rem 0.85rem; display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 0.82rem; font-weight: 800; color: #a7f3d0; text-transform: uppercase;">TotalGlobal TTC</span>
                            <strong style="color: #34d399; font-size: 1.25rem; font-family: monospace;">${Math.round(inv.total_ttc ||0).toLocaleString('fr-FR')} FCFA</strong>
                        </div>
                    </div>
                `;

                mgrGrid.innerHTML = mgrCards + grandTotalCard;
            }

            // 7. Ventilation fiscale DGI (Exigence 6)
            const tbodyTax = document.getElementById('detInvTaxBreakdownBody');
            let taxRulesList = [];
            try { taxRulesList = JSON.parse(inv.tax_details || '[]'); } catch(e) {}

            if (taxRulesList.length === 0) {
                tbodyTax.innerHTML = '<tr><td colspan="6" style="text-align: center; color: var(--text-muted); padding: 1.5rem;">Aucunetaxe DGI calculée pour le moment.</td></tr>';
            } else {
                tbodyTax.innerHTML = taxRulesList.map(tx => `
                    <tr style="border-bottom: 1px solid #334155;">
                        <td style="padding: 0.9rem 1.25rem; border-right: 1px solid #334155;"><strong style="color: white;">${tx.rule_name}</strong></td>
                        <td style="padding: 0.9rem 1.25rem; border-right: 1px solid #334155;"><span class="badge" style="background: rgba(99, 102, 241, 0.25); color: #a5b4fc;">${tx.tax_type}</span></td>
                        <td style="padding: 0.9rem 1.25rem; text-align: center; font-weight: 800; color: #fbbf24; border-right: 1px solid #334155; font-size: 1rem;">${tx.rate}%</td>
                        <td style="padding: 0.9rem 1.25rem; text-align: right; color: #93c5fd; font-family: monospace; font-size: 0.95rem; border-right: 1px solid #334155;">${Math.round(tx.total_base ||0).toLocaleString('fr-FR')} FCFA</td>
                        <td style="padding: 0.9rem 1.25rem; text-align: right; color: #fbbf24; font-weight: 800; font-family: monospace; font-size: 0.95rem; border-right: 1px solid #334155;">${Math.round(tx.total_tax ||0).toLocaleString('fr-FR')} FCFA</td>
                        <td style="padding: 0.9rem 1.25rem; color: #cbd5e1; font-size: 0.85rem; font-family: monospace;">Base ${tx.base || 'HT'}(${Math.round(tx.total_base || 0).toLocaleString('fr-FR')} FCFA) × ${tx.rate}%</td>
                    </tr>
                `).join('');
            }

            // 8. Historique et audit (Exigence 14)
            const auditTimeline = document.getElementById('detInvAuditTimeline');
            const logs = inv.audit_logs || [];

            if (logs.length === 0) {
                auditTimeline.innerHTML = '<div style="color: var(--text-muted); font-size: 0.9rem; padding: 1.5rem; background: #1e293b; border-radius: 12px; border: 1px solid #334155;">Aucunévénement consigné pour le moment.</div>';
            } else {
                auditTimeline.innerHTML = logs.map(l => {
                    const dt = l.created_at ? new Date(l.created_at).toLocaleDateString('fr-FR') : '-';
                    return `
                        <div style="background: #1e293b; border-left: 4px solid #6366f1; border-radius: 8px; padding: 0.85rem 1.15rem; border-top: 1px solid #334155; border-right: 1px solid #334155; border-bottom: 1px solid #334155;">
                            <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #94a3b8; margin-bottom: 0.4rem;">
                                <span><strong style="color: #a5b4fc;">${l.user_name}</strong> • <span class="badge" style="background: rgba(99, 102, 241, 0.2); color: #a5b4fc; font-size: 0.72rem;">${l.action_type}</span></span>
                                <span style="font-family: monospace;">${dt}</span>
                            </div>
                            <div style="font-size: 0.9rem; color: #f1f5f9; line-height: 1.5;">${l.description}</div>
                        </div>
                    `;
                }).join('');
            }

            // 9. Sceau de certification (Exigence 11)
            const stampSec = document.getElementById('detInvCertifiedStamp');
            if (inv.is_certified) {
                stampSec.classList.remove('hidden');
                document.getElementById('detStampRef').innerText = inv.dgi_fiscal_reference || '-';
                document.getElementById('detStampDate').innerText = inv.certified_at ? new Date(inv.certified_at).toLocaleDateString('fr-FR') : '-';
                document.getElementById('detStampAdmin').innerText = inv.certified_by || 'Administrateur';
                document.getElementById('detStampSig').innerText = inv.dgi_security_code || '-';
            } else {
                stampSec.classList.add('hidden');
            }
        }

        // 3. Recalcul manuel à la demande [ RECALCULER ] (Exigence 16)
        async function recalculateCurrentInvoice() {
            if (!currentDetailInvoice) return;
            try {
                const btn = document.getElementById('detBtnRecalculate');
                btn.disabled = true;
                btn.innerText = 'Recalcul en cours...';

                const res = await fetch(`/api/v1/billing/global-invoices/${currentDetailInvoice.id}/recalculate`, {
                    method: 'POST',
                    headers: { 'Authorization': 'Bearer ' + token }
                });
                if (!res.ok) {
                    const err = await res.json();
                    throw new Error(err.detail || "Erreur lors du recalcul.");
                }
                const updated = await res.json();
                currentDetailInvoice = updated;
                renderDetailModalContent(updated);
                loadGlobalInvoicesData();
                btn.disabled = false;
                btn.innerText = ' RECALCULER';
            } catch (err) {
                alert("Erreur de recalcul : " + err.message);
                const btn = document.getElementById('detBtnRecalculate');
                if (btn) { btn.disabled = false; btn.innerText = ' RECALCULER'; }
            }
        }

        // 4. Procédure de Certification [ CERTIFIER LA FACTURE ] (Exigences 11 & 16)
        function promptCertifyCurrentInvoice() {
            if (!currentDetailInvoice) return;
            document.getElementById('certifyConfirmNotes').value = '';
            document.getElementById('modalCertifyConfirm').classList.remove('hidden');
        }

        function promptCertifyGlobalInvoice(invoiceId) {
            openGlobalInvoiceDetail(invoiceId).then(() => {
                promptCertifyCurrentInvoice();
            });
        }

        function closeCertifyConfirmModal() {
            document.getElementById('modalCertifyConfirm').classList.add('hidden');
        }

        async function executeCertifyAction() {
            if (!currentDetailInvoice) return;
            try {
                const btn = document.getElementById('btnConfirmCertifyFinal');
                btn.disabled = true;
                btn.innerText = 'Scellement DGI en cours...';

                const notes = document.getElementById('certifyConfirmNotes').value;
                const res = await fetch(`/api/v1/billing/global-invoices/${currentDetailInvoice.id}/certify`, {
                    method: 'POST',
                    headers: {
                        'Authorization': 'Bearer ' + token,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ notes: notes })
                });

                if (!res.ok) {
                    const err = await res.json();
                    throw new Error(err.detail || "Certification rejetée.");
                }

                const certified = await res.json();
                currentDetailInvoice = certified;
                closeCertifyConfirmModal();
                renderDetailModalContent(certified);
                loadGlobalInvoicesData();
                alert(` Facture globale ${certified.invoice_number} certifiée avec succès auprès de la DGI !\nRéférence fiscale FNE : ${certified.dgi_fiscal_reference}\nLes données sont désormais scellées et verrouillées.`);
            } catch (err) {
                alert("Erreur lors de la certification : " + err.message);
            } finally {
                const btn = document.getElementById('btnConfirmCertifyFinal');
                if (btn) { btn.disabled = false; btn.innerText = ' Oui, Certifier Définitivement'; }
            }
        }

        // 5. Générer la facture globale pour la période en cours
        async function generateNewGlobalInvoice() {
            try {
                const res = await fetch('/api/v1/billing/global-invoices/generate', {
                    method: 'POST',
                    headers: {
                        'Authorization': 'Bearer ' + token,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ period_type: 'daily' })
                });
                if (!res.ok) throw new Error("Erreur génération facture.");
                const inv = await res.json();
                loadGlobalInvoicesData();
                openGlobalInvoiceDetail(inv.id);
            } catch (err) {
                alert(err.message);
            }
        }

        // 6. Gestion des règles fiscales DGI (Exigence 6)
        async function openTaxRulesModal() {
            document.getElementById('modalTaxRulesConfig').classList.remove('hidden');
            loadTaxRules();
        }

        function closeTaxRulesModal() {
            document.getElementById('modalTaxRulesConfig').classList.add('hidden');
            resetTaxRuleForm();
        }

        async function loadTaxRules() {
            try {
                const res = await fetch('/api/v1/billing/tax-rules', {
                    headers: { 'Authorization': 'Bearer ' + token }
                });
                if (res.ok) {
                    const rules = await res.json();
                    const tbody = document.getElementById('taxRulesTableBody');
                    if (!tbody) return;

                    tbody.innerHTML = rules.map(r => `
                        <tr>
                            <td><strong>${r.name}</strong></td>
                            <td><span class="badge" style="background: rgba(99, 102, 241, 0.2); color: #a5b4fc;">${r.tax_type}</span></td>
                            <td style="text-align: center; font-weight: bold; color: #fbbf24;">${r.rate}%</td>
                            <td>${r.calculation_base}</td>
                            <td style="text-align: center;">${r.calculation_order}</td>
                            <td>${r.tax_regime}</td>
                            <td>
                                ${r.is_active 
                                    ? '<span class="badge badge-success">Active</span>' 
                                    : '<span class="badge badge-danger">Inactive</span>'}
                            </td>
                            <td style="text-align: center; white-space: nowrap;">
                                <button class="btn btn-secondary" onclick="editTaxRule(${r.id})" style="padding: 0.25rem 0.5rem; font-size: 0.75rem;"></button>
                                <button class="btn btn-danger" onclick="toggleTaxRule(${r.id}, ${!r.is_active})" style="padding: 0.25rem 0.5rem; font-size: 0.75rem; margin-left: 4px;">
                                    ${r.is_active ? 'Désactiver' : 'Activer'}
                                </button>
                            </td>
                        </tr>
                    `).join('');
                }
            } catch(err) {
                console.error("Erreur chargement règles fiscales:", err);
            }
        }

        function resetTaxRuleForm() {
            document.getElementById('editTaxRuleId').value = '';
            document.getElementById('taxRuleName').value = '';
            document.getElementById('taxRuleType').value = 'VAT';
            document.getElementById('taxRuleRate').value = '';
            document.getElementById('taxRuleBase').value = 'HT';
            document.getElementById('taxRuleOrder').value = '1';
            document.getElementById('taxRuleRegime').value = 'TOUS';
            document.getElementById('taxRuleRounding').value = 'round_2_decimals';
            document.getElementById('taxRuleCondition').value = 'always';
            document.getElementById('taxRuleDesc').value = '';
            document.getElementById('taxRuleFormTitle').innerText = ' Ajouter une Règle Fiscale';
        }

        async function editTaxRule(ruleId) {
            try {
                const res = await fetch('/api/v1/billing/tax-rules', {
                    headers: { 'Authorization': 'Bearer ' + token }
                });
                const rules = await res.json();
                const rule = rules.find(r =>r.id === ruleId);
                if (!rule) return;

                document.getElementById('editTaxRuleId').value = rule.id;
                document.getElementById('taxRuleName').value = rule.name;
                document.getElementById('taxRuleType').value = rule.tax_type;
                document.getElementById('taxRuleRate').value = rule.rate;
                document.getElementById('taxRuleBase').value = rule.calculation_base;
                document.getElementById('taxRuleOrder').value = rule.calculation_order;
                document.getElementById('taxRuleRegime').value = rule.tax_regime;
                document.getElementById('taxRuleRounding').value = rule.rounding_mode;
                document.getElementById('taxRuleCondition').value = rule.application_condition;
                document.getElementById('taxRuleDesc').value = rule.description || '';
                document.getElementById('taxRuleFormTitle').innerText = ' Modifier la Règle Fiscale #' + rule.id;
            } catch(e) {}
        }

        async function saveTaxRuleAction() {
            const editId = document.getElementById('editTaxRuleId').value;
            const payload = {
                name: document.getElementById('taxRuleName').value.trim(),
                tax_type: document.getElementById('taxRuleType').value,
                rate: parseFloat(document.getElementById('taxRuleRate').value) || 0,
                calculation_base: document.getElementById('taxRuleBase').value,
                calculation_order: parseInt(document.getElementById('taxRuleOrder').value) || 1,
                tax_regime: document.getElementById('taxRuleRegime').value,
                rounding_mode: document.getElementById('taxRuleRounding').value,
                application_condition: document.getElementById('taxRuleCondition').value,
                description: document.getElementById('taxRuleDesc').value.trim()
            };

            if (!payload.name || payload.rate < 0) {
                alert("Veuillez saisir un nom et un taux valide.");
                return;
            }

            try {
                let url = '/api/v1/billing/tax-rules';
                let method = 'POST';
                if (editId) {
                    url += '/' + editId;
                    method = 'PUT';
                }

                const res = await fetch(url, {
                    method: method,
                    headers: {
                        'Authorization': 'Bearer ' + token,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });

                if (!res.ok) {
                    const err = await res.json();
                    throw new Error(err.detail || "Erreur enregistrement.");
                }

                resetTaxRuleForm();
                loadTaxRules();
                loadGlobalInvoicesData();
            } catch (err) {
                alert("Erreur: " + err.message);
            }
        }

        async function toggleTaxRule(ruleId, setActive) {
            try {
                await fetch(`/api/v1/billing/tax-rules/${ruleId}`, {
                    method: 'PUT',
                    headers: {
                        'Authorization': 'Bearer ' + token,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ is_active: setActive })
                });
                loadTaxRules();
                loadGlobalInvoicesData();
            } catch(e) {}
        }

        async function resetDefaultTaxRulesAction() {
            if (!confirm("Voulez-vous réinitialiser les règles vers le standard TVA 18% DGI ?")) return;
            try {
                await fetch('/api/v1/billing/tax-rules/reset-defaults', {
                    method: 'POST',
                    headers: { 'Authorization': 'Bearer ' + token }
                });
                loadTaxRules();
                loadGlobalInvoicesData();
            } catch(e) {}
        }

        // 7. Paramétrage de la période de facturation (Exigence 8)
        async function openBillingConfigModal() {
            try {
                const res = await fetch('/api/v1/billing/config', {
                    headers: { 'Authorization': 'Bearer ' + token }
                });
                if (res.ok) {
                    const cfg = await res.json();
                    document.getElementById('cfgBillingFrequency').value = cfg.billing_frequency || 'daily';
                    document.getElementById('cfgPricesMode').value = cfg.menu_prices_include_tax ? 'ttc' : 'ht';
                    document.getElementById('cfgTaxRegime').value = cfg.default_tax_regime || 'REEL_NORMAL';
                }
                document.getElementById('modalBillingConfig').classList.remove('hidden');
            } catch(e) {}
        }

        function closeBillingConfigModal() {
            document.getElementById('modalBillingConfig').classList.add('hidden');
        }

        async function saveBillingConfigAction() {
            try {
                const freq = document.getElementById('cfgBillingFrequency').value;
                const pricesMode = document.getElementById('cfgPricesMode').value === 'ttc';
                const regime = document.getElementById('cfgTaxRegime').value;

                const res = await fetch('/api/v1/billing/config', {
                    method: 'PUT',
                    headers: {
                        'Authorization': 'Bearer ' + token,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        billing_frequency: freq,
                        menu_prices_include_tax: pricesMode,
                        default_tax_regime: regime
                    })
                });

                if (res.ok) {
                    closeBillingConfigModal();
                    loadGlobalInvoicesData();
                    alert(" Fréquence de facturation mise à jour avec succès !");
                }
            } catch(e) {
                alert("Erreur: " + e.message);
            }
        }

        // 8. Aperçu et impression officielle DGI (Exigence 16)
        function openCurrentInvoicePrintPreview() {
            if (!currentDetailInvoice) return;
            openGlobalInvoicePrintPreview(currentDetailInvoice.id);
        }

        async function openGlobalInvoicePrintPreview(invoiceId) {
            try {
                const res = await fetch(`/api/v1/billing/global-invoices/${invoiceId}`, {
                    headers: { 'Authorization': 'Bearer ' + token }
                });
                if (!res.ok) throw new Error("Facture introuvable.");
                const inv = await res.json();

                // Garantir la configuration
                if (!restaurantConfig || !restaurantConfig.restaurant_name) {
                    try {
                        const cfgUrl = (token && currentUser && currentUser.role === 'admin')
                            ? '/api/v1/admin/settings'
                            : '/api/v1/settings';
                        const resCfg = await fetch(cfgUrl, { headers: token ? { 'Authorization': 'Bearer ' + token } : {} });
                        if (resCfg.ok) restaurantConfig = await resCfg.json();
                    } catch(e) {}
                }
                const cfg = restaurantConfig || {};

                const restoName = cfg.restaurant_name || cfg.company_name || "ÉTABLISSEMENT";
                const ifu = cfg.ifu || cfg.nif || "-";
                const nim = inv.dgi_nim || cfg.nim || "RESTO-DGI-MCF-01";
                const rccm = cfg.rccm || "-";
                const regime = cfg.default_tax_regime || "-";
                const division = cfg.fiscal_division || cfg.tax_center || "-";
                const phone = cfg.phone || "-";
                const address = cfg.address || "-";
                const email = cfg.email || "-";

                // Métadonnées
                const elNum = document.getElementById('printInvNum');
                if (elNum) elNum.innerText = inv.invoice_number;
                const elDate = document.getElementById('printInvDate');
                if (elDate) elDate.innerText = inv.created_at ? new Date(inv.created_at).toLocaleDateString('fr-FR') : new Date().toLocaleDateString('fr-FR');
                const elPer = document.getElementById('printInvPeriodLabel');
                if (elPer) elPer.innerText = inv.period_label || 'Période fiscale';
                const elRef = document.getElementById('printInvRef');
                if (elRef) elRef.innerText = inv.dgi_fiscal_reference || (inv.invoice_number + ' (e-MCF)');

                // QR Code officiel
                const qrContainer = document.getElementById('printInvQrContainer');
                if (qrContainer) {
                    const qrText = encodeURIComponent(`DGI-FNE|IFU:${ifu}|RCCM:${rccm}|FACT:${inv.invoice_number}|PERIODE:${inv.period_label}|TTC:${Math.round(inv.total_ttc || 0)}|HT:${Math.round(inv.total_ht || 0)}|REF:${inv.dgi_fiscal_reference || 'DGI-CERT'}`);
                    qrContainer.innerHTML = `<img src="https://api.qrserver.com/v1/create-qr-code/?size=120x120&margin=1&data=${qrText}" style="width: 78px; height: 78px; display: block; margin: 0 auto;" alt="QR DGI" />`;
                }

                // Vendeur
                const elName = document.getElementById('printInvRestoName');
                if (elName) elName.innerText = restoName;
                const elAddr = document.getElementById('printInvAddress');
                if (elAddr) elAddr.innerText = address;
                const elPhone = document.getElementById('printInvPhone');
                if (elPhone) elPhone.innerText = phone;
                const elIfu = document.getElementById('printInvIfu');
                if (elIfu) elIfu.innerText = ifu;
                const elRccm = document.getElementById('printInvRccm');
                if (elRccm) elRccm.innerText = rccm;
                const elRegime = document.getElementById('printInvTaxRegime');
                if (elRegime) elRegime.innerText = regime;

                // Client / DGI
                const elSalesDesc = document.getElementById('printInvSalesCountDesc');
                if (elSalesDesc) elSalesDesc.innerText = `${inv.total_sales_count || 0} commande(s) consolidée(s)`;
                const elCertBy = document.getElementById('printInvCertBy');
                if (elCertBy) elCertBy.innerText = inv.certified_by || 'Administrateur';

                // Tableau
                const tableBody = document.getElementById('printInvTableBody');
                if (tableBody) {
                    tableBody.innerHTML = `
                        <tr>
                            <td style="border: 1px solid #000000; padding: 12px 14px; font-size: 11.5px; line-height: 1.55; font-weight: 700; color: #000000;">
                                Ventes Globales Restauration &amp; Boissons (Groupe B - Norme DGI)<br>
                                <small style="color: #4b5563; font-weight: 400;">${inv.period_label}</small>
                            </td>
                            <td style="border: 1px solid #000000; padding: 12px 8px; font-size: 11.5px; line-height: 1.55; text-align: center; font-weight: 700;">
                                ${inv.total_sales_count || 1}
                            </td>
                            <td style="border: 1px solid #000000; padding: 12px 10px; font-size: 11.5px; line-height: 1.55; text-align: right; font-weight: 700;">
                                ${Math.round(inv.total_ttc || 0).toLocaleString('fr-FR')} FCFA
                            </td>
                            <td style="border: 1px solid #000000; padding: 12px 14px; font-size: 11.5px; line-height: 1.55; text-align: right; font-weight: 800;">
                                ${Math.round(inv.total_ttc || 0).toLocaleString('fr-FR')} FCFA
                            </td>
                        </tr>
                    `;
                }

                // Totaux
                const elSub = document.getElementById('printInvSubTotal');
                if (elSub) elSub.innerText = Math.round(inv.total_ht || 0).toLocaleString('fr-FR') + ' FCFA';
                const elTax = document.getElementById('printInvTaxAmount');
                if (elTax) elTax.innerText = Math.round(inv.total_taxes || 0).toLocaleString('fr-FR') + ' FCFA';
                const elGrand = document.getElementById('printInvGrandTotal');
                if (elGrand) elGrand.innerText = Math.round(inv.total_ttc || 0).toLocaleString('fr-FR') + ' FCFA';

                // Homologation
                const elRefDgi = document.getElementById('printInvRefDgi');
                if (elRefDgi) elRefDgi.innerText = inv.dgi_fiscal_reference || (inv.invoice_number + ' (e-MCF)');
                const elNimField = document.getElementById('printInvNim');
                if (elNimField) elNimField.innerText = nim;
                const elCertDate = document.getElementById('printInvCertDate');
                if (elCertDate) elCertDate.innerText = inv.certified_at ? new Date(inv.certified_at).toLocaleDateString('fr-FR') : (inv.created_at ? new Date(inv.created_at).toLocaleDateString('fr-FR') : '-');
                const elSha = document.getElementById('printInvSha256');
                if (elSha) elSha.innerText = inv.dgi_security_code ? (inv.dgi_security_code.substring(0, 36) + '...') : 'SCEAU_DGI_CONFORME';

                // Footer 3 colonnes
                const elFBrand = document.getElementById('printInvFooterBrand');
                if (elFBrand) elFBrand.innerText = restoName;
                const elFIfu = document.getElementById('printInvFooterIfu');
                if (elFIfu) elFIfu.innerText = ifu;
                const elFRccm = document.getElementById('printInvFooterRccm');
                if (elFRccm) elFRccm.innerText = rccm;
                const elFNim = document.getElementById('printInvFooterNim');
                if (elFNim) elFNim.innerText = nim;
                const elFAddr = document.getElementById('printInvFooterAddress');
                if (elFAddr) elFAddr.innerText = address;
                const elFPhone = document.getElementById('printInvFooterPhone');
                if (elFPhone) elFPhone.innerText = phone;
                const elFEmail = document.getElementById('printInvFooterEmail');
                if (elFEmail) elFEmail.innerText = email;
                const elFRegime = document.getElementById('printInvFooterRegime');
                if (elFRegime) elFRegime.innerText = regime;
                const elFDiv = document.getElementById('printInvFooterDivision');
                if (elFDiv) elFDiv.innerText = division;

                document.getElementById('modalGlobalInvoicePrint').classList.remove('hidden');
            } catch(err) {
                alert("Erreur: " + err.message);
            }
        }

        function closeGlobalInvoicePrintPreview() {
            document.getElementById('modalGlobalInvoicePrint').classList.add('hidden');
        }

        // --- COMMANDES ET FACTURATION DGI (CENTRALISATION & ACCUMULATION EN DIRECT) ---
        let currentDailyReport = null;
        let allAdminOrders = [];

        async function loadAdminOrdersData() {
            try {
                const res = await fetch('/api/v1/admin/orders', {
                    headers: { 'Authorization': 'Bearer ' + token }
                });
                if (res.ok) {
                    allAdminOrders = await res.json();
                    
                    // Calcul et addition au fur et à mesure en direct dans l'admin
                    const taxRate = (restaurantConfig && restaurantConfig.tax_rate) ? restaurantConfig.tax_rate : 18.0;
                    const taxFactor = 1 + (taxRate / 100);

                    let totalTTC = 0;
                    let totalHT = 0;
                    let totalTVA = 0;
                    let totalCount = allAdminOrders.length;
                    let totalChange = 0;

                    allAdminOrders.forEach(o => {
                        const ttc = o.total_amount || 0;
                        const ht = ttc / taxFactor;
                        const tva = ttc - ht;
                        totalTTC += ttc;
                        totalHT += ht;
                        totalTVA += tva;
                        totalChange += (o.change_amount || 0);
                    });

                    // Affichage dans les compteurs financiers cumulés
                    const elTTC = document.getElementById('admInvAccumulatedTTC');
                    if (elTTC) elTTC.innerText = Math.round(totalTTC).toLocaleString('fr-FR') + ' FCFA';

                    const elHT = document.getElementById('admInvAccumulatedHT');
                    if (elHT) elHT.innerText = Math.round(totalHT).toLocaleString('fr-FR') + ' FCFA';

                    const elTVA = document.getElementById('admInvAccumulatedTVA');
                    if (elTVA) elTVA.innerText = Math.round(totalTVA).toLocaleString('fr-FR') + ' FCFA';

                    const elCount = document.getElementById('admInvAccumulatedCount');
                    if (elCount) elCount.innerText = totalCount + ' facture(s)';

                    const elChange = document.getElementById('admInvAccumulatedChange');
                    if (elChange) elChange.innerText = Math.round(totalChange).toLocaleString('fr-FR') + ' FCFA';

                    renderAdminOrdersTable(allAdminOrders);
                }
            } catch (err) {
                console.error("Erreur chargement orders admin", err);
            }
        }

        function filterAdminInvoicesTable() {
            const q = (document.getElementById('admInvoiceSearch') ? document.getElementById('admInvoiceSearch').value : '').toLowerCase().trim();
            if (!q) {
                renderAdminOrdersTable(allAdminOrders);
                return;
            }
            const filtered = allAdminOrders.filter(o => {
                return (o.order_number && o.order_number.toLowerCase().includes(q)) ||
                       (o.manager_name && o.manager_name.toLowerCase().includes(q)) ||
                       (o.manager_login && o.manager_login.toLowerCase().includes(q)) ||
                       (o.payment_method && o.payment_method.toLowerCase().includes(q)) ||
                       (o.created_at && o.created_at.toLowerCase().includes(q));
            });
            renderAdminOrdersTable(filtered);
        }

        function renderAdminOrdersTable(ordersList) {
            const tbody = document.getElementById('adminOrdersTableBody');
            if (!tbody) return;

            if (!ordersList || ordersList.length === 0) {
                tbody.innerHTML = '<tr><td colspan="9" style="text-align: center; color: var(--text-muted);">Aucunefacture enregistrée pour le moment. Dès qu\’un gérant encaisse, elle s\’additionne ici.</td></tr>';
                return;
            }

            const taxRate = (restaurantConfig && restaurantConfig.tax_rate) ? restaurantConfig.tax_rate : 18.0;
            const taxFactor = 1 + (taxRate / 100);

            tbody.innerHTML = ordersList.map(o => {
                const dateStr = o.created_at ? new Date(o.created_at).toLocaleDateString('fr-FR') : 'N/A';
                const ttc = o.total_amount || 0;
                const ht = Math.round(ttc / taxFactor);
                const tva = Math.round(ttc - ht);
                const dgiBadge = o.is_certified_dgi 
                    ? `<span class="badge badge-success" title="Facture FNE : ${o.dgi_invoice_number || ''}">Certifié DGI</span>`
                    : '<span class="badge badge-warning">Enattente DGI</span>';
                
                return `
                    <tr>
                        <td><strong style="color: white;">${o.order_number}</strong></td>
                        <td><small style="color: var(--text-muted);">${dateStr}</small></td>
                        <td>
                            <strong>${o.manager_name || 'Gérant'}</strong>
                            ${o.manager_login ? '<br><small style="color: var(--text-muted);">(' +o.manager_login + ')</small>' : ''}
                        </td>
                        <td><span class="badge" style="background: rgba(99, 102, 241, 0.15); color: #a5b4fc;">${o.payment_method || 'Espèces(Cash)'}</span></td>
                        <td><span>${ht.toLocaleString('fr-FR')}FCFA</span></td>
                        <td><span style="color: #fbbf24;">${tva.toLocaleString('fr-FR')}FCFA</span></td>
                        <td><strong style="color: #34d399; font-size: 0.95rem;">${Math.round(ttc).toLocaleString('fr-FR')}FCFA</strong></td>
                        <td>${dgiBadge}</td>
                        <td>
                            <button class="btn btn-primary" style="background: linear-gradient(135deg, #f59e0b, #d97706); color: black; font-weight: 700; font-size: 0.75rem; padding: 0.35rem 0.75rem;" onclick="openRestaurantInvoiceModal(${o.id})">
                                 Facture Officielle
                            </button>
                        </td>
                    </tr>
                `;
            }).join('');

            // Mettre également à jour le tableau récapitulatif des factures récentes sur la page d'accueil Vue Exécutive
            const overviewTbody = document.getElementById('overviewRecentOrdersTableBody');
            if (overviewTbody) {
                if (!ordersList || ordersList.length === 0) {
                    overviewTbody.innerHTML = '<tr><td colspan="7" style="text-align: center; color: var(--text-muted);">Aucunefacture enregistrée pour le moment.</td></tr>';
                } else {
                    const recent10 = ordersList.slice(0, 10);
                    overviewTbody.innerHTML = recent10.map(o => {
                        const dateStr = o.created_at ? new Date(o.created_at).toLocaleDateString('fr-FR') : 'N/A';
                        const ttc = o.total_amount || 0;
                        const dgiBadge = o.is_certified_dgi 
                            ? `<span class="badge badge-success">Certifié</span>`
                            : '<span class="badge badge-warning">Enattente</span>';
                        return `
                            <tr>
                                <td><strong style="color: white;">${o.order_number}</strong></td>
                                <td><small style="color: var(--text-muted);">${dateStr}</small></td>
                                <td>
                                    <strong>${o.manager_name || 'Gérant'}</strong>
                                    ${o.manager_login ? '<br><small style="color: var(--text-muted);">(' +o.manager_login + ')</small>' : ''}
                                </td>
                                <td><span class="badge" style="background: rgba(99, 102, 241, 0.15); color: #a5b4fc;">${o.payment_method || 'Espèces(Cash)'}</span></td>
                                <td><strong style="color: #34d399; font-size: 0.95rem;">${Math.round(ttc).toLocaleString('fr-FR')}FCFA</strong></td>
                                <td>${dgiBadge}</td>
                                <td style="text-align: center;">
                                    <button class="btn btn-primary" style="background: linear-gradient(135deg, #f59e0b, #d97706); color: black; font-weight: 700; font-size: 0.75rem; padding: 0.3rem 0.65rem;" onclick="openRestaurantInvoiceModal(${o.id})">
                                         Facture Officielle
                                    </button>
                                </td>
                            </tr>
                        `;
                    }).join('');
                }
            }
        } // --- AFFICHAGE DE LA FACTURE OFFICIELLE (MODÈLE MONOCHROME DE RÉFÉRENCE - 100% DYNAMIQUE SANS VALEUR EN DUR) ---
        let currentInvoiceOrder = null;

        async function openRestaurantInvoiceModal(orderId) {
            let order = (allAdminOrders || []).find(o =>o.id === orderId);
            if (!order && typeof currentManagerOrders !== 'undefined') {
                order = (currentManagerOrders || []).find(o =>o.id === orderId);
            }

            if (!order || !order.items || order.items.length === 0) {
                try {
                    const res = await fetch(`/api/v1/admin/orders/${orderId}`, {
                        headers: token ? { 'Authorization': 'Bearer ' + token } : {}
                    });
                    if (res.ok) {
                        order = await res.json();
                    }
                } catch (e) {
                    console.warn("Impossible de charger les détails complets", e);
                }
            }

            if (!order) {
                alert("Détails de la facture introuvables.");
                return;
            }
            currentInvoiceOrder = order;

            // Garantir que la configuration est bien chargée depuis l'API / Base de données
            if (!restaurantConfig || !restaurantConfig.restaurant_name) {
                try {
                    const cfgUrl = (token && currentUser && currentUser.role === 'admin')
                        ? '/api/v1/admin/settings'
                        : '/api/v1/settings';
                    const resCfg = await fetch(cfgUrl, { headers: token ? { 'Authorization': 'Bearer ' + token } : {} });
                    if (resCfg.ok) {
                        restaurantConfig = await resCfg.json();
                    }
                } catch(e) {}
            }
            const cfg = restaurantConfig || {};

            // Données Établissement (100% dynamiques, aucun texte codé en dur)
            const brandName = cfg.restaurant_name || cfg.company_name || 'ÉTABLISSEMENT';
            const ifuVal = cfg.ifu || cfg.nif || '-';
            const rccmVal = cfg.rccm || '-';
            const nimVal = cfg.nim || 'RESTO-DGI-MCF-01';
            const regimeVal = cfg.default_tax_regime || '-';
            const divisionVal = cfg.fiscal_division || cfg.tax_center || '-';
            const addressVal = cfg.address || '-';
            const phoneVal = cfg.phone || '-';
            const emailVal = cfg.email || '-';

            // Données Commande & Client
            const invNum = order.order_number || ('CMD-' + order.id);
            const ordDate = order.created_at ? new Date(order.created_at) : new Date();
            const formattedDate = ordDate.toLocaleDateString('fr-FR');
            const dgiRef = order.dgi_invoice_number || (order.order_number ? (order.order_number + ' (e-MCF)') : 'DGI-FNE-OK');
            const shaCode = order.dgi_signature || order.dgi_security_code || ('SHA256-' + (order.order_number || order.id));
            const clientName = order.client_name || order.customer_name || (order.table_id ? `Table #${order.table_id} (Client)` : 'Client Comptoir / Vente directe');
            const managerName = order.manager_name || 'Gérant en service';
            const paymentMethod = (order.payment_method || 'Espèces (Cash)').toUpperCase();

            // 1. Badge DGI en-tête
            const elBadge = document.getElementById('invBadgeDgi');
            if (elBadge) {
                elBadge.innerText = order.is_certified_dgi 
                    ? ' FACTURE NORMALISÉE DGI (e-MCF)' 
                    : ' FACTURE RESTAURANT & GRAND MARCHÉ (e-MCF)';
            }

            // 2. Métadonnées En-tête Droite
            const elInvNum = document.getElementById('invPaperInvoiceNum');
            if (elInvNum) elInvNum.innerText = invNum;
            const elDate = document.getElementById('invPaperInvoiceDate');
            if (elDate) elDate.innerText = formattedDate;
            const elDueDate = document.getElementById('invPaperDueDate');
            if (elDueDate) elDueDate.innerText = 'Comptant à réception';
            const elDgiRef = document.getElementById('invPaperDgiRef');
            if (elDgiRef) elDgiRef.innerText = dgiRef;

            // 3. QR Code DGI en-tête
            const qrContainer = document.getElementById('invPaperQrContainer');
            if (qrContainer) {
                const qrText = encodeURIComponent(`DGI-FNE|IFU:${ifuVal}|RCCM:${rccmVal}|FACT:${invNum}|DATE:${formattedDate}|TTC:${Math.round(order.total_amount || 0)}|REF:${dgiRef}`);
                qrContainer.innerHTML = `<img src="https://api.qrserver.com/v1/create-qr-code/?size=120x120&margin=1&data=${qrText}" style="width: 78px; height: 78px; display: block; margin: 0 auto;" alt="QR DGI" />`;
            }

            // 4. Colonne Vendeur
            const elBrand = document.getElementById('invPaperBrandName');
            if (elBrand) elBrand.innerText = brandName;
            const elAddr = document.getElementById('invPaperAddress');
            if (elAddr) elAddr.innerText = addressVal;
            const elPhone = document.getElementById('invPaperPhone');
            if (elPhone) elPhone.innerText = phoneVal;
            const elIfu = document.getElementById('invPaperIfu');
            if (elIfu) elIfu.innerText = ifuVal;
            const elRccm = document.getElementById('invPaperRccm');
            if (elRccm) elRccm.innerText = rccmVal;
            const elRegime = document.getElementById('invPaperRegime');
            if (elRegime) elRegime.innerText = regimeVal;

            // 5. Colonne Client
            const elCust = document.getElementById('invPaperCustomerName');
            if (elCust) elCust.innerText = clientName;
            const elMgr = document.getElementById('invPaperManagerName');
            if (elMgr) elMgr.innerText = managerName;
            const elPayMode = document.getElementById('invPaperPaymentMode');
            if (elPayMode) elPayMode.innerText = paymentMethod;

            // 6. Tableau des articles avec adaptation dynamique à 85% de la feuille A4 (textes nets, sans chevauchement)
            const itemsTableBody = document.getElementById('invPaperItemsBody');
            const items = order.items || [];
            const itemCount = items.length || 1;

            // Barème dynamique : tire l'affiche vers le bas sur 85% de la feuille, grand confort de lecture, jamais superposé
            let rowFontSize = '12px';
            let rowPadding = '12px 14px';
            let thFontSize = '12px';
            let thPadding = '12px 14px';
            let secMargin = '1.75rem';
            let headerMargin = '1.75rem';
            let titleFontSize = '2.4rem';
            let qrSize = 78;
            let rowLineHeight = '1.55';

            if (itemCount >25) {
                rowFontSize = '9px';
                rowPadding = '3px 6px';
                thFontSize = '9px';
                thPadding = '3.5px 6px';
                secMargin = '0.55rem';
                headerMargin = '0.65rem';
                titleFontSize = '1.75rem';
                qrSize = 58;
                rowLineHeight = '1.35';
            } else if (itemCount >18) {
                rowFontSize = '9.5px';
                rowPadding = '4.5px 8px';
                thFontSize = '9.5px';
                thPadding = '5px 8px';
                secMargin = '0.85rem';
                headerMargin = '0.95rem';
                titleFontSize = '1.9rem';
                qrSize = 65;
                rowLineHeight = '1.4';
            } else if (itemCount >10) {
                rowFontSize = '10.5px';
                rowPadding = '6.5px 10px';
                thFontSize = '10.5px';
                thPadding = '7.5px 10px';
                secMargin = '1.15rem';
                headerMargin = '1.25rem';
                titleFontSize = '2.1rem';
                qrSize = 70;
                rowLineHeight = '1.45';
            } else if (itemCount >5) {
                rowFontSize = '11.5px';
                rowPadding = '9px 12px';
                thFontSize = '11.5px';
                thPadding = '10px 12px';
                secMargin = '1.45rem';
                headerMargin = '1.5rem';
                titleFontSize = '2.25rem';
                qrSize = 74;
                rowLineHeight = '1.5';
            }

            // Application dynamique aux conteneurs de la facture pour occuper 85% de la page
            const invModalPaper = document.querySelector('#invoiceModal .corporate-invoice-paper');
            if (invModalPaper) {
                invModalPaper.style.fontSize = (itemCount >18 ? '9.5px' : (itemCount >10 ? '10.5px' : '11.5px'));
                invModalPaper.style.minHeight = '250mm';
            }
            const invTitle = document.querySelector('#invoiceModal h1');
            if (invTitle) invTitle.style.fontSize = titleFontSize;
            
            const invHdrSec = document.getElementById('invPaperHeaderSec');
            if (invHdrSec) invHdrSec.style.marginBottom = headerMargin;
            const invVendorClientSec = document.getElementById('invPaperVendorClientSec');
            if (invVendorClientSec) invVendorClientSec.style.marginBottom = secMargin;
            const invTotalsSec = document.getElementById('invPaperTotalsSec');
            if (invTotalsSec) invTotalsSec.style.marginBottom = secMargin;
            const invCondSec = document.getElementById('invPaperCondBox');
            if (invCondSec) invCondSec.style.marginBottom = secMargin;

            const invHeaders = document.querySelectorAll('#invoiceModal .corporate-inv-table th');
            invHeaders.forEach(th => {
                th.style.fontSize = thFontSize;
                th.style.padding = thPadding;
                th.style.lineHeight = rowLineHeight;
            });
            const invTotalsCells = document.querySelectorAll('#invoiceModal .corporate-inv-totals-table td');
            invTotalsCells.forEach(td => {
                td.style.fontSize = (itemCount >18 ? '9.5px' : '11.5px');
                td.style.padding = (itemCount >18 ? '4.5px 7px' : (itemCount >10 ? '7px 10px' : '10px 12px'));
                td.style.lineHeight = rowLineHeight;
            });

            // Re-génération du QR code avec taille adaptée
            const qrContainerScaled = document.getElementById('invPaperQrContainer');
            if (qrContainerScaled) {
                const qrTextScaled = encodeURIComponent(`DGI-FNE|IFU:${ifuVal}|RCCM:${rccmVal}|FACT:${invNum}|DATE:${formattedDate}|TTC:${Math.round(order.total_amount || 0)}|REF:${dgiRef}`);
                qrContainerScaled.innerHTML = `<img src="https://api.qrserver.com/v1/create-qr-code/?size=120x120&margin=1&data=${qrTextScaled}" style="width: ${qrSize}px; height: ${qrSize}px; display: block; margin: 0 auto;" alt="QR DGI" />`;
            }

            if (items.length === 0) {
                itemsTableBody.innerHTML = `
                    <tr>
                        <td style="border: 1px solid #000000; padding: 14px 14px; font-size: ${rowFontSize}; line-height: ${rowLineHeight}; font-weight: 700; color: #000000;">Consommations &amp;Ventes Restauration</td>
                        <td style="border: 1px solid #000000; padding: 14px 8px; font-size: ${rowFontSize}; line-height: ${rowLineHeight}; text-align: center; font-weight: 700;">1</td>
                        <td style="border: 1px solid #000000; padding: 14px 10px; font-size: ${rowFontSize}; line-height: ${rowLineHeight}; text-align: right; font-weight: 700;">${Math.round(order.total_amount).toLocaleString('fr-FR')}FCFA</td>
                        <td style="border: 1px solid #000000; padding: 14px 14px; font-size: ${rowFontSize}; line-height: ${rowLineHeight}; text-align: right; font-weight: 800;">${Math.round(order.total_amount).toLocaleString('fr-FR')}FCFA</td>
                    </tr>
                `;
            } else {
                itemsTableBody.innerHTML = items.map(it => {
                    const name = it.item_name || it.menu_item_name || (it.menu_item ? it.menu_item.name : ('Plat #' + it.menu_item_id));
                    const qty = it.quantity || 1;
                    const price = it.unit_price || 0;
                    const lineTotal = it.subtotal || (qty * price);
                    return `
                        <tr>
                            <td style="border: 1px solid #000000; padding: ${rowPadding}; font-size: ${rowFontSize}; line-height: ${rowLineHeight}; font-weight: 700; color: #000000;">${name}</td>
                            <td style="border: 1px solid #000000; padding: ${rowPadding}; font-size: ${rowFontSize}; line-height: ${rowLineHeight}; text-align: center; font-weight: 700;">${qty}</td>
                            <td style="border: 1px solid #000000; padding: ${rowPadding}; font-size: ${rowFontSize}; line-height: ${rowLineHeight}; text-align: right; font-weight: 700;">${Math.round(price).toLocaleString('fr-FR')}FCFA</td>
                            <td style="border: 1px solid #000000; padding: ${rowPadding}; font-size: ${rowFontSize}; line-height: ${rowLineHeight}; text-align: right; font-weight: 800;">${Math.round(lineTotal).toLocaleString('fr-FR')}FCFA</td>
                        </tr>
                    `;
                }).join('');
            }

            // 7. Totaux Financiers DGI
            const taxRateVal = cfg.tax_rate || 18.0;
            const ttcVal = order.total_amount || 0;
            const htVal = ttcVal / (1 + (taxRateVal / 100));
            const taxVal = ttcVal - htVal;

            const elSubTot = document.getElementById('invPaperSubTotal');
            if (elSubTot) elSubTot.innerText = Math.round(htVal).toLocaleString('fr-FR') + ' FCFA';
            const elTaxRate = document.getElementById('invPaperTaxRate');
            if (elTaxRate) elTaxRate.innerText = `${taxRateVal}%`;
            const elTax = document.getElementById('invPaperTaxAmount');
            if (elTax) elTax.innerText = Math.round(taxVal).toLocaleString('fr-FR') + ' FCFA';
            const elGrand = document.getElementById('invPaperGrandTotal');
            if (elGrand) elGrand.innerText = Math.round(ttcVal).toLocaleString('fr-FR') + ' FCFA';

            // 8. Homologation DGI & Conditions
            const elPayTerms = document.getElementById('invPaperPaymentTerms');
            if (elPayTerms) elPayTerms.innerText = `Règlement comptant (${paymentMethod.toLowerCase()}).`;
            const elHRef = document.getElementById('invPaperHomologationRef');
            if (elHRef) elHRef.innerText = dgiRef;
            const elNim = document.getElementById('invPaperNim');
            if (elNim) elNim.innerText = nimVal;
            const elHDate = document.getElementById('invPaperHomologationDate');
            if (elHDate) elHDate.innerText = formattedDate;
            const elSha = document.getElementById('invPaperSha256');
            if (elSha) elSha.innerText = shaCode.length >36 ? shaCode.substring(0, 36) + '...' : shaCode;

            // 9. Pied de Page (3 Colonnes Référence)
            const elFBrand = document.getElementById('invFooterBrandName');
            if (elFBrand) elFBrand.innerText = brandName;
            const elFIfu = document.getElementById('invFooterIfu');
            if (elFIfu) elFIfu.innerText = ifuVal;
            const elFRccm = document.getElementById('invFooterRccm');
            if (elFRccm) elFRccm.innerText = rccmVal;
            const elFNim = document.getElementById('invFooterNim');
            if (elFNim) elFNim.innerText = nimVal;

            const elFAddr = document.getElementById('invFooterAddress');
            if (elFAddr) elFAddr.innerText = addressVal;
            const elFPhone = document.getElementById('invFooterPhone');
            if (elFPhone) elFPhone.innerText = phoneVal;
            const elFEmail = document.getElementById('invFooterEmail');
            if (elFEmail) elFEmail.innerText = emailVal;

            const elFRegime = document.getElementById('invFooterRegime');
            if (elFRegime) elFRegime.innerText = regimeVal;
            const elFDiv = document.getElementById('invFooterDivision');
            if (elFDiv) elFDiv.innerText = divisionVal;

            document.getElementById('invoiceModal').classList.remove('hidden');
        }

        function closeRestaurantInvoiceModal() {
            document.getElementById('invoiceModal').classList.add('hidden');
        }

        async function loadDailyReportData() {
            try {
                let targetDate = document.getElementById('reportDateInput').value;
                if (!targetDate) {
                    targetDate = new Date().toISOString().split('T')[0];
                    document.getElementById('reportDateInput').value = targetDate;
                }
                const res = await fetch(`/api/v1/admin/daily-report?target_date=${targetDate}`, {
                    headers: { 'Authorization': 'Bearer ' + token }
                });
                if (res.ok) {
                    const data = await res.json();
                    currentDailyReport = data;
                    
                    document.getElementById('reportTotalTTC').innerText = Math.round(data.total_ttc).toLocaleString('fr-FR') + ' FCFA';
                    document.getElementById('reportTotalHT').innerText = Math.round(data.total_ht).toLocaleString('fr-FR') + ' FCFA';
                    document.getElementById('reportTotalTVA').innerText = Math.round(data.total_tva).toLocaleString('fr-FR') + ' FCFA';
                    document.getElementById('reportTotalOrders').innerText = data.total_orders;

                    // Bannière DGI
                    const banner = document.getElementById('dgiStatusBanner');
                    const btnCert = document.getElementById('btnCertifyDGI');
                    if (data.is_certified_dgi) {
                        banner.style.background = 'rgba(16, 185, 129, 0.15)';
                        banner.style.border = '1px solid #10b981';
                        banner.innerHTML = `
                            <div>
                                <strong style="color: #34d399; font-size: 1rem;">JOURNÉE FISCALEMENT CERTIFIÉE AUPRÈS DE LA DGI</strong><br>
                                <span style="font-size: 0.85rem; color: #e2e8f0;">RéfFiscale : <strong>${data.dgi_reference}</strong> •Horodatage : ${new Date(data.dgi_certified_at).toLocaleString('fr-FR')}</span>
                            </div>
                            <span class="badge badge-success" style="font-size: 0.85rem; padding: 0.5rem 1rem;">CONFORMEDGI</span>
                        `;
                        btnCert.disabled = true;
                        btnCert.innerText = ' Déjà Certifié DGI';
                        btnCert.style.opacity = '0.6';
                    } else {
                        banner.style.background = 'rgba(245, 158, 11, 0.15)';
                        banner.style.border = '1px solid #f59e0b';
                        banner.innerHTML = `
                            <div>
                                <strong style="color: #fbbf24; font-size: 1rem;">Bilan Journalier non certifié auprès de la DGI</strong><br>
                                <span style="font-size: 0.85rem; color: #e2e8f0;">Cliquezci-dessous sur « Certifier la Journée avec la DGI » pour sceller les ventes du jour et générer la facture normalisée.</span>
                            </div>
                            <span class="badge badge-warning" style="font-size: 0.85rem; padding: 0.5rem 1rem;">ÀCERTIFIER</span>
                        `;
                        btnCert.disabled = false;
                        btnCert.innerText = ' Certifier la Journée avec la DGI';
                        btnCert.style.opacity = '1';
                    }

                    // Répartition par mode de paiement
                    const payContainer = document.getElementById('reportPaymentList');
                    const payKeys = Object.keys(data.payment_breakdown);
                    if (payKeys.length === 0) {
                        payContainer.innerHTML = '<span style="color: var(--text-muted); font-size: 0.85rem;">Aucunencaissement sur cette date.</span>';
                    } else {
                        payContainer.innerHTML = payKeys.map(k => `
                            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 0.4rem;">
                                <span style="font-size: 0.9rem;">${k}</span>
                                <strong>${Math.round(data.payment_breakdown[k]).toLocaleString('fr-FR')}FCFA</strong>
                            </div>
                        `).join('');
                    }

                    // Répartition par gérant
                    const mgrContainer = document.getElementById('reportManagerList');
                    if (data.manager_breakdown.length === 0) {
                        mgrContainer.innerHTML = '<span style="color: var(--text-muted); font-size: 0.85rem;">Aucungérant n\’a vendu sur cette date.</span>';
                    } else {
                        mgrContainer.innerHTML = data.manager_breakdown.map(m => `
                            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 0.4rem;">
                                <div>
                                    <strong style="font-size: 0.9rem;">${m.name}</strong>
                                    <span style="font-size: 0.75rem; color: var(--text-muted);">(${m.login} - ${m.orders_count}commandes)</span>
                                </div>
                                <strong style="color: var(--manager-accent);">${Math.round(m.total_amount).toLocaleString('fr-FR')}FCFA</strong>
                            </div>
                        `).join('');
                    }
                }
            } catch (err) {
                console.error(err);
            }
        }

        async function handleCertifyDGI() {
            const targetDate = document.getElementById('reportDateInput').value;
            if (!confirm(`Confirmez-vous la certification officielle de la journée du ${targetDate} auprès de la Direction Générale des Impôts (DGI) ? Cette action scelle fiscalement les montants.`)) {
                return;
            }
            try {
                const res = await fetch(`/api/v1/admin/daily-report/certify-dgi?target_date=${targetDate}`, {
                    method: 'POST',
                    headers: { 'Authorization': 'Bearer ' + token }
                });
                const resData = await res.json();
                if (res.ok) {
                    alert(` ${resData.message}\nRéférence Fiscale : ${resData.dgi_reference}`);
                    await loadDailyReportData();
                    await loadAdminOrdersData();
                } else {
                    alert(`Erreur : ${resData.detail || 'Impossible de certifier'}`);
                }
            } catch (err) {
                alert('Erreur réseau lors de la certification DGI : ' + err.message);
            }
        }

        function printDailyInvoiceModal() {
            if (!currentDailyReport) {
                alert("Veuillez d'abord charger les données de la journée.");
                return;
            }
            const d = currentDailyReport;
            const cfg = restaurantConfig || {};
            const rName = cfg.restaurant_name || cfg.company_name || 'ÉTABLISSEMENT';
            const rIfu = d.dgi_nif || cfg.ifu || cfg.nif || '-';
            const rNim = d.dgi_nim || cfg.nim || 'RESTO-DGI-MCF-01';
            const rRccm = cfg.rccm || '-';
            const rRegime = cfg.default_tax_regime || '-';
            const rDivision = cfg.fiscal_division || cfg.tax_center || '-';
            const rPhone = cfg.phone || '-';
            const rEmail = cfg.email || '-';
            const rAddress = cfg.address || '-';

            // Métadonnées
            const elInvNum = document.getElementById('modalDgiInvoiceNum');
            if (elInvNum) elInvNum.innerText = d.invoice_number || ('FACT-DGI-' + d.invoice_date);
            const elDate = document.getElementById('modalDgiInvoiceDate');
            if (elDate) elDate.innerText = d.invoice_date;
            const elRef = document.getElementById('modalDgiRef');
            if (elRef) elRef.innerText = d.dgi_reference || (d.invoice_number + ' (e-MCF)');

            // QR Code
            const qrContainer = document.getElementById('modalDgiQrContainer');
            if (qrContainer) {
                const qrText = encodeURIComponent(d.dgi_qr_code_data || `DGI-FNE|IFU:${rIfu}|RCCM:${rRccm}|FACT:${d.invoice_number}|DATE:${d.invoice_date}|TTC:${Math.round(d.total_ttc || 0)}|REF:${d.dgi_reference || d.invoice_number}`);
                qrContainer.innerHTML = `<img src="https://api.qrserver.com/v1/create-qr-code/?size=120x120&margin=1&data=${qrText}" style="width: 78px; height: 78px; display: block; margin: 0 auto;" alt="QR DGI" />`;
            }

            // Vendeur
            const elDgiName = document.getElementById('modalDgiRestoName');
            if (elDgiName) elDgiName.innerText = rName;
            const elDgiAddr = document.getElementById('modalDgiAddress');
            if (elDgiAddr) elDgiAddr.innerText = rAddress;
            const elDgiPhone = document.getElementById('modalDgiPhone');
            if (elDgiPhone) elDgiPhone.innerText = rPhone;
            const elDgiIfu = document.getElementById('modalDgiIfu');
            if (elDgiIfu) elDgiIfu.innerText = rIfu;
            const elDgiRccm = document.getElementById('modalDgiRccm');
            if (elDgiRccm) elDgiRccm.innerText = rRccm;
            const elDgiRegime = document.getElementById('modalDgiRegime');
            if (elDgiRegime) elDgiRegime.innerText = rRegime;

            // Client / Consolidation
            const elOrdersCnt = document.getElementById('modalDgiOrdersCountText');
            if (elOrdersCnt) elOrdersCnt.innerText = `${d.total_orders || 0} commande(s) clôturée(s)`;
            const elMgrNames = (d.manager_breakdown || []).map(m =>m.name).join(', ') || 'Gérants en caisse';
            const elMgrEl = document.getElementById('modalDgiManagerName');
            if (elMgrEl) elMgrEl.innerText = elMgrNames;

            // Lignes du tableau
            const itemsBody = document.getElementById('modalDgiItemsBody');
            if (itemsBody) {
                itemsBody.innerHTML = `
                    <tr>
                        <td style="border: 1px solid #000000; padding: 12px 14px; font-size: 11.5px; line-height: 1.55; font-weight: 700; color: #000000;">
                            Ventes Globales Restauration &amp; Boissons (Groupe B - Norme DGI)
                        </td>
                        <td style="border: 1px solid #000000; padding: 12px 8px; font-size: 11.5px; line-height: 1.55; text-align: center; font-weight: 700;">
                            ${d.total_orders || 1}
                        </td>
                        <td style="border: 1px solid #000000; padding: 12px 10px; font-size: 11.5px; line-height: 1.55; text-align: right; font-weight: 700;">
                            ${Math.round(d.total_ttc).toLocaleString('fr-FR')} FCFA
                        </td>
                        <td style="border: 1px solid #000000; padding: 12px 14px; font-size: 11.5px; line-height: 1.55; text-align: right; font-weight: 800;">
                            ${Math.round(d.total_ttc).toLocaleString('fr-FR')} FCFA
                        </td>
                    </tr>
                `;
            }

            // Totaux
            document.getElementById('modalTableHT').innerText = Math.round(d.total_ht).toLocaleString('fr-FR') + ' FCFA';
            document.getElementById('modalTableTVA').innerText = Math.round(d.total_tva).toLocaleString('fr-FR') + ' FCFA';
            document.getElementById('modalTableTTC').innerText = Math.round(d.total_ttc).toLocaleString('fr-FR') + ' FCFA';

            // Homologation
            const elHRef = document.getElementById('modalDgiHomologationRef');
            if (elHRef) elHRef.innerText = d.dgi_reference || (d.invoice_number + ' (e-MCF)');
            const elNim = document.getElementById('modalDgiNim');
            if (elNim) elNim.innerText = rNim;
            const elCertDate = document.getElementById('modalDgiCertDate');
            if (elCertDate) elCertDate.innerText = d.dgi_certified_at ? new Date(d.dgi_certified_at).toLocaleDateString('fr-FR') : d.invoice_date;
            const elSec = document.getElementById('modalDgiSecurity');
            if (elSec) elSec.innerText = d.dgi_security_code ? (d.dgi_security_code.substring(0, 36) + '...') : 'CERTIFICATION_DGI_VALIDEE';

            // Footer 3 colonnes
            const elFBrand = document.getElementById('modalDgiFooterBrand');
            if (elFBrand) elFBrand.innerText = rName;
            const elFIfu = document.getElementById('modalDgiFooterIfu');
            if (elFIfu) elFIfu.innerText = rIfu;
            const elFRccm = document.getElementById('modalDgiFooterRccm');
            if (elFRccm) elFRccm.innerText = rRccm;
            const elFNim = document.getElementById('modalDgiFooterNim');
            if (elFNim) elFNim.innerText = rNim;
            const elFAddr = document.getElementById('modalDgiFooterAddress');
            if (elFAddr) elFAddr.innerText = rAddress;
            const elFPhone = document.getElementById('modalDgiFooterPhone');
            if (elFPhone) elFPhone.innerText = rPhone;
            const elFEmail = document.getElementById('modalDgiFooterEmail');
            if (elFEmail) elFEmail.innerText = rEmail;
            const elFRegime = document.getElementById('modalDgiFooterRegime');
            if (elFRegime) elFRegime.innerText = rRegime;
            const elFDiv = document.getElementById('modalDgiFooterDivision');
            if (elFDiv) elFDiv.innerText = rDivision;

            document.getElementById('dgiInvoiceModal').classList.remove('hidden');
        }

        function closeDgiModal() {
            document.getElementById('dgiInvoiceModal').classList.add('hidden');
        }

        // =========================================================================
        // MODULE : COMMUNICATION DIRECTE ADMIN <->GÉRANT (SMS & APPEL VIDÉO WEBRTC)
        // =========================================================================
        let commContacts = [];
        let commActiveContact = null;
        let commLastMessageId = 0;
        let commPollerIntervalId = null;
        let commCurrentMode = null;
        let commIsSending = false;

        function escapeHtml(str) {
            if (!str) return '';
            return String(str)
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&#039;');
        }

        // WebRTC Global State
        let rtcPeerConnection = null;
        let rtcLocalStream = null;
        let rtcActiveCallType = 'video';
        let rtcActiveContactId = null;
        let rtcActiveContactName = '';
        let rtcCallTimerInterval = null;
        let rtcCallSeconds = 0;
        let pendingIncomingSignal = null;
        let ringtoneAudioCtx = null;

        const rtcIceConfig = {
            iceServers: [
                { urls: ["stun:stun.l.google.com:19302", "stun:stun1.l.google.com:19302"] }
            ]
        };

        // 1. Initialisation de la vue de communication
        async function initCommunicationChat(mode) {
            commCurrentMode = mode;
            await loadCommunicationContacts();

            if (mode === 'adm') {
                if (commContacts.length >0 && !commActiveContact) {
                    selectCommunicationContact(commContacts[0].id);
                } else if (commActiveContact) {
                    selectCommunicationContact(commActiveContact.id);
                }
            } else if (mode === 'mgr') {
                const adminContact = commContacts.find(c =>c.role === 'admin') || commContacts[0];
                if (adminContact) {
                    commActiveContact = adminContact;
                    const elName = document.getElementById('mgrChatAdminName');
                    if (elName) elName.innerText = adminContact.full_name + ' (Administrateur)';
                    await loadChatMessages(adminContact.id, true);
                }
            }
        }

        // 2. Chargement des contacts
        async function loadCommunicationContacts() {
            if (!token) return;
            try {
                const res = await fetch('/api/v1/communication/contacts', {
                    headers: { 'Authorization': 'Bearer ' + token }
                });
                if (!res.ok) return;
                commContacts = await res.json();

                if (currentUser && currentUser.role === 'admin') {
                    const countEl = document.getElementById('admChatManagersCount');
                    if (countEl) countEl.innerText = commContacts.length;

                    const listEl = document.getElementById('admChatContactsList');
                    if (listEl) {
                        if (commContacts.length === 0) {
                            listEl.innerHTML = '<div style="text-align: center; color: var(--text-muted); padding: 2rem 0; font-size: 0.85rem;">Aucungérant actif trouvé.</div>';
                        } else {
                            listEl.innerHTML = commContacts.map(c => {
                                const isSelected = commActiveContact && commActiveContact.id === c.id;
                                const statusColor = c.is_online ? '#10b981' : '#64748b';
                                const statusText = c.is_online ? 'En ligne' : 'Hors ligne';
                                const unreadBadge = c.unread_count >0 
                                    ? `<span style="background: #ef4444; color: white; border-radius: 9999px; font-size: 0.7rem; font-weight: 800; padding: 2px 7px;">${c.unread_count}</span>` 
                                    : '';
                                return `
                                <div onclick="selectCommunicationContact(${c.id})" style="padding: 0.75rem 1rem; border-radius: 10px; cursor: pointer; transition: all 0.2s; background: ${isSelected ? 'rgba(245, 158, 11, 0.15)' : 'rgba(19, 27, 46, 0.5)'}; border: 1px solid ${isSelected ? '#f59e0b' : 'rgba(255,255,255,0.05)'}; display: flex; align-items: center; justify-content: space-between;">
                                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                                        <div style="position: relative;">
                                            <div style="width: 36px; height: 36px; border-radius: 50%; background: #1e293b; display: flex; align-items: center; justify-content: center; font-size: 1rem;"></div>
                                            <span style="position: absolute; bottom: 0; right: 0; width: 10px; height: 10px; border-radius: 50%; background: ${statusColor}; border: 2px solid #0b0f19;"></span>
                                        </div>
                                        <div>
                                            <div style="font-weight: 700; font-size: 0.9rem; color: ${isSelected ? '#fbbf24' : 'var(--text-main)'};">${c.full_name}</div>
                                            <div style="font-size: 0.75rem; color: ${statusColor};">${statusText}</div>
                                        </div>
                                    </div>
                                    <div>${unreadBadge}</div>
                                </div>
                                `;
                            }).join('');
                        }
                    }
                }
            } catch (err) {
                console.error("Erreur contacts communication:", err);
            }
        }

        // 3. Sélection d'un interlocuteur par l'Admin
        async function selectCommunicationContact(contactId) {
            const found = commContacts.find(c =>c.id === contactId);
            if (!found) return;
            commActiveContact = found;

            const nameEl = document.getElementById('admChatActiveName');
            const statusEl = document.getElementById('admChatActiveStatus');
            if (nameEl) nameEl.innerText = found.full_name;
            if (statusEl) {
                const statusColor = found.is_online ? '#10b981' : '#94a3b8';
                const statusText = found.is_online ? ' Connecté (En ligne)' : ' Hors ligne';
                statusEl.innerHTML = `<span style="color: ${statusColor};">${statusText}</span>`;
            }

            loadCommunicationContacts();
            await loadChatMessages(contactId, true);
        }

        // 4. Chargement des messages instantanés
        async function loadChatMessages(contactId, reset = false) {
            if (!token || !contactId) return;
            try {
                const afterParam = reset ? '' : (commLastMessageId ? `&after_id=${commLastMessageId}` : '');
                const res = await fetch(`/api/v1/communication/messages?contact_id=${contactId}${afterParam}&limit=60`, {
                    headers: { 'Authorization': 'Bearer ' + token }
                });
                if (!res.ok) return;
                const msgs = await res.json();

                const containerId = (currentUser && currentUser.role === 'admin') 
                    ? 'admChatMessagesContainer' 
                    : 'mgrChatMessagesContainer';
                const container = document.getElementById(containerId);
                if (!container) return;

                if (reset) {
                    container.innerHTML = '';
                    commLastMessageId = 0;
                }

                if (reset && msgs.length === 0) {
                    container.innerHTML = '<div style="margin: auto; text-align: center; color: var(--text-muted); font-size: 0.88rem;">Aucunmessage échangé pour le moment. Dites bonjour ! </div>';
                    return;
                }

                if (msgs.length >0) {
                    const placeholder = container.querySelector('div[style*="margin: auto"]');
                    if (placeholder) placeholder.remove();

                    msgs.forEach(m => {
                        if (m.id >commLastMessageId) commLastMessageId = m.id;
                        appendMessageBubble(container, m);
                    });

                    container.scrollTop = container.scrollHeight;
                }
            } catch (err) {
                console.error("Erreur messages:", err);
            }
        }

        // 5. Ajout d'une bulle de message
        function appendMessageBubble(container, msg) {
            if (container.querySelector(`[data-msg-id="${msg.id}"]`)) return;

            const bubble = document.createElement('div');
            bubble.setAttribute('data-msg-id', msg.id);
            bubble.style.display = 'flex';
            bubble.style.flexDirection = 'column';
            bubble.style.maxWidth = '78%';

            const isAudio = msg.message_type === 'audio';

            if (msg.is_mine) {
                bubble.style.alignSelf = 'flex-end';
                const bgStyle = (currentUser && currentUser.role === 'admin')
                    ? 'linear-gradient(135deg, #f59e0b, #d97706)'
                    : 'linear-gradient(135deg, #10b981, #059669)';
                const txtColor = (currentUser && currentUser.role === 'admin') ? '#000000' : '#ffffff';
                
                let bodyHtml = '';
                if (isAudio) {
                    bodyHtml = `
                        <div style="display: flex; align-items: center; gap: 0.45rem; font-size: 0.8rem; font-weight: 800; margin-bottom: 0.35rem;">
                            <span></span>
                            <span>NoteVocale</span>
                        </div>
                        <audio controls preload="metadata" src="${msg.content}" style="max-width: 250px; height: 38px; border-radius: 8px; outline: none;"></audio>
                    `;
                } else {
                    bodyHtml = escapeHtml(msg.content);
                }

                bubble.innerHTML = `
                    <div style="background: ${bgStyle}; color: ${txtColor}; padding: ${isAudio ? '0.65rem 0.85rem' : '0.65rem 1rem'}; border-radius: 14px 14px 2px 14px; font-size: 0.9rem; font-weight: 500; word-break: break-word; box-shadow: 0 4px 12px rgba(0,0,0,0.25);">
                        ${bodyHtml}
                    </div>
                    <div style="font-size: 0.68rem; color: #94a3b8; align-self: flex-end; margin-top: 3px; display: flex; align-items: center; gap: 4px;">
                        <span>${msg.created_at || ''}</span>
                        <span style="color: #38bdf8;"></span>
                    </div>
                `;
            } else {
                bubble.style.alignSelf = 'flex-start';

                let bodyHtml = '';
                if (isAudio) {
                    bodyHtml = `
                        <div style="display: flex; align-items: center; gap: 0.45rem; font-size: 0.8rem; font-weight: 800; margin-bottom: 0.35rem; color: #38bdf8;">
                            <span></span>
                            <span>NoteVocale</span>
                        </div>
                        <audio controls preload="metadata" src="${msg.content}" style="max-width: 250px; height: 38px; border-radius: 8px; outline: none;"></audio>
                    `;
                } else {
                    bodyHtml = escapeHtml(msg.content);
                }

                bubble.innerHTML = `
                    <div style="font-size: 0.72rem; font-weight: 700; color: #fbbf24; margin-bottom: 2px; margin-left: 4px;">
                        ${escapeHtml(msg.sender_name)}
                    </div>
                    <div style="background: #1e293b; color: #f8fafc; border: 1px solid #334155; padding: ${isAudio ? '0.65rem 0.85rem' : '0.65rem 1rem'}; border-radius: 14px 14px 14px 2px; font-size: 0.9rem; word-break: break-word; box-shadow: 0 4px 12px rgba(0,0,0,0.25);">
                        ${bodyHtml}
                    </div>
                    <div style="font-size: 0.68rem; color: #64748b; margin-top: 3px; margin-left: 4px;">
                        <span>${msg.created_at || ''}</span>
                    </div>
                `;
            }
            container.appendChild(bubble);
        }

        // 6. Envoi d'un message SMS
        async function sendChatMessage(mode) {
            if (commIsSending) return;
            const inputId = mode === 'adm' ? 'admChatInput' : 'mgrChatInput';
            const input = document.getElementById(inputId);
            if (!input) return;

            const text = input.value.trim();
            if (!text) return;

            let targetId = commActiveContact ? commActiveContact.id : null;
            if (!targetId && mode === 'mgr') {
                const adminContact = commContacts.find(c =>c.role === 'admin') || commContacts[0];
                if (adminContact) targetId = adminContact.id;
            }

            if (!targetId) {
                alert("Veuillez sélectionner un destinataire.");
                return;
            }

            commIsSending = true;
            input.value = '';

            try {
                const res = await fetch('/api/v1/communication/messages', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + token
                    },
                    body: JSON.stringify({
                        receiver_id: targetId,
                        content: text,
                        message_type: 'text'
                    })
                });

                if (res.ok) {
                    const newMsg = await res.json();
                    if (newMsg.id >commLastMessageId) commLastMessageId = newMsg.id;
                    const containerId = mode === 'adm' ? 'admChatMessagesContainer' : 'mgrChatMessagesContainer';
                    const container = document.getElementById(containerId);
                    if (container) {
                        const placeholder = container.querySelector('div[style*="margin: auto"]');
                        if (placeholder) placeholder.remove();
                        appendMessageBubble(container, newMsg);
                        container.scrollTop = container.scrollHeight;
                    }
                } else {
                    const errData = await res.json().catch(() =>({}));
                    alert("Erreur d'envoi : " + (errData.detail || "Impossible d'envoyer le message"));
                }
            } catch (err) {
                console.error("Erreur envoi message:", err);
            } finally {
                commIsSending = false;
                input.focus();
            }
        }

        // --- ENREGISTREMENT ET ENVOI DE NOTES VOCALES (ADMIN <->GÉRANT) ---
        let voiceMediaRecorder = null;
        let voiceAudioChunks = [];
        let voiceTimerInterval = null;
        let voiceSeconds = 0;
        let voiceStream = null;

        function showVoiceRecordingUI(mode, isRecording) {
            const normalBar = document.getElementById(mode + 'ChatNormalBar');
            const voiceBar = document.getElementById(mode + 'ChatVoiceBar');
            if (normalBar) normalBar.classList.toggle('hidden', isRecording);
            if (voiceBar) voiceBar.classList.toggle('hidden', !isRecording);
            if (isRecording) {
                const timerEl = document.getElementById(mode + 'VoiceTimer');
                if (timerEl) timerEl.innerText = '0:00';
            }
        }

        async function startVoiceRecording(mode) {
            try {
                if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                    alert("L'enregistrement vocal requiert l'accès microphone (HTTPS ou localhost).");
                    return;
                }

                voiceStream = await navigator.mediaDevices.getUserMedia({ audio: true });

                let mimeType = '';
                if (window.MediaRecorder) {
                    if (MediaRecorder.isTypeSupported('audio/webm;codecs=opus')) {
                        mimeType = 'audio/webm;codecs=opus';
                    } else if (MediaRecorder.isTypeSupported('audio/webm')) {
                        mimeType = 'audio/webm';
                    } else if (MediaRecorder.isTypeSupported('audio/ogg;codecs=opus')) {
                        mimeType = 'audio/ogg;codecs=opus';
                    } else if (MediaRecorder.isTypeSupported('audio/mp4')) {
                        mimeType = 'audio/mp4';
                    }
                }

                voiceMediaRecorder = mimeType ? new MediaRecorder(voiceStream, { mimeType }) : new MediaRecorder(voiceStream);
                voiceAudioChunks = [];
                voiceSeconds = 0;

                voiceMediaRecorder.ondataavailable = (e) => {
                    if (e.data && e.data.size >0) {
                        voiceAudioChunks.push(e.data);
                    }
                };

                voiceMediaRecorder.start(250);

                showVoiceRecordingUI(mode, true);

                if (voiceTimerInterval) clearInterval(voiceTimerInterval);
                voiceTimerInterval = setInterval(() => {
                    voiceSeconds++;
                    const m = Math.floor(voiceSeconds / 60);
                    const s = voiceSeconds % 60;
                    const timerEl = document.getElementById(mode + 'VoiceTimer');
                    if (timerEl) timerEl.innerText = `${m}:${s < 10 ? '0' : ''}${s}`;
                }, 1000);

            } catch (err) {
                console.error("Erreur accès micro:", err);
                alert("Impossible d'accéder au microphone : " + (err.message || "Veuillez autoriser l'accès micro dans votre navigateur."));
            }
        }

        function cancelVoiceRecording(mode) {
            if (voiceTimerInterval) {
                clearInterval(voiceTimerInterval);
                voiceTimerInterval = null;
            }
            if (voiceMediaRecorder && voiceMediaRecorder.state !== 'inactive') {
                try {
                    voiceMediaRecorder.stop();
                } catch (e) {}
            }
            if (voiceStream) {
                try {
                    voiceStream.getTracks().forEach(t =>t.stop());
                } catch (e) {}
                voiceStream = null;
            }
            voiceAudioChunks = [];
            voiceMediaRecorder = null;
            showVoiceRecordingUI(mode, false);
        }

        async function stopAndSendVoiceRecording(mode) {
            if (!voiceMediaRecorder || voiceMediaRecorder.state === 'inactive') {
                cancelVoiceRecording(mode);
                return;
            }

            if (voiceTimerInterval) {
                clearInterval(voiceTimerInterval);
                voiceTimerInterval = null;
            }

            let targetId = commActiveContact ? commActiveContact.id : null;
            if (!targetId && mode === 'mgr') {
                const adminContact = commContacts.find(c =>c.role === 'admin') || commContacts[0];
                if (adminContact) targetId = adminContact.id;
            }

            if (!targetId) {
                alert("Veuillez sélectionner un destinataire avant d'envoyer la note vocale.");
                cancelVoiceRecording(mode);
                return;
            }

            voiceMediaRecorder.onstop = async () => {
                const mime = voiceMediaRecorder ? (voiceMediaRecorder.mimeType || 'audio/webm') : 'audio/webm';
                const blob = new Blob(voiceAudioChunks, { type: mime });
                if (voiceStream) {
                    try {
                        voiceStream.getTracks().forEach(t =>t.stop());
                    } catch (e) {}
                    voiceStream = null;
                }
                voiceMediaRecorder = null;
                voiceAudioChunks = [];
                showVoiceRecordingUI(mode, false);

                if (blob.size < 100) {
                    alert("Enregistrement vocal trop court.");
                    return;
                }

                const reader = new FileReader();
                reader.onloadend = async () => {
                    const base64Audio = reader.result;
                    await sendAudioMessage(targetId, base64Audio, mode);
                };
                reader.readAsDataURL(blob);
            };

            voiceMediaRecorder.stop();
        }

        async function sendAudioMessage(targetId, base64Audio, mode) {
            try {
                const res = await fetch('/api/v1/communication/messages', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + token
                    },
                    body: JSON.stringify({
                        receiver_id: targetId,
                        content: base64Audio,
                        message_type: 'audio'
                    })
                });

                if (res.ok) {
                    const newMsg = await res.json();
                    if (newMsg.id >commLastMessageId) commLastMessageId = newMsg.id;
                    const containerId = mode === 'adm' ? 'admChatMessagesContainer' : 'mgrChatMessagesContainer';
                    const container = document.getElementById(containerId);
                    if (container) {
                        const placeholder = container.querySelector('div[style*="margin: auto"]');
                        if (placeholder) placeholder.remove();
                        appendMessageBubble(container, newMsg);
                        container.scrollTop = container.scrollHeight;
                    }
                } else {
                    const errData = await res.json().catch(() =>({}));
                    alert("Erreur d'envoi du vocal : " + (errData.detail || "Échec"));
                }
            } catch (err) {
                console.error("Erreur envoi note vocale:", err);
                alert("Erreur réseau lors de l'envoi du vocal : " + err.message);
            }
        }

        function openDirectCommunicationChat() {
            if (currentUser && currentUser.role === 'admin') {
                switchAdminTab('chat');
            } else {
                switchManagerTab('chat');
            }
        }

        function handleChatInputKey(event, mode) {
            if (event.key === 'Enter') {
                event.preventDefault();
                sendChatMessage(mode);
            }
        }

        function insertQuickMessage(mode, text) {
            const inputId = mode === 'adm' ? 'admChatInput' : 'mgrChatInput';
            const input = document.getElementById(inputId);
            if (input) {
                input.value = text;
                input.focus();
            }
        }

        // 7. Surveillance d'arrière-plan
        function startCommunicationPoller() {
            if (commPollerIntervalId) clearInterval(commPollerIntervalId);
            commPollerIntervalId = setInterval(async () => {
                await pollCommunicationUpdates();
            }, 2000);
        }

        function stopCommunicationPoller() {
            if (commPollerIntervalId) {
                clearInterval(commPollerIntervalId);
                commPollerIntervalId = null;
            }
        }

        async function pollCommunicationUpdates() {
            if (!token) return;
            try {
                // A. Nombre de messages non lus
                const resUnread = await fetch('/api/v1/communication/unread_count', {
                    headers: { 'Authorization': 'Bearer ' + token }
                });
                if (resUnread.ok) {
                    const data = await resUnread.json();
                    const count = data.unread_count || 0;
                    
                    const admBadge = document.getElementById('admChatBadge');
                    if (admBadge) {
                        admBadge.innerText = count;
                        admBadge.classList.toggle('hidden', count === 0);
                    }
                    const mgrBadge = document.getElementById('mgrChatBadge');
                    if (mgrBadge) {
                        mgrBadge.innerText = count;
                        mgrBadge.classList.toggle('hidden', count === 0);
                    }
                    const hdrBadge = document.getElementById('headerChatBadge');
                    if (hdrBadge) {
                        hdrBadge.innerText = count;
                        hdrBadge.style.display = count >0 ? 'flex' : 'none';
                    }
                }

                // B. Signaux WebRTC pour les appels vidéo entrants
                const resSignals = await fetch('/api/v1/communication/signals', {
                    headers: { 'Authorization': 'Bearer ' + token }
                });
                if (resSignals.ok) {
                    const signals = await resSignals.json();
                    for (const s of signals) {
                        await handleIncomingWebRTCSignal(s);
                    }
                }

                // C. Si l'onglet Chat est actuellement visible, charger les nouveaux messages
                const admSec = document.getElementById('admSectionChat');
                const mgrSec = document.getElementById('mgrSectionChat');
                const isChatVisible = (admSec && !admSec.classList.contains('hidden')) || (mgrSec && !mgrSec.classList.contains('hidden'));

                if (isChatVisible) {
                    let targetId = commActiveContact ? commActiveContact.id : null;
                    if (!targetId && currentUser && currentUser.role !== 'admin') {
                        const adminContact = commContacts.find(c =>c.role === 'admin') || commContacts[0];
                        if (adminContact) targetId = adminContact.id;
                    }
                    if (targetId) {
                        await loadChatMessages(targetId, false);
                    }
                }
            } catch (err) {
                // Silencieux
            }
        }

        // =========================================================================
        // WEBRTC : APPELS VIDÉO & AUDIO EN TEMPS RÉEL (ADMIN <->GÉRANT)
        // =========================================================================

        async function initiateWebRTCCall(callType = 'video') {
            rtcActiveCallType = callType;

            let target = commActiveContact;
            if (!target && currentUser && currentUser.role !== 'admin') {
                target = commContacts.find(c =>c.role === 'admin') || commContacts[0];
            }
            if (!target) {
                alert("Veuillez sélectionner un correspondant pour l'appel.");
                return;
            }

            rtcActiveContactId = target.id;
            rtcActiveContactName = target.full_name;

            const modal = document.getElementById('videoCallModal');
            if (modal) modal.classList.remove('hidden');

            document.getElementById('callParticipantName').innerText = rtcActiveContactName;
            document.getElementById('callTypeBadge').innerText = callType === 'video' ? ' APPEL VIDÉO SÉCURISÉ' : ' APPEL AUDIO SÉCURISÉ';
            document.getElementById('callStatusText').innerText = "Sonnerie chez l'interlocuteur...";

            try {
                try {
                    rtcLocalStream = await navigator.mediaDevices.getUserMedia({
                        video: callType === 'video',
                        audio: true
                    });
                } catch (camErr) {
                    console.warn("Caméra indisponible, bascule audio seule:", camErr);
                    rtcLocalStream = await navigator.mediaDevices.getUserMedia({
                        video: false,
                        audio: true
                    });
                }

                const localVideo = document.getElementById('localVideo');
                if (localVideo) localVideo.srcObject = rtcLocalStream;

                setupPeerConnection();

                rtcLocalStream.getTracks().forEach(track => {
                    rtcPeerConnection.addTrack(track, rtcLocalStream);
                });

                const offer = await rtcPeerConnection.createOffer();
                await rtcPeerConnection.setLocalDescription(offer);

                await sendWebRTCSignal(rtcActiveContactId, 'offer', JSON.stringify(offer));

            } catch (err) {
                console.error("Erreur lancement appel:", err);
                alert("Impossible de démarrer l'appel : " + err.message);
                hangupActiveCall();
            }
        }

        function setupPeerConnection() {
            if (rtcPeerConnection) {
                try { rtcPeerConnection.close(); } catch(e){}
            }

            rtcPeerConnection = new RTCPeerConnection(rtcIceConfig);

            rtcPeerConnection.ontrack = (event) => {
                const remoteVideo = document.getElementById('remoteVideo');
                const placeholder = document.getElementById('remoteVideoPlaceholder');
                if (remoteVideo && event.streams && event.streams[0]) {
                    remoteVideo.srcObject = event.streams[0];
                    if (placeholder) placeholder.style.display = 'none';
                    document.getElementById('callStatusText').innerText = "Connecté (En direct) ";
                    startCallTimer();
                }
            };

            rtcPeerConnection.onicecandidate = async (event) => {
                if (event.candidate && rtcActiveContactId) {
                    await sendWebRTCSignal(rtcActiveContactId, 'candidate', JSON.stringify(event.candidate));
                }
            };

            rtcPeerConnection.onconnectionstatechange = () => {
                if (!rtcPeerConnection) return;
                const state = rtcPeerConnection.connectionState;
                if (state === 'connected') {
                    document.getElementById('callStatusText').innerText = "Liaison P2P Établie ";
                } else if (state === 'disconnected' || state === 'failed' || state === 'closed') {
                    hangupActiveCall(false);
                }
            };
        }

        async function handleIncomingWebRTCSignal(signal) {
            if (signal.signal_type === 'offer') {
                pendingIncomingSignal = signal;
                rtcActiveContactId = signal.sender_id;
                rtcActiveContactName = signal.sender_name;

                const incomingModal = document.getElementById('incomingCallModal');
                const callerNameEl = document.getElementById('incomingCallerName');
                if (callerNameEl) callerNameEl.innerText = signal.sender_name;
                if (incomingModal) incomingModal.classList.remove('hidden');

                playRingtone();

            } else if (signal.signal_type === 'answer') {
                if (rtcPeerConnection) {
                    try {
                        const answerDesc = new RTCSessionDescription(JSON.parse(signal.payload));
                        await rtcPeerConnection.setRemoteDescription(answerDesc);
                        document.getElementById('callStatusText').innerText = "Appel accepté, synchronisation... ";
                    } catch (e) {
                        console.error("Erreur setRemoteDescription answer:", e);
                    }
                }

            } else if (signal.signal_type === 'candidate') {
                if (rtcPeerConnection && rtcPeerConnection.remoteDescription) {
                    try {
                        const cand = new RTCIceCandidate(JSON.parse(signal.payload));
                        await rtcPeerConnection.addIceCandidate(cand);
                    } catch (e) {
                        console.error("Erreur addIceCandidate:", e);
                    }
                }

            } else if (signal.signal_type === 'hangup' || signal.signal_type === 'reject') {
                stopRingtone();
                const incomingModal = document.getElementById('incomingCallModal');
                if (incomingModal) incomingModal.classList.add('hidden');
                hangupActiveCall(false);
            }
        }

        async function acceptIncomingCall() {
            stopRingtone();
            const incomingModal = document.getElementById('incomingCallModal');
            if (incomingModal) incomingModal.classList.add('hidden');

            if (!pendingIncomingSignal) return;

            const modal = document.getElementById('videoCallModal');
            if (modal) modal.classList.remove('hidden');

            document.getElementById('callParticipantName').innerText = rtcActiveContactName;
            document.getElementById('callTypeBadge').innerText = ' APPEL VIDÉO SÉCURISÉ';
            document.getElementById('callStatusText').innerText = "Connexion en cours... ";

            try {
                try {
                    rtcLocalStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
                } catch (e) {
                    rtcLocalStream = await navigator.mediaDevices.getUserMedia({ video: false, audio: true });
                }

                const localVideo = document.getElementById('localVideo');
                if (localVideo) localVideo.srcObject = rtcLocalStream;

                setupPeerConnection();

                rtcLocalStream.getTracks().forEach(track => {
                    rtcPeerConnection.addTrack(track, rtcLocalStream);
                });

                const offerDesc = new RTCSessionDescription(JSON.parse(pendingIncomingSignal.payload));
                await rtcPeerConnection.setRemoteDescription(offerDesc);

                const answer = await rtcPeerConnection.createAnswer();
                await rtcPeerConnection.setLocalDescription(answer);

                await sendWebRTCSignal(rtcActiveContactId, 'answer', JSON.stringify(answer));
                startCallTimer();

            } catch (err) {
                console.error("Erreur acceptation appel:", err);
                alert("Erreur lors de la réponse à l'appel : " + err.message);
                hangupActiveCall();
            } finally {
                pendingIncomingSignal = null;
            }
        }

        async function rejectIncomingCall() {
            stopRingtone();
            const incomingModal = document.getElementById('incomingCallModal');
            if (incomingModal) incomingModal.classList.add('hidden');

            if (pendingIncomingSignal) {
                await sendWebRTCSignal(pendingIncomingSignal.sender_id, 'reject', '{}');
                pendingIncomingSignal = null;
            }
        }

        async function hangupActiveCall(notifyRemote = true) {
            stopRingtone();
            stopCallTimer();

            if (notifyRemote && rtcActiveContactId) {
                await fetch(`/api/v1/communication/call/hangup?contact_id=${rtcActiveContactId}`, {
                    method: 'POST',
                    headers: { 'Authorization': 'Bearer ' + token }
                }).catch(() => {});
            }

            if (rtcLocalStream) {
                rtcLocalStream.getTracks().forEach(t => {
                    try { t.stop(); } catch(e){}
                });
                rtcLocalStream = null;
            }

            if (rtcPeerConnection) {
                try { rtcPeerConnection.close(); } catch(e){}
                rtcPeerConnection = null;
            }

            const localVideo = document.getElementById('localVideo');
            if (localVideo) localVideo.srcObject = null;
            const remoteVideo = document.getElementById('remoteVideo');
            if (remoteVideo) remoteVideo.srcObject = null;

            const placeholder = document.getElementById('remoteVideoPlaceholder');
            if (placeholder) placeholder.style.display = 'flex';

            const modal = document.getElementById('videoCallModal');
            if (modal) modal.classList.add('hidden');

            const incomingModal = document.getElementById('incomingCallModal');
            if (incomingModal) incomingModal.classList.add('hidden');

            rtcActiveContactId = null;
            rtcActiveContactName = '';
        }

        async function sendWebRTCSignal(receiverId, signalType, payload) {
            if (!token || !receiverId) return;
            try {
                await fetch('/api/v1/communication/signal', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + token
                    },
                    body: JSON.stringify({
                        receiver_id: receiverId,
                        signal_type: signalType,
                        payload: payload
                    })
                });
            } catch (err) {
                console.error("Erreur envoi signal WebRTC:", err);
            }
        }

        function toggleLocalMicrophone() {
            if (!rtcLocalStream) return;
            const audioTrack = rtcLocalStream.getAudioTracks()[0];
            if (audioTrack) {
                audioTrack.enabled = !audioTrack.enabled;
                const btn = document.getElementById('btnToggleMic');
                if (btn) {
                    btn.innerText = audioTrack.enabled ? '' : '';
                    btn.style.background = audioTrack.enabled ? 'var(--surface-hover)' : 'rgba(239, 68, 68, 0.4)';
                }
            }
        }

        function toggleLocalCamera() {
            if (!rtcLocalStream) return;
            const videoTrack = rtcLocalStream.getVideoTracks()[0];
            if (videoTrack) {
                videoTrack.enabled = !videoTrack.enabled;
                const btn = document.getElementById('btnToggleCam');
                if (btn) {
                    btn.innerText = videoTrack.enabled ? '' : '';
                    btn.style.background = videoTrack.enabled ? 'var(--surface-hover)' : 'rgba(239, 68, 68, 0.4)';
                }
            }
        }

        function startCallTimer() {
            stopCallTimer();
            rtcCallSeconds = 0;
            const timerEl = document.getElementById('callDurationTimer');
            if (timerEl) timerEl.innerText = "00:00";
            rtcCallTimerInterval = setInterval(() => {
                rtcCallSeconds++;
                const mins = String(Math.floor(rtcCallSeconds / 60)).padStart(2, '0');
                const secs = String(rtcCallSeconds % 60).padStart(2, '0');
                if (timerEl) timerEl.innerText = `${mins}:${secs}`;
            }, 1000);
        }

        function stopCallTimer() {
            if (rtcCallTimerInterval) {
                clearInterval(rtcCallTimerInterval);
                rtcCallTimerInterval = null;
            }
        }

        function playRingtone() {
            try {
                if (!ringtoneAudioCtx) {
                    ringtoneAudioCtx = new (window.AudioContext || window.webkitAudioContext)();
                }
                if (ringtoneAudioCtx.state === 'suspended') {
                    ringtoneAudioCtx.resume();
                }
                const osc = ringtoneAudioCtx.createOscillator();
                const gain = ringtoneAudioCtx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(440, ringtoneAudioCtx.currentTime);
                osc.frequency.setValueAtTime(480, ringtoneAudioCtx.currentTime + 0.4);

                gain.gain.setValueAtTime(0.15, ringtoneAudioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, ringtoneAudioCtx.currentTime + 1.2);

                osc.connect(gain);
                gain.connect(ringtoneAudioCtx.destination);
                osc.start();
                osc.stop(ringtoneAudioCtx.currentTime + 1.2);
            } catch (e) {}
        }

        function stopRingtone() {}
    </script>

    <!-- MODAL FACTURE NORMALISÉE DGI JOURNALIÈRE (MODÈLE MONOCHROME DE RÉFÉRENCE) -->
    <div id="dgiInvoiceModal" class="hidden" style="position: fixed; inset: 0; background: rgba(0,0,0,0.85); z-index: 999; display: flex; align-items: center; justify-content: center; padding: 1.5rem; overflow-y: auto;">
        <div style="max-width: 860px; width: 100%; max-height: 95vh; overflow-y: auto; position: relative;">
            
            <div class="modal-actions-bar" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding: 0.75rem 1.25rem; background: #1f2937; border-radius: 12px; border: 1px solid #374151;">
                <span style="color: #34d399; font-weight: 700; font-size: 0.95rem;">
                     Facture Normalisée Journalière DGI (e-MCF)
                </span>
                <div style="display: flex; gap: 0.75rem;">
                    <button class="btn btn-primary" onclick="window.print()" style="background: #000000; color: white; border: 1px solid #475569; font-weight: 700; font-size: 0.85rem; padding: 0.5rem 1rem;">
                         Imprimer la Facture Fiscale
                    </button>
                    <button class="btn btn-secondary" onclick="closeDgiModal()" style="font-size: 0.85rem; padding: 0.5rem 1rem;">
                         Fermer
                    </button>
                </div>
            </div>

            <div class="corporate-invoice-paper">
                <!-- 1. EN-TÊTE -->
                <div id="invPaperHeaderSec" style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.25rem;">
                    <div>
                        <h1 style="font-size: 2.3rem; font-weight: 900; color: #000000; margin: 0 0 4px 0; letter-spacing: 1.5px; text-transform: uppercase; line-height: 1;">
                            FACTURE
                        </h1>
                        <div style="font-size: 0.75rem; font-weight: 800; color: #166534; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px;">
                             FACTURE NORMALISÉE JOURNALIÈRE DGI (e-MCF)
                        </div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 1rem; text-align: left;">
                        <table style="font-size: 0.82rem; color: #000000; border-collapse: collapse;">
                            <tr>
                                <td style="font-weight: 800; padding: 2px 8px 2px 0;">Numérode facture :</td>
                                <td id="modalDgiInvoiceNum" style="font-weight: 700; padding: 2px 0;">-</td>
                            </tr>
                            <tr>
                                <td style="font-weight: 800; padding: 2px 8px 2px 0;">Datede facturation :</td>
                                <td id="modalDgiInvoiceDate" style="font-weight: 600; padding: 2px 0;">-</td>
                            </tr>
                            <tr>
                                <td style="font-weight: 800; padding: 2px 8px 2px 0;">Échéance :</td>
                                <td style="font-weight: 600; padding: 2px 0;">Clôturejournalière</td>
                            </tr>
                            <tr>
                                <td style="font-weight: 800; padding: 2px 8px 2px 0;">Référence :</td>
                                <td id="modalDgiRef" style="font-weight: 700; padding: 2px 0; font-family: monospace;">-</td>
                            </tr>
                        </table>
                        <div style="text-align: center; border-left: 1.5px solid #000000; padding-left: 0.85rem; min-width: 85px;">
                            <div id="modalDgiQrContainer" style="width: 78px; height: 78px; margin: 0 auto;"></div>
                            <div style="font-size: 0.58rem; font-weight: 800; color: #166534; margin-top: 2px; letter-spacing: 0.5px;">
                                SCAN DGI e-MCF
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 2. SECTION VENDEUR ET CLIENT -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-bottom: 2rem;">
                    <!-- VENDEUR -->
                    <div style="font-size: 0.82rem; color: #111827; line-height: 1.45;">
                        <div style="font-size: 0.95rem; font-weight: 900; color: #000000; margin-bottom: 0.35rem;">
                            Vendeur
                        </div>
                        <div id="modalDgiRestoName" style="font-weight: 800; font-size: 0.9rem; color: #000000;">-</div>
                        <div id="modalDgiAddress" style="font-style: italic; color: #4b5563;">-</div>
                        <div>Tél : <span id="modalDgiPhone">-</span></div>
                        <div style="margin-top: 4px; font-size: 0.78rem; color: #374151;">
                            <span>IFU : <strong id="modalDgiIfu">-</strong></span> • 
                            <span>RCCM : <strong id="modalDgiRccm">-</strong></span>
                        </div>
                        <div style="font-size: 0.78rem; color: #374151;">
                            <span>Régime : <span id="modalDgiRegime">-</span></span>
                        </div>
                    </div>

                    <!-- CLIENT -->
                    <div style="font-size: 0.82rem; color: #111827; line-height: 1.45;">
                        <div style="font-size: 0.95rem; font-weight: 900; color: #000000; margin-bottom: 0.35rem;">
                            Client
                        </div>
                        <div style="font-weight: 800; font-size: 0.9rem; color: #000000;">SessionVentes Journalières Clôturée</div>
                        <div style="font-style: italic; color: #4b5563;">Gérant(s) : <strong id="modalDgiManagerName">Gérantsen caisse</strong></div>
                        <div style="color: #4b5563;">ConsommationsRestaurant &amp; Boissons</div>
                        <div style="margin-top: 4px; font-size: 0.78rem; color: #374151;">
                            <span>Activité : <strong id="modalDgiOrdersCountText">-</strong></span>
                        </div>
                    </div>
                </div>

                <!-- 3. TABLEAU -->
                <table class="corporate-inv-table">
                    <thead>
                        <tr>
                            <th style="width: 48%; text-align: left;">DESIGNATION</th>
                            <th style="width: 10%; text-align: center;">QTE</th>
                            <th style="width: 20%; text-align: right;">PRIXUNIT</th>
                            <th style="width: 22%; text-align: right;">MONTANT</th>
                        </tr>
                    </thead>
                    <tbody id="modalDgiItemsBody">
                        <!-- Dynamique -->
                    </tbody>
                </table>

                <!-- 4. TOTAUX -->
                <div style="width: 100%; margin-top: 0; margin-bottom: 2rem;">
                    <table class="corporate-inv-totals-table">
                        <tr>
                            <td colspan="2" style="font-weight: 800; text-transform: uppercase;">MONTANTHT</td>
                            <td id="modalTableHT" style="text-align: right; font-weight: 700;">0FCFA</td>
                        </tr>
                        <tr>
                            <td style="font-weight: 800;">TVA</td>
                            <td style="text-align: center; font-weight: 700; width: 45px;">18%</td>
                            <td id="modalTableTVA" style="text-align: right; font-weight: 700;">0FCFA</td>
                        </tr>
                        <tr class="total-ttc-row">
                            <td colspan="2" style="padding: 8px 10px; font-size: 0.9rem; letter-spacing: 0.5px; text-transform: uppercase;">TOTALTTC</td>
                            <td id="modalTableTTC" style="padding: 8px 10px; text-align: right; font-size: 0.95rem;">0FCFA</td>
                        </tr>
                    </table>
                </div>

                <!-- 5. CONDITIONS & HOMOLOGATION DGI (SANS SIGNATURE) -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-top: 0.6rem; margin-bottom: 1rem;">
                    <div>
                        <div style="font-weight: 900; font-size: 0.82rem; color: #000000; margin-bottom: 3px;">
                            Conditions et modalités de paiement
                        </div>
                        <div style="font-size: 0.76rem; color: #1f2937; margin-bottom: 6px; line-height: 1.4;">
                            Règlement comptant journalier clôturé (Espèces, Mobile Money, Carte bancaire).
                        </div>
                    </div>
                    <div>
                        <div style="border: 1px solid #166534; background: #f0fdf4; border-radius: 4px; padding: 6px 8px; font-size: 0.72rem; color: #14532d; line-height: 1.4;">
                            <div style="font-weight: 900; text-transform: uppercase; margin-bottom: 2px; color: #166534;">
                                 Homologation DGI / e-MCF
                            </div>
                            <div>Réf.FNE : <strong id="modalDgiHomologationRef">-</strong></div>
                            <div>Machine(NIM) : <strong id="modalDgiNim">-</strong> •Daté du : <span id="modalDgiCertDate">-</span></div>
                            <div>SceauSHA-256 : <span id="modalDgiSecurity" style="font-family: monospace; font-size: 0.65rem;">-</span></div>
                        </div>
                    </div>
                </div>

                <!-- 6. PIED DE PAGE 3 COLONNES -->
                <div style="font-size: 0.72rem; color: #374151; border-top: 1px solid #d1d5db; padding-top: 8px; line-height: 1.45;">
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem;">
                        <div>
                            <div style="font-weight: 800; color: #000000; text-transform: uppercase; font-size: 0.75rem; margin-bottom: 2px;">
                                Mon entreprise
                            </div>
                            <div id="modalDgiFooterBrand" style="font-weight: 700; color: #000000;">-</div>
                            <div>IFU : <span id="modalDgiFooterIfu">-</span></div>
                            <div>RCCM : <span id="modalDgiFooterRccm">-</span></div>
                            <div>NIM : <span id="modalDgiFooterNim">-</span></div>
                        </div>
                        <div>
                            <div style="font-weight: 800; color: #000000; text-transform: uppercase; font-size: 0.75rem; margin-bottom: 2px;">
                                Coordonnées
                            </div>
                            <div>Adresse : <span id="modalDgiFooterAddress">-</span></div>
                            <div>Tél : <span id="modalDgiFooterPhone">-</span></div>
                            <div>Email : <span id="modalDgiFooterEmail">-</span></div>
                        </div>
                        <div>
                            <div style="font-weight: 800; color: #000000; text-transform: uppercase; font-size: 0.75rem; margin-bottom: 2px;">
                                Informations fiscales
                            </div>
                            <div>Régime : <span id="modalDgiFooterRegime">-</span></div>
                            <div>Division : <span id="modalDgiFooterDivision">-</span></div>
                            <div>Certification : <strong>Conformee-MCF</strong></div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </div>

    <!-- MODAL REÇU DE CAISSE CLIENT (TICKET DE CAISSE) -->
    <div id="receiptModal" class="hidden" style="position: fixed; inset: 0; background: rgba(0,0,0,0.85); z-index: 1000; display: flex; align-items: center; justify-content: center; padding: 1rem;">
        <div style="background: white; color: #1e293b; max-width: 380px; width: 100%; max-height: 90vh; overflow-y: auto; border-radius: 12px; padding: 1.75rem; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5); font-family: monospace;">
            <div style="text-align: center; margin-bottom: 0.75rem;">
                <div id="recRestoLogoBox" style="margin-bottom: 0.35rem;"></div>
                <h3 id="recRestoName" style="font-size: 1.2rem; font-weight: 800; color: #0f172a; margin-bottom: 0.2rem;">LemoDaje Restaurant</h3>
                <p id="recRestoSub" style="font-size: 0.75rem; color: #64748b; font-weight: bold; margin-bottom: 0.25rem;">TICKETDE CAISSE &amp; REÇU CLIENT</p>
                <div id="recRestoMeta" style="font-size: 0.68rem; color: #64748b; line-height: 1.35;"></div>
                <div style="border-bottom: 1px dashed #94a3b8; margin: 0.75rem 0;"></div>
            </div>

            <div style="font-size: 0.8rem; line-height: 1.6; margin-bottom: 0.5rem;">
                <div><strong>N°Commande :</strong> <span id="recOrderNum">-</span></div>
                <div><strong>Date :</strong> <span id="recOrderDate">-</span></div>
                <div><strong>GérantCaisse :</strong> <span id="recManagerName">-</span>(<span id="recManagerLogin">-</span>)</div>
                <div><strong>Destination :</strong> <span id="recTableName">ÀEmporter</span></div>
            </div>

            <div style="border-bottom: 1px dashed #94a3b8; margin: 0.5rem 0;"></div>

            <!-- Articles commandés -->
            <div id="recItemsList" style="font-size: 0.8rem; margin-bottom: 0.5rem;">
                <!-- Dynamique -->
            </div>

            <div style="border-bottom: 2px solid #0f172a; margin: 0.75rem 0;"></div>

            <!-- Totaux & Calculs -->
            <div style="font-size: 1rem; font-weight: 800; display: flex; justify-content: space-between; margin-bottom: 0.4rem; color: #0f172a;">
                <span>TOTALTTC :</span>
                <span id="recTotalAmount">0FCFA</span>
            </div>
            <div style="font-size: 0.8rem; display: flex; justify-content: space-between; margin-bottom: 0.25rem; color: #475569;">
                <span>ModeRèglement :</span>
                <span id="recPaymentMethod">-</span>
            </div>
            <div style="font-size: 0.8rem; display: flex; justify-content: space-between; margin-bottom: 0.25rem; color: #475569;">
                <span>MontantVersé :</span>
                <span id="recAmountTendered">-FCFA</span>
            </div>
            <div style="font-size: 0.9rem; font-weight: 700; display: flex; justify-content: space-between; margin-bottom: 0.75rem; color: #059669;">
                <span>MonnaieRendue :</span>
                <span id="recChangeAmount">0FCFA</span>
            </div>

            <div style="border-bottom: 1px dashed #94a3b8; margin: 0.75rem 0;"></div>

            <div style="text-align: center; font-size: 0.75rem; color: #64748b; line-height: 1.4; margin-bottom: 1.25rem;">
                Merci de votre confiance et bon appétit !<br>
                <em>Conservezce ticket comme reçu de paiement</em>
            </div>

            <div style="display: flex; gap: 0.5rem; justify-content: flex-end;">
                <button class="btn btn-secondary" onclick="closeReceiptModal()" style="color: #334155; border: 1px solid #cbd5e1; font-size: 0.8rem; padding: 0.4rem 0.8rem;">Fermer</button>
                <button class="btn btn-primary" onclick="window.print()" style="font-size: 0.8rem; padding: 0.4rem 0.8rem; background: #0f172a; color: white;">Imprimer Reçu</button>
            </div>
        </div>
    </div>

    <!-- MODAL FACTURE OFFICIELLE RESTAURANT & CLIENT (CONFORME AU MODÈLE MONOCHROME DE RÉFÉRENCE) -->
    <div id="invoiceModal" class="hidden" style="position: fixed; inset: 0; background: rgba(0,0,0,0.85); z-index: 1010; display: flex; align-items: center; justify-content: center; padding: 1.5rem; overflow-y: auto;">
        <div style="max-width: 860px; width: 100%; max-height: 95vh; overflow-y: auto; position: relative;">
            
            <!-- Barre d'actions Modal -->
            <div class="modal-actions-bar" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding: 0.75rem 1.25rem; background: #1f2937; border-radius: 12px; border: 1px solid #374151;">
                <span style="color: #38bdf8; font-weight: 700; font-size: 0.95rem;">
                     Facture Officielle Restaurant &amp; DGI (Modèle A4 Normalisé)
                </span>
                <div style="display: flex; gap: 0.75rem;">
                    <button class="btn btn-primary" onclick="window.print()" style="background: #000000; color: white; border: 1px solid #475569; font-weight: 700; font-size: 0.85rem; padding: 0.5rem 1rem;">
                         Imprimer la Facture en PDF
                    </button>
                    <button class="btn btn-secondary" onclick="closeRestaurantInvoiceModal()" style="font-size: 0.85rem; padding: 0.5rem 1rem;">
                         Fermer
                    </button>
                </div>
            </div>

            <!-- LE CORPS DE LA FACTURE CONFORME AU MODÈLE DE RÉFÉRENCE EN IMAGE -->
            <div class="corporate-invoice-paper">
                
                <!-- 1. EN-TÊTE : TITRE 'FACTURE' À GAUCHE & MÉTADONNÉES + QR CODE DGI À DROITE -->
                <div id="invPaperHeaderSec" style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.25rem;">
                    <div>
                        <h1 style="font-size: 2.3rem; font-weight: 900; color: #000000; margin: 0 0 4px 0; letter-spacing: 1.5px; text-transform: uppercase; line-height: 1;">
                            FACTURE
                        </h1>
                        <div id="invBadgeDgi" style="font-size: 0.75rem; font-weight: 800; color: #166534; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px;">
                             FACTURE NORMALISÉE DGI (e-MCF)
                        </div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 1rem; text-align: left;">
                        <table style="font-size: 0.82rem; color: #000000; border-collapse: collapse;">
                            <tr>
                                <td style="font-weight: 800; padding: 2px 8px 2px 0;">Numérode facture :</td>
                                <td id="invPaperInvoiceNum" style="font-weight: 700; padding: 2px 0;">-</td>
                            </tr>
                            <tr>
                                <td style="font-weight: 800; padding: 2px 8px 2px 0;">Datede facturation :</td>
                                <td id="invPaperInvoiceDate" style="font-weight: 600; padding: 2px 0;">-</td>
                            </tr>
                            <tr>
                                <td style="font-weight: 800; padding: 2px 8px 2px 0;">Échéance :</td>
                                <td id="invPaperDueDate" style="font-weight: 600; padding: 2px 0;">Comptantà réception</td>
                            </tr>
                            <tr>
                                <td style="font-weight: 800; padding: 2px 8px 2px 0;">Référence :</td>
                                <td id="invPaperDgiRef" style="font-weight: 700; padding: 2px 0; font-family: monospace;">-</td>
                            </tr>
                        </table>
                        <!-- QR CODE OFFICIEL DGI INTÉGRÉ DANS L'EN-TÊTE -->
                        <div style="text-align: center; border-left: 1.5px solid #000000; padding-left: 0.85rem; min-width: 85px;">
                            <div id="invPaperQrContainer" style="width: 78px; height: 78px; margin: 0 auto;"></div>
                            <div style="font-size: 0.58rem; font-weight: 800; color: #166534; margin-top: 2px; letter-spacing: 0.5px;">
                                SCAN DGI e-MCF
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 2. SECTION VENDEUR ET CLIENT (DEUX COLONNES NETTES EXACTEMENT COMME SUR L'IMAGE) -->
                <div id="invPaperVendorClientSec" style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 1.25rem;">
                    <!-- COLONNE VENDEUR -->
                    <div style="font-size: 0.82rem; color: #111827; line-height: 1.45;">
                        <div style="font-size: 0.95rem; font-weight: 900; color: #000000; margin-bottom: 0.35rem;">
                            Vendeur
                        </div>
                        <div id="invPaperBrandName" style="font-weight: 800; font-size: 0.9rem; color: #000000;">-</div>
                        <div id="invPaperAddress" style="font-style: italic; color: #4b5563;">-</div>
                        <div>Tél : <span id="invPaperPhone">-</span></div>
                        <div style="margin-top: 4px; font-size: 0.78rem; color: #374151;">
                            <span>IFU : <strong id="invPaperIfu">-</strong></span> • 
                            <span>RCCM : <strong id="invPaperRccm">-</strong></span>
                        </div>
                        <div style="font-size: 0.78rem; color: #374151;">
                            <span>Régime : <span id="invPaperRegime">-</span></span>
                        </div>
                    </div>

                    <!-- COLONNE CLIENT / DESTINATAIRE -->
                    <div style="font-size: 0.82rem; color: #111827; line-height: 1.45;">
                        <div style="font-size: 0.95rem; font-weight: 900; color: #000000; margin-bottom: 0.35rem;">
                            Client
                        </div>
                        <div id="invPaperCustomerName" style="font-weight: 800; font-size: 0.9rem; color: #000000;">Client</div>
                        <div style="font-style: italic; color: #4b5563;">Géranten service : <strong id="invPaperManagerName">-</strong></div>
                        <div style="color: #4b5563;">ServiceRestauration &amp; Boissons</div>
                        <div style="margin-top: 4px; font-size: 0.78rem; color: #374151;">
                            <span>Règlement : <strong id="invPaperPaymentMode">-</strong></span>
                        </div>
                    </div>
                </div>

                <!-- 3. TABLEAU DES ARTICLES (DESIGNATION | QTE | PRIX UNIT | MONTANT) -->
                <table class="corporate-inv-table">
                    <thead>
                        <tr>
                            <th style="width: 48%; text-align: left;">DESIGNATION</th>
                            <th style="width: 10%; text-align: center;">QTE</th>
                            <th style="width: 20%; text-align: right;">PRIXUNIT</th>
                            <th style="width: 22%; text-align: right;">MONTANT</th>
                        </tr>
                    </thead>
                    <tbody id="invPaperItemsBody">
                        <!-- Rempli dynamiquement -->
                    </tbody>
                </table>

                <!-- 4. BLOC DES TOTAUX (ACCROCHÉ À DROITE SOUS LES COLONNES PRIX UNIT & MONTANT) -->
                <div id="invPaperTotalsSec" style="width: 100%; margin-top: 0; margin-bottom: 1rem;">
                    <table class="corporate-inv-totals-table">
                        <tr>
                            <td colspan="2" style="font-weight: 800; text-transform: uppercase;">MONTANTHT</td>
                            <td id="invPaperSubTotal" style="text-align: right; font-weight: 700;">0FCFA</td>
                        </tr>
                        <tr>
                            <td style="font-weight: 800;">TVA</td>
                            <td id="invPaperTaxRate" style="text-align: center; font-weight: 700; width: 45px;">18%</td>
                            <td id="invPaperTaxAmount" style="text-align: right; font-weight: 700;">0FCFA</td>
                        </tr>
                        <!-- TOTAL TTC EN FOND NOIR ET ÉCRITURE BLANCHE IDENTIQUE À L'IMAGE -->
                        <tr class="total-ttc-row">
                            <td colspan="2" style="padding: 8px 10px; font-size: 0.9rem; letter-spacing: 0.5px; text-transform: uppercase;">TOTALTTC</td>
                            <td id="invPaperGrandTotal" style="padding: 8px 10px; text-align: right; font-size: 0.95rem;">0FCFA</td>
                        </tr>
                    </table>
                </div>

                <!-- 5. CONDITIONS ET MODALITÉS DE PAIEMENT & HOMOLOGATION DGI (SANS SIGNATURE) -->
                <div id="invPaperCondBox" style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-top: 0.6rem; margin-bottom: 1rem;">
                    <!-- GAUCHE : CONDITIONS DE PAIEMENT -->
                    <div>
                        <div style="font-weight: 900; font-size: 0.82rem; color: #000000; margin-bottom: 3px;">
                            Conditions et modalités de paiement
                        </div>
                        <div id="invPaperPaymentTerms" style="font-size: 0.76rem; color: #1f2937; margin-bottom: 6px; line-height: 1.4;">
                            Règlement comptant à la commande.
                        </div>
                    </div>

                    <!-- DROITE : INFORMATIONS FISCALES DGI -->
                    <div>
                        <div style="border: 1px solid #166534; background: #f0fdf4; border-radius: 4px; padding: 6px 8px; font-size: 0.72rem; color: #14532d; line-height: 1.4;">
                            <div style="font-weight: 900; text-transform: uppercase; margin-bottom: 2px; color: #166534;">
                                 Homologation DGI / e-MCF
                            </div>
                            <div>Réf.FNE : <strong id="invPaperHomologationRef">-</strong></div>
                            <div>Machine(NIM) : <strong id="invPaperNim">-</strong> •Daté du : <span id="invPaperHomologationDate">-</span></div>
                            <div>SceauSHA-256 : <span id="invPaperSha256" style="font-family: monospace; font-size: 0.65rem;">-</span></div>
                        </div>
                    </div>
                </div>

                <!-- 6. PIED DE PAGE (3 COLONNES AU BAS DE LA PAGE EXACTEMENT COMME SUR L'IMAGE) -->
                <div style="font-size: 0.72rem; color: #374151; border-top: 1px solid #d1d5db; padding-top: 8px; line-height: 1.45;">
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem;">
                        <!-- COLONNE 1 : MON ENTREPRISE -->
                        <div>
                            <div style="font-weight: 800; color: #000000; text-transform: uppercase; font-size: 0.75rem; margin-bottom: 2px;">
                                Mon entreprise
                            </div>
                            <div id="invFooterBrandName" style="font-weight: 700; color: #000000;">-</div>
                            <div>IFU : <span id="invFooterIfu">-</span></div>
                            <div>RCCM : <span id="invFooterRccm">-</span></div>
                            <div>NIM : <span id="invFooterNim">-</span></div>
                        </div>

                        <!-- COLONNE 2 : COORDONNÉES -->
                        <div>
                            <div style="font-weight: 800; color: #000000; text-transform: uppercase; font-size: 0.75rem; margin-bottom: 2px;">
                                Coordonnées
                            </div>
                            <div>Adresse : <span id="invFooterAddress">-</span></div>
                            <div>Tél : <span id="invFooterPhone">-</span></div>
                            <div>Email : <span id="invFooterEmail">-</span></div>
                        </div>

                        <!-- COLONNE 3 : INFORMATIONS FISCALES & LÉGALES -->
                        <div>
                            <div style="font-weight: 800; color: #000000; text-transform: uppercase; font-size: 0.75rem; margin-bottom: 2px;">
                                Informations fiscales
                            </div>
                            <div>Régime : <span id="invFooterRegime">-</span></div>
                            <div>Division : <span id="invFooterDivision">-</span></div>
                            <div>Certification : <strong>Conformee-MCF</strong></div>
                        </div>
                    </div>
                </div>

            </div> <!-- /corporate-invoice-paper -->
        </div>
    </div>
    <!-- ========================================================================= -->
    <!-- MODAL 1 : FACTURE GLOBALE DÉTAILLÉE DYNAMIQUE (EXIGENCES 3, 11, 12, 13, 14, 15, 16) -->
    <!-- ========================================================================= -->
    <div id="modalGlobalInvoiceDetail" class="hidden" style="position: fixed; inset: 0; background: rgba(0,0,0,0.92); z-index: 1020; display: flex; align-items: center; justify-content: center; padding: 1.5rem; overflow-y: auto;">
        <div style="background: #0f172a; border: 1.5px solid #334155; border-radius: 20px; color: #f8fafc; max-width: 1250px; width: 100%; max-height: 95vh; overflow-y: auto; padding: 2rem; box-shadow: 0 25px 60px -15px rgba(0,0,0,0.9); position: relative;">
            
            <!-- EN-TÊTE PRINCIPAL DE LA FACTURE GLOBALE -->
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #334155; padding-bottom: 1.25rem; margin-bottom: 1.5rem; flex-wrap: wrap; gap: 1rem;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="width: 50px; height: 50px; border-radius: 12px; background: linear-gradient(135deg, #f59e0b, #d97706); display: flex; align-items: center; justify-content: center; font-size: 1.6rem; box-shadow: 0 4px 15px rgba(245, 158, 11, 0.35);">
                        
                    </div>
                    <div>
                        <div style="display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap;">
                            <h2 style="font-size: 1.6rem; color: #fbbf24; font-family: monospace; letter-spacing: -0.02em; margin: 0;" id="detInvNumber">
                                FACT-GLOB-XXXX
                            </h2>
                            <span id="detInvStatusBadge"></span>
                        </div>
                        <p style="font-size: 0.88rem; color: #94a3b8; margin: 0.25rem 0 0 0;">
                            Facture Globale Consolidée des Ventes • Conforme e-MCF / Direction Générale des Impôts (DGI)
                        </p>
                    </div>
                </div>
                <div>
                    <button class="btn btn-secondary" onclick="closeGlobalInvoiceDetailModal()" style="font-size: 0.95rem; padding: 0.55rem 1.25rem; border-color: #475569; background: #1e293b; color: #f1f5f9;">
                         Fermer le Dossier
                    </button>
                </div>
            </div>

            <!-- BANDEAU PRESTIGIEUX DU JOUR : DATE & GÉRANTS EN SERVICE (DATE UNIQUEMENT, AUCUNE HEURE) -->
            <div style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.16), rgba(16, 185, 129, 0.16)); border: 2px solid #fbbf24; border-radius: 14px; padding: 1.15rem 1.4rem; margin-bottom: 1.5rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; box-shadow: 0 6px 20px rgba(245, 158, 11, 0.25);">
                <div style="display: flex; align-items: center; gap: 1.5rem; flex-wrap: wrap;">
                    <div>
                        <div style="font-size: 0.72rem; font-weight: 800; text-transform: uppercase; color: #fbbf24; letter-spacing: 0.08em; margin-bottom: 0.25rem;">
                             DATE DE LA FACTURE DU JOUR
                        </div>
                        <div style="font-size: 1.25rem; font-weight: 900; color: #ffffff;">
                            <span id="detTopInvoiceDate">-</span>
                        </div>
                    </div>
                    <div style="border-left: 2px solid rgba(255,255,255,0.12); padding-left: 1.25rem;">
                        <div style="font-size: 0.72rem; font-weight: 800; text-transform: uppercase; color: #93c5fd; letter-spacing: 0.08em; margin-bottom: 0.25rem;">
                             GÉRANT(S) AYANT EFFECTUÉ LES VENTES DU JOUR
                        </div>
                        <div id="detTopInvoiceManagers" style="font-size: 1.2rem; font-weight: 800; color: #60a5fa;">
                            -
                        </div>
                    </div>
                </div>
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <span id="detTopInvoiceStatusBadge"></span>
                </div>
            </div>

            <!-- BANDEAU OFFICIEL EN-TÊTE ÉTABLISSEMENT & APPROBATION DGI (TOUJOURS EN HAUT) -->
            <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.95), rgba(15, 23, 42, 0.98)); border: 1.5px solid #38bdf8; border-radius: 16px; padding: 1.25rem 1.5rem; margin-bottom: 1.5rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1.5rem; box-shadow: 0 8px 25px rgba(0,0,0,0.4);">
                <!-- Gauche : Logo + Nom + Identifiants Fiscaux Complets -->
                <div style="display: flex; align-items: center; gap: 1.25rem; flex: 1; min-width: 320px;">
                    <div id="detInvLogoBox" style="width: 72px; height: 72px; border-radius: 12px; background: #faf7f2; border: 2px solid #bfa892; display: flex; align-items: center; justify-content: center; overflow: hidden; padding: 4px; flex-shrink: 0;">
                        <!-- Logo dynamique ou badge -->
                    </div>
                    <div>
                        <h3 id="detInvRestoBrand" style="font-size: 1.35rem; color: #f8fafc; font-weight: 800; margin: 0; letter-spacing: -0.01em;">LemoDaje Restaurant</h3>
                        <p id="detInvRestoSub" style="font-size: 0.8rem; color: #94a3b8; margin: 0.15rem 0 0.45rem 0;">Restaurant &amp;Grill Gastronomique</p>
                        <div style="display: flex; gap: 0.85rem; flex-wrap: wrap; font-size: 0.78rem; color: #cbd5e1;">
                            <div><span style="color: #64748b; font-weight: 700;">IFU :</span> <strong id="detInvHeaderIfu" style="color: #38bdf8; font-family: monospace;">-</strong></div>
                            <div><span style="color: #64748b; font-weight: 700;">RCCM :</span> <strong id="detInvHeaderRccm" style="color: #cbd5e1;">-</strong></div>
                            <div><span style="color: #64748b; font-weight: 700;">RÉGIME :</span> <strong id="detInvHeaderRegime" style="color: #fbbf24;">-</strong></div>
                            <div><span style="color: #64748b; font-weight: 700;">DIVISION :</span> <strong id="detInvHeaderDivision" style="color: #a5b4fc;">-</strong></div>
                        </div>
                        <div style="font-size: 0.74rem; color: #94a3b8; margin-top: 0.25rem;">
                            <span id="detInvHeaderPhone"> -</span> &nbsp;•&nbsp; <span id="detInvHeaderAddress"> -</span> &nbsp;•&nbsp; <span id="detInvHeaderEmail"> -</span>
                        </div>
                    </div>
                </div>

                <!-- Droite : LE CODE QR TOUJOURS EN HAUT DÉSIGNANT L'APPROBATION OFFICIELLE DE LA DGI -->
                <div style="background: rgba(16, 185, 129, 0.08); border: 2px solid #10b981; border-radius: 14px; padding: 0.85rem 1.15rem; display: flex; align-items: center; gap: 1rem; box-shadow: 0 4px 20px rgba(16, 185, 129, 0.25);">
                    <div id="detInvQrBox" style="width: 82px; height: 82px; background: white; border-radius: 8px; padding: 4px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(0,0,0,0.3);">
                        <!-- Image QR Code DGI -->
                    </div>
                    <div style="text-align: left;">
                        <div class="badge" style="background: #10b981; color: white; font-weight: 800; font-size: 0.72rem; padding: 0.3rem 0.6rem; letter-spacing: 0.03em;">
                             APPROBATION OFFICIELLE DGI
                        </div>
                        <div style="font-size: 0.92rem; font-weight: 900; color: #34d399; margin: 0.3rem 0 0.15rem 0;">
                            FACTURE CERTIFIÉE DGI
                        </div>
                        <div style="font-size: 0.74rem; color: #cbd5e1;">
                            Sceau FNE : <code id="detInvStampCode" style="color: #fbbf24; font-weight: bold;">-</code>
                        </div>
                        <div style="font-size: 0.68rem; color: #6ee7b7; margin-top: 0.2rem;">
                            Conformité e-MCF Validée
                        </div>
                    </div>
                </div>
            </div>

            <!-- GRILLE DES 4 CASES D'IDENTIFICATION & MENTIONS LÉGALES DE LA FACTURE -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
                
                <!-- CASE 1 : IDENTIFIANT & GÉRANT CONNECTÉ -->
                <div style="background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 1.15rem; box-shadow: inset 0 1px 0 rgba(255,255,255,0.05); border-left: 4px solid #3b82f6;">

                    <div style="font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: #93c5fd; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.4rem;">
                        <span></span>Case 1 • Gérant &amp; Prise de Service
                    </div>
                    <div style="font-size: 0.88rem; line-height: 1.6;">
                        <div><span style="color: #94a3b8;">Gérant :</span> <strong id="detInvManagerName" style="color: #60a5fa;">-</strong></div>
                        <div><span style="color: #94a3b8;">Datede service :</span> <span id="detInvOpenedAt" style="color: #f1f5f9; font-weight: 600;">-</span></div>
                        <div><span style="color: #94a3b8;">Fréquence :</span> <span id="detInvFrequencyBadge" class="badge" style="background: rgba(99, 102, 241, 0.25); color: #a5b4fc; font-weight: 700; font-size: 0.75rem;">Quotidienne</span></div>
                    </div>
                </div>

                <!-- CASE 2 : PÉRIODE FISCALE -->
                <div style="background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 1.15rem; box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);">
                    <div style="font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: #94a3b8; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.4rem;">
                        <span></span>Case 2 • Période Concernée
                    </div>
                    <div style="font-size: 0.88rem; line-height: 1.6;">
                        <div><span style="color: #94a3b8;">Libellé :</span> <strong id="detInvPeriodLabel" style="color: #fbbf24;">-</strong></div>
                        <div><span style="color: #94a3b8;">Datedébut :</span> <span id="detInvDateStart" style="color: #f1f5f9; font-weight: 600;">-</span></div>
                        <div><span style="color: #94a3b8;">Datefin :</span> <span id="detInvDateEnd" style="color: #f1f5f9; font-weight: 600;">-</span></div>
                    </div>
                </div>

                <!-- CASE 3 : ÉMETTEUR & CONFORMITÉ DGI -->
                <div style="background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 1.15rem; box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);">
                    <div style="font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: #94a3b8; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.4rem;">
                        <span></span>Case 3 • Émetteur &amp; DGI
                    </div>
                    <div style="font-size: 0.88rem; line-height: 1.6;">
                        <div><span style="color: #94a3b8;">Établissement :</span> <strong id="detInvRestoName" style="color: white;">LemoDaje Restaurant</strong></div>
                        <div><span style="color: #94a3b8;">NIFFiscal :</span> <span id="detInvNif" style="font-family: monospace; color: #93c5fd; font-weight: bold;">000123456789A</span></div>
                        <div><span style="color: #94a3b8;">NIMMachine :</span> <span id="detInvNim" style="font-family: monospace; color: #cbd5e1;">RESTO-DGI-MCF-01</span></div>
                    </div>
                </div>

                <!-- CASE 4 : CERTIFICATION & GOUVERNANCE -->
                <div style="background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 1.15rem; box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);">
                    <div style="font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: #94a3b8; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.4rem;">
                        <span></span>Case 4 • Contrôle &amp; Sceau
                    </div>
                    <div style="font-size: 0.88rem; line-height: 1.6;">
                        <div><span style="color: #94a3b8;">Réfe-MCF :</span> <code id="detInvFiscalRef" style="color: #fbbf24; font-size: 0.8rem; word-break: break-all;">Encours</code></div>
                        <div><span style="color: #94a3b8;">Certifiéele :</span> <span id="detInvCertDate" style="color: #cbd5e1;">-</span></div>
                        <div><span style="color: #94a3b8;">Par :</span> <span id="detInvCertBy" style="color: #f1f5f9; font-weight: 600;">-</span></div>
                    </div>
                </div>

            </div>

            <!-- BANNIÈRE DE CONTRÔLE DE COHÉRENCE ET ANOMALIES (EXIGENCE 15) -->
            <div id="detInvAnomaliesBanner" style="margin-bottom: 1.5rem;"></div>

            <!-- BARRE DES 3 BOUTONS D'ACTION OBLIGATOIRES (EXIGENCE 16) -->
            <div style="display: flex; gap: 1rem; align-items: center; justify-content: space-between; background: #1e293b; border: 1.5px solid #334155; padding: 1.1rem 1.4rem; border-radius: 14px; margin-bottom: 1.75rem; flex-wrap: wrap;">
                <div style="display: flex; align-items: center; gap: 0.85rem; flex-wrap: wrap;">
                    <span style="font-size: 0.85rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; color: #94a3b8;">
                        Actions d'Administration :
                    </span>
                    <!-- 1. BOUTON RECALCULER -->
                    <button id="detBtnRecalculate" class="btn btn-secondary" onclick="recalculateCurrentInvoice()" style="font-weight: 700; padding: 0.65rem 1.25rem; border: 1.5px solid #6366f1; color: #a5b4fc; background: rgba(99, 102, 241, 0.15); display: flex; align-items: center; gap: 0.5rem;">
                        <span></span>RECALCULER
                    </button>
                    <!-- 2. BOUTON APERÇU DE LA FACTURE -->
                    <button class="btn btn-secondary" onclick="openCurrentInvoicePrintPreview()" style="font-weight: 700; padding: 0.65rem 1.25rem; border: 1.5px solid #f59e0b; color: #fbbf24; background: rgba(245, 158, 11, 0.12); display: flex; align-items: center; gap: 0.5rem;">
                        <span></span>APERÇU DE LA FACTURE
                    </button>
                </div>
                <div>
                    <!-- 3. BOUTON CERTIFIER LA FACTURE -->
                    <button id="detBtnCertify" class="btn btn-primary" onclick="promptCertifyCurrentInvoice()" style="background: linear-gradient(135deg, #10b981, #059669); font-weight: 800; font-size: 1rem; padding: 0.75rem 1.8rem; box-shadow: 0 4px 18px rgba(16, 185, 129, 0.45); display: flex; align-items: center; gap: 0.6rem;">
                        <span></span>CERTIFIER LA FACTURE
                    </button>
                </div>
            </div>

            <!-- LES 4 GRANDES CASES DE TOTAUX FINANCIERS ULTRA-VISIBLES -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.15rem; margin-bottom: 2rem;">
                
                <!-- CASE TOTAUX 1 : TTC -->
                <div style="background: linear-gradient(145deg, rgba(16, 185, 129, 0.15), rgba(16, 185, 129, 0.05)); border: 2px solid #10b981; border-radius: 14px; padding: 1.35rem; box-shadow: 0 10px 25px -5px rgba(16, 185, 129, 0.2);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span style="font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; color: #a7f3d0;">TotalGénéral des Ventes</span>
                        <span style="font-size: 1.2rem;"></span>
                    </div>
                    <div id="detInvTotalTTC" style="font-size: 1.9rem; font-weight: 900; color: #34d399; font-family: monospace; letter-spacing: -0.02em;">0FCFA</div>
                    <div style="font-size: 0.75rem; color: #a7f3d0; margin-top: 0.4rem; opacity: 0.9;">
                        Montant Total TTC Encaissé (Toutes Ventes)
                    </div>
                </div>

                <!-- CASE TOTAUX 2 : HT -->
                <div style="background: linear-gradient(145deg, rgba(59, 130, 246, 0.15), rgba(59, 130, 246, 0.05)); border: 2px solid #3b82f6; border-radius: 14px; padding: 1.35rem; box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.2);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span style="font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; color: #bfdbfe;">BaseImposable Hors Taxes</span>
                        <span style="font-size: 1.2rem;"></span>
                    </div>
                    <div id="detInvTotalHT" style="font-size: 1.9rem; font-weight: 900; color: #60a5fa; font-family: monospace; letter-spacing: -0.02em;">0FCFA</div>
                    <div style="font-size: 0.75rem; color: #bfdbfe; margin-top: 0.4rem; opacity: 0.9;">
                        Chiffre d'Affaires Net Hors Taxes (HT)
                    </div>
                </div>

                <!-- CASE TOTAUX 3 : TAXES DGI -->
                <div style="background: linear-gradient(145deg, rgba(245, 158, 11, 0.15), rgba(245, 158, 11, 0.05)); border: 2px solid #f59e0b; border-radius: 14px; padding: 1.35rem; box-shadow: 0 10px 25px -5px rgba(245, 158, 11, 0.2);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span style="font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; color: #fde68a;">TaxesDGI Collectées</span>
                        <span style="font-size: 1.2rem;"></span>
                    </div>
                    <div id="detInvTotalTaxes" style="font-size: 1.9rem; font-weight: 900; color: #fbbf24; font-family: monospace; letter-spacing: -0.02em;">0FCFA</div>
                    <div style="font-size: 0.75rem; color: #fde68a; margin-top: 0.4rem; opacity: 0.9;">
                        TVA 18% et taxes calculées selon la DGI
                    </div>
                </div>

                <!-- CASE TOTAUX 4 : VOLUME DE VENTES -->
                <div style="background: linear-gradient(145deg, rgba(139, 92, 246, 0.15), rgba(139, 92, 246, 0.05)); border: 2px solid #8b5cf6; border-radius: 14px; padding: 1.35rem; box-shadow: 0 10px 25px -5px rgba(139, 92, 246, 0.2);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span style="font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; color: #ddd6fe;">Volumedes Ventes</span>
                        <span style="font-size: 1.2rem;"></span>
                    </div>
                    <div id="detInvSalesCount" style="font-size: 1.9rem; font-weight: 900; color: white; font-family: monospace; letter-spacing: -0.02em;">0</div>
                    <div style="font-size: 0.75rem; color: #ddd6fe; margin-top: 0.4rem; opacity: 0.9;">
                        Commandes enregistrées &amp; agrégées
                    </div>
                </div>

            </div>

            <!-- ONGLET SUB-NAVIGATION DANS LA FACTURE DÉTAILLÉE -->
            <div style="display: flex; gap: 0.65rem; margin-bottom: 1.5rem; border-bottom: 2px solid #334155; padding-bottom: 0.75rem; flex-wrap: wrap;">
                <button class="btn btn-secondary" id="detSubTabBtnLines" onclick="switchDetInvoiceSubTab('lines')" style="font-size: 0.88rem; font-weight: 700; border: 1.5px solid #f59e0b; color: #fbbf24; background: rgba(245, 158, 11, 0.1);">
                     1. Lignes de Facture (Ventes Gérants)
                </button>
                <button class="btn btn-secondary" id="detSubTabBtnManagers" onclick="switchDetInvoiceSubTab('managers')" style="font-size: 0.88rem; font-weight: 700; border: 1.5px solid #334155; color: #cbd5e1;">
                     2. Récapitulatif par Gérant
                </button>
                <button class="btn btn-secondary" id="detSubTabBtnTaxes" onclick="switchDetInvoiceSubTab('taxes')" style="font-size: 0.88rem; font-weight: 700; border: 1.5px solid #334155; color: #cbd5e1;">
                     3. Ventilation Fiscale DGI
                </button>
                <button class="btn btn-secondary" id="detSubTabBtnAudit" onclick="switchDetInvoiceSubTab('audit')" style="font-size: 0.88rem; font-weight: 700; border: 1.5px solid #334155; color: #cbd5e1;">
                     4. Journal d'Audit &amp; Traçabilité
                </button>
            </div>

            <!-- SOUS-SECTION A : TABLEAU DE LA FACTURE DYNAMIQUE (EXIGENCE 12 & 3) -->
            <div id="detSubSecLines">
                <div style="margin-bottom: 0.85rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
                    <div style="font-size: 0.88rem; color: #94a3b8;">
                        Chaque vente réalisée par un gérant est intégrée dans sa propre case avec les montants HT, Taxes et TTC calculés automatiquement :
                    </div>
                    <span class="badge" style="background: rgba(16, 185, 129, 0.2); color: #34d399; font-weight: 700; font-size: 0.8rem;">
                         Pré-remplissage 100% Automatique
                    </span>
                </div>
                
                <div style="overflow-x: auto; border: 1.5px solid #334155; border-radius: 12px; margin-bottom: 1.5rem; background: #0b1120;">
                    <table style="width: 100%; border-collapse: collapse; text-align: left;">
                        <thead>
                            <tr style="background: #1e293b; border-bottom: 2px solid #475569;">
                                <th style="padding: 1rem 0.85rem; color: #f1f5f9; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; border-right: 1px solid #334155;">Vente(Réf)</th>
                                <th style="padding: 1rem 0.85rem; color: #f1f5f9; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; border-right: 1px solid #334155;">Date</th>
                                <th style="padding: 1rem 0.85rem; color: #f1f5f9; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; border-right: 1px solid #334155;">GérantCaisse</th>
                                <th style="padding: 1rem 0.85rem; color: #f1f5f9; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; border-right: 1px solid #334155;">Produit /Service Vendu</th>
                                <th style="padding: 1rem 0.85rem; color: #f1f5f9; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; text-align: center; border-right: 1px solid #334155;">Qté</th>
                                <th style="padding: 1rem 0.85rem; color: #f1f5f9; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; text-align: right; border-right: 1px solid #334155;">PrixUnitaire</th>
                                <th style="padding: 1rem 0.85rem; color: #93c5fd; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; text-align: right; border-right: 1px solid #334155;">MontantHT</th>
                                <th style="padding: 1rem 0.85rem; color: #fbbf24; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; text-align: right; border-right: 1px solid #334155;">TaxeDGI (18%)</th>
                                <th style="padding: 1rem 0.85rem; color: #34d399; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; text-align: right;">TotalTTC</th>
                            </tr>
                        </thead>
                        <tbody id="detInvItemsBody">
                            <!-- Lignes de facture injectées dynamiquement -->
                        </tbody>
                        <tfoot id="detInvItemsFoot">
                            <!-- Totaux généraux injectés dynamiquement -->
                        </tfoot>
                    </table>
                </div>
            </div>

            <!-- SOUS-SECTION B : RÉCAPITULATIF PAR GÉRANT (EXIGENCE 13) -->
            <div id="detSubSecManagers" class="hidden">
                <div style="margin-bottom: 1.25rem; font-size: 0.9rem; color: #94a3b8;">
                    Contribution individuelle de chaque Gérant durant la période de facturation (Nombre de ventes, Chiffre d'Affaires HT, Taxes et TTC) :
                </div>
                <div id="detInvManagerCardsGrid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.25rem; margin-bottom: 1.5rem;">
                    <!-- Cartes gérants générées dynamiquement -->
                </div>
            </div>

            <!-- SOUS-SECTION C : VENTILATION FISCALE DGI (EXIGENCE 6) -->
            <div id="detSubSecTaxes" class="hidden">
                <div style="margin-bottom: 1.25rem; font-size: 0.9rem; color: #94a3b8;">
                    Moteur de calcul fiscal DGI appliqué automatiquement sur l'assiette imposable de la facture globale :
                </div>
                <div style="overflow-x: auto; border: 1.5px solid #334155; border-radius: 12px; margin-bottom: 1.5rem; background: #0b1120;">
                    <table style="width: 100%; border-collapse: collapse; text-align: left;">
                        <thead>
                            <tr style="background: #1e293b; border-bottom: 2px solid #475569;">
                                <th style="padding: 1rem 1.25rem; color: #f1f5f9; border-right: 1px solid #334155;">RègleFiscale Paramétrée</th>
                                <th style="padding: 1rem 1.25rem; color: #f1f5f9; border-right: 1px solid #334155;">Type</th>
                                <th style="padding: 1rem 1.25rem; color: #fbbf24; text-align: center; border-right: 1px solid #334155;">Taux(%)</th>
                                <th style="padding: 1rem 1.25rem; color: #93c5fd; text-align: right; border-right: 1px solid #334155;">AssietteImposable</th>
                                <th style="padding: 1rem 1.25rem; color: #fbbf24; text-align: right; border-right: 1px solid #334155;">MontantTaxe</th>
                                <th style="padding: 1rem 1.25rem; color: #f1f5f9;">FormuleExacte Appliquée</th>
                            </tr>
                        </thead>
                        <tbody id="detInvTaxBreakdownBody">
                            <!-- Règles de taxes injectées dynamiquement -->
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- SOUS-SECTION D : HISTORIQUE DES CALCULS & TRAÇABILITÉ (EXIGENCE 14) -->
            <div id="detSubSecAudit" class="hidden">
                <div style="margin-bottom: 1.25rem; font-size: 0.9rem; color: #94a3b8;">
                    Piste d'audit certifiée permettant de justifier et retracer comment chaque montant a été obtenu :
                </div>
                <div id="detInvAuditTimeline" style="display: flex; flex-direction: column; gap: 0.85rem; max-height: 420px; overflow-y: auto; padding-right: 0.5rem;">
                    <!-- Timeline d'audit injectée dynamiquement -->
                </div>
            </div>

            <!-- SCEAU DE CERTIFICATION DGI (SI FACTURE CERTIFIÉE) -->
            <div id="detInvCertifiedStamp" class="hidden" style="margin-top: 1.5rem; border: 2px dashed #10b981; border-radius: 14px; background: rgba(16, 185, 129, 0.08); padding: 1.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1.5rem;">
                    <div>
                        <div style="color: #34d399; font-weight: 800; font-size: 1.15rem; display: flex; align-items: center; gap: 0.6rem;">
                            <span></span>FACTURE GLOBALE CERTIFIÉE &amp; SCELLÉE PAR LA DGI
                        </div>
                        <div style="font-size: 0.88rem; color: #cbd5e1; margin-top: 0.5rem; line-height: 1.7;">
                            <div><strong>Réf.Fiscale FNE DGI :</strong> <code id="detStampRef" style="color: #fbbf24; font-weight: bold; font-size: 1rem;">-</code></div>
                            <div><strong>Datede Certification :</strong> <span id="detStampDate" style="color: white; font-weight: 600;">-</span>par <span id="detStampAdmin" style="color: #60a5fa; font-weight: bold;">-</span></div>
                            <div><strong>SceauCryptographique SHA-256 :</strong> <small id="detStampSig" style="font-family: monospace; color: #94a3b8; word-break: break-all;">-</small></div>
                        </div>
                    </div>
                    <div style="text-align: center;">
                        <div id="detStampQrBox" style="width: 105px; height: 105px; background: white; border: 2px solid #10b981; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 0.7rem; color: black; font-weight: bold; margin: 0 auto 0.4rem; padding: 4px;">
                             QR DGI
                        </div>
                        <span style="font-size: 0.75rem; color: #34d399; font-weight: 800; text-transform: uppercase;">e-MCFConforme</span>
                    </div>
                </div>
            </div>

        </div>
    </div>

    <!-- ========================================================================= -->
    <!-- MODAL 2 : CONFIGURATION DES RÈGLES FISCALES DGI (EXIGENCE 6) -->
    <!-- ========================================================================= -->
    <div id="modalTaxRulesConfig" class="hidden" style="position: fixed; inset: 0; background: rgba(0,0,0,0.88); z-index: 1030; display: flex; align-items: center; justify-content: center; padding: 1.5rem; overflow-y: auto;">
        <div style="background: #131b2e; border: 1px solid #23304e; border-radius: 18px; color: #f8fafc; max-width: 900px; width: 100%; max-height: 92vh; overflow-y: auto; padding: 2.25rem; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.7);">
            
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #23304e; padding-bottom: 1.25rem; margin-bottom: 1.5rem;">
                <div>
                    <h2 style="font-size: 1.4rem; color: #fbbf24; display: flex; align-items: center; gap: 0.5rem;">
                        <span></span>Paramétrage des Règles Fiscales DGI
                    </h2>
                    <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.25rem;">
                        Configurez les taxes applicables, taux, bases de calcul et régimes selon les dispositions de la DGI sans coder en dur.
                    </p>
                </div>
                <button class="btn btn-secondary" onclick="closeTaxRulesModal()">Fermer</button>
            </div>

            <!-- LISTE DES RÈGLES CONFIGURÉES -->
            <div style="margin-bottom: 2rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h3 style="font-size: 1.1rem; color: white;">RèglesFiscales Actives</h3>
                    <button class="btn btn-secondary" onclick="resetDefaultTaxRulesAction()" style="font-size: 0.8rem; border-color: #f59e0b; color: #fbbf24;">
                        ↺ Rétablir TVA 18% Standard DGI
                    </button>
                </div>
                <div style="overflow-x: auto;">
                    <table>
                        <thead>
                            <tr>
                                <th>Nomde la Taxe</th>
                                <th>Type</th>
                                <th style="text-align: center;">Taux(%)</th>
                                <th>Base</th>
                                <th style="text-align: center;">Ordre</th>
                                <th>RégimeFiscal</th>
                                <th>Statut</th>
                                <th style="text-align: center;">Actions</th>
                            </tr>
                        </thead>
                        <tbody id="taxRulesTableBody">
                            <!-- Rempli dynamiquement -->
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- FORMULAIRE D'AJOUT / MODIFICATION D'UNE RÈGLE FISCALE -->
            <div style="background: rgba(30, 41, 59, 0.4); border: 1px solid #23304e; border-radius: 12px; padding: 1.5rem;">
                <h3 id="taxRuleFormTitle" style="font-size: 1.1rem; color: #fbbf24; margin-bottom: 1rem;">Ajouter une Règle Fiscale</h3>
                <input type="hidden" id="editTaxRuleId" value="" />
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1rem; margin-bottom: 1.25rem;">
                    <div class="form-group" style="margin-bottom: 0;">
                        <label>Nomde la Règle :</label>
                        <input id="taxRuleName" class="form-control" type="text" placeholder="Ex: TVA 18% (Norme DGI)" required />
                    </div>
                    <div class="form-group" style="margin-bottom: 0;">
                        <label>Typede Taxe :</label>
                        <select id="taxRuleType" class="form-control">
                            <option value="VAT">TVA(Valeur Ajoutée)</option>
                            <option value="SPECIFIC">TaxeSpécifique</option>
                            <option value="WITHHOLDING">Prélèvement /Retenue</option>
                            <option value="EXCISE">Droitd'Accise</option>
                        </select>
                    </div>
                    <div class="form-group" style="margin-bottom: 0;">
                        <label>Tauxde Taxe (%) :</label>
                        <input id="taxRuleRate" class="form-control" type="number" step="0.01" min="0" placeholder="18.0" required />
                    </div>
                    <div class="form-group" style="margin-bottom: 0;">
                        <label>Basede Calcul :</label>
                        <select id="taxRuleBase" class="form-control">
                            <option value="HT">MontantHors Taxes (HT)</option>
                            <option value="TTC">MontantBrut (TTC)</option>
                        </select>
                    </div>
                    <div class="form-group" style="margin-bottom: 0;">
                        <label>Ordrede Calcul :</label>
                        <input id="taxRuleOrder" class="form-control" type="number" min="1" value="1" />
                    </div>
                    <div class="form-group" style="margin-bottom: 0;">
                        <label>RégimeFiscal Concerné :</label>
                        <select id="taxRuleRegime" class="form-control">
                            <option value="TOUS">Tousles régimes</option>
                            <option value="REEL_NORMAL">RéelNormal d'Imposition (RNI)</option>
                            <option value="RSI">RégimeSimplifié d'Imposition (RSI)</option>
                            <option value="SIMPLIFIE">RégimeSynthétique</option>
                        </select>
                    </div>
                    <div class="form-group" style="margin-bottom: 0;">
                        <label>Moded'Arrondi :</label>
                        <select id="taxRuleRounding" class="form-control">
                            <option value="round_2_decimals">Arrondi2 Décimales (0.01 FCFA)</option>
                            <option value="round_integer">ArrondiEntier FCFA (1 FCFA)</option>
                            <option value="ceil">PlafondSupérieur (Ceil)</option>
                            <option value="floor">PlancherInférieur (Floor)</option>
                        </select>
                    </div>
                    <div class="form-group" style="margin-bottom: 0;">
                        <label>Conditiond'Application :</label>
                        <select id="taxRuleCondition" class="form-control">
                            <option value="always">Toujoursapplicable</option>
                            <option value="threshold_min">Seuilde montant minimum</option>
                        </select>
                    </div>
                </div>

                <div class="form-group">
                    <label>Description /Référence Légale DGI :</label>
                    <input id="taxRuleDesc" class="form-control" type="text" placeholder="Ex: Art. 320 du Code Général des Impôts..." />
                </div>

                <div style="display: flex; justify-content: flex-end; gap: 0.75rem;">
                    <button class="btn btn-secondary" onclick="resetTaxRuleForm()">Réinitialiser</button>
                    <button class="btn btn-primary" onclick="saveTaxRuleAction()" style="background: linear-gradient(135deg, #f59e0b, #d97706); color: black; font-weight: bold;">
                         Enregistrer la Règle Fiscale
                    </button>
                </div>
            </div>

        </div>
    </div>

    <!-- ========================================================================= -->
    <!-- MODAL 3 : CONFIRMATION DE CERTIFICATION AVEC VERROUILLAGE (EXIGENCES 11 & 16) -->
    <!-- ========================================================================= -->
    <div id="modalCertifyConfirm" class="hidden" style="position: fixed; inset: 0; background: rgba(0,0,0,0.92); z-index: 1040; display: flex; align-items: center; justify-content: center; padding: 1.5rem;">
        <div style="background: #131b2e; border: 2px solid #10b981; border-radius: 18px; color: #f8fafc; max-width: 550px; width: 100%; padding: 2.25rem; box-shadow: 0 25px 50px -12px rgba(16, 185, 129, 0.4); text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;"></div>
            <h2 style="font-size: 1.45rem; color: #34d399; margin-bottom: 1rem;">Confirmationde Certification Fiscale DGI</h2>
            <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 10px; padding: 1.25rem; margin-bottom: 1.5rem; text-align: left; font-size: 0.95rem; line-height: 1.6; color: #f8fafc;">
                « <strong>Êtes-voussûr de vouloir certifier cette facture ?</strong><br>
                Après certification, les données seront <strong>définitivementverrouillées</strong>et ne pourront plus être modifiées directement. »
            </div>

            <div class="form-group" style="text-align: left; margin-bottom: 1.5rem;">
                <label style="color: var(--text-muted); font-size: 0.85rem;">Notesou mentions administratives (optionnel) :</label>
                <input id="certifyConfirmNotes" class="form-control" type="text" placeholder="Ex: Clôture fiscale approuvée" />
            </div>

            <div style="display: flex; justify-content: center; gap: 1rem;">
                <button class="btn btn-secondary" onclick="closeCertifyConfirmModal()" style="padding: 0.75rem 1.5rem;">
                    Annuler
                </button>
                <button id="btnConfirmCertifyFinal" class="btn btn-primary" onclick="executeCertifyAction()" style="background: linear-gradient(135deg, #10b981, #059669); font-weight: 800; font-size: 1rem; padding: 0.75rem 1.75rem;">
                     Oui, Certifier Définitivement
                </button>
            </div>
        </div>
    </div>

    <!-- ========================================================================= -->
    <!-- MODAL 4 : CONFIGURATION DE LA FRÉQUENCE DE FACTURATION (EXIGENCE 8) -->
    <!-- ========================================================================= -->
    <div id="modalBillingConfig" class="hidden" style="position: fixed; inset: 0; background: rgba(0,0,0,0.88); z-index: 1030; display: flex; align-items: center; justify-content: center; padding: 1.5rem;">
        <div style="background: #131b2e; border: 1px solid #23304e; border-radius: 18px; color: #f8fafc; max-width: 520px; width: 100%; padding: 2rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #23304e; padding-bottom: 1rem; margin-bottom: 1.5rem;">
                <h3 style="font-size: 1.25rem; color: #fbbf24;">Fréquence de Certification</h3>
                <button class="btn btn-secondary" onclick="closeBillingConfigModal()"></button>
            </div>
            
            <p style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 1.5rem;">
                Définissez la périodicité de regroupement et de certification des factures globales :
            </p>

            <div class="form-group">
                <label>FréquencePrincipale :</label>
                <select id="cfgBillingFrequency" class="form-control" style="font-size: 1rem; padding: 0.75rem;">
                    <option value="daily">Quotidienne (Une facture globale par jour)</option>
                    <option value="weekly">Hebdomadaire (Une facture globale par semaine)</option>
                    <option value="monthly">Mensuelle (Une facture globale par mois)</option>
                </select>
            </div>

            <div class="form-group">
                <label>Modede Saisie des Prix au Menu :</label>
                <select id="cfgPricesMode" class="form-control">
                    <option value="ttc">Prixau menu sont Toutes Taxes Comprises (TTC - Restauration)</option>
                    <option value="ht">Prixau menu sont Hors Taxes (HT)</option>
                </select>
            </div>

            <div class="form-group" style="margin-bottom: 1.75rem;">
                <label>RégimeFiscal par Défaut de l'Établissement :</label>
                <select id="cfgTaxRegime" class="form-control">
                    <option value="REEL_NORMAL">RéelNormal d'Imposition (RNI)</option>
                    <option value="RSI">RégimeSimplifié d'Imposition (RSI)</option>
                    <option value="SIMPLIFIE">RégimeSynthétique</option>
                    <option value="TOUS">Tousrégimes</option>
                </select>
            </div>

            <div style="display: flex; justify-content: flex-end; gap: 0.75rem;">
                <button class="btn btn-secondary" onclick="closeBillingConfigModal()">Annuler</button>
                <button class="btn btn-primary" onclick="saveBillingConfigAction()" style="background: linear-gradient(135deg, #f59e0b, #d97706); color: black; font-weight: bold;">
                     Appliquer la Fréquence
                </button>
            </div>
        </div>
    </div>

    <!-- ========================================================================= -->
    <!-- MODAL 5 : APERÇU IMPRESSION FACTURE GLOBALE DGI e-MCF (MODÈLE MONOCHROME DE RÉFÉRENCE) -->
    <div id="modalGlobalInvoicePrint" class="hidden" style="position: fixed; inset: 0; background: rgba(0,0,0,0.88); z-index: 1050; display: flex; align-items: center; justify-content: center; padding: 1.5rem; overflow-y: auto;">
        <div style="max-width: 860px; width: 100%; max-height: 95vh; overflow-y: auto; position: relative;">
            
            <div class="modal-actions-bar" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding: 0.75rem 1.25rem; background: #1f2937; border-radius: 12px; border: 1px solid #374151;">
                <span style="color: #fbbf24; font-weight: 700; font-size: 0.95rem;">
                     Facture Globale Consolidée DGI (e-MCF)
                </span>
                <div style="display: flex; gap: 0.75rem;">
                    <button class="btn btn-primary" onclick="window.print()" style="background: #000000; color: white; border: 1px solid #475569; font-weight: 700; font-size: 0.85rem; padding: 0.5rem 1rem;">
                         Imprimer la Facture Globale
                    </button>
                    <button class="btn btn-secondary" onclick="closeGlobalInvoicePrintPreview()" style="font-size: 0.85rem; padding: 0.5rem 1rem;">
                         Fermer
                    </button>
                </div>
            </div>

            <div class="corporate-invoice-paper">
                <!-- 1. EN-TÊTE -->
                <div id="invPaperHeaderSec" style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.25rem;">
                    <div>
                        <h1 style="font-size: 2.3rem; font-weight: 900; color: #000000; margin: 0 0 4px 0; letter-spacing: 1.5px; text-transform: uppercase; line-height: 1;">
                            FACTURE
                        </h1>
                        <div style="font-size: 0.75rem; font-weight: 800; color: #166534; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px;">
                             FACTURE GLOBALE NORMALISÉE DGI (e-MCF)
                        </div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 1rem; text-align: left;">
                        <table style="font-size: 0.82rem; color: #000000; border-collapse: collapse;">
                            <tr>
                                <td style="font-weight: 800; padding: 2px 8px 2px 0;">Numérode facture :</td>
                                <td id="printInvNum" style="font-weight: 700; padding: 2px 0;">-</td>
                            </tr>
                            <tr>
                                <td style="font-weight: 800; padding: 2px 8px 2px 0;">Datede facturation :</td>
                                <td id="printInvDate" style="font-weight: 600; padding: 2px 0;">-</td>
                            </tr>
                            <tr>
                                <td style="font-weight: 800; padding: 2px 8px 2px 0;">Périodefiscale :</td>
                                <td id="printInvPeriodLabel" style="font-weight: 600; padding: 2px 0;">-</td>
                            </tr>
                            <tr>
                                <td style="font-weight: 800; padding: 2px 8px 2px 0;">Référence :</td>
                                <td id="printInvRef" style="font-weight: 700; padding: 2px 0; font-family: monospace;">-</td>
                            </tr>
                        </table>
                        <div style="text-align: center; border-left: 1.5px solid #000000; padding-left: 0.85rem; min-width: 85px;">
                            <div id="printInvQrContainer" style="width: 78px; height: 78px; margin: 0 auto;"></div>
                            <div style="font-size: 0.58rem; font-weight: 800; color: #166534; margin-top: 2px; letter-spacing: 0.5px;">
                                SCAN DGI e-MCF
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 2. SECTION VENDEUR ET CLIENT -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-bottom: 2rem;">
                    <!-- VENDEUR -->
                    <div style="font-size: 0.82rem; color: #111827; line-height: 1.45;">
                        <div style="font-size: 0.95rem; font-weight: 900; color: #000000; margin-bottom: 0.35rem;">
                            Vendeur
                        </div>
                        <div id="printInvRestoName" style="font-weight: 800; font-size: 0.9rem; color: #000000;">-</div>
                        <div id="printInvAddress" style="font-style: italic; color: #4b5563;">-</div>
                        <div>Tél : <span id="printInvPhone">-</span></div>
                        <div style="margin-top: 4px; font-size: 0.78rem; color: #374151;">
                            <span>IFU : <strong id="printInvIfu">-</strong></span> • 
                            <span>RCCM : <strong id="printInvRccm">-</strong></span>
                        </div>
                        <div style="font-size: 0.78rem; color: #374151;">
                            <span>Régime : <span id="printInvTaxRegime">-</span></span>
                        </div>
                    </div>

                    <!-- CLIENT -->
                    <div style="font-size: 0.82rem; color: #111827; line-height: 1.45;">
                        <div style="font-size: 0.95rem; font-weight: 900; color: #000000; margin-bottom: 0.35rem;">
                            Client
                        </div>
                        <div style="font-weight: 800; font-size: 0.9rem; color: #000000;">DirectionGénérale des Impôts (DGI)</div>
                        <div style="font-style: italic; color: #4b5563;">ConsolidationFiscale des Sessions de Ventes</div>
                        <div style="color: #4b5563;">Agentde contrôle : <strong id="printInvCertBy">Administrateur</strong></div>
                        <div style="margin-top: 4px; font-size: 0.78rem; color: #374151;">
                            <span>Volume : <strong id="printInvSalesCountDesc">-</strong></span>
                        </div>
                    </div>
                </div>

                <!-- 3. TABLEAU -->
                <table class="corporate-inv-table">
                    <thead>
                        <tr>
                            <th style="width: 48%; text-align: left;">DESIGNATION</th>
                            <th style="width: 10%; text-align: center;">QTE</th>
                            <th style="width: 20%; text-align: right;">PRIXUNIT</th>
                            <th style="width: 22%; text-align: right;">MONTANT</th>
                        </tr>
                    </thead>
                    <tbody id="printInvTableBody">
                        <!-- Dynamique -->
                    </tbody>
                </table>

                <!-- 4. TOTAUX -->
                <div style="width: 100%; margin-top: 0; margin-bottom: 2rem;">
                    <table class="corporate-inv-totals-table">
                        <tr>
                            <td colspan="2" style="font-weight: 800; text-transform: uppercase;">MONTANTHT</td>
                            <td id="printInvSubTotal" style="text-align: right; font-weight: 700;">0FCFA</td>
                        </tr>
                        <tr>
                            <td style="font-weight: 800;">TVA</td>
                            <td style="text-align: center; font-weight: 700; width: 45px;">18%</td>
                            <td id="printInvTaxAmount" style="text-align: right; font-weight: 700;">0FCFA</td>
                        </tr>
                        <tr class="total-ttc-row">
                            <td colspan="2" style="padding: 8px 10px; font-size: 0.9rem; letter-spacing: 0.5px; text-transform: uppercase;">TOTALTTC</td>
                            <td id="printInvGrandTotal" style="padding: 8px 10px; text-align: right; font-size: 0.95rem;">0FCFA</td>
                        </tr>
                    </table>
                </div>

                <!-- 5. CONDITIONS & HOMOLOGATION DGI (SANS SIGNATURE) -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-top: 0.6rem; margin-bottom: 1rem;">
                    <div>
                        <div style="font-weight: 900; font-size: 0.82rem; color: #000000; margin-bottom: 3px;">
                            Conditions et modalités de paiement
                        </div>
                        <div style="font-size: 0.76rem; color: #1f2937; margin-bottom: 6px; line-height: 1.4;">
                            Règlement global consolidé des sessions de caisse.
                        </div>
                    </div>
                    <div>
                        <div style="border: 1px solid #166534; background: #f0fdf4; border-radius: 4px; padding: 6px 8px; font-size: 0.72rem; color: #14532d; line-height: 1.4;">
                            <div style="font-weight: 900; text-transform: uppercase; margin-bottom: 2px; color: #166534;">
                                 Homologation DGI / e-MCF
                            </div>
                            <div>Réf.FNE : <strong id="printInvRefDgi">-</strong></div>
                            <div>Machine(NIM) : <strong id="printInvNim">-</strong> •Daté du : <span id="printInvCertDate">-</span></div>
                            <div>SceauSHA-256 : <span id="printInvSha256" style="font-family: monospace; font-size: 0.65rem;">-</span></div>
                        </div>
                    </div>
                </div>

                <!-- 6. PIED DE PAGE 3 COLONNES -->
                <div style="font-size: 0.72rem; color: #374151; border-top: 1px solid #d1d5db; padding-top: 8px; line-height: 1.45;">
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem;">
                        <div>
                            <div style="font-weight: 800; color: #000000; text-transform: uppercase; font-size: 0.75rem; margin-bottom: 2px;">
                                Mon entreprise
                            </div>
                            <div id="printInvFooterBrand" style="font-weight: 700; color: #000000;">-</div>
                            <div>IFU : <span id="printInvFooterIfu">-</span></div>
                            <div>RCCM : <span id="printInvFooterRccm">-</span></div>
                            <div>NIM : <span id="printInvFooterNim">-</span></div>
                        </div>
                        <div>
                            <div style="font-weight: 800; color: #000000; text-transform: uppercase; font-size: 0.75rem; margin-bottom: 2px;">
                                Coordonnées
                            </div>
                            <div>Adresse : <span id="printInvFooterAddress">-</span></div>
                            <div>Tél : <span id="printInvFooterPhone">-</span></div>
                            <div>Email : <span id="printInvFooterEmail">-</span></div>
                        </div>
                        <div>
                            <div style="font-weight: 800; color: #000000; text-transform: uppercase; font-size: 0.75rem; margin-bottom: 2px;">
                                Informations fiscales
                            </div>
                            <div>Régime : <span id="printInvFooterRegime">-</span></div>
                            <div>Division : <span id="printInvFooterDivision">-</span></div>
                            <div>Certification : <strong>Conformee-MCF</strong></div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </div>

    <!-- MODAL WEBRTC APPEL VIDÉO & AUDIO EN DIRECT -->
    <div id="videoCallModal" class="hidden" style="position: fixed; inset: 0; background: rgba(5, 8, 15, 0.92); z-index: 1050; display: flex; align-items: center; justify-content: center; backdrop-filter: blur(8px); padding: 1.5rem;">
        <div style="background: #111827; border: 1.5px solid #374151; border-radius: 20px; width: 100%; max-width: 900px; height: 85vh; max-height: 680px; display: flex; flex-direction: column; overflow: hidden; position: relative; box-shadow: 0 25px 60px rgba(0,0,0,0.8);">
            
            <!-- Barre supérieure du call -->
            <div style="background: rgba(17, 24, 39, 0.95); padding: 0.85rem 1.5rem; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1f2937; z-index: 10;">
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <span id="callTypeBadge" style="background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 800;">
                         APPEL VIDÉO SÉCURISÉ
                    </span>
                    <span id="callParticipantName" style="font-weight: 700; color: white; font-size: 1rem;">Correspondant</span>
                    <span id="callDurationTimer" style="color: #9ca3af; font-size: 0.85rem; font-variant-numeric: tabular-nums;">00:00</span>
                </div>
                <div id="callStatusIndicator" style="font-size: 0.8rem; color: #fbbf24; display: flex; align-items: center; gap: 0.4rem;">
                    <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #fbbf24;"></span>
                    <span id="callStatusText">Établissementdu flux WebRTC...</span>
                </div>
            </div>

            <!-- Conteneur Vidéo Principal (Grand format) -->
            <div style="flex: 1; position: relative; background: #030712; display: flex; align-items: center; justify-content: center; overflow: hidden;">
                
                <!-- Vidéo Distante (Interlocuteur) -->
                <video id="remoteVideo" autoplay playsinline style="width: 100%; height: 100%; object-fit: contain; background: #030712;"></video>
                
                <!-- Placeholder si caméra distante inactive ou appel audio -->
                <div id="remoteVideoPlaceholder" style="position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; background: radial-gradient(circle, #1e293b 0%, #0f172a 100%);">
                    <div style="width: 100px; height: 100px; border-radius: 50%; background: #334155; display: flex; align-items: center; justify-content: center; font-size: 3rem; margin-bottom: 1rem; border: 3px solid #64748b;">
                        
                    </div>
                    <div id="remotePlaceholderName" style="font-size: 1.25rem; font-weight: 700; color: white; margin-bottom: 0.35rem;">Enattente de connexion...</div>
                    <div style="font-size: 0.85rem; color: #94a3b8;">Fluxvidéo et audio direct P2P</div>
                </div>

                <!-- Vidéo Locale (Incrustée en vignette PIP en bas à droite) -->
                <div id="localVideoContainer" style="position: absolute; bottom: 20px; right: 20px; width: 180px; height: 135px; border-radius: 14px; overflow: hidden; border: 2px solid #f59e0b; box-shadow: 0 10px 25px rgba(0,0,0,0.8); background: #0f172a; z-index: 20;">
                    <video id="localVideo" autoplay playsinline muted style="width: 100%; height: 100%; object-fit: cover;"></video>
                </div>
            </div>

            <!-- Barre flottante des commandes d'appel -->
            <div style="background: rgba(17, 24, 39, 0.95); padding: 1rem 1.5rem; display: flex; justify-content: center; align-items: center; gap: 1.25rem; border-top: 1px solid #1f2937; z-index: 10;">
                <button id="btnToggleMic" onclick="toggleLocalMicrophone()" class="btn btn-secondary" style="border-radius: 50%; width: 50px; height: 50px; padding: 0; display: flex; align-items: center; justify-content: center; font-size: 1.3rem;" title="Activer / Couper Micro">
                    
                </button>
                <button id="btnToggleCam" onclick="toggleLocalCamera()" class="btn btn-secondary" style="border-radius: 50%; width: 50px; height: 50px; padding: 0; display: flex; align-items: center; justify-content: center; font-size: 1.3rem;" title="Activer / Couper Caméra">
                    
                </button>
                <button onclick="hangupActiveCall()" class="btn btn-danger" style="border-radius: 9999px; padding: 0.7rem 2rem; font-weight: 800; font-size: 1rem; background: #dc2626; color: white; border: none; box-shadow: 0 4px 15px rgba(220, 38, 38, 0.5); display: flex; align-items: center; gap: 0.5rem;" title="Raccrocher">
                     Terminer l'appel
                </button>
            </div>

        </div>
    </div>

    <!-- MODAL APPEL ENTRANT (SONNERIE & NOTIFICATION) -->
    <div id="incomingCallModal" class="hidden" style="position: fixed; inset: 0; background: rgba(5, 8, 15, 0.88); z-index: 1060; display: flex; align-items: center; justify-content: center; backdrop-filter: blur(8px); padding: 1.5rem;">
        <div style="background: #111827; border: 2px solid #10b981; border-radius: 24px; width: 100%; max-width: 440px; padding: 2rem; text-align: center; box-shadow: 0 25px 60px rgba(16, 185, 129, 0.3);">
            <div style="width: 80px; height: 80px; border-radius: 50%; background: rgba(16, 185, 129, 0.15); border: 2px solid #10b981; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; margin: 0 auto 1.25rem;">
                
            </div>
            <div style="font-size: 0.8rem; font-weight: 800; color: #10b981; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.35rem;">
                Appel Vidéo Entrant
            </div>
            <h3 id="incomingCallerName" style="font-size: 1.4rem; font-weight: 800; color: white; margin-bottom: 0.5rem;">Correspondant</h3>
            <p style="color: #9ca3af; font-size: 0.875rem; margin-bottom: 1.75rem;">
                Demande de liaison vidéo directe WebRTC...
            </p>
            <div style="display: flex; gap: 1rem; justify-content: center;">
                <button onclick="rejectIncomingCall()" class="btn btn-danger" style="flex: 1; padding: 0.8rem 1rem; border-radius: 12px; font-weight: 700; font-size: 0.95rem; justify-content: center;">
                     Refuser
                </button>
                <button onclick="acceptIncomingCall()" class="btn btn-primary" style="flex: 1.4; padding: 0.8rem 1rem; border-radius: 12px; font-weight: 800; font-size: 0.95rem; background: linear-gradient(135deg, #10b981, #059669); justify-content: center; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);">
                     Décrocher
                </button>
            </div>
        </div>
    </div>
</body>
</html>
"""
