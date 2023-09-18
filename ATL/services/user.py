from sqlalchemy.orm import Session
from ATL.models.user import User
from ATL.schemas.user import UserCreate
from ATL.auth.password_handler import verify_password, get_password_hash

# Funktion zur Abfrage eines Benutzers anhand seiner ID
def get_user(db: Session, user_id: int):
    """
    Gibt die Daten eines Benutzers anhand seiner ID zurück.

    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param user_id: Die ID des Benutzers.
    :type user_id: int
    :return: Die Benutzerdaten.
    :rtype: User
    """
    return db.query(User).filter(User.id == user_id).first()

# Funktion zur Abfrage eines Benutzers anhand seines Namens
def get_user_by_name(db: Session, name: str):
    """
    Gibt die Daten eines Benutzers anhand seines Namens zurück.

    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param name: Der Name des Benutzers.
    :type name: str
    :return: Die Benutzerdaten.
    :rtype: User
    """
    return db.query(User).filter(User.name == name).first()

# Funktion zur Authentifizierung eines Benutzers
def authenticate_user(db: Session, name: str, password: str):
    """
    Authentifiziert einen Benutzer anhand seines Namens und seines Passworts.

    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param name: Der Name des Benutzers.
    :type name: str
    :param password: Das Passwort des Benutzers.
    :type password: str
    :return: True, wenn die Authentifizierung erfolgreich ist, andernfalls False.
    :rtype: bool
    """
    db_user = get_user_by_name(db, name)
    if not db_user:
        return False
    else:
        return verify_password(password, db_user.hashed_password)

# Funktion zur Überprüfung, ob ein Benutzername bereits registriert ist
def is_name_already_registered(db: Session, name: str):
    """
    Überprüft, ob ein Benutzername bereits registriert ist.

    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param name: Der Name, der überprüft werden soll.
    :type name: str
    :return: True, wenn der Name bereits registriert ist, andernfalls False.
    :rtype: bool
    """
    db_user = get_user_by_name(db, name)
    if db_user:
        return True
    else:
        return False

# Funktion zur Registrierung eines neuen Benutzers
def register_new_user(db: Session, user: UserCreate):
    """
    Registriert einen neuen Benutzer in der Datenbank.

    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param user: Die Daten des neuen Benutzers.
    :type user: UserCreate
    :return: Die erstellten Benutzerdaten.
    :rtype: User
    """
    hashed_password = get_password_hash(user.hashed_password)
    db_user = User(name=user.name, hashed_password=hashed_password, is_authorised=user.is_authorised)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
