from sqlalchemy.orm import Session
from ATL.models.customer import Customer
from ATL.schemas.customer import CustomerCreate

# Funktion zur Abfrage eines Kunden anhand seiner ID
def get_customer(db: Session, customer_id: int):
    """
    Gibt die Daten eines Kunden anhand seiner ID zurück.

    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param customer_id: Die ID des Kunden.
    :type customer_id: int
    :return: Die Kundendaten.
    :rtype: Customer
    """
    return db.query(Customer).filter(Customer.id == customer_id).first()

# Funktion zur Abfrage eines Kunden anhand seines Namens
def get_customer_by_name(db: Session, name: str):
    """
    Gibt die Daten eines Kunden anhand seines Namens zurück.

    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param name: Der Name des Kunden.
    :type name: str
    :return: Die Kundendaten.
    :rtype: Customer
    """
    return db.query(Customer).filter(Customer.name == name).first()

# Funktion zur Abfrage einer Liste von Kunden mit optionalen Überspringen und Begrenzen
def get_customers(db: Session, skip: int = 0, limit: int = 100):
    """
    Gibt eine Liste von Kunden zurück.

    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param skip: Die Anzahl der Kunden, die übersprungen werden sollen.
    :type skip: int
    :param limit: Die maximale Anzahl der Kunden, die zurückgegeben werden sollen.
    :type limit: int
    :return: Eine Liste von Kunden.
    :rtype: list[Customer]
    """
    return db.query(Customer).offset(skip).limit(limit).all()

# Funktion zur Erstellung eines neuen Kunden
def create_customer(db: Session, customer: CustomerCreate):
    """
    Erstellt einen neuen Kunden.

    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param customer: Die Daten des neuen Kunden.
    :type customer: CustomerCreate
    :return: Die erstellten Kundendaten.
    :rtype: Customer
    """
    db_customer = Customer(name=customer.name, id=customer.id, adress=customer.adress, adressNr=customer.adressNr, email=customer.email, tel=customer.tel, city=customer.city, postalCode=customer.postalCode)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

# Funktion zur Aktualisierung eines Kunden anhand seiner ID
def update_customer(db: Session, customer_id: int, customer_update: CustomerCreate):
    """
    Aktualisiert die Daten eines Kunden anhand seiner ID.

    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param customer_id: Die ID des Kunden.
    :type customer_id: int
    :param customer_update: Die aktualisierten Kundendaten.
    :type customer_update: CustomerCreate
    :return: Die aktualisierten Kundendaten oder None, wenn der Kunde nicht gefunden wurde.
    :rtype: Customer
    """
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not db_customer:
        return None
    for attr, value in customer_update.dict().items():
        setattr(db_customer, attr, value)
    db.commit()
    db.refresh(db_customer)
    return db_customer

# Funktion zum Löschen eines Kunden anhand seiner ID
def delete_customer(db: Session, customer_id: int):
    """
    Löscht einen Kunden anhand seiner ID.

    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param customer_id: Die ID des zu löschenden Kunden.
    :type customer_id: int
    :return: Die gelöschten Kundendaten oder None, wenn der Kunde nicht gefunden wurde.
    :rtype: Customer
    """
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not db_customer:
        return None
    db.delete(db_customer)
    db.commit()
    return db_customer
