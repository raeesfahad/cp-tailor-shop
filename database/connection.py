from sqlmodel import create_engine,SQLModel
from database import tables


class SQLite:

  
  def __init__(self):
       
       self.engine = None
       self.connected = False
  
  def connect(self):
      
     url = f"sqlite:///db_file"
     self.engine = create_engine(url)
     SQLModel.metadata.create_all(self.engine)
     self.connected = True
