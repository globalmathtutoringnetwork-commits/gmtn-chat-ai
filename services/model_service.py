import streamlit as st
import google.generativeai as genai
import traceback
from config.settings import SECRET_KEY,MODEL_NAME
from config.constants import SYSTEM_PROMPT, WEBSITE_URL, EMAIL, INSTAGRAM

# ----------------------------
# Setup Model API
# ----------------------------
genai.configure(api_key=SECRET_KEY)
model = genai.GenerativeModel(MODEL_NAME)

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
            f"- 🌐 [Website]({WEBSITE_URL})\n"
            f"- 📧 [Email ID]: <a href='mailto:{EMAIL}'>{EMAIL}</a>\n"
            f"- 📸 [Instagram]({INSTAGRAM})",
            unsafe_allow_html=True
        )
        return "⚠️ An error occurred. Please check the official GMTN channels above."
