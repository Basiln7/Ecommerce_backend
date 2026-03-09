from pydantic import BaseModel

class Login(BaseModel):
    email:str
    password:str

class UserOut(BaseModel):
    id: int
    name: str
    email:str
    password:str
    img_path:str
    is_verify:bool
    
    class Config:
        from_attributes=True