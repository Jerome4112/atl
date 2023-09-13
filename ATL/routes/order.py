from fastapi import APIRouter
from ATL.schemas.order import Order, OrderCreate
#from ATL.schemas.posts import Post, PostCreate
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from ATL.dependencies import get_db
from ATL.services.order import (
    create_order as create_order_service,
    get_order, get_orders, update_order, delete_order,add_program
)


router = APIRouter(prefix="/order")

@router.get("/", response_model=list[Order], tags=["Order"])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = get_orders(db, skip=skip, limit=limit)
    return orders


@router.get("/{order_id}", response_model=Order, tags=["Order"])
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.post("/{customer_id},{employee_id}", response_model=Order, tags=["Order"])
def create_order(customer_id: int, employee_id: int, order: OrderCreate, db: Session = Depends(get_db)):
    db_order = get_order(db, order.id)
    if db_order:
        raise HTTPException(status_code=400, detail="Order already registered")
    return create_order_service(db=db, order=order, customer_id=customer_id, employee_id=employee_id)

@router.put("/{order_id}", response_model=OrderCreate, tags=["Order"])
def update_order_by_id(order_id: int,order_update: OrderCreate, db: Session = Depends(get_db)):
    updated_order = update_order(db=db, order_id=order_id, order_update=order_update)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

@router.delete("/{order_id}", response_model=Order, tags=["Order"])
def delete_order_by_id(order_id: int, db: Session = Depends(get_db)):
    deleted_order = delete_order(db=db, order_id=order_id)
    if not deleted_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return deleted_order

@router.post("/add_program", tags=["Order"])
def add_program_to_order(order_id: int, program_id: int, db: Session = Depends(get_db)):
    order_program = add_program(db, order_id, program_id)
    if not order_program:
        raise HTTPException(status_code=404, detail="Order or Program not found")
    return {"message": "Program added to order successfully"}


