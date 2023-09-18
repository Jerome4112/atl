from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    """
    Generiert einen Hash-Wert für das gegebene Passwort.

    :param password: Das zu hashende Passwort.
    :type password: str
    :return: Der generierte Passwort-Hash.
    :rtype: str
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    """
    Überprüft, ob das gegebene Klartext-Passwort mit dem gehashten Passwort übereinstimmt.

    :param plain_password: Das Klartext-Passwort, das überprüft werden soll.
    :type plain_password: str
    :param hashed_password: Das gehashte Passwort, mit dem verglichen werden soll.
    :type hashed_password: str
    :return: True, wenn das Klartext-Passwort mit dem gehashten Passwort übereinstimmt, andernfalls False.
    :rtype: bool
    """
    return pwd_context.verify(plain_password, hashed_password)
    #True or false