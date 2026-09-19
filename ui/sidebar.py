import streamlit as st

from config.constants import GMTN_LOGO, EMAIL, WEBSITE_URL, INSTAGRAM, GMTN_NAME


def render_sidebar() -> None:
    st.markdown(
        """
        <style>
            section[data-testid="stSidebar"] {
                width: 268px !important;
                min-width: 268px !important;
                background: rgba(8, 20, 34, 0.96);
                border-right: 1px solid rgba(164, 190, 220, 0.14);
            }

            div[data-testid="stSidebarNav"] {
                padding-top: 0.3rem;
            }

            .gmt-sidebar-brand {
                display: flex;
                align-items: center;
                gap: 0.7rem;
                padding: 0.45rem 0 1.15rem 0;
                border-bottom: 1px solid rgba(164, 190, 220, 0.12);
            }

            .gmt-sidebar-brand img {
                width: 38px;
                height: 38px;
                border-radius: 13px;
                box-shadow: 0 0 0 4px rgba(109, 184, 255, 0.08);
            }

            .gmt-sidebar-brand-title {
                font-size: 0.9rem;
                font-weight: 700;
                line-height: 1.25;
                letter-spacing: -0.01em;
                color: #f3f6fb;
            }

            .gmt-sidebar-brand-subtitle {
                display: block;
                margin-top: 0.2rem;
                color: #8fa7be;
                font-size: 0.7rem;
                font-weight: 400;
            }

            .gmt-sidebar-label {
                color: #7890a7;
                font-size: 0.66rem;
                letter-spacing: 0.07em;
                text-transform: uppercase;
                margin: 1.15rem 0 0.45rem 0;
            }

            section[data-testid="stSidebar"] .stButton > button,
            section[data-testid="stSidebar"] .stLinkButton > button {
                min-height: 37px;
                border-radius: 10px;
                border: 1px solid transparent;
                background: transparent;
                color: #edf3ff;
                padding: 0.45rem 0.65rem;
                font-weight: 500;
                justify-content: flex-start;
                text-align: left;
                font-size: 0.84rem;
                transition: background 180ms ease, border-color 180ms ease, transform 180ms ease;
            }

            section[data-testid="stSidebar"] .stButton > button:hover,
            section[data-testid="stSidebar"] .stLinkButton > button:hover {
                background: rgba(109, 184, 255, 0.08);
                border-color: rgba(109, 184, 255, 0.16);
                transform: translateX(2px);
            }

            section[data-testid="stSidebar"] .stButton > button:focus-visible,
            section[data-testid="stSidebar"] .stLinkButton > button:focus-visible {
                outline: 2px solid rgba(109, 184, 255, 0.75);
                outline-offset: 2px;
            }

            section[data-testid="stSidebar"] .stButton > button {
                background: #12304d;
                border-color: rgba(109, 184, 255, 0.18);
                color: #ffffff;
            }

            section[data-testid="stSidebar"] .stButton > button::first-letter,
            section[data-testid="stSidebar"] .stLinkButton > button::first-letter {
                color: #8ecbff;
            }

            .gmt-sidebar-meta {
                color: #8197ac;
                font-size: 0.73rem;
                line-height: 1.5;
                margin-top: 1.35rem;
                padding: 1rem 0 0.2rem;
                border-top: 1px solid rgba(164, 190, 220, 0.12);
            }

            @media (max-width: 900px) {
                section[data-testid="stSidebar"] { width: 238px !important; min-width: 238px !important; }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="gmt-sidebar-brand">
            <img src="{GMTN_LOGO}" alt="GMTN logo" />
            <div>
                <div class="gmt-sidebar-brand-title">{GMTN_NAME}</div>
                <div class="gmt-sidebar-brand-subtitle">Isha · AI Learning Assistant</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown('<div class="gmt-sidebar-label">Quick Actions</div>', unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="gmt-sidebar-actions">', unsafe_allow_html=True)
            if st.button("+  New Chat", key="sidebar_new_chat", use_container_width=True):
                st.session_state.messages = []
                st.session_state.pending_prompt = None
                st.rerun()
            st.link_button("Book a Demo", WEBSITE_URL, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="gmt-sidebar-label">Explore GMTN</div>', unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="gmt-sidebar-actions">', unsafe_allow_html=True)
            st.link_button("Web  Website", WEBSITE_URL, use_container_width=True)
            st.link_button("Social  Instagram", INSTAGRAM, use_container_width=True)
            st.link_button("Mail  Email", f"mailto:{EMAIL}", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(
            """
            <div class="gmt-sidebar-meta">
                Trusted Math & Computer Science guidance for learners worldwide.
            </div>
            """,
            unsafe_allow_html=True,
        )
