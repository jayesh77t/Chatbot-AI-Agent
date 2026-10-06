from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="QnA Bot", page_icon="🤖", layout="centered")

# ── Custom CSS – user bubbles right, AI bubbles left ─────────────────────────
st.markdown("""
<style>
/* Import font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Page background */
.stApp {
    background: #0f1117;
}

/* Title */
.chat-title {
    text-align: center;
    color: #e2e8f0;
    font-size: 1.3rem;
    font-weight: 600;
    letter-spacing: 0.01em;
    padding: 1rem 0 0.5rem;
    border-bottom: 1px solid #1e2130;
    margin-bottom: 1rem;
}

/* ── Chat wrapper ── */
.chat-wrapper {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    padding: 0.5rem 0 1rem;
}

/* ── Row: controls alignment ── */
.msg-row {
    display: flex;
    align-items: flex-end;
    gap: 0.5rem;
}

/* AI → left-aligned */
.msg-row.ai  { justify-content: flex-start; }

/* User → right-aligned */
.msg-row.user { justify-content: flex-end; }

/* ── Avatar circle ── */
.avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    flex-shrink: 0;
}
.avatar.ai   { background: #2d3748; color: #90cdf4; }
.avatar.user { background: #2b4a7a; color: #bee3f8; }

/* ── Bubble ── */
.bubble {
    max-width: 72%;
    padding: 0.65rem 1rem;
    border-radius: 18px;
    font-size: 0.92rem;
    line-height: 1.55;
    word-wrap: break-word;
}

/* AI bubble */
.bubble.ai {
    background: #1e2130;
    color: #cbd5e0;
    border-bottom-left-radius: 4px;
}

/* User bubble */
.bubble.user {
    background: #1a4a8a;
    color: #ebf4ff;
    border-bottom-right-radius: 4px;
}

/* ── Timestamp ── */
.ts {
    font-size: 0.68rem;
    color: #4a5568;
    margin: 0 0.4rem 0.15rem;
    white-space: nowrap;
}

/* ── Input bar tweaks ── */
.stChatInputContainer {
    border-top: 1px solid #1e2130 !important;
    padding-top: 0.75rem;
}
</style>
""", unsafe_allow_html=True)

# ── LLM ───────────────────────────────────────────────────────────────────────
llm = ChatGroq(model="openai/gpt-oss-20b")

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="chat-title">🤖 QnA Bot</div>', unsafe_allow_html=True)

# ── Render existing messages ──────────────────────────────────────────────────
chat_html = '<div class="chat-wrapper">'

for msg in st.session_state.messages:
    role    = msg.get("role")           # "user" or "ai"
    content = msg.get("content", "")

    if role == "user":
        chat_html += f"""
        <div class="msg-row user">
            <div class="bubble user">{content}</div>
            <div class="avatar user">You</div>
        </div>"""
    else:
        chat_html += f"""
        <div class="msg-row ai">
            <div class="avatar ai">🤖</div>
            <div class="bubble ai">{content}</div>
        </div>"""

chat_html += '</div>'
st.markdown(chat_html, unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
query = st.chat_input("Ask anything…")

if query:
    # 1. Save & immediately render the user message
    st.session_state.messages.append({"role": "user", "content": query})

    # 2. Call LLM
    with st.spinner("Thinking…"):
        res = llm.invoke(st.session_state.messages)

    # 3. Save AI response
    st.session_state.messages.append({"role": "ai", "content": res.content})

    # 4. Rerun to re-render the full chat
    st.rerun()

print(st.session_state.messages)