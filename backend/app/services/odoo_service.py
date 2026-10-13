import xmlrpc.client
import logging
import datetime
import time
from typing import Optional, Dict, Any, Tuple, List
from app.core.config import settings

logger = logging.getLogger("odoo_service")

class OdooService:
    def __init__(self):
        self.url = settings.ODOO_URL
        self.db = settings.ODOO_DB
        self.username = settings.ODOO_USER
        self.password = settings.ODOO_PASSWORD
        self._uid: Optional[int] = None
        self._common_proxy = None
        self._object_proxy = None

    def _get_common(self):
        if not self._common_proxy:
            self._common_proxy = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/common", allow_none=True)
        return self._common_proxy

    def _get_object(self):
        if not self._object_proxy:
            self._object_proxy = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/object", allow_none=True)
        return self._object_proxy

    def authenticate(self) -> int:
        """Authentifie le backend auprès d'Odoo et retourne le UID."""
        try:
            common = self._get_common()
            uid = common.authenticate(self.db, self.username, self.password, {})
            if not uid:
                raise ValueError(f"Échec d'authentification Odoo sur la base '{self.db}' avec l'utilisateur '{self.username}'.")
            self._uid = uid
            return uid
        except Exception as e:
            logger.error(f"Erreur d'authentification Odoo: {e}")
            raise

    def execute_kw(self, model: str, method: str, args: Optional[List[Any]] = None, kwargs: Optional[Dict[str, Any]] = None) -> Any:
        """Exécute un appel ORM Odoo via XML-RPC."""
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        if not self._uid:
            self.authenticate()
        try:
            models = self._get_object()
            return models.execute_kw(self.db, self._uid, self.password, model, method, args, kwargs)
        except Exception as e:
            logger.warning(f"Tentative de ré-authentification Odoo suite à: {e}")
            self.authenticate()
            models = self._get_object()
            return models.execute_kw(self.db, self._uid, self.password, model, method, args, kwargs)

    def test_connection(self) -> Dict[str, Any]:
        """Vérifie la disponibilité et l'état de collaboration avec Odoo."""
        try:
            uid = self.authenticate()
            pos_configs = self.execute_kw('pos.config', 'search_read', [[]], {'fields': ['id', 'name'], 'limit': 1})
            pos_config_id = pos_configs[0]['id'] if pos_configs else None

            return {
                "connected": True,
                "odoo_url": self.url,
                "database": self.db,
                "user_id": uid,
                "pos_config_id": pos_config_id,
                "message": "Connexion Odoo active. Moteur Restaurant prêt à collaborer."
            }
        except Exception as e:
            return {
                "connected": False,
                "odoo_url": self.url,
                "database": self.db,
                "user_id": None,
                "pos_config_id": None,
                "message": f"Erreur de connexion Odoo: {str(e)}"
            }

    def get_or_create_default_floor(self) -> int:
        """Récupère ou crée la salle principale du restaurant dans Odoo."""
        floors = self.execute_kw('restaurant.floor', 'search_read', [[]], {'fields': ['id', 'name'], 'limit': 1})
        if floors:
            return floors[0]['id']
        
        pos_config_id = self.get_or_create_pos_config()
        floor_id = self.execute_kw('restaurant.floor', 'create', [{
            'name': 'Salle Principale',
            'pos_config_ids': [[6, 0, [pos_config_id]]]
        }])
        return floor_id

    def get_or_create_pos_config(self) -> int:
        """Trouve ou configure le Point de Vente Restaurant."""
        configs = self.execute_kw('pos.config', 'search_read', [[]], {'fields': ['id', 'name'], 'limit': 1})
        if configs:
            return configs[0]['id']
        
        config_id = self.execute_kw('pos.config', 'create', [{
            'name': 'Caisse Restaurant Principale',
            'module_pos_restaurant': True
        }])
        return config_id

    def get_or_open_session(self) -> int:
        """Récupère ou ouvre une session POS pour synchroniser les commandes."""
        pos_config_id = self.get_or_create_pos_config()
        sessions = self.execute_kw('pos.session', 'search_read', [
            [['config_id', '=', pos_config_id], ['state', '!=', 'closed']]
        ], {'fields': ['id', 'state'], 'limit': 1})
        
        if sessions:
            sess = sessions[0]
            if sess['state'] != 'opened':
                try:
                    self.execute_kw('pos.session', 'write', [[sess['id']], {'state': 'opened'}])
                except Exception:
                    pass
            return sess['id']
        
        # Créer et ouvrir une session
        new_session_id = self.execute_kw('pos.session', 'create', [{
            'user_id': self._uid,
            'config_id': pos_config_id
        }])
        try:
            self.execute_kw('pos.session', 'write', [[new_session_id], {'state': 'opened'}])
        except Exception:
            pass
        return new_session_id

    def sync_table_to_odoo(self, table_id: int, table_name: str, seats: int = 4) -> int:
        """Synchronise une table du backend vers Odoo (restaurant.table)."""
        floor_id = self.get_or_create_default_floor()
        existing = self.execute_kw('restaurant.table', 'search_read', [
            ['|', ['backend_table_id', '=', str(table_id)], ['name', '=', table_name]]
        ], {'fields': ['id'], 'limit': 1})

        table_vals = {
            'name': table_name,
            'seats': seats,
            'floor_id': floor_id,
            'backend_table_id': str(table_id)
        }

        if existing:
            odoo_table_id = existing[0]['id']
            self.execute_kw('restaurant.table', 'write', [[odoo_table_id], table_vals])
            return odoo_table_id
        else:
            return self.execute_kw('restaurant.table', 'create', [table_vals])

    def sync_product_to_odoo(self, item_id: int, name: str, price: float, category_name: Optional[str] = None) -> Tuple[int, int]:
        """Synchronise un plat/produit vers Odoo (product.product)."""
        existing = self.execute_kw('product.product', 'search_read', [
            ['|', ['backend_item_id', '=', str(item_id)], ['name', '=', name]]
        ], {'fields': ['id', 'product_tmpl_id'], 'limit': 1})

        product_vals = {
            'name': name,
            'list_price': price,
            'available_in_pos': True,
            'backend_item_id': str(item_id),
            'is_restaurant_dish': True,
            'type': 'consu'
        }

        if category_name:
            try:
                pos_cat = self.execute_kw('pos.category', 'search_read', [
                    [('name', '=', category_name)]
                ], {'fields': ['id'], 'limit': 1})
                if pos_cat:
                    product_vals['restaurant_category_id'] = pos_cat[0]['id']
                    product_vals['pos_categ_ids'] = [(6, 0, [pos_cat[0]['id']])]
            except Exception:
                pass

        if existing:
            product_id = existing[0]['id']
            tmpl_id = existing[0]['product_tmpl_id'][0] if isinstance(existing[0]['product_tmpl_id'], (list, tuple)) else existing[0]['product_tmpl_id']
            self.execute_kw('product.product', 'write', [[product_id], product_vals])
            return product_id, tmpl_id
        else:
            product_id = self.execute_kw('product.product', 'create', [product_vals])
            read_res = self.execute_kw('product.product', 'read', [[product_id]], {'fields': ['product_tmpl_id']})
            tmpl_id = read_res[0]['product_tmpl_id'][0] if read_res and read_res[0].get('product_tmpl_id') else 0
            return product_id, tmpl_id

    def sync_order_to_pos(
        self,
        order_number: str,
        table_name: str,
        items: List[Dict[str, Any]],
        total_amount: float,
        manager_id: Optional[int] = None
    ) -> int:
        """
        Crée une commande Point de Vente (pos.order) dans Odoo.
        Le backend orchestre la vente et la fait enregistrer dans Odoo.
        """
        session_id = self.get_or_open_session()
        
        lines = []
        total_ht = round(total_amount / 1.18, 2) if total_amount > 0 else 0.0
        total_tax = round(total_amount - total_ht, 2) if total_amount > 0 else 0.0

        for it in items:
            product_id = it.get('odoo_product_id')
            if not product_id:
                product_id, _ = self.sync_product_to_odoo(
                    item_id=it['menu_item_id'],
                    name=it['name'],
                    price=it['price']
                )
            
            qty = it.get('quantity', 1)
            price_unit = it.get('price', 0.0)
            subtotal = qty * price_unit
            line_ht = round(subtotal / 1.18, 2)
            lines.append([0, 0, {
                'product_id': product_id,
                'qty': qty,
                'price_unit': price_unit,
                'price_subtotal': line_ht,
                'price_subtotal_incl': subtotal,
                'name': it['name']
            }])

        pos_config_id = self.get_or_create_pos_config()
        pos_config = self.execute_kw('pos.config', 'read', [[pos_config_id]], {'fields': ['payment_method_ids']})
        allowed_methods = pos_config[0].get('payment_method_ids', []) if pos_config else []
        payment_method_id = allowed_methods[0] if allowed_methods else None

        order_vals: Dict[str, Any] = {
            'name': order_number,
            'session_id': session_id,
            'pos_reference': f"Order {session_id:05d}-001-{int(time.time() * 1000) % 10000000:07d}",
            'lines': lines,
            'amount_total': total_amount,
            'amount_paid': total_amount,
            'amount_tax': total_tax,
            'amount_return': 0.0,
            'backend_order_id': order_number,
            'backend_table_number': table_name,
            'backend_sync_status': 'synced'
        }

        if manager_id:
            order_vals['user_id'] = manager_id

        if payment_method_id:
            order_vals['payment_ids'] = [[0, 0, {
                'payment_method_id': payment_method_id,
                'amount': total_amount,
                'payment_date': datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            }]]

        odoo_order_id = self.execute_kw('pos.order', 'create', [order_vals])
        try:
            self.execute_kw('pos.order', 'action_pos_order_paid', [[odoo_order_id]])
        except Exception as e:
            logger.warning(f"Validation action_pos_order_paid Odoo: {e}")
        return odoo_order_id

    def get_pos_user_groups(self) -> List[int]:
        """Récupère les IDs des groupes 'Utilisateur interne', 'Point de Vente / Responsable' et 'Facturation'."""
        try:
            base_grp = self.execute_kw('ir.model.data', 'check_object_reference', ['base', 'group_user'])
            pos_grp = self.execute_kw('ir.model.data', 'check_object_reference', ['point_of_sale', 'group_pos_manager'])
            bill_grp = self.execute_kw('ir.model.data', 'check_object_reference', ['account', 'group_account_invoice'])
            return [base_grp[1], pos_grp[1], bill_grp[1]]
        except Exception as e:
            logger.warning(f"Impossible de résoudre les groupes Odoo via ir.model.data: {e}")
            return [1, 50, 23]

    def sync_manager_user_to_odoo(self, username: str, full_name: str, email: str, password: str) -> int:
        """
        Crée ou met à jour le compte Gérant dans Odoo (res.users) :
        - Attribue le mot de passe dédié
        - Restreint les droits aux modules Restaurant / POS (aucun accès aux menus d'administration)
        """
        groups = self.get_pos_user_groups()
        existing = self.execute_kw('res.users', 'search_read', [
            [['login', '=', username]]
        ], {'fields': ['id'], 'limit': 1})

        user_vals = {
            'name': full_name,
            'login': username,
            'email': email,
            'password': password,
            'groups_id': [(6, 0, groups)],
            'active': True
        }

        if existing:
            user_id = existing[0]['id']
            self.execute_kw('res.users', 'write', [[user_id], user_vals])
            return user_id
        else:
            user_ids = self.execute_kw('res.users', 'create', [[user_vals]])
            return user_ids[0] if isinstance(user_ids, (list, tuple)) else user_ids

    def toggle_odoo_user_active(self, odoo_user_id: int, is_active: bool) -> None:
        """Active ou suspend un utilisateur dans Odoo."""
        if odoo_user_id:
            try:
                self.execute_kw('res.users', 'write', [[odoo_user_id], {'active': is_active}])
            except Exception as e:
                logger.error(f"Erreur lors de la modification de l'état actif dans Odoo: {e}")

    def archive_odoo_user(self, odoo_user_id: int) -> None:
        """Archive un utilisateur dans Odoo (active=False)."""
        self.toggle_odoo_user_active(odoo_user_id, False)

    def sync_all_from_odoo(self, db) -> Dict[str, int]:
        """
        Interroge Odoo et importe / synchronise toutes les données dans la base locale PostgreSQL :
        - Les Gérants (res.users avec is_restaurant_manager=True)
        - Les Plats (product.product ou product.template avec available_in_pos=True)
        - Les Tables (restaurant.table)
        - Les Commandes (pos.order)
        """
        from app.models.user import User
        from app.models.restaurant import MenuItem, RestaurantTable, Order, OrderItem, PosSession
        from app.core.security import hash_password

        counts = {"managers": 0, "dishes": 0, "tables": 0, "orders": 0, "sessions": 0}

        # 1. Gérants
        try:
            odoo_managers = self.execute_kw('res.users', 'search_read', [
                [['is_restaurant_manager', '=', True]]
            ], {'fields': ['id', 'name', 'login', 'active']})
            for m in odoo_managers:
                user = db.query(User).filter((User.odoo_user_id == m['id']) | (User.username == m['login'])).first()
                if not user:
                    user = User(
                        username=m['login'],
                        email=f"{m['login']}@restaurant.local",
                        full_name=m['name'],
                        role='manager',
                        hashed_password=hash_password('Pass1234!'),
                        is_active=m['active'],
                        odoo_user_id=m['id']
                    )
                    db.add(user)
                    counts["managers"] += 1
                else:
                    if user.odoo_user_id != m['id'] or user.full_name != m['name'] or user.is_active != m['active']:
                        user.odoo_user_id = m['id']
                        user.full_name = m['name']
                        user.is_active = m['active']
                        counts["managers"] += 1
        except Exception as e:
            logger.error(f"Erreur lors de la synchro des gérants depuis Odoo: {e}")

        # 2. Plats / Produits
        try:
            odoo_products = self.execute_kw('product.product', 'search_read', [
                [['available_in_pos', '=', True]]
            ], {'fields': ['id', 'name', 'lst_price', 'product_tmpl_id']})
            for p in odoo_products:
                tmpl_id = p['product_tmpl_id'][0] if isinstance(p.get('product_tmpl_id'), (list, tuple)) else p.get('product_tmpl_id')
                item = db.query(MenuItem).filter((MenuItem.odoo_product_id == p['id']) | (MenuItem.name == p['name'])).first()
                if not item:
                    item = MenuItem(
                        name=p['name'],
                        price=float(p.get('lst_price', 0.0)),
                        is_available=True,
                        odoo_product_id=p['id'],
                        odoo_template_id=tmpl_id
                    )
                    db.add(item)
                    counts["dishes"] += 1
                else:
                    if item.odoo_product_id != p['id'] or abs(item.price - float(p.get('lst_price', 0.0))) > 0.01:
                        item.odoo_product_id = p['id']
                        item.odoo_template_id = tmpl_id
                        item.price = float(p.get('lst_price', item.price))
                        counts["dishes"] += 1
        except Exception as e:
            logger.error(f"Erreur lors de la synchro des plats depuis Odoo: {e}")

        # 3. Tables
        try:
            odoo_tables = self.execute_kw('restaurant.table', 'search_read', [[]], {'fields': ['id', 'name', 'seats']})
            for t in odoo_tables:
                table = db.query(RestaurantTable).filter((RestaurantTable.odoo_table_id == t['id']) | (RestaurantTable.name == t['name'])).first()
                if not table:
                    table = RestaurantTable(
                        name=t['name'],
                        capacity=t.get('seats', 4),
                        odoo_table_id=t['id'],
                        status='available'
                    )
                    db.add(table)
                    counts["tables"] += 1
                else:
                    if table.odoo_table_id != t['id']:
                        table.odoo_table_id = t['id']
                        counts["tables"] += 1
        except Exception as e:
            logger.error(f"Erreur lors de la synchro des tables depuis Odoo: {e}")

        # 4. Commandes POS
        try:
            odoo_orders = self.execute_kw('pos.order', 'search_read', [[]], {
                'fields': ['id', 'name', 'amount_total', 'state', 'date_order', 'table_id', 'lines', 'user_id', 'session_id']
            })
            for o in odoo_orders:
                clean_name = (o.get('name') or '').replace('CMD-', '')
                order = db.query(Order).filter(
                    (Order.odoo_pos_order_id == o['id']) | 
                    (Order.order_number == o.get('name')) | 
                    (Order.order_number == clean_name)
                ).first()
                table_id = None
                if o.get('table_id'):
                    odoo_tid = o['table_id'][0] if isinstance(o['table_id'], (list, tuple)) else o['table_id']
                    matched_tbl = db.query(RestaurantTable).filter(RestaurantTable.odoo_table_id == odoo_tid).first()
                    if matched_tbl:
                        table_id = matched_tbl.id

                mgr_name = o['user_id'][1] if isinstance(o.get('user_id'), (list, tuple)) else None
                sess_name = o['session_id'][1] if isinstance(o.get('session_id'), (list, tuple)) else None
                mgr_login = None

                if sess_name:
                    s_matched = db.query(PosSession).filter(PosSession.session_name == sess_name).first()
                    if s_matched:
                        if not mgr_name and s_matched.manager_name:
                            mgr_name = s_matched.manager_name
                        mgr_login = s_matched.manager_login

                order_dt = None
                if o.get('date_order'):
                    try:
                        order_dt = datetime.datetime.fromisoformat(o['date_order'])
                    except Exception:
                        pass

                target_status = 'paid' if o['state'] == 'paid' else ('done' if o['state'] == 'done' else 'pending')
                if not order:
                    order = Order(
                        order_number=o['name'],
                        table_id=table_id,
                        status=target_status,
                        total_amount=float(o.get('amount_total', 0.0)),
                        odoo_pos_order_id=o['id'],
                        odoo_sync_status='synced',
                        manager_name=mgr_name,
                        manager_login=mgr_login,
                        session_name=sess_name,
                        payment_method="Espèces (Cash)",
                        created_at=order_dt or datetime.datetime.utcnow()
                    )
                    db.add(order)
                    counts["orders"] += 1
                else:
                    if order.status != target_status or abs(order.total_amount - float(o.get('amount_total', 0.0))) > 0.01:
                        order.status = target_status
                        order.total_amount = float(o.get('amount_total', order.total_amount))
                        order.odoo_sync_status = 'synced'
                        counts["orders"] += 1
                    if mgr_name and not order.manager_name:
                        order.manager_name = mgr_name
                    if mgr_login and not order.manager_login:
                        order.manager_login = mgr_login
                    if sess_name and not order.session_name:
                        order.session_name = sess_name
                    if order_dt:
                        order.created_at = order_dt
        except Exception as e:
            logger.error(f"Erreur lors de la synchro des commandes depuis Odoo: {e}")

        # 5. Sessions de Caisse POS (Traçabilité & Horaires des Gérants)
        try:
            odoo_sessions = self.execute_kw('pos.session', 'search_read', [[]], {
                'fields': ['id', 'name', 'user_id', 'start_at', 'stop_at', 'state', 'total_payments_amount', 'cash_register_difference']
            })
            for s in odoo_sessions:
                sess_rec = db.query(PosSession).filter(PosSession.odoo_session_id == s['id']).first()
                mgr_name = s['user_id'][1] if isinstance(s.get('user_id'), (list, tuple)) else "Gérant"
                start_at = None
                if s.get('start_at'):
                    try:
                        start_at = datetime.datetime.fromisoformat(s['start_at'])
                    except Exception:
                        pass
                stop_at = None
                if s.get('stop_at'):
                    try:
                        stop_at = datetime.datetime.fromisoformat(s['stop_at'])
                    except Exception:
                        pass

                total_sales = float(s.get('total_payments_amount', 0.0) or 0.0)
                cash_diff = float(s.get('cash_register_difference', 0.0) or 0.0)

                if not sess_rec:
                    sess_rec = PosSession(
                        odoo_session_id=s['id'],
                        session_name=s['name'],
                        manager_name=mgr_name,
                        start_at=start_at or datetime.datetime.utcnow(),
                        stop_at=stop_at,
                        state=s.get('state', 'opened'),
                        total_sales=total_sales,
                        cash_difference=cash_diff
                    )
                    db.add(sess_rec)
                    counts["sessions"] += 1
                else:
                    sess_rec.session_name = s['name']
                    sess_rec.manager_name = mgr_name
                    if start_at:
                        sess_rec.start_at = start_at
                    if stop_at:
                        sess_rec.stop_at = stop_at
                    sess_rec.state = s.get('state', sess_rec.state)
                    sess_rec.total_sales = total_sales
                    sess_rec.cash_difference = cash_diff
        except Exception as e:
            logger.error(f"Erreur lors de la synchro des sessions depuis Odoo: {e}")

        db.commit()
        return counts

    def sync_manager_session_invoice(
        self,
        invoice_number: str,
        manager_name: str,
        manager_id: int,
        date_str: str,
        time_str: str
    ) -> Optional[int]:
        """
        Crée ou initialise immédiatement la Facture Globale de Session dans Odoo :
        - Dans restaurant.daily.report : porte le nom du gérant, l'heure de connexion, TTC/HT/TVA à 0 FCFA.
        - Dans account.move : crée la facture client correspondante au statut brouillon.
        """
        try:
            report_id = self.execute_kw(
                'restaurant.daily.report',
                'create_manager_session_report',
                [manager_id, f"{date_str} {time_str}", manager_name]
            )
            logger.info(f"Facture de session créée dans Odoo pour {manager_name} (ID: {report_id})")
            return report_id
        except Exception as e:
            logger.warning(f"Erreur sync_manager_session_invoice Odoo: {e}")
            return None

    def sync_company_settings_to_odoo(self, config) -> bool:
        """
        Synchronise les données d'identité et de fiscalité du restaurant vers la société principale dans Odoo (res.company).
        Met à jour : nom, ifu/vat, phone, email, street, website, et logo (si base64).
        """
        try:
            company_ids = self.execute_kw('res.company', 'search', [[]], {'limit': 1})
            if not company_ids:
                return False
            comp_id = company_ids[0]
            vals = {}
            if getattr(config, 'restaurant_name', None):
                vals['name'] = config.restaurant_name
            ifu_val = getattr(config, 'ifu', None) or getattr(config, 'nif', None)
            if ifu_val:
                vals['vat'] = ifu_val
            if getattr(config, 'phone', None):
                vals['phone'] = config.phone
            if getattr(config, 'email', None):
                vals['email'] = config.email
            if getattr(config, 'address', None):
                vals['street'] = config.address
            if getattr(config, 'website', None):
                vals['website'] = config.website
            logo_url = getattr(config, 'logo_url', None)
            if logo_url and logo_url.startswith('data:image'):
                try:
                    base64_data = logo_url.split(',', 1)[1]
                    vals['logo'] = base64_data
                except Exception:
                    pass
            if vals:
                self.execute_kw('res.company', 'write', [[comp_id], vals])
                logger.info(f"Paramètres du restaurant synchronisés avec succès vers Odoo res.company #{comp_id}")
            return True
        except Exception as e:
            logger.warning(f"Erreur sync_company_settings_to_odoo: {e}")
            return False

odoo_service = OdooService()


