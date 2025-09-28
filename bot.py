import re
import streamlit as st
from config.constants import WELCOME, GMTN_LOGO
from ui.sidebar import render_sidebar
from ui.chat import render_chat_history
from services.model_service import send_message_to_model
from services.logger import log_chat

# ----------------------------
# Helper: Render response with proper code formatting
# ----------------------------
def render_response(reply: str):
    """
    Render text and code blocks properly.
    Supports Markdown + fenced code blocks.
    """
    code_block_pattern = r"```(\w+)?\n([\s\S]*?)```"
    matches = re.findall(code_block_pattern, reply)

    if matches:
        # Split into text/code parts
        parts = re.split(code_block_pattern, reply)
        i = 0
        while i < len(parts):
            if i % 3 == 0:  # Normal text
                if parts[i].strip():
                    st.markdown(parts[i])
                i += 1
            elif i % 3 == 1:  # Language
                language = parts[i] if parts[i] else None
                code = parts[i + 1]
                st.code(code, language=language)
                i += 2
    else:
        # No fenced code blocks -> normal markdown
        st.markdown(reply)


# ----------------------------
# App UI
# ----------------------------
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 3rem;
            padding-bottom: 2rem;
        }
        h2 {
            margin-top: 0rem;
            margin-bottom: 0.3rem;
            display: flex;
            gap: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
        .gmt-header {
            display: flex;
            align-items: center;
            gap: 12px;
            white-space: nowrap;   
            font-size: 1.6em;       
            font-weight: 700;
        }
        .gmt-logo {
            height: 45px;   /* default */
            width: auto;
        }
        @media (max-width: 600px) {
            .gmt-logo {
                height: 50px;  /* slightly bigger on mobile */
            }
            .gmt-header {
                font-size: 1.4em; /* slightly smaller text */
            }
        }
    </style>

    <div class="gmt-header">
        <img src="https://global-math-tutoring-network.netlify.app/globalmath.svg"
             alt="GMTN Logo" class="gmt-logo">
        GMTN AI Assistant
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    "Get instant answers about **Global Math Tutoring Network (GMTN)**. "
    "Explore Math & Computer Science programs, book demo sessions, "
    "and start your journey toward stronger problem-solving skills today!"
)

# Initialize session
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "model", "parts": [WELCOME]}]

with st.sidebar:
    render_sidebar()

# Display chat history
render_chat_history()

# Handle user input
user_prompt = st.chat_input("💬 Ask about GMTN or Math/CS…")
if user_prompt:
    # Log user message
    log_chat("user", user_prompt)

    # Show user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_prompt, unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "parts": [user_prompt]})

    # Show assistant response
    with st.chat_message("assistant", avatar=GMTN_LOGO):
        with st.spinner("Isha is thinking... 🤔"):
            reply = send_message_to_model(user_prompt)

        render_response(reply)  # ✅ fixed renderer

    # Log assistant message
    log_chat("AI", reply)

    st.session_state.messages.append({"role": "assistant", "parts": [reply]})
