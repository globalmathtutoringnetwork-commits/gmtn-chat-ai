import streamlit as st
from config.constants import GMTN_LOGO

def render_chat_history():
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "assistant"
        avatar = "👤" if role == "user" else GMTN_LOGO
        with st.chat_message(role, avatar=avatar):
            st.markdown(msg["parts"][0], unsafe_allow_html=True)
