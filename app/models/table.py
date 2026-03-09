from sqlalchemy import Integer,String,ForeignKey,Boolean
from sqlalchemy.orm import mapped_column,relationship
from app.db.base import Base

class User(Base):
    __tablename__="users"
    id = mapped_column(Integer,primary_key=True,index=True)
    name=mapped_column(String,nullable=False)
    email=mapped_column(String,index=True,unique=True,nullable=False)
    password=mapped_column(String,nullable=False)
    img_path=mapped_column(String,nullable=False)
    role=mapped_column(String,default="user")
    is_verify=mapped_column(Boolean,default=False,nullable=False)

    cart=relationship("Cart",back_populates="user")


class Products(Base):
    __tablename__="products"

    id=mapped_column(Integer,primary_key=True,index=True)
    product_name=mapped_column(String,nullable=False,unique=True,index=True)
    price=mapped_column(Integer,nullable=False)
    product_img=mapped_column(String,nullable=False)

    cart1=relationship("Cart",back_populates="product")

class Cart(Base):

    __tablename__="carts"
    id=mapped_column(Integer,primary_key=True,index=True)
    user_id=mapped_column(Integer,ForeignKey("users.id"))
    product_id=mapped_column(Integer,ForeignKey("products.id"))
    quantity=mapped_column(Integer,nullable=False)

    user=relationship("User",back_populates="cart")
    product=relationship("Products",back_populates="cart1")
