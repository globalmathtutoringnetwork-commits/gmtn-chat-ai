from datetime import datetime

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


def _greeting(name: str) -> str:
    hour = datetime.now().hour
    if hour < 12:
        salutation = "Good morning"
    elif hour < 18:
        salutation = "Good afternoon"
    else:
        salutation = "Good evening"
    return f"{salutation}, {name} 👋" if name else f"{salutation} 👋"


def render_empty_state() -> None:
    name = st.session_state.get("user_name", "").strip()
    greeting = _greeting(name)

    st.markdown(
        f"""
        <div class="gmt-ambient" aria-hidden="true">
            <span class="gmt-equation gmt-equation-one">∑ f(x) = ∫ y dx</span>
            <span class="gmt-equation gmt-equation-two">&lt;/&gt; 0101  ∴  x²</span>
            <span class="gmt-grid-line gmt-grid-line-one"></span>
            <span class="gmt-grid-line gmt-grid-line-two"></span>
        </div>
        <section class="gmt-empty-state" role="region" aria-label="Start a conversation with Isha">
            <div class="gmt-identity-orbit">
                <span class="gmt-orbit-ring"></span>
                <div class="gmt-empty-logo">
                    <img src="{GMTN_LOGO}" alt="GMTN logo" />
                </div>
            </div>
            <div class="gmt-identity-kicker">GLOBAL MATH TUTORING NETWORK</div>
            <div class="gmt-empty-title">Meet Isha.</div>
            <div class="gmt-empty-subtitle">Your AI learning companion</div>
            <div class="gmt-greeting">{greeting}</div>
            <p class="gmt-empty-copy">
                I’m here to make Math, Computer Science, courses, and your next learning step feel a little clearer.
            </p>
            <div class="gmt-capability-row" aria-label="Isha capabilities">
                <span>∑ Math</span><span>&lt;/&gt; Computer Science</span><span>✦ Courses</span><span>◇ Guidance</span>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    # if not name:
    #     with st.form("isha_name_form", clear_on_submit=False):
    #         name_input = st.text_input(
    #             "What should I call you?",
    #             placeholder="What should I call you? (optional)",
    #             label_visibility="collapsed",
    #         )
    #         if st.form_submit_button("Continue  →", use_container_width=False):
    #             st.session_state.user_name = name_input.strip()
    #             st.rerun()

    suggestions = [
        "What Math courses do you offer?",
        "Tell me about your Computer Science courses",
        "How can I book a demo session?",
        "Which course is right for my child?",
    ]

    st.markdown('<div class="gmt-suggestions-label">Start with a direction</div>', unsafe_allow_html=True)
    columns = st.columns(2)
    for index, prompt in enumerate(suggestions):
        with columns[index % 2]:
            if st.button(prompt, key=f"suggestion_{index}", use_container_width=True):
                st.session_state.pending_prompt = prompt
                st.rerun()
