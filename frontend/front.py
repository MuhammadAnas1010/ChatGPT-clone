import streamlit as st
import requests
from api_auth_front import push_data_db_from_redis

if 'is_authenticated' not in st.session_state:
    st.session_state['is_authenticated'] = False


if 'name' not in st.session_state:
    st.session_state['name']=None

    
page_1=st.Page(
    page='pages/login.py',
    title='Login/register',
    default=True
)
page_2=st.Page(
    page='pages/chat.py',
    title='Chat with',
)
page_3=st.Page(
    page='pages/about.py',
    title='About'
)
page_4=st.Page(
    page='pages/hello.py',
    title="Hello",
    default=True
)
page_5=st.Page(
    page='pages/otp.py',
    title='User Verification'
)
def logout():
    print("Logout function called!")
    response = push_data_db_from_redis(st.session_state["active_chat_id"])
    print(f"Push data response: {response}")
    st.session_state['is_authenticated'] = False
    st.session_state['token'] = None
    st.rerun()
if st.session_state['is_authenticated'] == True and st.session_state['OTP_authenticated']==True:
    print("User is authenticated — rendering sidebar")
    with st.sidebar:
        st.write(f"### Welcome, {st.session_state['name']}! 👋")
        st.write("---")

        if st.button("Logout", type="secondary"):
            print("Logout button pressed!")
            logout()

if not st.session_state['is_authenticated']:
    # If not authenticated, only show the Login/register page
    pg = st.navigation([page_1])
    pg.run()
elif st.session_state['is_authenticated'] and not st.session_state.get('OTP_authenticated', False):
    pg=st.navigation([page_5])
    pg.run()

elif st.session_state['is_authenticated'] and st.session_state['OTP_authenticated']:

    pg = st.navigation([page_4,page_2, page_3]) # You can add login_page here if you want it to always appear
    pg.run()