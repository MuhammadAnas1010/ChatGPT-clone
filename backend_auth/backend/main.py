from backend.db.users import verify_user,register_user
#from backend.db.connection import get_db_connection
#from backend.auth.jwt_handler import access_jwt_token
from fastapi import FastAPI,status
from backend.auth.auth_utils import Loginrequest,loginresponse,errorresponse,registerrequest,registerresponse,registerresponse_error
from typing import Union
from fastapi.responses import JSONResponse



app=FastAPI()
@app.post('/login',response_model=Union[loginresponse,errorresponse])
async def check_validation(user: Loginrequest):
    result= await verify_user(user.email,user.password)
    print(result)
    if result.get('status')== 'success':
        return JSONResponse(
            #status_code=status.HTTP_401_UNAUTHORIZED,
            status_code=status.HTTP_200_OK,
            content={
                "status": result.get('status'),
                "token": result.get('token')
            }
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "status": "failed",
                "reason": result.get('reason')
            }
        )


@app.post('/register')
async def make_user(register:registerrequest):
    result=await register_user(register.name,register.email,register.password)
    if result.get('status')== 'success':
        return JSONResponse(
            #status_code=status.HTTP_401_UNAUTHORIZED,
            status_code=status.HTTP_200_OK,
            content={
                "status": "success",
                "reason": "registered"
            }
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "status": "failed",
                "reason": "not registered"
            }
        )
   


