import streamlit as st
import random
import time
import smtplib
from email.message import EmailMessage

st.title("User Verification VIA OTP")

def send_email(receiver_email, OTP):
    msg = EmailMessage()
    msg.set_content(f"This is your OTP: {OTP}\nIt is valid for 5 minutes.")
    msg['To'] = receiver_email
    msg['Subject'] = "Your OTP code"
    msg["From"] = 'Chat GPT Clone OTP 😏'

    smg = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smg.login("ansshami6@gmail.com", 'gboy rddy rcmw qtkg')  # App password
    smg.send_message(msg)

# Generate OTP once
if "OTP_Number" not in st.session_state:
    st.session_state['OTP_Number'] = "".join([str(random.randint(0, 9)) for _ in range(6)])

st.write(st.session_state['OTP_Number'])  # (for testing)

st.text("Press the button below to receive an OTP in your email.")
button = st.button("Get OTP",type="primary")
placeholder = st.empty()

# If OTP button is pressed
if button:
    with placeholder:
        st.warning("This OTP is valid only for 5 minutes.")
        time.sleep(3)
    placeholder.empty()
    
    # Send email
    send_email(st.session_state['user_email'], st.session_state['OTP_Number'])

    # Track OTP sent and time
    st.session_state['otp_sent'] = True
    st.session_state['otp_time'] = time.time()

# If OTP has been sent
if st.session_state.get('otp_sent'):
    st.subheader("Enter Your OTP Below:")
    otp_input = st.text_input(label="OTP")

    # Check OTP expiry (5 minutes)
    if time.time() - st.session_state['otp_time'] > 300:
        st.error("OTP expired. Please request a new one.")
        st.session_state['otp_sent'] = False  # Reset
    elif otp_input:
        if otp_input == st.session_state['OTP_Number']:
            st.success("OTP Verified ✅")
            st.session_state["OTP_authenticated"] = True
            st.rerun()
        else:
            st.error("Invalid OTP. Please try again.")
