from pydantic import BaseModel

class ProdectOut(BaseModel):
    id:int
    product_name:str
    price:int
    product_img:str

    class Config:
        from_attributes=True

class UpdateProduct(BaseModel):
    product_name:str
    price:int

class CartAdd(BaseModel):
    product_id:int
    quantity:int

class CartOut(BaseModel):
    id:int
    product_name:str
    price:int
    quantity:int
    totel_price:float

    class Config:
        from_attributes=True