import traceback

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

from config.constants import EMAIL, INSTAGRAM, SYSTEM_PROMPT, WEBSITE_URL
from config.settings import MODEL_NAME, SECRET_KEY


@st.cache_resource
def get_llm():
    if not SECRET_KEY:
        raise ValueError("Missing SECRET_KEY for Gemini access.")

    return ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        google_api_key=SECRET_KEY,
        temperature=0.7,
    )


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)


@st.cache_resource
def get_chain():
    return prompt | get_llm()


def _get_history() -> list[HumanMessage | AIMessage]:
    history = []
    for message in st.session_state.get("messages", [])[:-1]:
        if message["role"] == "user":
            history.append(HumanMessage(content=message["parts"][0]))
        elif message["role"] in {"model", "assistant"}:
            history.append(AIMessage(content=message["parts"][0]))
    return history


def _content_to_text(content: object) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            item.get("text", "")
            for item in content
            if isinstance(item, dict) and isinstance(item.get("text"), str)
        )
    return ""


def _connection_error() -> str:
    return (
        "I’m having trouble connecting right now. Please try again in a moment. "
        f"For official GMTN updates, visit {WEBSITE_URL}, email {EMAIL}, or Instagram {INSTAGRAM}."
    )


def stream_message_to_model(prompt_text: str):
    try:
        yielded_text = False
        for chunk in get_chain().stream(
            {"input": prompt_text, "history": _get_history()}
        ):
            text = _content_to_text(getattr(chunk, "content", chunk))
            if text:
                yielded_text = True
                yield text
        if not yielded_text:
            yield "I’m having trouble connecting right now. Please try again in a moment."
    except Exception:
        traceback.print_exc()
        yield _connection_error()


def send_message_to_model(prompt_text: str) -> str:
    return "".join(stream_message_to_model(prompt_text)).strip()
