from typing import Optional
from pydantic import BaseModel,EmailStr,Field

class UserSchema(BaseModel):
    fullname:str=Field(...,min_length=1, max_length=50)
    email:EmailStr=Field(...)
    password:str=Field(...,min_length=4, max_length=10)

    class Config:
     schema_extra = {
        "example": {
            "fullname": "Mayank Kumar Singh",
            "email": "mayank@example.com",
            "password": "pass1234"
        }
    }

class UserModel(BaseModel):
    fullname:Optional[str]
    email:Optional[EmailStr]
    password:Optional[str]

    class Config:
     schema_extra = {
        "example": {
            "fullname": "Mayank Kumar Singh",
            "email": "mayank@example.com",
            "password": "pass12344"
        }
    }

