from pydantic import BaseModel,EmailStr,Field,field_validator
from typing import Annotated,Literal

class Loginrequest(BaseModel):
    email: Annotated[str,Field(...,description='Email of user')]
    password: Annotated[str,Field(...,description='Password of user')]

    @field_validator('email')
    @classmethod
    def lower_email(cls,email):
        return email.lower()
    
class loginresponse(BaseModel):
    status:Literal['success']
    token:str

class errorresponse(BaseModel):
    status:Literal['failed']
    reason: str

class registerrequest(BaseModel):
    name:str=Field(...,description="Name of User")
    email:EmailStr=Field(...,description='Unique Email of user')
    password:str=Field(...,description='User\'s new password')

class registerresponse(BaseModel):
    status:str=Literal['success']
    reason:str
    name:str
class registerresponse_error(BaseModel):
    status:str=Literal['failed','fail']
    reason:str