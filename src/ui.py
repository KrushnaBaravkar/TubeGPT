"""
app.py
------
Streamlit UI for VidQuery — YouTube RAG Pipeline
"""

import streamlit as st
import time
import re

# ── Page Config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="VidQuery",
    page_icon="▶",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f;
    color: #e8e6f0;
    font-family: 'DM Mono', monospace;
}

[data-testid="stAppViewContainer"] {
    background: #0a0a0f;
}

[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] { display: none; }
[data-testid="stSidebar"] { background: #0d0d14; border-right: 1px solid #1e1e2e; }

/* ── Hide default Streamlit elements ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Main container ── */
.main .block-container {
    padding: 2rem 3rem 4rem 3rem;
    max-width: 1100px;
    margin: 0 auto;
}

/* ── Hero Header ── */
.vid-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.4rem;
}

.vid-logo {
    width: 44px;
    height: 44px;
    background: linear-gradient(135deg, #ff4444, #ff2266);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    flex-shrink: 0;
    box-shadow: 0 0 20px rgba(255,68,68,0.4);
}

.vid-title {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.03em;
}

.vid-title span {
    color: #ff4444;
}

.vid-subtitle {
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    color: #555570;
    margin-bottom: 2.5rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* ── Divider ── */
.vid-divider {
    height: 1px;
    background: linear-gradient(90deg, #ff4444 0%, #1e1e2e 60%);
    margin: 1.5rem 0 2rem 0;
}

/* ── URL Input Card ── */
.url-card {
    background: #0f0f1a;
    border: 1px solid #1e1e2e;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}

.url-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #ff4444, transparent);
}

.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    color: #ff4444;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.section-label::before {
    content: '//';
    opacity: 0.5;
}

/* ── Streamlit input overrides ── */
.stTextInput > div > div > input {
    background: #13131f !important;
    border: 1px solid #2a2a3e !important;
    border-radius: 10px !important;
    color: #e8e6f0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s ease !important;
}

.stTextInput > div > div > input:focus {
    border-color: #ff4444 !important;
    box-shadow: 0 0 0 2px rgba(255,68,68,0.15) !important;
}

.stTextInput > div > div > input::placeholder {
    color: #3a3a5c !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #ff4444, #cc2233) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.65rem 1.8rem !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    text-transform: uppercase !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(255,68,68,0.35) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* Secondary button */
.secondary-btn > button {
    background: transparent !important;
    border: 1px solid #2a2a3e !important;
    color: #888899 !important;
}

.secondary-btn > button:hover {
    border-color: #ff4444 !important;
    color: #ff4444 !important;
    box-shadow: none !important;
}

/* ── Video Info Card ── */
.video-info-card {
    background: #0f0f1a;
    border: 1px solid #1e1e2e;
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.video-info-thumb {
    width: 80px;
    height: 50px;
    border-radius: 8px;
    overflow: hidden;
    flex-shrink: 0;
    background: #1a1a2e;
}

.video-info-thumb img {
    width: 100%; height: 100%; object-fit: cover;
}

.video-info-meta {
    flex: 1;
}

.video-info-id {
    font-size: 0.7rem;
    color: #ff4444;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.2rem;
}

.video-info-status {
    font-size: 0.8rem;
    color: #aaaabb;
}

.status-dot {
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #22cc88;
    margin-right: 6px;
    box-shadow: 0 0 6px #22cc88;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* ── Stats Row ── */
.stats-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.stat-chip {
    background: #13131f;
    border: 1px solid #1e1e2e;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-size: 0.72rem;
    color: #666680;
    font-family: 'DM Mono', monospace;
}

.stat-chip strong {
    color: #ff4444;
    font-weight: 500;
}

/* ── Chat Area ── */
.chat-container {
    background: #0f0f1a;
    border: 1px solid #1e1e2e;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    min-height: 120px;
    max-height: 520px;
    overflow-y: auto;
}

/* scrollbar */
.chat-container::-webkit-scrollbar { width: 4px; }
.chat-container::-webkit-scrollbar-track { background: transparent; }
.chat-container::-webkit-scrollbar-thumb { background: #2a2a3e; border-radius: 4px; }

/* ── Message bubbles ── */
.msg {
    margin-bottom: 1.2rem;
    display: flex;
    gap: 0.75rem;
    align-items: flex-start;
    animation: fadeUp 0.3s ease;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}

.msg-avatar {
    width: 30px; height: 30px;
    border-radius: 8px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    margin-top: 2px;
}

.msg-avatar.user  { background: #1e1e3a; color: #8888ff; border: 1px solid #2e2e5a; }
.msg-avatar.bot   { background: #1f1010; color: #ff4444; border: 1px solid #3e1010; }

.msg-body { flex: 1; }

.msg-role {
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
    color: #444460;
}

.msg-role.user { color: #5555aa; }
.msg-role.bot  { color: #aa3333; }

.msg-text {
    font-size: 0.88rem;
    line-height: 1.65;
    color: #d0cee0;
    background: #13131f;
    border: 1px solid #1e1e2e;
    border-radius: 4px 12px 12px 12px;
    padding: 0.75rem 1rem;
}

.msg-text.user {
    background: #12122a;
    border-color: #2a2a4a;
    border-radius: 12px 4px 12px 12px;
    color: #c0bede;
}

/* ── Query input row ── */
.query-row {
    display: flex;
    gap: 0.75rem;
    align-items: flex-end;
}

/* ── Transcript toggle ── */
.transcript-box {
    background: #0d0d18;
    border: 1px solid #1a1a28;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-size: 0.75rem;
    color: #666680;
    line-height: 1.7;
    max-height: 200px;
    overflow-y: auto;
    font-family: 'DM Mono', monospace;
}

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 3rem 2rem;
    color: #333350;
}

.empty-state .icon { font-size: 3rem; margin-bottom: 1rem; opacity: 0.4; }
.empty-state p { font-size: 0.82rem; line-height: 1.6; }

/* ── Step indicators ── */
.step-indicator {
    display: flex;
    gap: 0.5rem;
    align-items: center;
    font-size: 0.75rem;
    color: #555570;
    margin: 0.5rem 0;
    font-family: 'DM Mono', monospace;
}

.step-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #ff4444;
    box-shadow: 0 0 6px #ff4444;
    flex-shrink: 0;
}

/* ── Spinner override ── */
.stSpinner > div { border-top-color: #ff4444 !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #0f0f1a !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 10px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
    color: #888899 !important;
}

/* ── Error / warning ── */
.stAlert {
    background: #1a0f0f !important;
    border: 1px solid #3a1515 !important;
    border-radius: 10px !important;
    color: #cc6666 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: #13131f !important;
    border: 1px solid #2a2a3e !important;
    border-radius: 10px !important;
    color: #e8e6f0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
}

/* ── Slider ── */
.stSlider > div > div > div > div {
    background: #ff4444 !important;
}

/* ── Column gap fix ── */
[data-testid="column"] { gap: 0.75rem; }

/* ── Mobile ── */
@media (max-width: 768px) {
    .main .block-container { padding: 1rem 1rem 3rem 1rem; }
    .stats-row { flex-wrap: wrap; }
    .vid-title { font-size: 1.5rem; }
}
</style>
""", unsafe_allow_html=True)


# ── Session State Init ────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "indexed":       False,
        "index_result":  None,
        "chat_history":  [],   # list of {"role": "user"|"bot", "text": str}
        "video_id":      None,
        "transcript":    None,
        "chunk_count":   0,
        "char_count":    0,
        "current_url":   "",
        "top_k":         4,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ── Helper: extract video ID for thumbnail ────────────────────────────────────
def extract_video_id_safe(url: str) -> str | None:
    patterns = [
        r"(?:v=)([A-Za-z0-9_-]{11})",
        r"youtu\.be/([A-Za-z0-9_-]{11})",
        r"embed/([A-Za-z0-9_-]{11})",
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url.strip()):
        return url.strip()
    return None


# ── Lazy pipeline imports (so app loads even if deps missing) ─────────────────
@st.cache_resource(show_spinner=False)
def load_pipeline():
    from indexing     import index_video
    from retrieval    import get_context_from_vector_store
    from augmentation import augment_context
    from generation   import _generation
    return index_video, get_context_from_vector_store, augment_context, _generation


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="vid-header">
    <div class="vid-logo">▶</div>
    <div class="vid-title">Vid<span>Query</span></div>
</div>
<div class="vid-subtitle">YouTube · RAG Pipeline · Ask anything about any video</div>
<div class="vid-divider"></div>
""", unsafe_allow_html=True)


# ── Layout: two columns ───────────────────────────────────────────────────────
left_col, right_col = st.columns([1, 1.6], gap="large")


# ══════════════════════════════════════════════════════════════════════════════
# LEFT COLUMN — Video Indexing
# ══════════════════════════════════════════════════════════════════════════════
with left_col:

    # URL Input Card
    st.markdown('<div class="url-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Video Source</div>', unsafe_allow_html=True)

    url_input = st.text_input(
        label="url",
        label_visibility="collapsed",
        placeholder="https://youtube.com/watch?v=...",
        key="url_field",
        value=st.session_state.current_url,
    )

    col_btn1, col_btn2 = st.columns([2, 1])
    with col_btn1:
        index_btn = st.button("⚡  Index Video", key="index_btn", use_container_width=True)
    with col_btn2:
        with st.container():
            st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
            clear_btn = st.button("✕ Clear", key="clear_btn", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close url-card

    # ── Index Button Logic ────────────────────────────────────────────────────
    if clear_btn:
        for key in ["indexed", "index_result", "chat_history", "video_id",
                    "transcript", "chunk_count", "char_count", "current_url"]:
            st.session_state[key] = [] if key == "chat_history" else (False if key == "indexed" else None if key != "current_url" else "")
        st.rerun()

    if index_btn and url_input.strip():
        vid_id = extract_video_id_safe(url_input.strip())
        if not vid_id:
            st.error("❌  Invalid YouTube URL or video ID.")
        else:
            st.session_state.current_url = url_input.strip()
            try:
                index_video, get_context, augment, generate = load_pipeline()

                with st.spinner(""):
                    st.markdown("""
                    <div class="step-indicator"><div class="step-dot"></div>Fetching transcript…</div>
                    """, unsafe_allow_html=True)
                    time.sleep(0.3)

                    result = index_video(url_input.strip())

                st.session_state.indexed      = True
                st.session_state.index_result = result
                st.session_state.video_id     = result["video_id"]
                st.session_state.transcript   = result["transcript"]
                st.session_state.chunk_count  = len(result["chunks"])
                st.session_state.char_count   = len(result["transcript"])
                st.session_state.chat_history = []
                st.rerun()

            except Exception as e:
                st.error(f"**Indexing failed:** {e}")

    elif index_btn:
        st.warning("Please paste a YouTube URL first.")

    # ── Video Info (after indexing) ───────────────────────────────────────────
    if st.session_state.indexed and st.session_state.video_id:
        vid_id = st.session_state.video_id
        thumb_url = f"https://img.youtube.com/vi/{vid_id}/mqdefault.jpg"

        st.markdown(f"""
        <div class="video-info-card">
            <div class="video-info-thumb">
                <img src="{thumb_url}" alt="thumbnail" />
            </div>
            <div class="video-info-meta">
                <div class="video-info-id">ID: {vid_id}</div>
                <div class="video-info-status">
                    <span class="status-dot"></span>Indexed &amp; ready
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Stats
        st.markdown(f"""
        <div class="stats-row">
            <div class="stat-chip"><strong>{st.session_state.chunk_count}</strong> chunks</div>
            <div class="stat-chip"><strong>{st.session_state.char_count:,}</strong> chars</div>
            <div class="stat-chip"><strong>{st.session_state.char_count // 4:,}</strong> est. tokens</div>
        </div>
        """, unsafe_allow_html=True)

        # Settings
        st.markdown('<div class="section-label" style="margin-top:1rem;">Retrieval Settings</div>', unsafe_allow_html=True)
        st.session_state.top_k = st.slider(
            "Top-K chunks to retrieve",
            min_value=1, max_value=10,
            value=st.session_state.top_k,
            help="How many transcript chunks to use as context per answer"
        )

        # Transcript viewer
        with st.expander("📄  View raw transcript"):
            st.markdown(f'<div class="transcript-box">{st.session_state.transcript[:3000]}{"…" if len(st.session_state.transcript) > 3000 else ""}</div>', unsafe_allow_html=True)

    else:
        # Empty state
        if not st.session_state.indexed:
            st.markdown("""
            <div class="empty-state">
                <div class="icon">▶</div>
                <p>Paste a YouTube URL above<br>and click <strong>Index Video</strong><br>to get started.</p>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# RIGHT COLUMN — Chat Interface
# ══════════════════════════════════════════════════════════════════════════════
with right_col:

    st.markdown('<div class="section-label">Conversation</div>', unsafe_allow_html=True)

    # ── Chat history display ──────────────────────────────────────────────────
    chat_html = '<div class="chat-container">'

    if not st.session_state.chat_history:
        chat_html += """
        <div class="empty-state">
            <div class="icon" style="font-size:2rem;">💬</div>
            <p>Index a video, then ask anything.<br>
            <span style="color:#444460">"What is this video about?"<br>
            "Summarize the key points."<br>
            "Explain the part about X."</span></p>
        </div>
        """
    else:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                chat_html += f"""
                <div class="msg">
                    <div class="msg-avatar user">👤</div>
                    <div class="msg-body">
                        <div class="msg-role user">You</div>
                        <div class="msg-text user">{msg["text"]}</div>
                    </div>
                </div>
                """
            else:
                chat_html += f"""
                <div class="msg">
                    <div class="msg-avatar bot">▶</div>
                    <div class="msg-body">
                        <div class="msg-role bot">VidQuery</div>
                        <div class="msg-text">{msg["text"]}</div>
                    </div>
                </div>
                """

    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

    # ── Query Input ───────────────────────────────────────────────────────────
    if st.session_state.indexed:
        q_col, btn_col = st.columns([5, 1])
        with q_col:
            query = st.text_input(
                label="query",
                label_visibility="collapsed",
                placeholder="Ask anything about this video…",
                key="query_input",
            )
        with btn_col:
            ask_btn = st.button("Ask →", key="ask_btn", use_container_width=True)

        # Suggested questions
        st.markdown('<div class="section-label" style="margin-top:0.8rem; margin-bottom:0.5rem;">Quick Asks</div>', unsafe_allow_html=True)
        q1, q2, q3 = st.columns(3)
        with q1:
            if st.button("📋 Summarize", key="q_sum", use_container_width=True):
                st.session_state["_quick_q"] = "Summarize this video in detail."
        with q2:
            if st.button("🔑 Key points", key="q_key", use_container_width=True):
                st.session_state["_quick_q"] = "What are the key takeaways from this video?"
        with q3:
            if st.button("❓ Main topic", key="q_top", use_container_width=True):
                st.session_state["_quick_q"] = "What is the main topic of this video?"

        # Use quick question if clicked
        final_query = query
        if "_quick_q" in st.session_state and st.session_state["_quick_q"]:
            final_query = st.session_state["_quick_q"]
            st.session_state["_quick_q"] = ""

        # ── Answer Generation ─────────────────────────────────────────────────
        if (ask_btn or final_query != query) and final_query.strip():
            try:
                _, get_context, augment, generate = load_pipeline()

                st.session_state.chat_history.append({
                    "role": "user",
                    "text": final_query.strip()
                })

                with st.spinner("Thinking…"):
                    vector_store      = st.session_state.index_result["vector_store"]
                    retrieved_context = get_context(vector_store, final_query.strip())
                    final_context     = augment(retrieved_context, final_query.strip())
                    answer            = generate(final_query.strip(), final_context)

                st.session_state.chat_history.append({
                    "role": "bot",
                    "text": answer
                })
                st.rerun()

            except Exception as e:
                st.error(f"**Error generating answer:** {e}")

        # Clear chat
        if st.session_state.chat_history:
            st.markdown("<div style='margin-top:0.5rem;'>", unsafe_allow_html=True)
            with st.container():
                st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
                if st.button("🗑  Clear chat", key="clear_chat"):
                    st.session_state.chat_history = []
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="text-align:center; padding: 1.5rem; color:#333350; font-size:0.8rem;">
            Index a video on the left to unlock the chat.
        </div>
        """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; margin-top:3rem; font-size:0.65rem; color:#252535; letter-spacing:0.1em; text-transform:uppercase;">
    VidQuery · YouTube RAG Pipeline · Powered by LangChain + OpenAI + FAISS
</div>
""", unsafe_allow_html=True)