from typing import Optional,List
from sqlmodel import Field, SQLModel, create_engine, Relationship


 
 


class Product(SQLModel, table=True):
   id: Optional[int] = Field(default=None, primary_key=True)
   product_type : str
   date_of_order : str
   date_of_return : str
   charges : str
   is_order_completed : bool
  

   
class Customer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name : str
    last_name: str
    mobile_number : Optional[int] = None
    order : Optional[int] = Field( default=None, foreign_key="product.id")
   
   
   
