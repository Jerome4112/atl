from fastapi import FastAPI

from ATL.models import customer as customer_schema
from ATL.models import employee as employee_schema
from ATL.models import order as order_schema
from ATL.database import engine
from ATL.routes import customer, employee, order

customer_schema.Customer.metadata.create_all(bind=engine)
employee_schema.Employee.metadata.create_all(bind=engine)
order_schema.Order.metadata.create_all(bind=engine)
#post.Post.metadata.create_all(bind=engine)
#comment.Comment.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(customer.router)
app.include_router(employee.router)
app.include_router(order.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

#poetry run uvicorn ATL.main:app --reload