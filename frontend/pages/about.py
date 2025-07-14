import streamlit as st
import json
# if not st.session_state.get("is_authenticated"):
#     st.warning("You must login first.")
#     st.stop()
# st.title("developer chat-----")
# response=st.session_state['chat_id']
# st.text(response)
# st.write('----------')
dic={'name':'Anas','age':20}

var=json.dumps(dic)
print(var[0])