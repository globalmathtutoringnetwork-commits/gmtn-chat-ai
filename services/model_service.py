import traceback

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from google.genai.errors import ClientError

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
        max_tokens=512,
        thinking_level="minimal",
        retries=0,
        request_timeout=30,
    )


@st.cache_resource
def get_fallback_llm():
    if not SECRET_KEY:
        raise ValueError("Missing SECRET_KEY for Gemini access.")

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=SECRET_KEY,
        temperature=0.7,
        max_tokens=512,
        thinking_budget=0,
        retries=0,
        request_timeout=30,
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


@st.cache_resource
def get_fallback_chain():
    return prompt | get_fallback_llm()


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
        "I’m sorry, I couldn’t complete that request right now. "
        "Please try again in a moment. If you need help immediately, you can reach GMTN here:\n\n"
        f"- [Visit our website]({WEBSITE_URL})\n"
        f"- [Email us](mailto:{EMAIL})\n"
        f"- [Message us on Instagram]({INSTAGRAM})"
    )


def _quota_error() -> str:
    return (
        "Isha is temporarily unavailable for a moment. Please try again shortly. "
        "For immediate assistance, please contact GMTN through one of these channels:\n\n"
        f"- [Visit our website]({WEBSITE_URL})\n"
        f"- [Email us](mailto:{EMAIL})\n"
        f"- [Message us on Instagram]({INSTAGRAM})"
    )


def stream_message_to_model(prompt_text: str):
    request = {"input": prompt_text, "history": _get_history()}
    try:
        yielded_text = False
        for chunk in get_chain().stream(request):
            text = _content_to_text(getattr(chunk, "content", chunk))
            if text:
                yielded_text = True
                yield text
        if not yielded_text:
            yield "I’m having trouble connecting right now. Please try again in a moment."
    except ClientError as exc:
        traceback.print_exc()
        if getattr(exc, "code", None) == 429 or "RESOURCE_EXHAUSTED" in str(exc):
            try:
                for chunk in get_fallback_chain().stream(request):
                    text = _content_to_text(getattr(chunk, "content", chunk))
                    if text:
                        yield text
            except Exception:
                traceback.print_exc()
                yield _quota_error()
        else:
            yield _connection_error()
    except Exception:
        traceback.print_exc()
        yield _connection_error()


def send_message_to_model(prompt_text: str) -> str:
    return "".join(stream_message_to_model(prompt_text)).strip()
