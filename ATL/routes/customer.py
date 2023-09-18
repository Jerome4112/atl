from fastapi import APIRouter
from ATL.auth.auth_handler import oauth2_scheme
from ATL.schemas.customer import Customer, CustomerCreate
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from ATL.dependencies import get_db
from ATL.services.customer import (
    get_customer_by_name,
    create_customer as create_customer_service,
    get_customer, get_customers, update_customer,
    delete_customer
)

# Erstellen eines API-Routers für die Customer-Entität
router = APIRouter(prefix="/customer")

# Route zum Erstellen eines neuen Kunden
@router.post("/", response_model=CustomerCreate, tags=["Customer"])
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Erstellt einen neuen Kunden.

    :param customer: Die Daten des neuen Kunden.
    :type customer: CustomerCreate
    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param token: Das OAuth2-Token zur Authentifizierung.
    :type token: str
    :return: Die erstellten Kundendaten.
    :rtype: CustomerCreate
    """
    db_customer = get_customer_by_name(db, name=customer.name)
    if db_customer:
        raise HTTPException(status_code=400, detail="Name already registered")
    return create_customer_service(db=db, customer=customer)

# Route zum Abrufen einer Liste von Kunden
@router.get("/", response_model=list[CustomerCreate], tags=["Customer"])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Gibt eine Liste von Kunden zurück.

    :param skip: Die Anzahl der Kunden, die übersprungen werden sollen.
    :type skip: int
    :param limit: Die maximale Anzahl der Kunden, die zurückgegeben werden sollen.
    :type limit: int
    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param token: Das OAuth2-Token zur Authentifizierung.
    :type token: str
    :return: Eine Liste von Kundendaten.
    :rtype: list[CustomerCreate]
    """
    customer = get_customers(db, skip=skip, limit=limit)
    return customer

# Route zum Abrufen eines einzelnen Kunden anhand seiner ID
@router.get("/{customer_id}", response_model=Customer, tags=["Customer"])
def read_customer_Orders(customer_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Gibt die Daten eines einzelnen Kunden anhand seiner ID zurück.

    :param customer_id: Die ID des Kunden.
    :type customer_id: int
    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param token: Das OAuth2-Token zur Authentifizierung.
    :type token: str
    :return: Die Kundendaten.
    :rtype: Customer
    """
    db_customer = get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

# Route zum Aktualisieren eines Kunden anhand seiner ID
@router.put("/{customer_id}", response_model=CustomerCreate, tags=["Customer"])
def update_customer_by_id(customer_id: int, customer_update: CustomerCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Aktualisiert die Daten eines Kunden anhand seiner ID.

    :param customer_id: Die ID des Kunden.
    :type customer_id: int
    :param customer_update: Die aktualisierten Kundendaten.
    :type customer_update: CustomerCreate
    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param token: Das OAuth2-Token zur Authentifizierung.
    :type token: str
    :return: Die aktualisierten Kundendaten.
    :rtype: CustomerCreate
    """
    updated_customer = update_customer(db=db, customer_id=customer_id, customer_update=customer_update)
    if not updated_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated_customer

# Route zum Löschen eines Kunden anhand seiner ID
@router.delete("/{customer_id}", response_model=Customer, tags=["Customer"])
def delete_customer_by_id(customer_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Löscht einen Kunden anhand seiner ID.

    :param customer_id: Die ID des zu löschenden Kunden.
    :type customer_id: int
    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param token: Das OAuth2-Token zur Authentifizierung.
    :type token: str
    :return: Die gelöschten Kundendaten.
    :rtype: Customer
    """
    deleted_customer = delete_customer(db=db, customer_id=customer_id)
    if not deleted_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return deleted_customer
