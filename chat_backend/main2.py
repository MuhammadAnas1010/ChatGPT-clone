from fastapi import FastAPI,status,Depends
from fastapi.responses import JSONResponse
from auth.user_auth import get_current_user
from auth.auth_utilis import new_chat_redis
from db.store_data import add_chat,add_from_redis_to_db,get_previous_chat_id,get_previous_chat_from_chat_id
import redis
import json
redis_client = redis.Redis(host='localhost', port=6379, db=0)


app=FastAPI()

@app.post('/chat/new')
async def make_chatid(user_id:int = Depends(get_current_user)):
    if user_id:
        try:
            result=await add_chat(user_id,title="New chat")
            print(result['chat_id'])
            if result:
                return {'status': 'success', 'reason': 'User added successfully', 'chat_id': result['chat_id']}
        except:
            return {"status":"Can't create chat (meri marzi)"}
    else:
        return {'Status':'User not found'}    
 
@app.get('/previous_chatid')
async def get_user_previous_chatid(user_id:int=Depends(get_current_user)):
    if user_id:
        try:
            result=await get_previous_chat_id(user_id)
            chat_list = [
            {'chat_id': record['chat_id'], 'title': record['title'],'created':record['created_at']}  for record in result]
            print(chat_list)
            if result:
                return {'status': 'success', 'reason': 'chat_id retrived successfully', 'chat_id': chat_list}
        except:
            return {"status":"Can't create chat (meri marziii)"}
    else:
        return {'Status':'User not found'}

@app.get("/previous_chat")
async def previous_chat_of_chat_id(chat_id:int,user_id=Depends(get_current_user)):
    if chat_id and user_id:
        try:
            records =await get_previous_chat_from_chat_id(chat_id)
            chat_list = [
            {'sender': record['sender'], 'content': record['content']}  for record in records]
            print("fuck",chat_list)
            if records:
                return {'status': 'success', 'reason': 'chat_id retrived successfully', 'chat_id': chat_list}
        except:
            return {"status":"Can't create chat (meri marziii)"}
    else:
        return {'Status':'User not found'}


# print(r.ping())  # True

# #r.set('foo', 'bar')
# #r.expire('foo', 10)


@app.post('/chat/{chat_id}/message')
async def store_in_redis(chat_id:int,data:new_chat_redis,user_id:int=Depends(get_current_user)):
    if user_id:
        redis_client.rpush(f"chat:{chat_id}:message", data.model_dump_json())
        #print(redis_client.lrange(f'chat:{chat_id}:message', 0, -1))
        #print('success1')
        return {'status':"Successfull"}

@app.post('/chat/{chat_id}/message/push')
async def Push_to_db_from_redis_messages(chat_id:int,user_id:int=Depends(get_current_user)):
    if user_id:
        try:
            redis_messages=redis_client.lrange(f"chat:{chat_id}:message",0,-1)
            #print(f"Redis messages retrieved: {redis_messages}")
            final_messages=[]
            for msg in redis_messages:
                final_messages.append(json.loads(msg.decode("utf-8")))
                print(final_messages)
            result=await add_from_redis_to_db(final_messages,chat_id)
            if result["status"]=="success":
                redis_client.delete(f"chat:{chat_id}:message")
                print('yes')
                return {'status':"Successfull"}
        except Exception as e:
            print("error:",e)
            return {'status':"failed"}
       
