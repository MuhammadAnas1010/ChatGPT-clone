import bcrypt
from db.connection import get_db_connection
async def add_chat(user_id: int, title:str):
    pool = await get_db_connection()

    try:
        async with pool.acquire() as conn:
            # exist = await conn.fetchrow('SELECT id FROM users WHERE email=$1', email)
            # if exist is not None:
            #     return {'status': 'Failed', 'reason': 'User Already exists'}

            # hashed_password = hash_password(password)
            result = await conn.fetchrow(
                "INSERT INTO chat (user_id, title) VALUES ($1, $2) RETURNING chat_id",
                user_id, title)
            return result


            #return 1
            #return {'status': 'success', 'reason': 'User added successfully', 'name': user_id}

    except Exception as e:
        print("Database error:", e)
        return {"status": "failed", "reason": "Internal error"}
    
async def add_from_redis_to_db(messages:list,chat_id:int):
    pool = await get_db_connection()

    try:
        async with pool.acquire() as conn:
            for msg in messages:
                sender=msg.get("sender")
                content=msg.get("content")
                await conn.fetchrow(
                    "INSERT INTO messages (chat_id, sender,content) VALUES ($1, $2, $3)",
                    chat_id, sender,content)
            print("hell yes")
            return {'status':"success"}

    except Exception as e:
        print("Database error:", e)
        return {"status": "failed", "reason": e}
async def get_previous_chat_id(user_id:int):
    pool = await get_db_connection()

    try:
        async with pool.acquire() as conn:
            result = await conn.fetch(
                    "select chat_id, title, created_at from chat where user_id = $1",
                    user_id)
            return result
            

    except Exception as e:
        print("Database error:", e)
        return {"status": "failed", "reason": e}
async def get_previous_chat_from_chat_id(chat_id:int):
    pool=await get_db_connection()

    try:
        async with pool.acquire() as conn:
            print(chat_id)
            result=await conn.fetch(
                  "select sender, content, created_at from messages where chat_id =$1",
                    chat_id)
            print(result)
            return result
    except Exception as e:
        print("Database error:", e)
        return {"status": "failed", "reason": e}