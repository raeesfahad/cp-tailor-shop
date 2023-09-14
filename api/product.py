from fastapi import APIRouter, HTTPException
from database.tables import *
from database.schemas import *
from database.connection import SQLite
from sqlmodel import Session, select

db = SQLite()
db.connect()

router = APIRouter(
    prefix="/api/products",
    tags=["orders"])


@router.get("/all")
async def read_products():
    if db.connected:
        with Session(db.engine) as session:
            statment = select(Product)
            results = session.exec(statment)
            return results.all()
    raise HTTPException(status_code=503, detail="error happend, cannot fetch data")


@router.post("/create")
async def create(product:Product):
    if db.connected:
        with Session(db.engine) as session:
            session.add(product)
            session.commit()
            session.refresh(product)
            return product
    raise HTTPException(status_code=503, detail="error happend, cannot fetch data")


@router.get("/single/{id}")
async def read_order_single(id : int):
    if db.connected:
        with Session(db.engine) as session:
           order = session.exec(select(Product).where(Product.id == id))
           return order.first()
    raise HTTPException(status_code=503, detail="error happend, cannot fetch data")


@router.patch("/update/{id}")
async def update_order(id : int, product : ProductCreate):
    if db.connected:
        with Session(db.engine) as session:
            db_product = session.get(Product, id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Order not Found")
        product_data = product_data.dict(exclude_unset=True)
        for key, value in product_data.items():
            setattr(db_product, key, value)
        session.add(db_product)
        session.commit()
        session.refresh(db_product)
        return db_product
    raise HTTPException(status_code=503, detail="error happend, cannot fetch data")
    


@router.delete("/delete/{id}")
async def delete_order(id: int):
    if db.connected:
        with Session(db.engine) as session:
            product = session.get(Product, id)
            if not product:
                raise HTTPException(status_code=404, detail="Order Not Found")
            session.delete(product)
            session.commit()
            return {"deleted": True}
    raise HTTPException(status_code=503, detail="error happend, cannot fetch data")
