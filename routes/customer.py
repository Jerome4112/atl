from fastapi import APIRouter
from ATL.schemas.customer import Customer, CustomerCreate
from ATL.schemas.employee import Employee, EmployeeCreate
#from ATL.schemas.posts import Post, PostCreate
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from ATL.dependencies import get_db
from ATL.services.customer import (
    get_customer_by_name,
    create_customer as create_customer_service,
    get_customer, get_customers
)
from ATL.services.employee import (
    create_employee as create_employee_service,
    get_employee
)
#from ATL.services.posts import create_user_post

router = APIRouter(prefix="/customer")


@router.post("/", response_model=Customer)
def create_customer( customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = get_customer_by_name(db, name=customer.name)
    if db_customer:
        raise HTTPException(status_code=400, detail="Name already registered")
    return create_customer_service(db=db, customer=customer)


@router.get("/", response_model=list[CustomerCreate])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customer = get_customers(db, skip=skip, limit=limit)
    return customer


@router.get("/{customer_id}", response_model=Customer)
def read_customer_workers(customer_id: int, db: Session = Depends(get_db)):
    db_customer = get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.post("/{customer_id}", response_model=Employee)
def create_employee( customer_id: int,employee: EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = get_employee(db, employee.id)
    if db_employee:
        raise HTTPException(status_code=400, detail="Employee already registered")
    return create_employee_service(db=db, employee=employee, customer_id=customer_id)

