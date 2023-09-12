from sqlalchemy.orm import Session

from ATL.models.customer import Customer
from ATL.schemas.customer import CustomerCreate


def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()


def get_customer_by_name(db: Session, name: str):
    return db.query(Customer).filter(Customer.name == name).first()


def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Customer).offset(skip).limit(limit).all()


def create_customer(db: Session, customer: CustomerCreate):
    db_customer = Customer(name=customer.name, id=customer.id, adress=customer.adress, adressNr=customer.adressNr, email=customer.email, tel=customer.tel, city=customer.city, postalCode=customer.postalCode)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, customer_id: int, customer_update: CustomerCreate):
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not db_customer:
        return None
    for attr, value in customer_update.dict().items():
        setattr(db_customer, attr, value)
    db.commit()
    db.refresh(db_customer)
    
    return db_customer

def delete_customer(db: Session, customer_id: int):
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not db_customer:
        return None
    db.delete(db_customer)
    db.commit()
    
    return db_customer

