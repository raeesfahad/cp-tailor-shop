from sqlmodel import Session, select
from api import product,customer,users
from fastapi import FastAPI,Depends
from database.connection import create_database_and_models, get_session
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.sql import func

from database.models import Customer, Product


app = FastAPI()

origins = ["http://localhost", "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)



app.include_router(product.router)
app.include_router(customer.router)
app.include_router(users.router)




@app.on_event("startup")
def on_startup():
    print("INFO : connecting to data source...")
    create_database_and_models()
    print("INFO : connected")


@app.get("/stats")
def return_stats(session : Session = Depends(get_session), user = Depends(users.manager)):
     statment = select(Product)
     orders = session.exec(statment)
     total_orders = len(orders.all())
     #customers
     select_customers = select(Customer)
     customers = session.exec(select_customers)
     total_customers = len(customers.all())
     #completed orders

     completed_orders = session.exec(select(Product).where(Product.completed == True)).all()
     get_value = session.query(func.sum(Product.price))
     total_balance = get_value.scalar()
   

     return {

          "orders_total" : total_orders,
          "customers_total" : total_customers,
          "completed_orders" : len(completed_orders),
          "total_balance" : total_balance

     }
