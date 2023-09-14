
from typing import Optional
from . tables import Product
from sqlmodel import SQLModel


class ProductCreate(SQLModel):
     product_type : str
     date_of_order : str
     date_of_return : str
     charges : str
     is_order_completed : bool

class ProductRead(SQLModel):
     id: int
     product_type : str
     date_of_order : str
     date_of_return : str
     charges : str
     is_order_completed : bool