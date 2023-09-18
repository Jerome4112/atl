from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from ATL.services import user as services
from ATL.dependencies import get_db
from ATL.schemas.user import UserCreate
from ATL.auth.auth_handler import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

# Erstellen eines API-Routers für Benutzer-Authentifizierung und Registrierung
router = APIRouter(prefix="/user")

# Route für Benutzeranmeldung
@router.post("/login", tags=["User"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Ermöglicht einem Benutzer die Authentifizierung und Ausgabe eines Zugriffstokens.

    :param form_data: Die Anmeldeinformationen des Benutzers.
    :type form_data: OAuth2PasswordRequestForm
    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :return: Ein Zugriffstoken für den authentifizierten Benutzer.
    :rtype: dict
    """
    authenticated = services.authenticate_user(db, form_data.username, form_data.password)
    if authenticated:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        data = {"name": form_data.username}
        token = create_access_token(data, access_token_expires)
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

# Route für die Benutzerregistrierung
@router.post("/register", tags=["User"])
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Registriert einen neuen Benutzer und gibt ein Zugriffstoken aus.

    :param user: Die Registrierungsdaten des neuen Benutzers.
    :type user: UserCreate
    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :return: Ein Zugriffstoken für den registrierten Benutzer.
    :rtype: dict
    """
    if not services.is_name_already_registered(db, user.name):
        db_user = services.register_new_user(db, user)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        data = {"name": db_user.name}
        token = create_access_token(data, access_token_expires)
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=400, detail="Name already registered")
