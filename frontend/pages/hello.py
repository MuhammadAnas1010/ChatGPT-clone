import streamlit as st
import requests
import datetime
from api_auth_front import load_user_chats


# Initialize session state for chats if not exists
if 'user_chats' not in st.session_state:
    st.session_state['user_chats'] = {}
if 'active_chat_id' not in st.session_state:
    st.session_state['active_chat_id'] = None
if 'chats_loaded' not in st.session_state:
    st.session_state['chats_loaded'] = False

# Check if user is authenticated
if not st.session_state.get('token'):
    st.error("🚫 Please login first!")
    st.stop()

# Load chats from database when user first arrives (only once per session)
if not st.session_state['chats_loaded']:
    with st.spinner("Loading your chats..."):
        if load_user_chats():
            st.session_state['chats_loaded'] = True
            st.success("✅ Chats loaded successfully!")
        else:
            st.info("ℹ️ No previous chats found or failed to load.")
            st.session_state['chats_loaded'] = True

st.markdown("""
<div style="text-align: center; padding: 2rem;">
    <h1>👋 Welcome to GPT-Clone</h1>
    <p style="font-size: 1.2rem; color: #666;">Your own AI-powered assistant, built with FastAPI & Streamlit</p>
</div>
""", unsafe_allow_html=True)

# Always show sidebar (even if empty)
st.sidebar.title("💬 Your Chats")

if st.session_state['user_chats']:
    # Show ALL chats as clickable buttons
    for chat_id, chat_data in st.session_state['user_chats'].items():
        chat_name = chat_data.get('name', f'Chat {str(chat_id)[:8]}')
        created_time = chat_data.get('created_at', 'Unknown')
        
        # Show all chats as buttons
        if str(chat_id) == str(st.session_state.get('active_chat_id')):
            # Active chat - show with fire emoji
            if st.sidebar.button(f"🔥 {chat_name} (Active)", key=f"home_active_{chat_id}", type="primary"):
                pass  # Already active
        else:
            # Inactive chat - show as regular button
            if st.sidebar.button(f"📝 {chat_name}", key=f"home_chat_{chat_id}"):
                st.session_state['active_chat_id'] = str(chat_id)
                st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.write(f"**Total chats: {len(st.session_state['user_chats'])}**")
    
    # Add refresh button
    if st.sidebar.button("🔄 Refresh Chats"):
        st.session_state['chats_loaded'] = False
        st.rerun()
else:
    st.sidebar.info("No chats yet. Create one below!")

# Center the start button
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("🚀 Start New Chat", type="primary", use_container_width=True):
        try:
            # Check if user is authenticated
            if not st.session_state.get('token'):
                st.error("🚫 Please login first!")
                st.stop()
            
            header = {'Authorization': f"Bearer {st.session_state['token']}"}
            response = requests.post(url="http://127.0.0.1:8000/chat/new", headers=header)
            
            st.write("Status Code:", response.status_code)
            
            if response.status_code == 200:
                response_json = response.json()
                st.json(response_json)
                
                # Extract chat information - try multiple possible keys
                chat_id = (response_json.get("chat_id") or 
                          response_json.get("name") or 
                          response_json.get("id") or
                          str(response_json.get("data", {}).get("id", "")) or
                          f"chat_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')}")  # Added microseconds for uniqueness
                
                # Ensure unique chat ID
                original_chat_id = str(chat_id)
                counter = 1
                while str(chat_id) in st.session_state['user_chats']:
                    chat_id = f"{original_chat_id}_{counter}"
                    print(chat_id)
                    counter += 1
                
                # Store chat in session state
                chat_name = f"Chat {len(st.session_state['user_chats']) + 1}"
                st.session_state['user_chats'][str(chat_id)] = {
                    'name': chat_name,
                    'created_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    'messages': [],
                    'response_data': response_json
                }
                
                # Set as active chat
                st.session_state['active_chat_id'] = str(chat_id)
                
                st.success(f"✅ New chat created! Chat ID: {chat_id}")
                st.info("💡 You can now see all your chats in the sidebar!")
                
                # Debug info
                st.write("**Debug Info:**")
                st.write(f"Total chats: {len(st.session_state['user_chats'])}")
                st.write(f"Active chat ID: {st.session_state['active_chat_id']}")
                st.write(f"All chat IDs: {list(st.session_state['user_chats'].keys())}")
                
                # Force a rerun after a small delay
                st.rerun()
            else:
                st.error(f"🚫 Failed to create chat. Status: {response.status_code}")
                
        except Exception as e:
            st.error(f"🚫 Request failed: {e}")

# Show active chat indicator
if st.session_state.get('active_chat_id'):
    active_chat = st.session_state['user_chats'].get(st.session_state['active_chat_id'])
    if active_chat:
        st.info(f"🔥 Ready to chat! Go to the chat page to continue with: **{active_chat['name']}**")

# Add some instructions
st.markdown("""
---
### 📋 How it works:
1. **Create a new chat** by clicking the "Start New Chat" button
2. **Your chats will appear** in the left sidebar
3. **Click on any chat** to resume where you left off
4. **Navigate to the chat page** to start messaging

### 💾 Persistence:
- Your chats are saved in the database
- You can switch between multiple chats
- Each chat maintains its own conversation history
- Use the refresh button to reload chats from the database
""")

# Debug section (remove this in production)
with st.expander("🔧 Debug Info"):
    st.write("**Session State:**")
    st.write(f"Total chats: {len(st.session_state.get('user_chats', {}))}")
    st.write(f"Active chat ID: {st.session_state.get('active_chat_id', 'None')}")
    st.write(f"User chats: {list(st.session_state.get('user_chats', {}).keys())}")
    st.write(f"Is authenticated: {st.session_state.get('is_authenticated', False)}")
    st.write(f"Has token: {bool(st.session_state.get('token'))}")
    st.write(f"Chats loaded: {st.session_state.get('chats_loaded', False)}")
    
    if st.button("Clear All Chats"):
        st.session_state['user_chats'] = {}
        st.session_state['active_chat_id'] = None
        st.session_state['chats_loaded'] = False
        st.success("All chats cleared!")
        st.rerun()
    
    if st.button("Force Reload Chats"):
        st.session_state['chats_loaded'] = False
        st.rerun()