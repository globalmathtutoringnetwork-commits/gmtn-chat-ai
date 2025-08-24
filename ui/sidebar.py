import streamlit as st
from config.constants import WELCOME, GMTN_LOGO, EMAIL, WEBSITE_URL, INSTAGRAM, GMTN_NAME

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
