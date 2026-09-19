import streamlit as st

from config.constants import GMTN_LOGO


def render_chat_history() -> None:
    if not st.session_state.get("messages"):
        return

    for message in st.session_state.messages:
        role = "user" if message["role"] == "user" else "assistant"
        avatar = "👤" if role == "user" else GMTN_LOGO
        with st.chat_message(role, avatar=avatar):
            st.markdown(message["parts"][0])


def render_empty_state() -> None:
    st.markdown(
        f"""
        <div class="gmt-empty-state">
            <div class="gmt-empty-hero">
                <div class="gmt-empty-logo">
                    <img src="{GMTN_LOGO}" alt="GMTN logo" />
                </div>
                <div class="gmt-empty-title">Hi, I’m Isha 👋</div>
                <div class="gmt-empty-subtitle">GMTN AI Assistant</div>
            </div>
            <p class="gmt-empty-copy">
                I can help you explore GMTN’s Math and Computer Science programs, understand the right course for your goals, and answer common admissions and demo questions.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    suggestions = [
        "What Math courses do you offer?",
        "Tell me about your Computer Science courses",
        "How can I book a demo session?",
        "Which course is right for my child?",
    ]

    columns = st.columns(2)
    for index, prompt in enumerate(suggestions):
        with columns[index % 2]:
            if st.button(prompt, key=f"suggestion_{index}", use_container_width=True):
                st.session_state.pending_prompt = prompt
                st.rerun()
