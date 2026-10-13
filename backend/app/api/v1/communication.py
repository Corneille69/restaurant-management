from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc
import datetime

from app.core.database import get_db
from app.models.user import User, UserRole
from app.models.communication import CommunicationMessage, WebRTCSignal
from app.api.deps import get_current_user

router = APIRouter(prefix="/communication", tags=["Communication Admin <-> Gérant"])

# --- Schémas Pydantic ---
class SendMessageRequest(BaseModel):
    receiver_id: Optional[int] = None
    content: str
    message_type: Optional[str] = "text"

class MessageResponse(BaseModel):
    id: int
    sender_id: int
    sender_name: str
    sender_role: str
    receiver_id: Optional[int]
    content: str
    message_type: str
    is_read: bool
    created_at: str
    is_mine: bool

class ContactResponse(BaseModel):
    id: int
    full_name: str
    username: str
    role: str
    is_online: bool
    unread_count: int

class SignalRequest(BaseModel):
    receiver_id: int
    signal_type: str # call_request, offer, answer, candidate, hangup, reject
    payload: str

class SignalResponse(BaseModel):
    id: int
    sender_id: int
    sender_name: str
    receiver_id: int
    signal_type: str
    payload: str
    created_at: str


@router.get("/contacts", response_model=List[ContactResponse])
def get_communication_contacts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retourne la liste des contacts pour la discussion :
    - Pour l'Admin : tous les gérants
    - Pour un Gérant : l'administrateur
    """
    contacts = []
    if current_user.role == UserRole.ADMIN.value or current_user.role == "admin":
        # Admin voit tous les gérants actifs
        managers = db.query(User).filter(
            User.role.in_([UserRole.MANAGER.value, "manager"]),
            User.is_active == True
        ).all()
        for m in managers:
            unread = db.query(CommunicationMessage).filter(
                CommunicationMessage.sender_id == m.id,
                CommunicationMessage.receiver_id == current_user.id,
                CommunicationMessage.is_read == False
            ).count()
            contacts.append(ContactResponse(
                id=m.id,
                full_name=m.full_name,
                username=m.username,
                role=m.role,
                is_online=m.is_online,
                unread_count=unread
            ))
    else:
        # Gérant voit l'administrateur (ou tous les admins)
        admins = db.query(User).filter(
            User.role.in_([UserRole.ADMIN.value, "admin"]),
            User.is_active == True
        ).all()
        for a in admins:
            unread = db.query(CommunicationMessage).filter(
                CommunicationMessage.sender_id == a.id,
                CommunicationMessage.receiver_id == current_user.id,
                CommunicationMessage.is_read == False
            ).count()
            contacts.append(ContactResponse(
                id=a.id,
                full_name=a.full_name,
                username=a.username,
                role=a.role,
                is_online=a.is_online,
                unread_count=unread
            ))
    return contacts


@router.post("/messages", response_model=MessageResponse)
def send_message(
    payload: SendMessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Envoi d'un message direct SMS/Chat entre Admin et Gérant.
    """
    receiver_id = payload.receiver_id
    if not receiver_id:
        if current_user.role in [UserRole.MANAGER.value, "manager"]:
            # Trouver l'admin par défaut
            admin = db.query(User).filter(User.role.in_([UserRole.ADMIN.value, "admin"]), User.is_active == True).first()
            if not admin:
                raise HTTPException(status_code=404, detail="Administrateur introuvable.")
            receiver_id = admin.id
        else:
            raise HTTPException(status_code=400, detail="Veuillez spécifier le destinataire (receiver_id).")

    receiver = db.query(User).filter(User.id == receiver_id, User.is_active == True).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="Destinataire introuvable.")

    msg = CommunicationMessage(
        sender_id=current_user.id,
        receiver_id=receiver_id,
        message_type=payload.message_type or "text",
        content=payload.content.strip(),
        is_read=False,
        created_at=datetime.datetime.utcnow()
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)

    return MessageResponse(
        id=msg.id,
        sender_id=current_user.id,
        sender_name=current_user.full_name,
        sender_role=current_user.role,
        receiver_id=receiver_id,
        content=msg.content,
        message_type=msg.message_type,
        is_read=False,
        created_at=msg.created_at.strftime("%H:%M:%S"),
        is_mine=True
    )


