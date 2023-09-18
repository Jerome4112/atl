from fastapi import APIRouter
from ATL.schemas.employee import Employee, EmployeeCreate, Employee_order
from ATL.auth.auth_handler import oauth2_scheme
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from ATL.dependencies import get_db
from ATL.services.employee import (
    create_employee as create_employee_service,
    get_employee, get_employees, update_employee, delete_employee, get_employee_order
)

# Erstellen eines API-Routers für die Employee-Entität
router = APIRouter(prefix="/employee")

# Route zum Abrufen einer Liste von Mitarbeitern
@router.get("/", response_model=list[Employee], tags=["Employee"])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Gibt eine Liste von Mitarbeitern zurück.

    :param skip: Die Anzahl der Mitarbeiter, die übersprungen werden sollen.
    :type skip: int
    :param limit: Die maximale Anzahl der Mitarbeiter, die zurückgegeben werden sollen.
    :type limit: int
    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param token: Das OAuth2-Token zur Authentifizierung.
    :type token: str
    :return: Eine Liste von Mitarbeitern.
    :rtype: list[Employee]
    """
    employees = get_employees(db, skip=skip, limit=limit)
    return employees

# Route zum Abrufen eines einzelnen Mitarbeiters anhand seiner ID
@router.get("/{employee_id}", response_model=Employee, tags=["Employee"])
def read_employee(employee_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Gibt die Daten eines einzelnen Mitarbeiters anhand seiner ID zurück.

    :param employee_id: Die ID des Mitarbeiters.
    :type employee_id: int
    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param token: Das OAuth2-Token zur Authentifizierung.
    :type token: str
    :return: Die Mitarbeitersdaten.
    :rtype: Employee
    """
    db_employee = get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

# Route zum Erstellen eines neuen Mitarbeiters für einen bestimmten Kunden
@router.post("/{customer_id}", response_model=Employee, tags=["Employee"])
def create_employee(customer_id: int, employee: EmployeeCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Erstellt einen neuen Mitarbeiter für einen bestimmten Kunden.

    :param customer_id: Die ID des Kunden, für den der Mitarbeiter erstellt werden soll.
    :type customer_id: int
    :param employee: Die Daten des neuen Mitarbeiters.
    :type employee: EmployeeCreate
    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param token: Das OAuth2-Token zur Authentifizierung.
    :type token: str
    :return: Die erstellten Mitarbeitersdaten.
    :rtype: Employee
    """
    db_employee = get_employee(db, employee.id)
    if db_employee:
        raise HTTPException(status_code=400, detail="Employee already registered")
    return create_employee_service(db=db, employee=employee, customer_id=customer_id)

# Route zum Abrufen von Bestellungen, die einem bestimmten Mitarbeiter zugeordnet sind
@router.get("/{employee_id}", response_model=Employee_order, tags=["Employee"])
def read_order_by_employee(employee_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Gibt Bestellungen zurück, die einem bestimmten Mitarbeiter zugeordnet sind.

    :param employee_id: Die ID des Mitarbeiters.
    :type employee_id: int
    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param token: Das OAuth2-Token zur Authentifizierung.
    :type token: str
    :return: Die Bestellungen, die dem Mitarbeiter zugeordnet sind.
    :rtype: Employee_order
    """
    db_employee = get_employee_order(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

# Route zum Aktualisieren eines Mitarbeiters anhand seiner ID
@router.put("/{employee_id}", response_model=EmployeeCreate, tags=["Employee"])
def update_employee_by_id(employee_id: int, employee_update: EmployeeCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Aktualisiert die Daten eines Mitarbeiters anhand seiner ID.

    :param employee_id: Die ID des Mitarbeiters.
    :type employee_id: int
    :param employee_update: Die aktualisierten Mitarbeitersdaten.
    :type employee_update: EmployeeCreate
    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param token: Das OAuth2-Token zur Authentifizierung.
    :type token: str
    :return: Die aktualisierten Mitarbeitersdaten.
    :rtype: EmployeeCreate
    """
    updated_employee = update_employee(db=db, employee_id=employee_id, employee_update=employee_update)
    if not updated_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated_employee

# Route zum Löschen eines Mitarbeiters anhand seiner ID
@router.delete("/{employee_id}", response_model=Employee, tags=["Employee"])
def delete_employee_by_id(employee_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Löscht einen Mitarbeiter anhand seiner ID.

    :param employee_id: Die ID des zu löschenden Mitarbeiters.
    :type employee_id: int
    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param token: Das OAuth2-Token zur Authentifizierung.
    :type token: str
    :return: Die gelöschten Mitarbeitersdaten.
    :rtype: Employee
    """
    deleted_employee = delete_employee(db=db, employee_id=employee_id)
    if not deleted_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return deleted_employee
