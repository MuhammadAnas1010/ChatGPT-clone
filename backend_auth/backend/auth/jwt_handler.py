import jwt
import os
from dotenv import load_dotenv
import bcrypt



def access_jwt_token(data: dict) -> str:
    try:
        load_dotenv()
        algorithm='HS256'
        secret=os.getenv('secret_key')
        encoded_jwt = jwt.encode(data, secret, algorithm=algorithm)

        # Handle different versions of PyJWT
        if isinstance(encoded_jwt, bytes):
            encoded_jwt = encoded_jwt.decode('utf-8')

        return encoded_jwt
    except Exception as e:
        print("JWT generation error:", e)
        raise




def hash_password(plain_password: str) -> str:
    # Convert string to bytes
    password_bytes = plain_password.encode('utf-8')
    # Generate salt and hash password
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    # Return hashed password as string to store in DB
    return hashed.decode('utf-8')
    