from sqlalchemy.orm import Session
from ATL.models.order import Order
from ATL.schemas.order import OrderCreate
from ATL.models.orderPrograms import OrderPrograms

# Funktion zur Abfrage einer Bestellung anhand ihrer ID
def get_order(db: Session, order_id: int):
    """
    Gibt die Daten einer Bestellung anhand ihrer ID zurück.

    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param order_id: Die ID der Bestellung.
    :type order_id: int
    :return: Die Bestelldaten.
    :rtype: Order
    """
    return db.query(Order).filter(Order.id == order_id).first()

# Funktion zur Abfrage einer Liste von Bestellungen mit optionalen Überspringen und Begrenzen
def get_orders(db: Session, skip: int = 0, limit: int = 100):
    """
    Gibt eine Liste von Bestellungen zurück.

    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param skip: Die Anzahl der Bestellungen, die übersprungen werden sollen.
    :type skip: int
    :param limit: Die maximale Anzahl der Bestellungen, die zurückgegeben werden sollen.
    :type limit: int
    :return: Eine Liste von Bestellungen.
    :rtype: list[Order]
    """
    return db.query(Order).offset(skip).limit(limit).all()

# Funktion zur Erstellung einer neuen Bestellung
def create_order(db: Session, order: OrderCreate, customer_id: int, employee_id: int):
    """
    Erstellt eine neue Bestellung.

    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param order: Die Daten der neuen Bestellung.
    :type order: OrderCreate
    :param customer_id: Die ID des zugehörigen Kunden.
    :type customer_id: int
    :param employee_id: Die ID des zugehörigen Mitarbeiters.
    :type employee_id: int
    :return: Die erstellten Bestelldaten.
    :rtype: Order
    """
    db_order = Order(id=order.id, title=order.title, hardware=order.hardware, details=order.details, customer_id=customer_id, employee_id=employee_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

# Funktion zur Aktualisierung einer Bestellung anhand ihrer ID
def update_order(db: Session, order_id: int, order_update: OrderCreate):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        return None
    for attr, value in order_update.dict().items():
        setattr(db_order, attr, value)
    db.commit()
    return db_order

# Funktion zum Löschen einer Bestellung anhand ihrer ID
def delete_order(db: Session, order_id: int):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        return None
    db.delete(db_order)
    db.commit()
    return db_order

# Funktion zum Hinzufügen eines Programms zu einer Bestellung
def add_program(db: Session, order_id: int, program_id: int):
    # Überprüfen, ob die Bestellung und das Programm vorhanden sind
    order_program = OrderPrograms(order_id=order_id, program_id=program_id)
    db.add(order_program)
    db.commit()
    db.refresh(order_program)
    return order_program
