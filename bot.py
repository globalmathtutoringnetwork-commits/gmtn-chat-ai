import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import traceback
from constants import SYSTEM_PROMPT, WELCOME, GMTN_LOGO, EMAIL, WEBSITE_URL, INSTAGRAM, GMTN_NAME

# ----------------------------
# Setup Model API
# ----------------------------
load_dotenv()
api_key = os.getenv("SECRET_KEY") or st.secrets["SECRET_KEY"]
model_name=os.getenv("MODEL_NAME") or st.secrets["MODEL_NAME"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name)

# ----------------------------
# Functions
# ----------------------------
def render_sidebar():
    st.markdown(
        """
        <style>
        [data-testid="collapsedControl"], button[aria-label="Toggle sidebar"], 
        button[title="Toggle sidebar"], button[title="Open sidebar"], 
        button[title="Expand sidebar"], button[title="Show sidebar"] {
            position: fixed !important;
            top: 16px !important;
            left: 16px !important;
            transform: none !important;
            margin: 0 !important;
            z-index: 10000 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 10px;">
            <img src="{GMTN_LOGO}" alt="GMTN Logo" width="40">
            <h3 style="margin: 0;">{GMTN_NAME}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.header("⚡ Quick Actions")
    if st.button("🗑️ Start New Chat"):
        st.session_state.messages = [{"role": "model", "parts": [WELCOME]}]
        st.rerun()
    if st.button("📅 Book a Demo Session"):
        st.markdown(f"[👉 Click here to schedule]({WEBSITE_URL})")
    st.markdown("---")
    st.header("📌 Official Links")
    st.markdown(
        f"""
        - 🌐 [Website]({WEBSITE_URL})  
        - 📧 <a href='mailto:{EMAIL}'>{EMAIL}</a>  
        - 📸 [Instagram]({INSTAGRAM})
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")
    st.caption(f"📚 Powered by {GMTN_NAME} (GMTN)")


def render_chat_history():
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "assistant"
        avatar = "👤" if role == "user" else GMTN_LOGO
        with st.chat_message(role, avatar=avatar):
            st.markdown(msg["parts"][0], unsafe_allow_html=True)


def send_message_to_model(prompt: str) -> str:
    try:
        chat_history = [
            {"role": "user" if m["role"] == "user" else "model", "parts": m["parts"]}
            for m in st.session_state.messages
        ]
        convo = model.start_chat(history=chat_history)
        model_reply = convo.send_message(SYSTEM_PROMPT + "\n\n" + prompt)
        return model_reply.text.strip()
    except Exception:
        traceback.print_exc()
        st.markdown(
            f"⚠️ Oops! Something went wrong. Please try again later, "
            f"or contact us via our official channels:\n\n"
            f"- 🌐 [Website]: {WEBSITE_URL}\n"
            f"- 📧 [Email ID]: <a href='mailto:{EMAIL}'>{EMAIL}</a>\n"
            f"- 📸 [Instagram]: {INSTAGRAM}",
            unsafe_allow_html=True
        )
        return "⚠️ An error occurred. Please check the official GMTN channels above."


# ----------------------------
# App UI
# ----------------------------
st.set_page_config(page_title="GMTN AI Agent", page_icon="📚", layout="wide")
st.title("📚 GMTN – Official AI Agent")
st.caption("Answers about Global Math Tutoring Network (GMTN) – Math & CS only")

# Initialize session
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "model", "parts": [WELCOME]}]

with st.sidebar:
    render_sidebar()

# Display chat history
render_chat_history()

# Handle user input
user_prompt = st.chat_input(f"💬 Ask about {GMTN_NAME} or Math/CS…")
if user_prompt:
    # Show user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_prompt, unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "parts": [user_prompt]})

    # Show assistant response
    with st.chat_message("assistant", avatar=GMTN_LOGO):
        with st.spinner("Isha is thinking... 🤔"):
            reply = send_message_to_model(user_prompt)

        st.markdown(reply.replace("\n", "<br>"), unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "parts": [reply]})
