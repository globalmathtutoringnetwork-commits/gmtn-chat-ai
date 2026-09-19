import streamlit as st

from config.constants import GMTN_LOGO, EMAIL, WEBSITE_URL, INSTAGRAM, GMTN_NAME


def render_sidebar() -> None:
    st.markdown(
        """
        <style>
            section[data-testid="stSidebar"] {
                width: 240px !important;
                min-width: 240px !important;
                background: rgba(9, 24, 39, 0.96);
            }

            div[data-testid="stSidebarNav"] {
                padding-top: 0.65rem;
            }

            .gmt-sidebar-brand {
                display: flex;
                align-items: center;
                gap: 0.7rem;
                padding: 0.2rem 0 0.8rem 0;
            }

            .gmt-sidebar-brand img {
                width: 30px;
                height: 30px;
                border-radius: 9px;
            }

            .gmt-sidebar-brand-title {
                font-size: 0.96rem;
                font-weight: 700;
                line-height: 1.25;
                letter-spacing: -0.02em;
                color: #f3f6fb;
            }

            .gmt-sidebar-label {
                color: #b8c6d6;
                font-size: 0.68rem;
                letter-spacing: 0.1em;
                text-transform: uppercase;
                margin: 0.9rem 0 0.6rem 0;
            }

            .gmt-sidebar-actions .stButton > button,
            .gmt-sidebar-actions .stLinkButton > button {
                min-height: 40px;
                border-radius: 10px;
                border: 1px solid rgba(255,255,255,0.08);
                background: rgba(255,255,255,0.02);
                color: #edf3ff;
                padding: 0.55rem 0.8rem;
                font-weight: 500;
                justify-content: flex-start;
                text-align: left;
            }

            .gmt-sidebar-actions .stButton > button:hover,
            .gmt-sidebar-actions .stLinkButton > button:hover {
                background: rgba(255,255,255,0.04);
                border-color: rgba(212, 175, 55, 0.25);
            }

            .gmt-sidebar-meta {
                color: #9db0c0;
                font-size: 0.78rem;
                line-height: 1.5;
                margin-top: 1rem;
                padding-top: 0.8rem;
                border-top: 1px solid rgba(255,255,255,0.06);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="gmt-sidebar-brand">
            <img src="{GMTN_LOGO}" alt="GMTN logo" />
            <div class="gmt-sidebar-brand-title">{GMTN_NAME}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown('<div class="gmt-sidebar-label">Quick Actions</div>', unsafe_allow_html=True)
        if st.button("New Chat", key="sidebar_new_chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.pending_prompt = None
            st.rerun()
        st.link_button("Book a Demo", WEBSITE_URL, use_container_width=True)

        st.markdown('<div class="gmt-sidebar-label">Explore GMTN</div>', unsafe_allow_html=True)
        st.link_button("Website", WEBSITE_URL, use_container_width=True)
        st.link_button("Instagram", INSTAGRAM, use_container_width=True)
        st.link_button("Email", f"mailto:{EMAIL}", use_container_width=True)

        st.markdown(
            """
            <div class="gmt-sidebar-meta">
                Trusted Math & Computer Science guidance for learners worldwide.
            </div>
            """,
            unsafe_allow_html=True,
        )
