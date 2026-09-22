from pydantic import BaseModel

class ProductCreate(BaseModel):
    name:str
    price:float

class ProductUpdate(BaseModel):
    name:str
    price:float