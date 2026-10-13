import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.models.user import User, UserRole
from app.models.restaurant import ManagerWorkSession, ManagerActivityLog
from app.schemas.user import LoginRequest, TokenResponse, UserResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentification & Espaces"])

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """
    Connexion sécurisée :
    - Vérifie les identifiants et le mot de passe (haché bcrypt).
    - Détermine l'espace dédié de l'utilisateur ('admin' ou 'manager').
    - Si gérant : active le statut EN LIGNE (is_online=True), ouvre une session de travail et consigne l'horodatage.
    - Renvoie le token JWT pour sécuriser l'accès à son espace.
    """
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ce compte utilisateur a été désactivé par l'administrateur.",
        )

    now = datetime.datetime.utcnow()
    # Gestion spécifique de la présence en direct du gérant
    if user.role == UserRole.MANAGER.value:
        user.is_online = True
        user.last_login_at = now

        # Clôturer d'éventuelles sessions antérieures restées ouvertes
        past_sessions = db.query(ManagerWorkSession).filter(
            ManagerWorkSession.user_id == user.id,
            ManagerWorkSession.is_online == True
        ).all()
        for ps in past_sessions:
            ps.is_online = False
            ps.logout_at = now

        # Ouvrir la nouvelle session de service
        new_session = ManagerWorkSession(
            user_id=user.id,
            manager_name=user.full_name,
            manager_login=user.username,
            login_at=now,
            is_online=True,
            total_sales_amount=0.0,
            total_orders_count=0,
            total_tendered_amount=0.0,
            total_change_amount=0.0,
            last_activity_at=now
        )
        db.add(new_session)

        # Enregistrer l'action dans le journal des faits et gestes
        activity = ManagerActivityLog(
            user_id=user.id,
            manager_name=user.full_name,
            manager_login=user.username,
            action_type="LOGIN",
            description=f"🟢 Connexion & Début de service du gérant {user.full_name} ({user.username}) à {now.strftime('%H:%M:%S')}.",
            created_at=now
        )
        db.add(activity)
        db.commit()

        # Création automatique de la facture globale de session pour ce gérant
        try:
            from app.services.billing_service import billing_service
            billing_service.create_invoice_for_manager_session(user, db)
        except Exception as e:
            print(f"Erreur création facture globale pour le gérant: {e}")

        # Synchroniser la prise de service dans Odoo en direct
        try:
            from app.services.odoo_service import odoo_service
            if user.odoo_user_id:
                odoo_service.execute_kw('res.users', 'write', [[user.odoo_user_id], {
                    'is_online': True,
                    'last_login_time': now.strftime('%Y-%m-%d %H:%M:%S')
                }])
            odoo_service.execute_kw('restaurant.activity.log', 'create', [{
                'manager_id': user.odoo_user_id or False,
                'manager_name': user.full_name,
                'manager_login': user.username,
                'action_type': 'login',
                'description': f"🟢 Connexion & Début de service du gérant {user.full_name} ({user.username}).",
                'activity_time': now.strftime('%Y-%m-%d %H:%M:%S')
            }])
        except Exception:
            pass

    assigned_space = "admin" if user.role == UserRole.ADMIN.value else "manager"
    access_token = create_access_token(data={
        "sub": user.username,
        "role": user.role,
        "user_id": user.id
    })

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role,
        "username": user.username,
        "full_name": user.full_name,
        "assigned_space": assigned_space
    }

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Déconnexion sécurisée :
    - Bascule le statut du gérant à INACTIF / HORS LIGNE (is_online=False).
    - Horodate la fin de service avec l'heure de déconnexion.
    - Clôture la session de travail en conservant le total des ventes et l'argent encaissé.
    - Consigne l'événement dans le journal d'activité.
    """
    now = datetime.datetime.utcnow()
    current_user.is_online = False
    current_user.last_logout_at = now

    total_sales = 0.0
    total_orders = 0
    if current_user.role == UserRole.MANAGER.value:
        active_sess = db.query(ManagerWorkSession).filter(
            ManagerWorkSession.user_id == current_user.id,
            ManagerWorkSession.is_online == True
        ).order_by(ManagerWorkSession.id.desc()).first()

        if active_sess:
            active_sess.is_online = False
            active_sess.logout_at = now
            active_sess.last_activity_at = now
            total_sales = active_sess.total_sales_amount
            total_orders = active_sess.total_orders_count

        activity = ManagerActivityLog(
            user_id=current_user.id,
            manager_name=current_user.full_name,
            manager_login=current_user.username,
            action_type="LOGOUT",
            description=f"⚪ Déconnexion & Fin de service du gérant {current_user.full_name} ({current_user.username}). Bilan session : {total_orders} vente(s) totalisant {total_sales:,.0f} FCFA.",
            amount=total_sales,
            created_at=now
        )
        db.add(activity)

        # Synchroniser la fin de service dans Odoo en direct
        try:
            from app.services.odoo_service import odoo_service
            if current_user.odoo_user_id:
                odoo_service.execute_kw('res.users', 'write', [[current_user.odoo_user_id], {
                    'is_online': False,
                    'last_logout_time': now.strftime('%Y-%m-%d %H:%M:%S')
                }])
            odoo_service.execute_kw('restaurant.activity.log', 'create', [{
                'manager_id': current_user.odoo_user_id or False,
                'manager_name': current_user.full_name,
                'manager_login': current_user.username,
                'action_type': 'logout',
                'description': f"⚪ Déconnexion & Fin de service du gérant {current_user.full_name} ({current_user.username}). Bilan : {total_orders} ventes, {total_sales:,.0f} FCFA.",
                'amount': total_sales,
                'activity_time': now.strftime('%Y-%m-%d %H:%M:%S')
            }])
        except Exception:
            pass

    db.commit()
    return {
        "message": "Déconnexion enregistrée avec succès.",
        "logout_at": now.isoformat(),
        "total_sales_session": total_sales,
        "total_orders_session": total_orders
    }

@router.post("/login-form", response_model=TokenResponse)
def login_form(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Endpoint compatible avec Swagger UI OAuth2."""
    payload = LoginRequest(username=form_data.username, password=form_data.password)
    return login(payload, db)

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Retourne les informations du profil connecté."""
    return current_user

