from sqlalchemy.orm import Session

from ATL.models.order import Order
from ATL.schemas.order import OrderCreate
from ATL.models.orderPrograms import OrderPrograms

def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Order).offset(skip).limit(limit).all()


def create_order(db: Session, order: OrderCreate, customer_id: int, employee_id: int ):
    db_order = Order(id=order.id, title=order.title, hardware=order.hardware, details=order.details, customer_id=customer_id, employee_id=employee_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order(db: Session, order_id: int, order_update: OrderCreate):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        return None
    for attr, value in order_update.dict().items():
        setattr(db_order, attr, value)
    db.commit()
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        return None
    db.delete(db_order)
    db.commit()
    
    return db_order

def add_program_to_order(db: Session, order_id: int, program_id: int):
    # Überprüfen, ob die Bestellung und das Programm vorhanden sind
    order_program = OrderPrograms(order_id=order_id, program_id=program_id)
    db.add(order_program)
    db.commit()
    db.refresh(order_program)
    return order_program