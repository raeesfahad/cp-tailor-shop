from typing import Optional,List
from datetime import datetime
from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel, create_engine, Relationship



class CustomerBase(SQLModel):
    first_name : str
    last_name: str
    mobile_number : Optional[str] = None
    measurments : dict = Field(sa_column=Column(JSON), default={})




class Customer(CustomerBase, table=True):
   id: Optional[int] = Field(default=None, primary_key=True)
   product : List["Product"] = Relationship(back_populates="customer")


class CustomerRead(CustomerBase):
   id : int

class CustomerCreate(CustomerBase):
   pass

class CustomerUpdate(SQLModel):
    first_name : Optional[str] = None
    last_name: Optional[str] = None
    mobile_number : Optional[str] = None
    measurments : dict = Field(sa_column=Column(JSON), default={})



class ProductBase(SQLModel):
    suit_type : str = Field(index=True)
    color_choice: str
    delivery_date: datetime
    date_of_order : datetime = datetime.now()
    urgent_order: bool
    price: float
    completed: bool = False
    customer_id : Optional[int] = Field(default=None, foreign_key="customer.id")


class Product(ProductBase, table=True):
   id: Optional[int] = Field(default=None, primary_key=True)
   customer : Optional["Customer"] = Relationship(back_populates="product")



class ProductCreate(ProductBase):
   pass


class ProductRead(ProductBase):
   id : int


class ProductUpdate(SQLModel):

    suit_type : Optional[str] = None
    color_choice: Optional[str] = None
    delivery_date: Optional[datetime] = None
    date_of_order : Optional[datetime] = datetime.now()
    urgent_order: Optional[bool] = False
    price: Optional[float] = None
    completed: bool = False
    customer_id : Optional[int] = Field(default=None, foreign_key="customer.id")


class ProductReadWithCustomer(ProductRead):
    customer: Optional[CustomerRead] = None


class CustomerReadWithProducts(CustomerRead):
    product: List[ProductRead] = []



class UserBase(SQLModel):
   first_name : str
   last_name : str
   email : str
   joined : datetime = datetime.now()

class User(UserBase, table=True):
   id: Optional[int] = Field(default=None, primary_key=True)
   password : str
   password_again : str


class UserCreate(UserBase):
   password : str
   password_again : str

class UserRead(UserBase):
   id : int



class UserUpdate(SQLModel):
   first_name : Optional[str] = None
   last_name : Optional[str] = None
   joined : Optional[datetime] = datetime.now()
   password : Optional[str] = None
   password_again : Optional[str] = None








