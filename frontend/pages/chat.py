import streamlit as st
from openai import OpenAI
from api_auth_front import add_redis,push_data_db_from_redis,load_user_chats
import os
from dotenv import load_dotenv
load_dotenv()

secret_key=os.getenv('api_key')
# chat.py
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=secret_key,
)


def model_response(prompt):
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            extra_body={
                'temperature': 0.5,
                'stream': False
            },
            messages=prompt
        )
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        return f"Error: {str(e)}"

# Check authentication first
if not st.session_state.get("is_authenticated"):
    st.warning("You must login first.")
    st.stop()

# Initialize chat system if not exists
if 'user_chats' not in st.session_state:
    st.session_state['user_chats'] = {}
if 'active_chat_id' not in st.session_state:
    st.session_state['active_chat_id'] = None
if 'chats_loaded' not in st.session_state:
    st.session_state['chats_loaded'] = False

# Load chats from database when user first arrives (only once per session)
if not st.session_state['chats_loaded']:
    with st.spinner("Loading your chats..."):
        if load_user_chats():
            st.session_state['chats_loaded'] = True
        else:
            st.session_state['chats_loaded'] = True

# Always show sidebar
st.sidebar.title("💬 Your Chats")

# Debug info in sidebar
st.sidebar.write(f"Total chats: {len(st.session_state['user_chats'])}")

if st.session_state['user_chats']:
    # Show all chats
    for chat_id, chat_data in st.session_state['user_chats'].items():
        chat_name = chat_data.get('name', f'Chat {str(chat_id)[:8]}')
        created_time = chat_data.get('created_at', 'Unknown')
        
        # Show ALL chats as buttons (not just inactive ones)
        if str(chat_id) == str(st.session_state.get('active_chat_id')):
            # Active chat - show as highlighted button
            if st.sidebar.button(f"🔥 {chat_name} (Active)", key=f"active_chat_{chat_id}", type="primary"):
                # Already active, no need to change
                pass
        else:
            # Inactive chat - show as regular button
            if st.sidebar.button(f"📝 {chat_name}", key=f"select_chat_{chat_id}"):
                st.session_state['active_chat_id'] = str(chat_id)
                st.rerun()
    
    st.sidebar.markdown("---")
    
    # Option to create new chat
    if st.sidebar.button("➕ Create New Chat"):
        st.sidebar.info("Go to the home page to create a new chat!")
        
    # Option to delete current chat
    if st.session_state.get('active_chat_id'):
        if st.sidebar.button("🗑️ Delete Current Chat", type="secondary"):
            if str(st.session_state['active_chat_id']) in st.session_state['user_chats']:
                # Push data to database before deleting
                try:
                    push_data_db_from_redis(int(st.session_state['active_chat_id']))
                except:
                    pass
                
                del st.session_state['user_chats'][str(st.session_state['active_chat_id'])]
                st.session_state['active_chat_id'] = None
                st.success("Chat deleted!")
                st.rerun()
    
    # Add refresh button
    if st.sidebar.button("🔄 Refresh Chats"):
        st.session_state['chats_loaded'] = False
        st.rerun()
else:
    st.sidebar.info("No chats yet. Create one from the home page!")

# Main chat interface
if not st.session_state.get('active_chat_id'):
    st.title("💬 ChatBot")
    st.info("👈 Please select a chat from the sidebar or create a new one from the home page!")
    
    # Show debug info on main page too
    with st.expander("🔧 Debug Info"):
        st.write("**Session State:**")
        st.write(f"Total chats: {len(st.session_state.get('user_chats', {}))}")
        st.write(f"Active chat ID: {st.session_state.get('active_chat_id', 'None')}")
        st.write(f"User chats: {list(st.session_state.get('user_chats', {}).keys())}")
        st.write(f"Chats loaded: {st.session_state.get('chats_loaded', False)}")
        
        if st.button("Create Test Chat"):
            import datetime
            test_id = f"test_{datetime.datetime.now().strftime('%H%M%S')}"
            st.session_state['user_chats'][test_id] = {
                'name': f'Test Chat {len(st.session_state["user_chats"]) + 1}',
                'created_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                'messages': [],
                'response_data': {}
            }
            st.session_state['active_chat_id'] = test_id
            st.success("Test chat created!")
            st.rerun()
    
    st.stop()

# Get active chat
active_chat = st.session_state['user_chats'].get(str(st.session_state['active_chat_id']))
if not active_chat:
    st.error("Selected chat not found!")
    st.write(f"Looking for chat ID: {st.session_state['active_chat_id']}")
    st.write(f"Available chats: {list(st.session_state['user_chats'].keys())}")
    st.session_state['active_chat_id'] = None
    st.rerun()

# Display chat title
st.title(f"💬 {active_chat['name']}")
st.caption(f"Created: {active_chat['created_at']} | Chat ID: {str(st.session_state['active_chat_id'])}...")

# Initialize messages for this specific chat if not exists
if 'messages' not in active_chat:
    active_chat['messages'] = []

# Display chat history
for message in active_chat['messages']:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What's on your mind?"):
    # Add user message
    with st.chat_message('user'):
        st.markdown(prompt)
    active_chat['messages'].append({'role': 'user', 'content': prompt})
    prompt = str(prompt)
    data = {
        'sender': 'user',
        'content': prompt
    }
    result = add_redis(st.session_state['active_chat_id'], data)
    
    # Get AI response
    with st.spinner("Thinking..."):
        response = model_response(active_chat['messages'])
        data = {
            'sender': 'assistant',
            'content': response
        }
        result = add_redis(st.session_state['active_chat_id'], data)
        print("success22")
    
    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(response)
    active_chat['messages'].append({'role': 'assistant', 'content': response})
    
    # Save the updated chat back to session state
    st.session_state['user_chats'][str(st.session_state['active_chat_id'])] = active_chat
    
    # Auto-push to database after each conversation
    try:
        push_data_db_from_redis(int(st.session_state['active_chat_id']))
    except Exception as e:
        print(f"Failed to push to database: {e}")

# Chat statistics
if active_chat.get('messages'):
    st.sidebar.markdown("---")
    st.sidebar.markdown("📊 **Chat Stats**")
    st.sidebar.write(f"Messages: {len(active_chat['messages'])}")
    st.sidebar.write(f"User messages: {len([m for m in active_chat['messages'] if m['role'] == 'user'])}")
    st.sidebar.write(f"AI responses: {len([m for m in active_chat['messages'] if m['role'] == 'assistant'])}")
    
    # Manual push button
    if st.sidebar.button("💾 Save to Database"):
        try:
            if push_data_db_from_redis(int(st.session_state['active_chat_id'])):
                st.sidebar.success("✅ Saved!")
            else:
                st.sidebar.error("❌ Failed to save")
        except Exception as e:
            st.sidebar.error(f"❌ Error: {e}")