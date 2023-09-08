from fastapi import APIRouter
from ATL.schemas.employee import Employee, EmployeeCreate
#from ATL.schemas.posts import Post, PostCreate
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from ATL.dependencies import get_db
from ATL.services.employee import (
    get_employee_by_name,
    create_employee as create_employee_service,
    get_employee, get_employees
)
#from ATL.services.posts import create_user_post

router = APIRouter(prefix="/employee")


"""@router.post("/", response_model=Employee)
def create_employee( employee: EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = get_employee(db, employee.id)
    if db_employee:
        raise HTTPException(status_code=400, detail="Employee already registered")
    return create_employee_service(db=db, employee=employee)"""


@router.get("/", response_model=list[Employee])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    employees = get_employees(db, skip=skip, limit=limit)
    return employees


@router.get("/{employee_id}", response_model=Employee)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee