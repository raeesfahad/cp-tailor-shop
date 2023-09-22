from fastapi import APIRouter, HTTPException, Depends
from database.models import *
from database.connection import get_session
from sqlmodel import Session, select


router = APIRouter(
    prefix="/api/order",
    tags=["orders"])



@router.post("/create", response_model=ProductRead)
async def create(*, product:ProductBase, session : Session = Depends(get_session)):
    db_product = Product.from_orm(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product



@router.get("/get/all", response_model=list[ProductRead])
async def read_products(*, session : Session = Depends(get_session)):
    statment = select(Product)
    results = session.exec(statment)
    return results.all()





@router.get("/get/{id}", response_model=ProductReadWithCustomer)
async def read_order_single(*, id : int, session : Session = Depends(get_session)):
    order = session.exec(select(Product).where(Product.id == id))
    return order.first()



@router.patch("/update/{id}", response_model=ProductRead)
async def update_order(*, id : int, product : ProductUpdate, session : Session = Depends(get_session)):
    db_product = session.get(Product, id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Order not found")
    product_data = product.dict(exclude_unset=True)
    for key, value in product_data.items():
        setattr(db_product, key, value)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product
    


@router.delete("/delete/{id}")
async def delete_order(*, id: int, session : Session = Depends(get_session)):
    product = session.get(Product, id)
    if not product:
            raise HTTPException(status_code=404, detail="Order Not Found")
    session.delete(product)
    session.commit()
    return {"deleted": product.product_type}



     
