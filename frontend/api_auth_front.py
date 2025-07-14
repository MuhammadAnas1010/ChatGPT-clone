import requests
from fastapi import FastAPI
import streamlit as st

def verify_login(email:str,password:str):
    data={
        'email':email,
        'password':password
    }
    response=requests.post(url='http://127.0.0.1:8001/login',json=data)
    if response.status_code == 200:
        try:
            res_json = response.json()
            return res_json
        except Exception as e:
            print("Error parsing JSON:", e)
            return res_json
    else:
        try:
            error_json = response.json()
            return error_json
        except:
            print("Login failed. Server returned:", response.text)
            return 
def register_user(name:str,email:str,password:str):
    data={
        'name':name,
        'email':email,
        'password':password
    }
    response=requests.post(url='http://127.0.0.1:8001/register',json=data)
    if response.status_code==200:
        try:
            res_json = response.json()
            # print('ID:', res_json.get('user_id'))
            # print('Name:', res_json.get('name'))  # Only if you're sending `name`
            # print('Email:', res_json.get('email'))
            return 1
        except Exception as e:
            print("Error parsing JSON:", e)
            return 0
    else:
        try:
            error_json = response.json()
            print("Error:", error_json.get("reason", "User not found"))
        except:
            print("Login failed. Server returned:", response.text)
        return 0

def add_redis(chat_id:int,data:dict):
    header = {'Authorization': f"Bearer {st.session_state['token']}"}
    response = requests.post(url=f"http://127.0.0.1:8000/chat/{chat_id}/message", headers=header,json=data)
    if response.status_code==200:
        print('success')
        return True

def push_data_db_from_redis(chat_id:int):
    print(f"Making request to: http://127.0.0.1:8000/chat/{chat_id}/message/push")
    header = {'Authorization': f"Bearer {st.session_state['token']}"}
    response = requests.post(url=f"http://127.0.0.1:8000/chat/{chat_id}/message/push", headers=header)
    print(f"Status code: {response.status_code}")
    print(f"Response text: {response.text}")
    if response.status_code == 200:
        print('success1234')
        return True
    else:
        print('Request failed')
        return False
def retrive_data_from_redis_from_db():
    header = {'Authorization': f"Bearer {st.session_state['token']}"}
    response= requests.get(f"http://127.0.0.1:8000/previous_chatid", headers=header)
    print(response.text)
    try:
        if response.status_code==200:
            return response.json()
        else:
            return {"status":'Failed'}
    except Exception as e:
        return e
    

def fetch_chat_messages(chat_id: int):
    header = {'Authorization': f"Bearer {st.session_state['token']}"}
    response = requests.get(f"http://127.0.0.1:8000/previous_chat?chat_id={chat_id}", headers=header)
    print(f"Fetching messages for chat_id: {chat_id}")
    print(f"Response status: {response.status_code}")
    print(f"Response text: {response.text}")
    try:
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": 'Failed', "error": f"HTTP {response.status_code}"}
    except Exception as e:
        print(f"Exception in fetch_chat_messages: {e}")
        return {"status": 'Failed', "error": str(e)}



#print(verify_login('john.doe@example.com','password123'))
def load_user_chats():
    """Load user's chats from database"""
    if not st.session_state.get('token'):
        return False
    
    try:
        # Get user's chat IDs
        chat_data = retrive_data_from_redis_from_db()
        print(f"Chat data received: {chat_data}")
        
        if chat_data and chat_data.get('status') == 'success':
            chat_list = chat_data.get('chat_id', [])
            print(f"Processing {len(chat_list)} chats")
            
            # Clear existing chats
            st.session_state['user_chats'] = {}
            
            # Load each chat with its messages
            for chat_info in chat_list:
                chat_id = str(chat_info['chat_id'])
                print(f"Loading chat {chat_id}")
                
                # Fetch messages for this chat
                messages_data = fetch_chat_messages(chat_info['chat_id'])
                messages = []
                
                if messages_data and messages_data.get('status') == 'success':
                    message_list = messages_data.get('chat_id', [])
                    messages = [{'role': msg['sender'], 'content': msg['content']} for msg in message_list]
                    print(f"Loaded {len(messages)} messages for chat {chat_id}")
                else:
                    print(f"No messages or failed to load messages for chat {chat_id}: {messages_data}")
                
                # Store chat in session state (even if no messages)
                st.session_state['user_chats'][chat_id] = {
                    'name': chat_info.get('title', f'Chat {chat_id[:8]}'),
                    'created_at': chat_info.get('created', 'Unknown'),
                    'messages': messages,
                    'response_data': {}
                }
            
            print(f"Successfully loaded {len(st.session_state['user_chats'])} chats")
            return True
        else:
            print(f"Failed to load chats: {chat_data}")
            return False
            
    except Exception as e:
        print(f"Error loading chats: {e}")
        import traceback
        traceback.print_exc()
        return False