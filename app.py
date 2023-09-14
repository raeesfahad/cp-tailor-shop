from api import product
from fastapi import FastAPI


app = FastAPI()

app.include_router(product.router)


@app.get("/")
def index():
    return "Hello, World"

