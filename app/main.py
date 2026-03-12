from fastapi import FastAPI,Form,UploadFile,File,Depends,HTTPException
from sqlalchemy.orm import session
from jose import jwt,JWTError
from app.db.session import get_db
from app.models.table import User,Products,Cart
from app.schemas.auth  import Login,UserOut
from app.schemas.product import ProdectOut,UpdateProduct,CartAdd,CartOut
from app.core.security import create_access_token,verify_token,create_refresh_token,verify_refresh_token
from typing import List
from fastapi.staticfiles import StaticFiles
import os,random
from fastapi_mail import FastMail, MessageSchema, MessageType
from app.sevices.email_sevices import conf
UPLOAD_DIR="user_imgs"
os.makedirs(UPLOAD_DIR,exist_ok=True)

app=FastAPI()
app.mount("/user_img",StaticFiles(directory=UPLOAD_DIR),name="user_img")

@app.get("/")
def check():
    return {"sever":"run successfully"}
@app.post("/refresh")
def get_new_access_token(token:str,db:session=Depends(get_db)):
    create_token=verify_refresh_token(token)
    if not create_token:
        raise HTTPException(status_code=401,detail="invalid token")
    new_token=create_access_token({"sub":create_token["sub"]},db)
    return{"access_token":new_token,"token_type":"bearer"}
    
@app.post("/signup",tags=["auth"])
async def rejister(name:str=Form(...),
             email:str=Form(...),
             password:str=Form(...),
             img:UploadFile=File(...),
             db:session=Depends(get_db)):
    
    exisit=db.query(User).filter(User.email==email).first()
    if exisit:
        raise HTTPException(status_code=409,detail="user email allready exist")
    file_path=os.path.join("user_imgs",img.filename)
    with open(file_path,"wb")as f:
        f.write(await img.read())
    new_user=User(name=name,email=email,password=password,img_path=f"/user_img/{img.filename}",role="user")
    db.add(new_user)
    db.commit()
    return{"sidnup":"compleated"}
verift_otp={}
@app.post("/email_otp",tags=["auth"])
async def email_otp(email:str,db:session=Depends(get_db)):
    exist=db.query(User).filter(email==User.email).first()
    if not exist:
        raise HTTPException(status_code=409,detail="this email did not signup")
    otp=random.randint(100000,999999)
    verift_otp[email]=otp
    message=MessageSchema(
        subject="Your verication OTP",
        recipients=[email],
        body=f"<h2>Your OTP is: {otp}</h2>",
        subtype=MessageType.html
    )
    fm=FastMail(conf)
    await fm.send_message(message)
    exist.is_verify=True
    db.commit()
    return{"otp":"send successfully",
           "otp":otp}
@app.post("/verify_otp",tags=["auth"])
def verify_otp(email:str,otp:int):
    if email not in verift_otp:
        raise HTTPException(status_code=409,detail="email did not send otp")
    if verift_otp[email]!=otp:
        raise HTTPException(status_code=401,detail="wrong otp ")
    return{"email_otp":"successfull"}
@app.post("/login",tags=["auth"])
def login(data:Login,db:session=Depends(get_db)):
    user=db.query(User).filter(User.email==data.email).first()
    if not user:
        raise HTTPException(status_code=401,detail="email not  founr")
    if data.password!=user.password:
        raise HTTPException(status_code=401,detail="wrong password")
    token=create_access_token({"sub":data.email},db)
    refresh_token=create_refresh_token({"sub":data.email},db)
    return{"token":token,
           "refresh_token":refresh_token,
           "token_type":"bearer"}

@app.get("/view_users",response_model=List[UserOut],tags=["auth"])
def view_users(db:session=Depends(get_db)):
    users=db.query(User).all()
    return users
UPLOAD_DIR1="product_img"
os.makedirs(UPLOAD_DIR1,exist_ok=True)
app.mount("/product_img",StaticFiles(directory=UPLOAD_DIR1),name="product_img")
@app.post("/add_product",tags=["product"])
async def add_product(name:str=Form(...),
                price:int=Form(...),
                p_img:UploadFile=File(...),
                db:session=Depends(get_db),
                token:dict=Depends(verify_token)):
    product=db.query(Products).filter(name==Products.product_name).first()
    if product:
        raise HTTPException(status_code=401,detail="product already exist")
    file_path=os.path.join("product_img",p_img.filename)
    with open(file_path,"wb")as f:
        f.write(await p_img.read())
    new_product=Products(product_name=name,price=price,product_img=file_path)
    db.add(new_product)
    db.commit()
    return{"product":"added succesfully"}
    
@app.put("/update_product",tags=["product"])
def update_product(data:UpdateProduct,db:session=Depends(get_db),token:dict=Depends(verify_token)):
    product=db.query(Products).filter(data.product_name==Products.product_name).first()
    if not product:
        raise HTTPException(status_code=401,detail="product not found")
    product.price=data.price
    db.commit()
    return{"product":"updation success"}
@app.get("/view_product",response_model=List[ProdectOut],tags=["product"])
def view_product(db:session=Depends(get_db),token:dict=Depends(verify_token)):
    products=db.query(Products).all()
    return products
@app.delete("/delete_product",tags=["product"])
def delete_product(name:str,db:session=Depends(get_db),token:dict=Depends(verify_token)):
    product=db.query(Products).filter(name==Products.product_name).first()
    if not product:
        raise HTTPException(status_code=409,detail="product not found")
    db.delete(product)
    db.commit()
    return {"product":"deleted successfull"}


@app.post("/add_cart",tags=["cart"])
def add_cart(data:CartAdd,db:session=Depends(get_db),token:dict=Depends(verify_token)):
    user=db.query(User).filter(User.email==token["sub"]).first()
    product=db.query(Products).filter(data.product_id==Products.id).first()
    if not product:
        raise HTTPException(status_code=409,detail="product not found")
    if data.quantity <= 0:
        raise HTTPException(status_code=404,detail="quatity must be positive amount")
    new_item=Cart(user_id=user.id,product_id=data.product_id,quantity=data.quantity)
    db.add(new_item)
    db.commit()
    return {"cart":"product added successfully"}
@app.get("/view_cart",response_model=List[CartOut],tags=["cart"])
def view_cart(db:session=Depends(get_db),token:dict=Depends(verify_token)):
    user_cart=db.query(User).filter(User.email==token["sub"]).first()
    cart_data=(db.query(Cart.id ,Products.product_name,Products.price,Cart.quantity,(Products.price * Cart.quantity).label("totel_price"))
               .join(Products,Products.id==Cart.product_id)
               .filter(user_cart.id==Cart.user_id).all())
    return cart_data

@app.delete("/delete_cart",tags=["cart"])
def delete_cart(id:int,db:session=Depends(get_db),token:dict=Depends(verify_token)):
    item=db.query(Cart).filter(Cart.id==id).first()
    if not item:
        raise HTTPException(status_code=409,detail="product not found")
    db.delete(item)
    db.commit()
    return {"cart item":"deleted successfully"}