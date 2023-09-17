from api import product,customer,users
from fastapi import FastAPI,Depends
from database.connection import create_database_and_models


app = FastAPI()

app.include_router(product.router)
app.include_router(customer.router)
app.include_router(users.router)




@app.on_event("startup")
def on_startup():
    print("INFO : connecting to data source...")
    create_database_and_models()
    print("INFO : connected")



@app.get("/admin")
def index(user = Depends(users.manager)):
    return "comming soon, stay tuned"
