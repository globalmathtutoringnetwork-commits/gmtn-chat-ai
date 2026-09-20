import streamlit as st

from config.constants import GMTN_LOGO
from services.logger import log_chat_async
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

            /* Isha product shell */
            :root {
                --gmt-bg: #07111f;
                --gmt-surface: #0c1b2d;
                --gmt-surface-strong: #10243a;
                --gmt-line: rgba(164, 190, 220, 0.14);
                --gmt-text: #f5f8fc;
                --gmt-muted: #94a8bd;
                --gmt-accent: #6db8ff;
                --gmt-gold: #d4af37;
                --gmt-radius-sm: 10px;
                --gmt-radius-md: 16px;
                --gmt-shadow: 0 18px 50px rgba(0, 0, 0, 0.22);
            }

            html, body, [data-testid="stAppViewContainer"] {
                background:
                    radial-gradient(circle at 68% 12%, rgba(65, 135, 205, 0.11), transparent 32rem),
                    var(--gmt-bg);
            }

            [data-testid="stHeader"] { background: transparent; }
            .main .block-container {
                max-width: 1180px;
                padding: 0 2.4rem 6.5rem !important;
            }

            [data-testid="stSidebar"] {
                background: rgba(8, 20, 34, 0.96);
                border-right: 1px solid var(--gmt-line);
            }

            .gmt-header {
                min-height: 54px;
                padding: 0 0 0.9rem;
                margin-bottom: 1.35rem;
                border-bottom: 1px solid var(--gmt-line);
            }

            .gmt-header-brand img {
                width: 36px;
                height: 36px;
                border-radius: 12px;
                box-shadow: 0 0 0 4px rgba(109, 184, 255, 0.08);
            }

            .gmt-header-title {
                font-size: 1.08rem;
                letter-spacing: -0.02em;
            }

            .gmt-header-subtitle {
                font-size: 0.7rem;
                letter-spacing: 0.04em;
                text-transform: none;
            }

            .gmt-top-action .stButton > button {
                min-height: 34px;
                border-radius: var(--gmt-radius-sm);
                border-color: var(--gmt-line);
                background: rgba(255, 255, 255, 0.035);
                font-size: 0.82rem;
            }

            .stChatMessage {
                max-width: 1040px;
                margin: 0 auto;
                padding: 0.55rem 0;
                animation: gmt-message-in 260ms ease-out both;
            }

            .stChatMessage [data-testid="stChatMessageContent"] {
                max-width: none;
                margin: 0;
                line-height: 1.65;
            }

            .stChatMessage[data-testid="stChatMessageUser"] {
                justify-content: flex-end;
            }

            .stChatMessage[data-testid="stChatMessageUser"] [data-testid="stChatMessageContent"] {
                max-width: min(78%, 650px);
                padding: 0.82rem 1rem;
                border: 1px solid rgba(109, 184, 255, 0.14);
                border-radius: 18px 18px 5px 18px;
                background: linear-gradient(135deg, #163653, #12304d);
                box-shadow: 0 8px 22px rgba(0, 0, 0, 0.12);
            }

            .stChatMessage[data-testid="stChatMessageAssistant"] [data-testid="stChatMessageContent"] {
                max-width: min(88%, 760px);
                padding: 0.15rem 0.65rem 0.25rem 0.25rem;
            }

            .stChatMessage [data-testid="stChatMessageAvatar"] {
                border-radius: 11px;
                box-shadow: 0 0 0 3px rgba(109, 184, 255, 0.08);
            }

            .stChatMessage code {
                border: 1px solid var(--gmt-line);
                border-radius: 6px;
                background: #081522;
            }

            .gmt-thinking {
                display: inline-flex;
                align-items: center;
                gap: 0.45rem;
                color: var(--gmt-muted);
                font-size: 0.88rem;
                padding: 0.35rem 0;
            }

            .gmt-thinking-dots {
                display: inline-flex;
                gap: 0.18rem;
            }

            .gmt-thinking-dots span {
                width: 0.3rem;
                height: 0.3rem;
                border-radius: 50%;
                background: var(--gmt-accent);
                animation: gmt-thinking-dot 1.1s ease-in-out infinite;
            }

            .gmt-thinking-dots span:nth-child(2) { animation-delay: 0.15s; }
            .gmt-thinking-dots span:nth-child(3) { animation-delay: 0.3s; }

            .stChatInput {
                max-width: 1040px;
                margin: 0 auto;
                border: 1px solid rgba(130, 169, 207, 0.28);
                border-radius: 18px;
                background: rgba(13, 32, 52, 0.94);
                box-shadow: var(--gmt-shadow);
                transition: border-color 180ms ease, box-shadow 180ms ease;
            }

            .stChatInput:focus-within {
                border-color: rgba(109, 184, 255, 0.7);
                box-shadow: 0 0 0 3px rgba(109, 184, 255, 0.1), var(--gmt-shadow);
            }

            .stChatInput textarea {
                min-height: 48px;
                padding: 0.78rem 1rem !important;
                font-size: 0.95rem;
            }

            .gmt-empty-state {
                max-width: 820px;
                margin: clamp(2.5rem, 13vh, 8rem) auto 0;
                padding: 0;
                animation: gmt-fade-up 460ms ease-out both;
            }

            .gmt-empty-logo {
                width: 64px;
                height: 64px;
                border-radius: 20px;
                border-color: rgba(109, 184, 255, 0.35);
                background: rgba(109, 184, 255, 0.1);
                box-shadow: 0 0 32px rgba(109, 184, 255, 0.13);
            }

            .gmt-empty-logo img { width: 38px; height: 38px; }
            .gmt-empty-title { font-size: clamp(2rem, 4vw, 3.2rem); letter-spacing: -0.055em; }
            .gmt-empty-subtitle {
                font-size: 0.84rem;
                letter-spacing: 0.02em;
                text-transform: none;
                color: var(--gmt-accent);
            }
            .gmt-empty-copy { max-width: 580px; font-size: 0.96rem; }

            .gmt-empty-grid .stButton > button {
                min-height: 52px;
                border-radius: var(--gmt-radius-md);
                border-color: var(--gmt-line);
                background: rgba(255, 255, 255, 0.035);
                text-align: left;
                transition: transform 180ms ease, border-color 180ms ease, background 180ms ease;
            }

            .gmt-empty-grid .stButton > button:hover {
                transform: translateY(-2px);
                border-color: rgba(109, 184, 255, 0.48);
                background: rgba(109, 184, 255, 0.08);
            }

            @keyframes gmt-fade-up { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
            @keyframes gmt-message-in { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }

            @media (max-width: 768px) {
                .main .block-container { padding: 0.7rem 0.85rem 6rem !important; }
                .gmt-header { margin-bottom: 0.8rem; }
                .stChatMessage[data-testid="stChatMessageUser"] [data-testid="stChatMessageContent"],
                .stChatMessage[data-testid="stChatMessageAssistant"] [data-testid="stChatMessageContent"] { max-width: 90%; }
                .gmt-empty-state { margin-top: 3.5rem; }
            }

            @media (prefers-reduced-motion: reduce) {
                *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
            }

            /* Welcome composition */
            .main .block-container { position: relative; overflow: hidden; }
            .block-container {
                max-width: 1180px !important;
                padding: 0 2.4rem 6.5rem !important;
            }

            .gmt-ambient {
                position: absolute;
                inset: 0 0 auto;
                height: 620px;
                pointer-events: none;
                overflow: hidden;
                opacity: 0.42;
                mask-image: linear-gradient(to bottom, black, transparent 82%);
            }

            .gmt-equation {
                position: absolute;
                color: rgba(135, 187, 232, 0.13);
                font-family: Georgia, serif;
                font-size: 1.05rem;
                letter-spacing: 0.04em;
                animation: gmt-drift 12s ease-in-out infinite alternate;
            }

            .gmt-equation-one { top: 18%; left: 5%; transform: rotate(-8deg); }
            .gmt-equation-two { top: 33%; right: 3%; font-family: 'Courier New', monospace; font-size: 0.75rem; animation-delay: -4s; }

            .gmt-grid-line {
                position: absolute;
                width: 280px;
                height: 180px;
                border-top: 1px solid rgba(109, 184, 255, 0.08);
                border-right: 1px solid rgba(109, 184, 255, 0.08);
                transform: skewY(-18deg) rotate(12deg);
            }

            .gmt-grid-line-one { top: 20%; right: 12%; }
            .gmt-grid-line-two { top: 44%; left: 12%; transform: skewY(18deg) rotate(-12deg); opacity: 0.55; }

            .gmt-empty-state {
                position: relative;
                z-index: 1;
                max-width: 1040px;
                margin-top: clamp(0.65rem, 2.5vh, 1.8rem);
            }

            .gmt-identity-orbit {
                position: relative;
                width: 92px;
                height: 92px;
                margin: 0 auto 1rem;
                display: grid;
                place-items: center;
            }

            .gmt-orbit-ring {
                position: absolute;
                inset: 0;
                border: 1px solid rgba(109, 184, 255, 0.3);
                border-radius: 50%;
                box-shadow: 0 0 30px rgba(109, 184, 255, 0.08);
                animation: gmt-breathe 4.5s ease-in-out infinite;
            }

            .gmt-orbit-ring::after {
                content: "";
                position: absolute;
                width: 5px;
                height: 5px;
                top: 8px;
                right: 13px;
                border-radius: 50%;
                background: var(--gmt-gold);
                box-shadow: 0 0 12px rgba(212, 175, 55, 0.65);
            }

            .gmt-empty-logo {
                width: 70px;
                height: 70px;
                margin: 0;
                border-radius: 23px;
                border-color: rgba(212, 175, 55, 0.32);
                background: rgba(17, 46, 72, 0.92);
                box-shadow: 0 12px 36px rgba(0, 0, 0, 0.24), 0 0 26px rgba(109, 184, 255, 0.12);
            }

            .gmt-empty-logo img { width: 44px; height: 44px; }

            .gmt-identity-kicker {
                color: #829ab1;
                font-size: 0.65rem;
                font-weight: 600;
                letter-spacing: 0.16em;
                line-height: 1.4;
            }

            .gmt-empty-title {
                margin-top: 0.3rem;
                font-size: clamp(2.5rem, 5vw, 4.2rem);
                letter-spacing: -0.065em;
            }

            .gmt-empty-subtitle {
                margin-top: 0.3rem;
                margin-bottom: 0.9rem;
                font-size: 1rem;
                color: #a8d5ff;
            }

            .gmt-greeting {
                color: #f7fbff;
                font-size: 1.18rem;
                font-weight: 600;
                letter-spacing: -0.02em;
                animation: gmt-fade-up 500ms 180ms ease-out both;
            }

            .gmt-empty-copy { margin-bottom: 0.8rem; }

            .gmt-capability-row {
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 0.45rem;
                margin: 0 auto 1.25rem;
            }

            .gmt-capability-row span {
                padding: 0.36rem 0.62rem;
                border: 1px solid rgba(164, 190, 220, 0.14);
                border-radius: 999px;
                color: #9cb2c7;
                background: rgba(255, 255, 255, 0.025);
                font-size: 0.72rem;
            }

            div[data-testid="stForm"] {
                position: relative;
                z-index: 2;
                max-width: 440px;
                margin: 0 auto 1.25rem;
                padding: 0.42rem;
                border: 1px solid rgba(109, 184, 255, 0.2);
                border-radius: 16px;
                background: rgba(13, 32, 52, 0.82);
                box-shadow: 0 15px 40px rgba(0, 0, 0, 0.16);
            }

            div[data-testid="stForm"] input {
                border: 0 !important;
                background: transparent !important;
                color: var(--gmt-text) !important;
            }

            div[data-testid="stFormSubmitButton"] button {
                min-height: 38px;
                border: 1px solid rgba(109, 184, 255, 0.3);
                border-radius: 11px;
                background: rgba(109, 184, 255, 0.13);
                color: #dff1ff;
                font-size: 0.82rem;
                transition: transform 180ms ease, background 180ms ease;
            }

            div[data-testid="stFormSubmitButton"] button:hover {
                transform: translateY(-1px);
                background: rgba(109, 184, 255, 0.22);
            }

            .gmt-suggestions-label {
                position: relative;
                z-index: 1;
                margin: 0 auto 0.5rem;
                color: #7890a7;
                font-size: 0.68rem;
                letter-spacing: 0.1em;
                text-transform: uppercase;
            }

            button[aria-label="What Math courses do you offer?"],
            button[aria-label="Tell me about your Computer Science courses"],
            button[aria-label="How can I book a demo session?"],
            button[aria-label="Which course is right for my child?"] {
                min-height: 64px !important;
                border: 1px solid rgba(164, 190, 220, 0.16) !important;
                border-radius: 15px !important;
                background: rgba(255, 255, 255, 0.035) !important;
                color: #eaf3fb !important;
                text-align: left !important;
                line-height: 1.35 !important;
                transition: transform 180ms ease, border-color 180ms ease, background 180ms ease !important;
            }

            button[aria-label="What Math courses do you offer?"]::before { content: "∑  "; color: #8ecbff; }
            button[aria-label="Tell me about your Computer Science courses"]::before { content: "</>  "; color: #8ecbff; }
            button[aria-label="How can I book a demo session?"]::before { content: "✦  "; color: var(--gmt-gold); }
            button[aria-label="Which course is right for my child?"]::before { content: "◇  "; color: #8ecbff; }

            button[aria-label="What Math courses do you offer?"]:hover,
            button[aria-label="Tell me about your Computer Science courses"]:hover,
            button[aria-label="How can I book a demo session?"]:hover,
            button[aria-label="Which course is right for my child?"]:hover {
                transform: translateY(-2px);
                border-color: rgba(109, 184, 255, 0.48) !important;
                background: rgba(109, 184, 255, 0.09) !important;
            }

            @keyframes gmt-breathe { 0%, 100% { transform: scale(1); opacity: 0.72; } 50% { transform: scale(1.04); opacity: 1; } }
            @keyframes gmt-drift { from { transform: translate3d(0, 0, 0) rotate(-8deg); } to { transform: translate3d(8px, -5px, 0) rotate(-5deg); } }
            @keyframes gmt-thinking-dot { 0%, 60%, 100% { transform: translateY(0); opacity: 0.35; } 30% { transform: translateY(-3px); opacity: 1; } }

            @media (max-width: 600px) {
                .block-container { padding: 0.5rem 0.85rem 5rem !important; }
                .gmt-empty-state { margin-top: 0.65rem; }
                .gmt-identity-orbit { width: 76px; height: 76px; margin-bottom: 0.65rem; }
                .gmt-empty-logo { width: 59px; height: 59px; border-radius: 19px; }
                .gmt-empty-logo img { width: 37px; height: 37px; }
                .gmt-identity-kicker { font-size: 0.58rem; letter-spacing: 0.12em; }
                .gmt-empty-title { font-size: 2.5rem; }
                .gmt-empty-subtitle { margin-bottom: 0.55rem; font-size: 0.88rem; }
                .gmt-greeting { font-size: 1.05rem; }
                .gmt-empty-copy { max-width: 330px; margin-bottom: 0.5rem; font-size: 0.86rem; line-height: 1.45; }
                .gmt-capability-row { max-width: 330px; }
                .gmt-capability-row { margin-bottom: 0.75rem; }
                .gmt-capability-row span { padding: 0.28rem 0.5rem; font-size: 0.62rem; }
                div[data-testid="stForm"] { margin-bottom: 0.75rem; }
                .gmt-suggestions-label { margin-top: 0.2rem; }
                .gmt-ambient { height: 520px; }
            }

            @media (min-width: 601px) and (max-height: 760px) {
                .block-container { padding: 0.2rem 2.4rem 4.5rem !important; }
                .gmt-empty-state { margin-top: 0.2rem; }
                .gmt-identity-orbit { width: 68px; height: 68px; margin-bottom: 0.4rem; }
                .gmt-empty-logo { width: 54px; height: 54px; border-radius: 18px; }
                .gmt-empty-logo img { width: 34px; height: 34px; }
                .gmt-identity-kicker { font-size: 0.55rem; }
                .gmt-empty-title { font-size: 2.6rem; }
                .gmt-empty-subtitle { margin-bottom: 0.35rem; font-size: 0.86rem; }
                .gmt-greeting { font-size: 1rem; }
                .gmt-empty-copy { max-width: 620px; margin-bottom: 0.35rem; font-size: 0.82rem; line-height: 1.35; }
                .gmt-capability-row { margin-bottom: 0.45rem; }
                .gmt-capability-row span { padding: 0.22rem 0.45rem; font-size: 0.62rem; }
                div[data-testid="stForm"] { margin-bottom: 0.45rem; padding: 0.28rem; }
                div[data-testid="stForm"] input { min-height: 32px; }
                div[data-testid="stFormSubmitButton"] button { min-height: 31px; padding: 0.25rem 0.65rem; }
                button[aria-label="What Math courses do you offer?"],
                button[aria-label="Tell me about your Computer Science courses"],
                button[aria-label="How can I book a demo session?"],
                button[aria-label="Which course is right for my child?"] { min-height: 39px !important; }
                .gmt-suggestions-label { margin-bottom: 0.3rem; }
            }

            /* Keep the empty state and composer within one viewport. */
            .main .block-container,
            .block-container {
                padding-top: 0 !important;
                padding-bottom: 0.4rem !important;
            }

            .gmt-empty-state {
                margin-top: 0.2rem !important;
            }

            .gmt-identity-orbit {
                width: 72px;
                height: 72px;
                margin-bottom: 0.45rem;
            }

            .gmt-empty-logo {
                width: 58px;
                height: 58px;
                border-radius: 18px;
            }

            .gmt-empty-logo img {
                width: 36px;
                height: 36px;
            }

            .gmt-empty-title {
                font-size: clamp(2.2rem, 4vw, 3.3rem);
            }

            .gmt-empty-subtitle {
                margin-bottom: 0.45rem;
            }

            .gmt-greeting {
                font-size: 1.05rem;
            }

            .gmt-empty-copy {
                margin-bottom: 0.45rem;
                font-size: 0.88rem;
                line-height: 1.4;
            }

            .gmt-capability-row {
                margin-bottom: 0.55rem;
            }

            div[data-testid="stForm"] {
                margin-bottom: 0.55rem;
                padding: 0.3rem;
                background: rgba(20, 42, 65, 0.5);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
            }

            div[data-testid="stForm"] input {
                min-height: 36px;
            }

            div[data-testid="stFormSubmitButton"] button {
                min-height: 34px;
            }

            .gmt-suggestions-label {
                margin-bottom: 0.35rem;
            }

            button[aria-label="What Math courses do you offer?"],
            button[aria-label="Tell me about your Computer Science courses"],
            button[aria-label="How can I book a demo session?"],
            button[aria-label="Which course is right for my child?"] {
                min-height: 46px !important;
                border-radius: 12px !important;
                background: rgba(255, 255, 255, 0.045) !important;
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
            }

            .stChatInput {
                background: rgba(13, 32, 52, 0.72);
                backdrop-filter: blur(18px);
                -webkit-backdrop-filter: blur(18px);
            }

            body:has(.gmt-empty-state) section.stMain {
                overflow-y: hidden !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def inject_background_scene() -> None:
    st.markdown(
        f"""
        <style>
            .gmt-bg-scene {{
                position: fixed;
                inset: 0;
                z-index: 0;
                overflow: hidden;
                pointer-events: none;
                background:
                    radial-gradient(circle at 50% 42%, rgba(43, 106, 157, 0.15), transparent 34%),
                    radial-gradient(circle at 12% 18%, rgba(212, 175, 55, 0.08), transparent 22%),
                    linear-gradient(135deg, rgba(7, 17, 31, 0.1), rgba(3, 10, 20, 0.28));
            }}

            .gmt-bg-logo {{
                position: fixed;
                left: 50%;
                top: 50%;
                width: min(70vw, 920px);
                height: auto;
                transform: translate(-50%, -50%);
                background-image: url("{GMTN_LOGO}");
                background-repeat: no-repeat;
                background-size: contain;
                opacity: 0.085;
                filter: grayscale(0.25) saturate(0.7) contrast(0.9);
                mix-blend-mode: screen;
                animation: gmt-logo-breathe 12s ease-in-out infinite;
            }}

            .gmt-bg-orbit {{
                position: absolute;
                left: 50%;
                top: 50%;
                width: min(74vw, 980px);
                height: min(28vw, 360px);
                border: 1px solid rgba(109, 184, 255, 0.2);
                border-radius: 50%;
                transform: translate(-50%, -50%) rotate(-17deg);
                box-shadow: 0 0 42px rgba(109, 184, 255, 0.1);
                animation: gmt-orbit-spin 24s linear infinite;
            }}

            .gmt-bg-orbit::after {{
                content: "";
                position: absolute;
                left: 18%;
                top: -4px;
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #d4af37;
                box-shadow: 0 0 18px rgba(212, 175, 55, 0.9);
            }}

            .gmt-bg-orbit-two {{
                width: min(58vw, 760px);
                height: min(21vw, 270px);
                transform: translate(-50%, -50%) rotate(32deg);
                border-color: rgba(212, 175, 55, 0.1);
                animation-duration: 31s;
                animation-direction: reverse;
            }}

            .gmt-bg-orbit-two::after {{
                left: auto;
                right: 22%;
                background: #8ecbff;
                box-shadow: 0 0 18px rgba(142, 203, 255, 0.9);
            }}

            .gmt-bg-stars,
            .gmt-bg-stars::before,
            .gmt-bg-stars::after {{
                position: absolute;
                display: block;
                width: 2px;
                height: 2px;
                border-radius: 50%;
                background: rgba(225, 239, 255, 0.8);
                box-shadow:
                    8vw 12vh rgba(225, 239, 255, 0.42),
                    18vw 68vh rgba(212, 175, 55, 0.5),
                    29vw 26vh rgba(225, 239, 255, 0.32),
                    42vw 82vh rgba(225, 239, 255, 0.44),
                    56vw 18vh rgba(212, 175, 55, 0.46),
                    67vw 72vh rgba(225, 239, 255, 0.35),
                    78vw 34vh rgba(225, 239, 255, 0.5),
                    91vw 14vh rgba(212, 175, 55, 0.42),
                    88vw 86vh rgba(225, 239, 255, 0.34),
                    12vw 92vh rgba(225, 239, 255, 0.38);
                content: "";
                animation: gmt-stars-drift 18s linear infinite;
            }}

            .gmt-bg-stars {{
                left: 0;
                top: 0;
                opacity: 0.58;
            }}

            .gmt-bg-stars::before {{
                left: 17vw;
                top: 31vh;
                opacity: 0.45;
                transform: scale(0.65);
                animation-duration: 25s;
                animation-delay: -8s;
            }}

            .gmt-bg-stars::after {{
                left: 8vw;
                top: 74vh;
                opacity: 0.34;
                transform: scale(1.35);
                animation-duration: 31s;
                animation-delay: -15s;
            }}

            .gmt-bg-operator {{
                position: absolute;
                color: rgba(145, 198, 239, 0.3);
                font-family: Georgia, serif;
                font-size: clamp(1.2rem, 2vw, 2rem);
                letter-spacing: 0.04em;
                text-shadow: 0 0 22px rgba(109, 184, 255, 0.36);
                animation: gmt-operator-float 16s ease-in-out infinite alternate;
            }}

            .gmt-bg-operator-one {{ left: 8%; top: 24%; animation-delay: -3s; }}
            .gmt-bg-operator-two {{ left: 17%; top: 76%; font-size: 1rem; animation-delay: -11s; }}
            .gmt-bg-operator-three {{ right: 10%; top: 22%; color: rgba(212, 175, 55, 0.34); animation-delay: -7s; }}
            .gmt-bg-operator-four {{ right: 16%; top: 72%; font-family: 'Courier New', monospace; font-size: 0.82rem; animation-delay: -13s; }}
            .gmt-bg-operator-five {{ left: 43%; top: 12%; font-size: 0.9rem; animation-delay: -5s; }}
            .gmt-bg-operator-six {{ left: 70%; top: 52%; font-family: 'Courier New', monospace; font-size: 0.75rem; animation-delay: -9s; }}
            .gmt-bg-operator-seven {{ left: 31%; top: 87%; color: rgba(212, 175, 55, 0.38); animation-delay: -2s; }}
            .gmt-bg-operator-eight {{ right: 29%; top: 8%; font-family: 'Courier New', monospace; font-size: 0.72rem; animation-delay: -14s; }}
            .gmt-bg-operator-nine {{ left: 4%; top: 52%; font-size: 1.25rem; animation-delay: -6s; }}
            .gmt-bg-operator-ten {{ right: 3%; top: 46%; color: rgba(212, 175, 55, 0.32); font-size: 1.15rem; animation-delay: -10s; }}

            .gmt-bg-rail {{
                position: absolute;
                height: 1px;
                width: 31vw;
                background: linear-gradient(90deg, transparent, rgba(109, 184, 255, 0.16), transparent);
                transform: rotate(-18deg);
                animation: gmt-rail-shift 20s ease-in-out infinite alternate;
            }}

            .gmt-bg-rail-one {{ left: -5vw; top: 35%; }}
            .gmt-bg-rail-two {{ right: -5vw; top: 64%; transform: rotate(21deg); animation-delay: -8s; }}

            .gmt-ambient {{ display: none !important; }}

            [data-testid="stAppViewContainer"] > .main,
            [data-testid="stSidebar"] {{
                position: relative;
                z-index: 1;
            }}

            @keyframes gmt-logo-breathe {{
                0%, 100% {{ opacity: 0.032; transform: translate(-50%, -50%) scale(0.98); }}
                50% {{ opacity: 0.06; transform: translate(-50%, -50%) scale(1.02); }}
            }}

            @keyframes gmt-stars-drift {{
                from {{ opacity: 0.28; transform: translate3d(-1vw, 1vh, 0); }}
                to {{ opacity: 0.8; transform: translate3d(2vw, -2vh, 0); }}
            }}

            @keyframes gmt-operator-float {{
                from {{ transform: translate3d(-8px, 5px, 0) rotate(-5deg); }}
                to {{ transform: translate3d(12px, -12px, 0) rotate(5deg); }}
            }}

            @keyframes gmt-rail-shift {{
                from {{ opacity: 0.25; transform: translateX(-2vw) rotate(-18deg); }}
                to {{ opacity: 0.7; transform: translateX(5vw) rotate(-14deg); }}
            }}

            @keyframes gmt-orbit-spin {{
                from {{ transform: translate(-50%, -50%) rotate(-17deg); }}
                to {{ transform: translate(-50%, -50%) rotate(343deg); }}
            }}

            @media (max-width: 768px) {{
                .gmt-bg-logo {{ width: 96vw; opacity: 0.055; }}
                .gmt-bg-orbit {{ width: 112vw; height: 42vw; }}
                .gmt-bg-orbit-two {{ width: 92vw; height: 34vw; }}
                .gmt-bg-operator {{ font-size: 1rem; }}
                .gmt-bg-operator-one {{ left: 4%; top: 22%; }}
                .gmt-bg-operator-three {{ right: 4%; top: 28%; }}
                .gmt-bg-operator-four {{ right: 5%; top: 76%; }}
                .gmt-bg-operator-eight {{ right: 4%; top: 12%; }}
                .gmt-bg-operator-nine {{ left: 2%; top: 55%; }}
                .gmt-bg-operator-ten {{ right: 2%; top: 50%; }}
            }}

            @media (prefers-reduced-motion: reduce) {{
                .gmt-bg-logo,
                .gmt-bg-orbit,
                .gmt-bg-orbit-two,
                .gmt-bg-stars,
                .gmt-bg-stars::before,
                .gmt-bg-stars::after,
                .gmt-bg-operator,
                .gmt-bg-rail {{ animation: none !important; }}
            }}
        </style>
        <div class="gmt-bg-scene" aria-hidden="true">
            <div class="gmt-bg-logo"></div>
            <div class="gmt-bg-orbit"></div>
            <div class="gmt-bg-orbit gmt-bg-orbit-two"></div>
            <div class="gmt-bg-stars"></div>
            <span class="gmt-bg-operator gmt-bg-operator-one">∑ f(x)</span>
            <span class="gmt-bg-operator gmt-bg-operator-two">∫ dy</span>
            <span class="gmt-bg-operator gmt-bg-operator-three">π · ∞</span>
            <span class="gmt-bg-operator gmt-bg-operator-four">&lt;/&gt; 0101</span>
            <span class="gmt-bg-operator gmt-bg-operator-five">x² + y²</span>
            <span class="gmt-bg-operator gmt-bg-operator-six">f(x) → ∂y</span>
            <span class="gmt-bg-operator gmt-bg-operator-seven">Δt · ∇</span>
            <span class="gmt-bg-operator gmt-bg-operator-eight">{{ a² + b² }}</span>
            <span class="gmt-bg-operator gmt-bg-operator-nine">∞</span>
            <span class="gmt-bg-operator gmt-bg-operator-ten">Σ 01</span>
            <span class="gmt-bg-rail gmt-bg-rail-one"></span>
            <span class="gmt-bg-rail gmt-bg-rail-two"></span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def reset_chat() -> None:
    st.session_state.messages = []
    st.session_state.pending_prompt = None
    st.rerun()


def reset_empty_state_scroll() -> None:
    st.markdown(
        """
        <script>
            const resetIshaScroll = () => {
                const main = window.parent.document.querySelector('section.stMain');
                if (main) main.scrollTo({ top: 0, behavior: 'instant' });
            };
            requestAnimationFrame(resetIshaScroll);
            setTimeout(resetIshaScroll, 120);
            setTimeout(resetIshaScroll, 600);
            setTimeout(resetIshaScroll, 1200);
        </script>
        """,
        unsafe_allow_html=True,
    )

def hide_welcome_during_generation() -> None:
    st.markdown(
        """
        <style>
            .gmt-ambient,
            .gmt-empty-state,
            .gmt-suggestions-label,
            div[data-testid="stForm"],
            button[aria-label="What Math courses do you offer?"],
            button[aria-label="Tell me about your Computer Science courses"],
            button[aria-label="How can I book a demo session?"],
            button[aria-label="Which course is right for my child?"] {
                display: none !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def submit_prompt(prompt: str) -> None:
    text = (prompt or "").strip()
    if not text:
        return

    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.session_state.messages.append({"role": "user", "parts": [text]})
    user_name = st.session_state.get("user_name", "").strip()
    logged_text = f"[{user_name}] {text}" if user_name else text
    log_chat_async("user", logged_text)

    with st.chat_message("user", avatar="👤"):
        st.markdown(text)

    with st.chat_message("assistant", avatar=GMTN_LOGO):
        response_placeholder = st.empty()
        response_placeholder.markdown(
            '<div class="gmt-thinking">Isha is thinking '
            '<span class="gmt-thinking-dots"><span></span><span></span><span></span></span></div>',
            unsafe_allow_html=True,
        )
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
    log_chat_async("AI", clean_reply)


st.set_page_config(
    page_title="Isha | GMTN AI Assistant",
    page_icon=GMTN_LOGO,
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_styles()
inject_background_scene()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

with st.sidebar:
    render_sidebar()

user_prompt = st.chat_input("Ask Isha about GMTN, Math, or Computer Science…")

if st.session_state.pending_prompt:
    requested_prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None
    hide_welcome_during_generation()
    if st.session_state.messages:
        render_chat_history()
    submit_prompt(requested_prompt)
    st.rerun()

if user_prompt:
    hide_welcome_during_generation()
    if st.session_state.messages:
        render_chat_history()
    submit_prompt(user_prompt)
    st.rerun()

if st.session_state.messages:
    render_chat_history()
else:
    render_empty_state()
    reset_empty_state_scroll()
