import streamlit as st
import traceback
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from config.settings import SECRET_KEY,MODEL_NAME
from config.constants import SYSTEM_PROMPT, WEBSITE_URL, EMAIL, INSTAGRAM

# ----------------------------
# Setup Langchain Model
# ----------------------------
llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    google_api_key=SECRET_KEY,
    temperature=0.7
)

# Create prompt template with system message
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

def send_message_to_model(prompt_text: str) -> str:
    try:
        # Convert streamlit messages to langchain format
        history = []
        if "messages" in st.session_state:
            for msg in st.session_state.messages[:-1]:  # Exclude current user message
                if msg["role"] == "user":
                    history.append(HumanMessage(content=msg["parts"][0]))
                elif msg["role"] == "model" or msg["role"] == "assistant":
                    history.append(AIMessage(content=msg["parts"][0]))
        
        # Create the chain
        chain = prompt | llm
        
        # Invoke the chain
        response = chain.invoke({
            "input": prompt_text,
            "history": history
        })
        
        return response.content.strip()
        
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
