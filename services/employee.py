from sqlalchemy.orm import Session

from ATL.models.employee import Employee
from ATL.schemas.employee import EmployeeCreate


def get_employee(db: Session, employee_id: int):
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