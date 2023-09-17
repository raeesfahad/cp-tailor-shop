from fastapi import APIRouter, HTTPException, Depends
from database.models import *
from database.connection import get_session
from sqlmodel import Session, select


router = APIRouter(
    prefix="/api/customer",
    tags=["customer"])




@router.post("/create", response_model=CustomerRead)
async def create(*, customer:CustomerBase , session : Session = Depends(get_session)):
    db_customer = Customer.from_orm(customer)
    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)
    return db_customer



@router.get("/get/all", response_model=list[CustomerRead])
async def read_customers(*, session : Session = Depends(get_session)):
    statment = select(Customer)
    results = session.exec(statment)
    return results.all()



@router.get("/{id}" , response_model=CustomerReadWithProducts)
async def read_single_customer(*, id : int, session : Session = Depends(get_session)):
    customer = session.exec(select(Customer).where(Customer.id == id))
    return customer.first()



@router.patch("/update/{id}", response_model=CustomerRead)
async def update_customer(*, id : int, customer : CustomerUpdate, session : Session = Depends(get_session)):
    db_customer = session.get(Customer, id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Order not Found")
    customer = customer.dict(exclude_unset=True)
    for key, value in customer.items():
        setattr(db_customer, key, value)
    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)
    return db_customer




@router.delete("/delete/{id}")
async def delete_customer(*, id: int, session : Session = Depends(get_session)):
    customer = session.get(Customer, id)
    if not customer:
        raise HTTPException(status_code=404, detail="Order Not Found")
    session.delete(customer)
    session.commit()
    return {"deleted": customer.first_name}
