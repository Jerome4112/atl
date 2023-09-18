from fastapi import APIRouter
from ATL.auth.auth_handler import oauth2_scheme
from ATL.schemas.order import Order, OrderCreate
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from ATL.dependencies import get_db
from ATL.services.order import (
    create_order as create_order_service,
    get_order, get_orders, update_order, delete_order, add_program
)

# Erstellen eines API-Routers für die Order-Entität
router = APIRouter(prefix="/order")

# Route zum Abrufen einer Liste von Bestellungen
@router.get("/", response_model=list[Order], tags=["Order"])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Gibt eine Liste von Bestellungen zurück.

    :param skip: Die Anzahl der Bestellungen, die übersprungen werden sollen.
    :type skip: int
    :param limit: Die maximale Anzahl der Bestellungen, die zurückgegeben werden sollen.
    :type limit: int
    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param token: Das OAuth2-Token zur Authentifizierung.
    :type token: str
    :return: Eine Liste von Bestellungen.
    :rtype: list[Order]
    """
    orders = get_orders(db, skip=skip, limit=limit)
    return orders

# Route zum Abrufen einer einzelnen Bestellung anhand ihrer ID
@router.get("/{order_id}", response_model=Order, tags=["Order"])
def read_order(order_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Gibt die Daten einer einzelnen Bestellung anhand ihrer ID zurück.

    :param order_id: Die ID der Bestellung.
    :type order_id: int
    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param token: Das OAuth2-Token zur Authentifizierung.
    :type token: str
    :return: Die Bestelldaten.
    :rtype: Order
    """
    db_order = get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

# Route zum Erstellen einer neuen Bestellung für einen bestimmten Kunden und Mitarbeiter
@router.post("/{customer_id},{employee_id}", response_model=Order, tags=["Order"])
def create_order(customer_id: int, employee_id: int, order: OrderCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Erstellt eine neue Bestellung für einen bestimmten Kunden und Mitarbeiter.

    :param customer_id: Die ID des Kunden, für den die Bestellung erstellt werden soll.
    :type customer_id: int
    :param employee_id: Die ID des Mitarbeiters, der die Bestellung erstellt.
    :type employee_id: int
    :param order: Die Daten der neuen Bestellung.
    :type order: OrderCreate
    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param token: Das OAuth2-Token zur Authentifizierung.
    :type token: str
    :return: Die erstellten Bestelldaten.
    :rtype: Order
    """
    db_order = get_order(db, order.id)
    if db_order:
        raise HTTPException(status_code=400, detail="Order already registered")
    return create_order_service(db=db, order=order, customer_id=customer_id, employee_id=employee_id)

# Route zum Aktualisieren einer Bestellung anhand ihrer ID
@router.put("/{order_id}", response_model=OrderCreate, tags=["Order"])
def update_order_by_id(order_id: int, order_update: OrderCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Aktualisiert die Daten einer Bestellung anhand ihrer ID.

    :param order_id: Die ID der Bestellung.
    :type order_id: int
    :param order_update: Die aktualisierten Bestelldaten.
    :type order_update: OrderCreate
    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param token: Das OAuth2-Token zur Authentifizierung.
    :type token: str
    :return: Die aktualisierten Bestelldaten.
    :rtype: OrderCreate
    """
    updated_order = update_order(db=db, order_id=order_id, order_update=order_update)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

# Route zum Löschen einer Bestellung anhand ihrer ID
@router.delete("/{order_id}", response_model=Order, tags=["Order"])
def delete_order_by_id(order_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Löscht eine Bestellung anhand ihrer ID.

    :param order_id: Die ID der zu löschenden Bestellung.
    :type order_id: int
    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param token: Das OAuth2-Token zur Authentifizierung.
    :type token: str
    :return: Die gelöschten Bestelldaten.
    :rtype: Order
    """
    deleted_order = delete_order(db=db, order_id=order_id)
    if not deleted_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return deleted_order

# Route zum Hinzufügen eines Programms zu einer Bestellung
@router.post("/add_program_to_order", tags=["Order"])
def add_program_to_order(order_id: int, program_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Fügt ein Programm zu einer Bestellung hinzu.

    :param order_id: Die ID der Bestellung.
    :type order_id: int
    :param program_id: Die ID des Programms, das hinzugefügt werden soll.
    :type program_id: int
    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param token: Das OAuth2-Token zur Authentifizierung.
    :type token: str
    :return: Eine Bestätigungsnachricht.
    :rtype: dict
    """
    order_program = add_program(db, order_id, program_id)
    if not order_program:
        raise HTTPException(status_code=404, detail="Order or Program not found")
    return {"message": "Program added to order successfully"}