@router.get("/messages", response_model=List[MessageResponse])
def get_messages(
    contact_id: Optional[int] = Query(None, description="ID du contact avec qui échanger"),
    after_id: Optional[int] = Query(None, description="Récupère uniquement les messages ayant un ID supérieur"),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère le fil de conversation instantané entre le connecté et son interlocuteur.
    Marque automatiquement les messages reçus comme lus.
    """
    target_id = contact_id
    if not target_id:
        if current_user.role in [UserRole.MANAGER.value, "manager"]:
            admin = db.query(User).filter(User.role.in_([UserRole.ADMIN.value, "admin"]), User.is_active == True).first()
            if admin:
                target_id = admin.id
        else:
            first_manager = db.query(User).filter(User.role.in_([UserRole.MANAGER.value, "manager"]), User.is_active == True).first()
            if first_manager:
                target_id = first_manager.id

    if not target_id:
        return []

    # Filtrer les messages échangés entre current_user et target_id
    query = db.query(CommunicationMessage).filter(
        or_(
            and_(CommunicationMessage.sender_id == current_user.id, CommunicationMessage.receiver_id == target_id),
            and_(CommunicationMessage.sender_id == target_id, CommunicationMessage.receiver_id == current_user.id)
        )
    )

    if after_id:
        query = query.filter(CommunicationMessage.id > after_id)

    messages = query.order_by(CommunicationMessage.id.asc()).limit(limit).all()

    # Marquer les messages reçus comme lus
    unread_ids = [m.id for m in messages if m.receiver_id == current_user.id and not m.is_read]
    if unread_ids:
        db.query(CommunicationMessage).filter(CommunicationMessage.id.in_(unread_ids)).update(
            {"is_read": True}, synchronize_session=False
        )
        db.commit()

    # Récupérer les noms des utilisateurs pour l'affichage
    target_user = db.query(User).filter(User.id == target_id).first()
    target_name = target_user.full_name if target_user else "Correspondant"

    result = []
    for m in messages:
        is_mine = (m.sender_id == current_user.id)
        sender_name = current_user.full_name if is_mine else target_name
        sender_role = current_user.role if is_mine else (target_user.role if target_user else "user")
        result.append(MessageResponse(
            id=m.id,
            sender_id=m.sender_id,
            sender_name=sender_name,
            sender_role=sender_role,
            receiver_id=m.receiver_id,
            content=m.content,
            message_type=m.message_type,
            is_read=m.is_read,
            created_at=m.created_at.strftime("%H:%M:%S") if m.created_at else "",
            is_mine=is_mine
        ))

    return result


@router.get("/unread_count")
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Nombre total de messages non lus pour l'utilisateur connecté."""
    count = db.query(CommunicationMessage).filter(
        CommunicationMessage.receiver_id == current_user.id,
        CommunicationMessage.is_read == False
    ).count()
    return {"unread_count": count}


# --- Signaux WebRTC pour Appel Vidéo & Audio ---

@router.post("/signal", response_model=dict)
def send_signal(
    payload: SignalRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Envoi d'un signal WebRTC (call_request, offer, answer, candidate, hangup, reject).
    """
    # Si c'est un hangup ou reject, nettoyer les signaux précédents non consommés
    if payload.signal_type in ["hangup", "reject"]:
        db.query(WebRTCSignal).filter(
            or_(
                and_(WebRTCSignal.sender_id == current_user.id, WebRTCSignal.receiver_id == payload.receiver_id),
                and_(WebRTCSignal.sender_id == payload.receiver_id, WebRTCSignal.receiver_id == current_user.id)
            )
        ).update({"status": "cancelled"}, synchronize_session=False)

    sig = WebRTCSignal(
        sender_id=current_user.id,
        receiver_id=payload.receiver_id,
        signal_type=payload.signal_type,
        payload=payload.payload,
        status="pending",
        created_at=datetime.datetime.utcnow()
    )
    db.add(sig)
    db.commit()
    return {"status": "sent", "signal_id": sig.id}


@router.get("/signals", response_model=List[SignalResponse])
def get_pending_signals(
    after_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les signaux WebRTC en attente adressés à l'utilisateur connecté (dans les 60 dernières secondes).
    """
    time_limit = datetime.datetime.utcnow() - datetime.timedelta(seconds=60)
    query = db.query(WebRTCSignal).filter(
        WebRTCSignal.receiver_id == current_user.id,
        WebRTCSignal.status == "pending",
        WebRTCSignal.created_at >= time_limit
    )
    if after_id:
        query = query.filter(WebRTCSignal.id > after_id)

    signals = query.order_by(WebRTCSignal.id.asc()).all()

    response = []
    consumed_ids = []
    for s in signals:
        sender_user = db.query(User).filter(User.id == s.sender_id).first()
        s_name = sender_user.full_name if sender_user else f"Utilisateur {s.sender_id}"
        response.append(SignalResponse(
            id=s.id,
            sender_id=s.sender_id,
            sender_name=s_name,
            receiver_id=s.receiver_id,
            signal_type=s.signal_type,
            payload=s.payload,
            created_at=s.created_at.strftime("%H:%M:%S")
        ))
        consumed_ids.append(s.id)

    if consumed_ids:
        db.query(WebRTCSignal).filter(WebRTCSignal.id.in_(consumed_ids)).update(
            {"status": "consumed"}, synchronize_session=False
        )
        db.commit()

    return response


@router.post("/call/hangup")
def hangup_call(
    contact_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Met fin immédiatement à tout appel en cours avec le contact."""
    db.query(WebRTCSignal).filter(
        or_(
            and_(WebRTCSignal.sender_id == current_user.id, WebRTCSignal.receiver_id == contact_id),
            and_(WebRTCSignal.sender_id == contact_id, WebRTCSignal.receiver_id == current_user.id)
        )
    ).update({"status": "cancelled"}, synchronize_session=False)
    
    # Enregistrer un signal hangup pour avertir l'autre partie
    sig = WebRTCSignal(
        sender_id=current_user.id,
        receiver_id=contact_id,
        signal_type="hangup",
        payload="{}",
        status="pending",
        created_at=datetime.datetime.utcnow()
    )
    db.add(sig)
    db.commit()
    return {"status": "call_ended"}
