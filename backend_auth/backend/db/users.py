from backend.db.connection import get_db_connection
from backend.auth.jwt_handler import access_jwt_token, hash_password
import bcrypt

async def verify_user(email: str, password: str):
    pool = await get_db_connection()

    try:
        async with pool.acquire() as conn:
            result = await conn.fetchrow(
                'SELECT id, email, hased_password, name FROM users WHERE email=$1', email
            )

            if result is None:
                return {'status': 'failed', 'reason': 'user not found'}

            id, email, hased_password, name = result.values()

            if bcrypt.checkpw(password.encode('utf-8'), hased_password.encode('utf-8')):
                info = {'user_id': id, 'name': name, 'email': email}
                token = access_jwt_token(info)
                return {'status': 'success', 'token': token}
            else:
                return {'status': 'failed', 'reason': 'wrong password'}

    except Exception as e:
        print("Database error:", e)
        return {'status': 'failed', 'reason': 'Internal error'}

async def register_user(name: str, email: str, password: str):
    pool = await get_db_connection()

    try:
        async with pool.acquire() as conn:
            exist = await conn.fetchrow('SELECT id FROM users WHERE email=$1', email)
            if exist is not None:
                return {'status': 'Failed', 'reason': 'User Already exists'}

            hashed_password = hash_password(password)
            await conn.execute(
                "INSERT INTO users (name, email, hased_password) VALUES ($1, $2, $3)",
                name, email, hashed_password
            )

            return {'status': 'success', 'reason': 'User added successfully', 'name': name}

    except Exception as e:
        print("Database error:", e)
        return {"status": "failed", "reason": "Internal error"}
