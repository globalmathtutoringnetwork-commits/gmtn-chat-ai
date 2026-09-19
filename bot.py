import streamlit as st

from config.constants import GMTN_LOGO, GMTN_NAME
from services.logger import log_chat
from services.model_service import stream_message_to_model
from ui.chat import render_chat_history, render_empty_state
from ui.sidebar import render_sidebar


def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

            :root {
                --gmt-bg: #071924;
                --gmt-surface: #0d2134;
                --gmt-surface-strong: #102b42;
                --gmt-surface-soft: rgba(255,255,255,0.02);
                --gmt-line: rgba(255,255,255,0.07);
                --gmt-text: #f3f6fb;
                --gmt-muted: #a1b2c7;
                --gmt-accent: #d4af37;
                --gmt-accent-soft: rgba(212,175,55,0.12);
            }

            html, body, [data-testid="stAppViewContainer"] {
                background: var(--gmt-bg);
                color: var(--gmt-text);
                font-family: 'Inter', sans-serif;
            }

            .main .block-container {
                padding-top: 0.5rem !important;
                padding-bottom: 1.2rem !important;
                max-width: 1040px;
            }

            [data-testid="stSidebar"] {
                background: rgba(10, 25, 38, 0.98);
                border-right: 1px solid var(--gmt-line);
            }

            [data-testid="stSidebar"] > div {
                padding-top: 0.7rem;
            }

            .stButton > button,
            .stLinkButton > button {
                transition: border-color 0.15s ease, background-color 0.15s ease, transform 0.15s ease;
            }

            .stButton > button:hover,
            .stLinkButton > button:hover {
                border-color: rgba(212, 175, 55, 0.45);
                background: rgba(255,255,255,0.04);
                transform: translateY(-1px);
            }

            .stChatMessage {
                padding: 0.18rem 0 0.32rem 0;
            }

            .stChatMessage [data-testid="stChatMessageContent"] {
                max-width: 760px;
                margin: 0 auto;
            }

            .stChatMessage[data-testid="stChatMessageUser"] [data-testid="stChatMessageContent"] {
                padding-left: 0.6rem;
            }

            .stChatMessage[data-testid="stChatMessageAssistant"] [data-testid="stChatMessageContent"] {
                padding-right: 0.6rem;
            }

            .gmt-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 1rem;
                min-height: 64px;
                padding: 0.25rem 0 0.75rem 0;
                border-bottom: 1px solid rgba(255,255,255,0.05);
                margin-bottom: 0.8rem;
            }

            .gmt-header-brand {
                display: flex;
                align-items: center;
                gap: 0.8rem;
                min-width: 0;
            }

            .gmt-header-brand img {
                width: 32px;
                height: 32px;
                border-radius: 9px;
            }

            .gmt-header-copy {
                display: flex;
                flex-direction: column;
                min-width: 0;
            }

            .gmt-header-title {
                font-size: 1.5rem;
                line-height: 1.1;
                font-weight: 700;
                letter-spacing: -0.04em;
                color: var(--gmt-text);
            }

            .gmt-header-subtitle {
                font-size: 0.68rem;
                letter-spacing: 0.09em;
                text-transform: uppercase;
                color: var(--gmt-muted);
            }

            .gmt-top-action {
                display: flex;
                justify-content: flex-end;
            }

            .gmt-top-action .stButton > button {
                min-height: 36px;
                border-radius: 10px;
                background: rgba(255,255,255,0.02);
                color: var(--gmt-text);
                border: 1px solid rgba(255,255,255,0.08);
                padding: 0.55rem 0.9rem;
                font-weight: 500;
            }

            .gmt-empty-state {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                margin: 1.1rem auto 0;
                max-width: 760px;
                padding: 0.8rem 0 0.4rem;
            }

            .gmt-empty-logo {
                width: 52px;
                height: 52px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 16px;
                border: 1px solid rgba(212,175,55,0.22);
                background: rgba(212,175,55,0.08);
                margin-bottom: 0.7rem;
            }

            .gmt-empty-logo img {
                width: 30px;
                height: 30px;
            }

            .gmt-empty-title {
                font-size: clamp(1.9rem, 2.5vw, 2.5rem);
                line-height: 1.1;
                font-weight: 700;
                letter-spacing: -0.04em;
                margin: 0 0 0.15rem 0;
            }

            .gmt-empty-subtitle {
                color: var(--gmt-muted);
                font-size: 0.72rem;
                letter-spacing: 0.12em;
                text-transform: uppercase;
                margin-bottom: 0.9rem;
            }

            .gmt-empty-copy {
                max-width: 620px;
                margin: 0 auto 1.2rem;
                color: var(--gmt-muted);
                font-size: 0.98rem;
                line-height: 1.6;
            }

            .gmt-empty-grid {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 0.7rem;
                width: min(100%, 740px);
            }

            .gmt-empty-grid .stButton > button {
                width: 100%;
                min-height: 46px;
                border-radius: 12px;
                background: rgba(255,255,255,0.02);
                border: 1px solid rgba(255,255,255,0.08);
                color: var(--gmt-text);
                font-weight: 500;
                padding: 0.75rem 0.8rem;
                text-align: left;
                line-height: 1.4;
                white-space: normal;
            }

            .stChatInput {
                border-radius: 16px;
                border: 1px solid rgba(255,255,255,0.08);
                background: rgba(17,33,49,0.8);
                box-shadow: none;
            }

            .stChatInput textarea {
                background: transparent !important;
                border: none !important;
                color: var(--gmt-text) !important;
                font-size: 0.98rem;
                padding: 0.8rem 0.95rem !important;
                min-height: 54px;
            }

            .stChatInput textarea::placeholder {
                color: var(--gmt-muted) !important;
                opacity: 1;
            }

            @media (max-width: 768px) {
                .main .block-container {
                    padding-left: 0.7rem !important;
                    padding-right: 0.7rem !important;
                }

                .gmt-empty-grid {
                    grid-template-columns: 1fr;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def reset_chat() -> None:
    st.session_state.messages = []
    st.session_state.pending_prompt = None
    st.rerun()


def submit_prompt(prompt: str) -> None:
    text = (prompt or "").strip()
    if not text:
        return

    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.session_state.messages.append({"role": "user", "parts": [text]})
    log_chat("user", text)

    with st.chat_message("user", avatar="👤"):
        st.markdown(text)

    with st.chat_message("assistant", avatar=GMTN_LOGO):
        response_placeholder = st.empty()
        streamed_parts = []
        for chunk in stream_message_to_model(text):
            streamed_parts.append(chunk)
            response_placeholder.markdown("".join(streamed_parts) + "▌")
        reply = "".join(streamed_parts)
        response_placeholder.markdown(reply)

    clean_reply = (reply or "").strip() or (
        "I’m having trouble connecting right now. Please try again in a moment."
    )
    st.session_state.messages.append({"role": "assistant", "parts": [clean_reply]})
    log_chat("AI", clean_reply)


st.set_page_config(
    page_title="Isha | GMTN AI Assistant",
    page_icon=GMTN_LOGO,
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_styles()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

with st.sidebar:
    render_sidebar()

header = st.container()
with header:
    col_brand, col_action = st.columns([5, 1])
    with col_brand:
        st.markdown(
            f"""
            <div class="gmt-header-brand">
                <img src="{GMTN_LOGO}" alt="GMTN logo" />
                <div class="gmt-header-copy">
                    <span class="gmt-header-title">Isha</span>
                    <span class="gmt-header-subtitle">{GMTN_NAME}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_action:
        if st.button("New Chat", key="topbar_new_chat", use_container_width=True):
            reset_chat()

if st.session_state.pending_prompt:
    requested_prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None
    submit_prompt(requested_prompt)

if st.session_state.messages:
    render_chat_history()
else:
    render_empty_state()

user_prompt = st.chat_input("Ask Isha about GMTN, Math, or Computer Science…")
if user_prompt:
    submit_prompt(user_prompt)
    st.rerun()
