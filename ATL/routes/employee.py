from fastapi import APIRouter
from ATL.schemas.employee import Employee, EmployeeCreate, Employee_order
#from ATL.schemas.posts import Post, PostCreate
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from ATL.dependencies import get_db
from ATL.services.employee import (
    create_employee as create_employee_service,
    get_employee, get_employees, update_employee, delete_employee, get_employee_order
)
#from ATL.services.posts import create_user_post

router = APIRouter(prefix="/employee")

@router.get("/", response_model=list[Employee], tags=["Employee"])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    employees = get_employees(db, skip=skip, limit=limit)
    return employees

"""""
@router.get("/{employee_id}", response_model=Employee, tags=["Employee"])
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee
"""
@router.post("/{customer_id}", response_model=Employee, tags=["Employee"])
def create_employee( customer_id: int,employee: EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = get_employee(db, employee.id)
    if db_employee:
        raise HTTPException(status_code=400, detail="Employee already registered")
    return create_employee_service(db=db, employee=employee, customer_id=customer_id)

@router.get("/{employee_id}", response_model=Employee_order, tags=["Employee"])
def read_order_by_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = get_employee_order(db, employee_id_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@router.put("/{employee_id}", response_model=EmployeeCreate, tags=["Employee"])
def update_employee_by_id(employee_id: int,employee_update: EmployeeCreate, db: Session = Depends(get_db)):
    updated_employee = update_employee(db=db, employee_id=employee_id, employee_update=employee_update)
    if not updated_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated_employee

@router.delete("/{employee_id}", response_model=Employee, tags=["Employee"])
def delete_employee_by_id(employee_id: int, db: Session = Depends(get_db)):
    deleted_employee = delete_employee(db=db, employee_id=employee_id)
    if not deleted_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return deleted_employee
