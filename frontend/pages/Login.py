import streamlit as st
from api_auth_front import verify_login,register_user
import jwt
from streamlit_js_eval import streamlit_js_eval

if "OTP" not in st.session_state:
    st.session_state['OTP']=False
if "OTP_authenticated" not in st.session_state:
    st.session_state['OTP_authenticated']=False
if "user_email" not in st.session_state:
    st.session_state['user_email']=None

st.title("Chat GPT-Clone by Anas 📲")
choice=st.radio('Login/Registration',['Login','Registration'])
with st.form("Login formform"):
    if choice == 'Login':
        email=st.text_input(label='Email',placeholder="abc@example.com")
        password=st.text_input(label='Password',placeholder="*******", type="password")
        submit=st.form_submit_button(label="Login")

        if submit:
            response=verify_login(email,password)
            if response.get('status')=='success':
                st.session_state['user_email']=email
                st.session_state['is_authenticated'] = True
                st.session_state['token'] = response.get('token')
                decoded = jwt.decode(st.session_state['token'], options={"verify_signature": False})
                st.session_state['name']=decoded.get('name')
                token = response.get('token')
                streamlit_js_eval(js_expressions=f"localStorage.setItem('jwt', '{token}')", key="set")
                st.success("User logged in successfully!")
                st.session_state['OTP']=True
                # Call store_session if it has other logic, but it now calls st.rerun()
                # store_session(response) # This will now effectively call st.rerun()

                # Simpler: just set session state and rerun directly if store_session is only for this
                st.rerun() # Essential to immediately trigger the re-evaluation in front.py
            else:
                st.error(f"Login failed: {response.get('message', 'Invalid credentials')}")
                st.session_state['is_authenticated'] = False
                st.session_state['token']=None
    else:
        user=st.text_input(label='Username')
        email=st.text_input(label='Email',placeholder='Abc@example.com')
        password=st.text_input(label='password',placeholder='*********', type="password")
        submit=st.form_submit_button(label="Registration")

        if submit:
            response=register_user(user,email,password)
            if response==1:
                st.success("user registered sucessfully")
            else:
                st.error("Already existed")