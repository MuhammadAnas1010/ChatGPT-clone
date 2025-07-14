from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv
import jwt


load_dotenv()
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='token')

secret=os.getenv('secret_key')

def get_current_user(token: str =Depends(oauth2_scheme)):
    
    try:
        result=jwt.decode(token,secret,algorithms=['HS256'])
        user_id = result.get('user_id')
        if not user_id:
            raise HTTPException(status_code=402,detail="user not found")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")