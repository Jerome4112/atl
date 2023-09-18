from sqlalchemy.orm import Session

from ATL.models.employee import Employee
from ATL.schemas.employee import EmployeeCreate, Employee_order
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Funktion zur Abfrage eines Mitarbeiters anhand seiner ID
def get_employee(db: Session, employee_id: int):
    """
    Gibt die Daten eines Mitarbeiters anhand seiner ID zurück.

    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param employee_id: Die ID des Mitarbeiters.
    :type employee_id: int
    :return: Die Mitarbeiterdaten.
    :rtype: Employee
    """
    return db.query(Employee).filter(Employee.id == employee_id).first()

# Funktion zur Abfrage eines Mitarbeiters anhand seines Namens
def get_employee_by_name(db: Session, name: str):
    """
    Gibt die Daten eines Mitarbeiters anhand seines Namens zurück.

    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param name: Der Name des Mitarbeiters.
    :type name: str
    :return: Die Mitarbeiterdaten.
    :rtype: Employee
    """
    return db.query(Employee).filter(Employee.name == name).first()

# Funktion zur Abfrage eines Mitarbeiters anhand seiner ID
def get_employee_order(db: Session, employee_id: int):
    """
    Gibt die Bestelldaten eines Mitarbeiters anhand seiner ID zurück.

    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param employee_id: Die ID des Mitarbeiters.
    :type employee_id: int
    :return: Die Bestelldaten des Mitarbeiters.
    :rtype: Employee_order
    """
    return db.query(Employee_order).filter(Employee.id == employee_id).first()

# Funktion zur Abfrage aller Mitarbeiter mit optionaler Seitenbegrenzung
def get_employees(db: Session, skip: int = 0, limit: int = 100):
    """
    Gibt eine Liste von Mitarbeitern mit optionaler Seitenbegrenzung zurück.

    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param skip: Die Anzahl der Datensätze, die übersprungen werden sollen.
    :type skip: int
    :param limit: Die maximale Anzahl von Datensätzen, die zurückgegeben werden sollen.
    :type limit: int
    :return: Eine Liste von Mitarbeitern.
    :rtype: list[Employee]
    """
    return db.query(Employee).offset(skip).limit(limit).all()

# Funktion zur Erstellung eines neuen Mitarbeiters
def create_employee(db: Session, employee: EmployeeCreate, customer_id: int):
    """
    Erstellt einen neuen Mitarbeiter in der Datenbank.

    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param employee: Die Daten des neuen Mitarbeiters.
    :type employee: EmployeeCreate
    :param customer_id: Die ID des zugehörigen Kunden.
    :type customer_id: int
    :return: Die erstellten Mitarbeiterdaten.
    :rtype: Employee
    """
    db_employee = Employee(
        id=employee.id,
        first_name=employee.first_name,
        last_name=employee.last_name,
        email=employee.email,
        passwordEmail=employee.passwordEmail,
        tel=employee.tel,
        customer_id=customer_id
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

# Funktion zur Aktualisierung eines Mitarbeiters anhand seiner ID
def update_employee(db: Session, employee_id: int, employee_update: EmployeeCreate):
    """
    Aktualisiert die Mitarbeiterdaten anhand der Mitarbeiter-ID.

    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param employee_id: Die ID des Mitarbeiters, der aktualisiert werden soll.
    :type employee_id: int
    :param employee_update: Die aktualisierten Mitarbeiterdaten.
    :type employee_update: EmployeeCreate
    :return: Die aktualisierten Mitarbeiterdaten.
    :rtype: Employee
    """
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        return None
    for attr, value in employee_update.dict().items():
        setattr(db_employee, attr, value)
    db.commit()
    return db_employee

# Funktion zur Löschung eines Mitarbeiters anhand seiner ID
def delete_employee(db: Session, employee_id: int):
    """
    Löscht einen Mitarbeiter anhand seiner ID.

    :param db: Die Datenbank-Sitzung.
    :type db: Session
    :param employee_id: Die ID des zu löschenden Mitarbeiters.
    :type employee_id: int
    :return: Die gelöschten Mitarbeiterdaten.
    :rtype: Employee
    """
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        return None
    db.delete(db_employee)
    db.commit()
    return db_employee
