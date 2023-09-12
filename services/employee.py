from sqlalchemy.orm import Session

from ATL.models.employee import Employee
from ATL.schemas.employee import EmployeeCreate, Employee_order


def get_employee(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.id == employee_id).first()

def get_employee_order(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.id == employee_id).first()


def get_employee_by_name(db: Session, name: str):
    return db.query(Employee).filter(Employee.name == name).first()


def get_employees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Employee).offset(skip).limit(limit).all()


def create_employee(db: Session, employee: EmployeeCreate, customer_id: int):
    db_employee = Employee(id=employee.id, first_name=employee.first_name, last_name=employee.last_name, email=employee.email, tel=employee.tel, customer_id=customer_id)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def update_employee(db: Session, employee_id: int, employee_update: EmployeeCreate):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        return None
    for attr, value in employee_update.dict().items():
        setattr(db_employee, attr, value)
    db.commit()
    return db_employee

def delete_employee(db: Session, employee_id: int):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        return None
    db.delete(db_employee)
    db.commit()
    
    return db_employee

