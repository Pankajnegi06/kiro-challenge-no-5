"""
Uttarakhand Local Guide - Pahadi Guide
Built for Kiro Heroes Week 5 Challenge
"""

import streamlit as st
import os
from pathlib import Path

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

st.set_page_config(
    page_title="Pahadi Guide | Uttarakhand Local Guide",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Complete themed CSS with aggressive selectors
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');
    
    :root {
        --bg-primary: #0a0a0f;
        --bg-secondary: #12121a;
        --accent-green: #10b981;
        --accent-emerald: #34d399;
        --accent-orange: #f97316;
        --text-primary: #ffffff;
        --text-secondary: #94a3b8;
        --glass-bg: rgba(255, 255, 255, 0.03);
        --glass-border: rgba(255, 255, 255, 0.08);
    }
    
    * { font-family: 'Inter', sans-serif !important; }
    
    /* Hide footer and menu */
    footer, #MainMenu { visibility: hidden !important; display: none !important; }
    
    /* CRITICAL: Hide the keyboard_double_arrow_right completely */
    button[kind="header"] {
        font-size: 0 !important;
        color: transparent !important;
    }
    
    button[kind="header"]::after {
        content: "☰ Menu" !important;
        font-size: 14px !important;
        color: var(--accent-emerald) !important;
    }
    
    /* Target the collapsed control specifically */
    [data-testid="collapsedControl"] {
        font-size: 0 !important;
        color: transparent !important;
        background: var(--bg-secondary) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
    }
    
    [data-testid="collapsedControl"] span {
        font-size: 0 !important;
    }
    
    [data-testid="collapsedControl"]::after {
        content: "☰ Menu" !important;
        font-size: 14px !important;
        color: var(--accent-emerald) !important;
    }
    
    /* Main app background */
    .stApp {
        background: var(--bg-primary) !important;
        background-image: 
            radial-gradient(ellipse 80% 50% at 50% -20%, rgba(16, 185, 129, 0.12), transparent),
            radial-gradient(ellipse 60% 40% at 100% 100%, rgba(249, 115, 22, 0.08), transparent) !important;
    }
    
    /* Header styling */
    header[data-testid="stHeader"] {
        background: var(--bg-primary) !important;
        border-bottom: 1px solid var(--glass-border) !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(16, 185, 129, 0.05) 0%, var(--bg-secondary) 30%) !important;
        border-right: 1px solid var(--glass-border) !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background: transparent !important;
    }
    
    /* HIDE ALL INPUT LABELS */
    .stTextInput label, [data-testid="stWidgetLabel"] {
        display: none !important;
    }
    
    /* Hero */
    .hero-box {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 40px;
        margin-bottom: 24px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .hero-box::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--accent-green), var(--accent-orange), transparent);
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 50px;
        padding: 6px 14px;
        font-size: 11px;
        color: var(--accent-emerald);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
        margin-bottom: 16px;
    }
    
    .hero-title {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 48px;
        font-weight: 700;
        background: linear-gradient(135deg, #fff 0%, var(--accent-emerald) 50%, var(--accent-orange) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 8px;
    }
    
    .hero-sub {
        font-size: 16px;
        color: var(--text-secondary);
        margin-bottom: 24px;
    }
    
    .chips {
        display: flex;
        gap: 10px;
        justify-content: center;
        flex-wrap: wrap;
    }
    
    .chip {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 10px;
        padding: 10px 16px;
        font-size: 13px;
        color: var(--text-primary);
    }
    
    /* CHAT INPUT - Compact and centered */
    .stChatFloatingInputContainer {
        background: var(--bg-primary) !important;
        padding: 12px 0 !important;
    }
    
    [data-testid="stChatInput"] {
        max-width: 900px !important;
        margin: 0 auto !important;
        background: transparent !important;
    }
    
    .stChatInput, .stChatInput > div, .stChatInputContainer {
        background: var(--bg-secondary) !important;
        border-color: var(--glass-border) !important;
    }
    
    div[data-testid="stChatInput"] > div {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 12px !important;
        padding: 8px 12px !important;
    }
    
    .stChatInput textarea, .stChatInput input {
        background: var(--bg-secondary) !important;
        color: var(--accent-emerald) !important;
        border: none !important;
        padding: 4px 8px !important;
        min-height: 40px !important;
        max-height: 120px !important;
    }
    
    .stChatInput textarea::placeholder {
        color: var(--text-secondary) !important;
    }
    
    /* CHAT MESSAGES - Compact */
    [data-testid="stChatMessageContainer"] {
        background: transparent !important;
        max-width: 900px !important;
        margin: 0 auto !important;
    }
    
    .stChatMessage, [data-testid="stChatMessage"] {
        background: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid rgba(16, 185, 129, 0.2) !important;
        border-radius: 12px !important;
        margin: 10px 0 !important;
        padding: 12px 16px !important;
    }
    
    /* Sidebar text input */
    .stTextInput > div > div {
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 8px !important;
    }
    
    .stTextInput input {
        color: var(--accent-emerald) !important;
        background: transparent !important;
    }
    
    /* BUTTONS */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-green) 0%, var(--accent-emerald) 100%) !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-weight: 700 !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4) !important;
    }
    
    /* Region badges */
    .badge-garhwal {
        display: inline-block;
        background: rgba(249, 115, 22, 0.15);
        border: 1px solid rgba(249, 115, 22, 0.3);
        color: #fbbf24;
        padding: 8px 16px;
        border-radius: 50px;
        font-size: 12px;
        font-weight: 600;
        margin: 8px 0 16px 0;
    }
    
    .badge-kumaon {
        display: inline-block;
        background: rgba(59, 130, 246, 0.15);
        border: 1px solid rgba(59, 130, 246, 0.3);
        color: #93c5fd;
        padding: 8px 16px;
        border-radius: 50px;
        font-size: 12px;
        font-weight: 600;
        margin: 8px 0 16px 0;
    }
    
    /* Sidebar styling */
    .side-card {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
    }
    
    .side-label {
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: var(--accent-green) !important;
        font-weight: 600;
        margin-bottom: 10px;
        margin-top: 16px;
    }
    
    .api-link {
        display: block;
        text-align: center;
        color: var(--accent-emerald) !important;
        font-size: 11px;
        margin-top: 8px;
        text-decoration: none;
    }
    
    .api-link:hover {
        text-decoration: underline;
    }
    
    .status-demo {
        background: rgba(249, 115, 22, 0.1);
        border: 1px solid rgba(249, 115, 22, 0.2);
        border-radius: 8px;
        padding: 10px;
        color: var(--accent-orange);
        font-size: 12px;
        text-align: center;
        margin-top: 8px;
    }
    
    .status-ok {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 8px;
        padding: 10px;
        color: var(--accent-emerald);
        font-size: 12px;
        text-align: center;
        margin-top: 8px;
    }
    
    .ctx-file {
        padding: 6px 0;
        font-size: 12px;
        color: var(--text-secondary);
    }
    
    .ctx-ok { color: var(--accent-emerald) !important; }
    
    .foot {
        text-align: center;
        padding: 20px;
        border-top: 1px solid var(--glass-border);
        margin-top: 20px;
        font-size: 11px;
        color: var(--text-secondary);
    }
    
    .foot b { color: var(--accent-green); }
    
    /* Markdown - Compact */
    .stMarkdown { color: var(--text-primary) !important; }
    .stMarkdown h2 { 
        color: var(--accent-emerald) !important; 
        font-size: 16px !important;
        margin: 8px 0 6px 0 !important;
    }
    .stMarkdown h3 { 
        color: var(--text-primary) !important; 
        font-size: 14px !important;
        margin: 6px 0 4px 0 !important;
    }
    .stMarkdown strong { color: var(--accent-emerald) !important; }
    .stMarkdown p, .stMarkdown li { 
        color: var(--text-secondary) !important;
        font-size: 13px !important;
        line-height: 1.5 !important;
        margin: 4px 0 !important;
    }
    
    .stMarkdown table { 
        width: 100% !important; 
        margin: 8px 0 !important;
        font-size: 13px !important;
    }
    .stMarkdown th {
        background: rgba(16, 185, 129, 0.1) !important;
        color: var(--accent-emerald) !important;
        padding: 8px !important;
        font-size: 12px !important;
    }
    .stMarkdown td {
        padding: 8px !important;
        border-bottom: 1px solid var(--glass-border) !important;
        color: var(--text-secondary) !important;
        font-size: 12px !important;
    }
    .stMarkdown blockquote {
        border-left: 3px solid var(--accent-green) !important;
        background: rgba(16, 185, 129, 0.05) !important;
        padding: 8px 12px !important;
        border-radius: 0 8px 8px 0 !important;
        margin: 8px 0 !important;
        font-size: 13px !important;
    }
    .stMarkdown ul, .stMarkdown ol {
        margin: 4px 0 !important;
        padding-left: 20px !important;
    }
    
    hr { border-color: var(--glass-border) !important; }
    
    .main .block-container { padding-bottom: 100px !important; }
</style>
""", unsafe_allow_html=True)


def load_context_files():
    context = {}
    kiro_dir = Path(__file__).parent / ".kiro"
    for f in ["product.md", "system.md", "garhwal_context.md", "kumaon_context.md"]:
        fp = kiro_dir / f
        context[f.replace(".md", "")] = fp.read_text(encoding="utf-8") if fp.exists() else ""
    return context


def detect_region(text: str) -> str:
    t = text.lower()
    g = ["dehradun", "mussoorie", "rishikesh", "haridwar", "tehri", "uttarkashi", "chamoli", "rudraprayag", "pauri", "lansdowne", "gangotri", "yamunotri", "kedarnath", "badrinath", "garhwal", "landour", "dhanaulti"]
    k = ["nainital", "almora", "pithoragarh", "bageshwar", "champawat", "kathgodam", "bhimtal", "sattal", "naukuchiatal", "ranikhet", "munsiyari", "kumaon", "binsar", "jageshwar", "kausani"]
    gs, ks = sum(1 for x in g if x in t), sum(1 for x in k if x in t)
    return "garhwal" if gs > ks else "kumaon" if ks > gs else "general"


def get_system_prompt(ctx: dict, region: str) -> str:
    base = ctx.get("system", "")
    prod = ctx.get("product", "")
    if region == "garhwal":
        rc, ri = ctx.get("garhwal_context", ""), "GARHWAL: Use Bhulla, Bal, Semanya."
    elif region == "kumaon":
        rc, ri = ctx.get("kumaon_context", ""), "KUMAON: Use Daju, Thehra, Pailag."
    else:
        rc, ri = ctx.get("garhwal_context", "") + ctx.get("kumaon_context", ""), "GENERAL"
    return f"{base}\n\n{ri}\n\n{prod}\n\n{rc}"


def get_response(msgs: list, ctx: dict, region: str) -> str:
    key = os.getenv("GROQ_API_KEY", "")
    if not key or not GROQ_AVAILABLE:
        return demo_response(msgs[-1]["content"], region)
    try:
        client = Groq(api_key=key)
        r = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": get_system_prompt(ctx, region)}] + msgs,
            temperature=0.7, max_tokens=1024
        )
        return r.choices[0].message.content
    except:
        return demo_response(msgs[-1]["content"], region)


def demo_response(inp: str, region: str) -> str:
    t = inp.lower()
    
    if any(w in t for w in ["food", "eat", "sweet", "mithai"]):
        if region == "kumaon" or "almora" in t or "nainital" in t:
            return """## 🙏 Pailag, Daju!

**Real Kumaoni flavors**, thehra!

### 🍬 Bal Mithai
| 📍 Where | Kheem Singh's, Mall Road, Almora |
|----------|----------------------------------|
| 💡 Tip | Fresh khoya, butter paper wrap |

### Must-Try
- **Bhatt ki Churkani** — Black soybean curry
- **Aloo ke Gutke** — Potatoes with Jamboo herb
- **Singori** — Khoya in Maalu leaf

### 🍜 Nainital Spots
- Sonam's Momos @ Tibetan Market
- Sakley's (est. 1944)
- Cafe Chica

> Skip Maggi—this is real Pahadi food!"""
        return """## 🙏 Semanya, Bhulla!

**Real Garhwali food**, bal!

### 🍲 Kafuli (State Food)
| 🥬 What | Spinach + fenugreek in iron kadhai |
|---------|-----------------------------------|
| ✨ Secret | Iron makes it dark green |

### Must-Try
- **Phaanu** — Thick lentil soup
- **Chainsoo** — Roasted black gram dal
- **Bhang ki Chutney** — Hemp seeds (legal!)

### 🍳 Mussoorie
- Lovely Omelette Centre
- Char Dukan
- Landour Bakehouse

> Skip Maggi—that's tourist stuff, bal!"""
    
    if any(w in t for w in ["visit", "place", "go", "see", "travel"]):
        if region == "kumaon" or "nainital" in t:
            return """## 🙏 Pailag!

**Local spots** in Kumaon, thehra:

### Skip Crowds
| ❌ Crowded | ✅ Local Gem |
|-----------|-------------|
| Nainital Lake | Sattal, Naukuchiatal |
| Mall Road | Tibetan Market |

### Hidden Gems
- **Binsar** — 300+ bird species
- **Jageshwar** — 124 ancient temples
- **Pangot** — World-class birding

> Hill Time = 30km/hour!"""
        return """## 🙏 Semanya, Bhulla!

**Real Garhwal**, bal:

### Skip Traps
| ❌ Crowded | ✅ Better |
|-----------|----------|
| Gun Hill | Landour |
| Kempty Falls | Neer Garh |

### Landour Walk
1. Char Dukan — Bun Omelette
2. Gol Chakkar
3. Lal Tibba sunset

> Locals value silence here!"""
    
    if any(w in t for w in ["transport", "jeep", "taxi", "reach"]):
        return """## 🚗 Transport Tips

### Hill Time Rule
| Speed | 30 km/hour |
|-------|-----------|
| Monsoon | 1.5x time |

### Shared Jeep
- Leave only when **FULL**
- Ask "How many seats empty?"
- **Front seat** = best views

### Hill Code
1. Uphill has right of way
2. Horn at blind curves
3. No night driving

> Stay safe!"""
    
    if any(w in t for w in ["slang", "word", "phrase", "speak", "language", "say"]):
        return """## 🗣️ Pahadi Slang Guide

### Greetings
| Region | Greeting | Meaning |
|--------|----------|---------|
| Garhwal | **Semanya** | Hello |
| Kumaon | **Pailag** | I touch your feet |

### Brother Terms
| Garhwal | Kumaon | Use For |
|---------|--------|---------|
| **Bhulla** | **Daju** | Waiters, drivers |

### Filler Words
- Garhwal: **"Bal"** — "It's cold, bal!"
- Kumaon: **"Thehra"** — "He went, thehra."

> Use these and locals will love you!"""
    
    term = "Daju" if region == "kumaon" else "Bhulla"
    greet = "Pailag" if region == "kumaon" else "Semanya"
    
    return f"""## 🙏 {greet}, {term}!

Welcome to **Uttarakhand** — Devbhoomi!

I'm your **Pahadi Guide** — a local friend.

### Ask About
| 🍲 Food | Local cuisine |
| 📍 Places | Hidden gems |
| 🚗 Transport | Hill travel |
| 🗣️ Slang | Local phrases |

### Try
- "What to eat in Almora?"
- "Hidden spots in Mussoorie?"
- "How to reach Nainital?"

> What to explore, {term}?"""


def main():
    ctx = load_context_files()
    
    # Hero
    st.markdown("""
    <div class="hero-box">
        <div class="hero-badge">🏔️ Kiro Heroes Week 5</div>
        <div class="hero-title">Pahadi Guide</div>
        <div class="hero-sub">AI-powered local companion for Uttarakhand</div>
        <div class="chips">
            <div class="chip">🗣️ Slang</div>
            <div class="chip">🍲 Food</div>
            <div class="chip">🚗 Transport</div>
            <div class="chip">📍 Gems</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="side-label">About</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="side-card">
            <p style="color: #94a3b8; font-size: 13px; margin: 0;">
                Hyper-local AI guide for <b style="color: #34d399;">Garhwal</b> 
                and <b style="color: #93c5fd;">Kumaon</b> regions.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="side-label">Quick Actions</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🍲 Food", use_container_width=True):
                st.session_state.qa = "What are must-try local foods?"
        with c2:
            if st.button("📍 Places", use_container_width=True):
                st.session_state.qa = "What are hidden gems tourists miss?"
        c3, c4 = st.columns(2)
        with c3:
            if st.button("🗣️ Slang", use_container_width=True):
                st.session_state.qa = "Teach me local Pahadi slang"
        with c4:
            if st.button("🚗 Travel", use_container_width=True):
                st.session_state.qa = "How does hill transport work?"
        
        st.markdown('<div class="side-label">API Settings</div>', unsafe_allow_html=True)
        key = st.text_input("api", type="password", label_visibility="collapsed", placeholder="Groq API Key (optional)")
        if key:
            os.environ["GROQ_API_KEY"] = key
        
        # Add Groq console link
        st.markdown('<a href="https://console.groq.com" target="_blank" class="api-link">🔑 Get API Key → console.groq.com</a>', unsafe_allow_html=True)
        
        if not os.getenv("GROQ_API_KEY") or not GROQ_AVAILABLE:
            st.markdown('<div class="status-demo">🎮 Demo Mode</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-ok">✅ Connected</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="side-label">Context Files</div>', unsafe_allow_html=True)
        for n, c in ctx.items():
            icon = "✅" if c else "❌"
            cls = "ctx-ok" if c else ""
            st.markdown(f'<div class="ctx-file {cls}">{icon} {n}.md</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="foot">Built for <b>Kiro Heroes</b><br>🏔️ <b>Devbhoomi</b> 🏔️</div>', unsafe_allow_html=True)
    
    # Chat
    if "msgs" not in st.session_state:
        st.session_state.msgs = []
    
    for m in st.session_state.msgs:
        with st.chat_message(m["role"], avatar="🧑" if m["role"] == "user" else "🏔️"):
            st.markdown(m["content"])
    
    if "qa" in st.session_state and st.session_state.qa:
        prompt = st.session_state.qa
        st.session_state.qa = None
        st.session_state.msgs.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑"):
            st.markdown(prompt)
        region = detect_region(prompt)
        with st.chat_message("assistant", avatar="🏔️"):
            with st.spinner("🏔️"):
                resp = get_response(st.session_state.msgs, ctx, region)
                st.markdown(resp)
        st.session_state.msgs.append({"role": "assistant", "content": resp})
        st.rerun()
    
    if prompt := st.chat_input("Ask about Uttarakhand..."):
        st.session_state.msgs.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑"):
            st.markdown(prompt)
        
        region = detect_region(prompt)
        if region == "garhwal":
            st.markdown('<div class="badge-garhwal">🏔️ Garhwal Region</div>', unsafe_allow_html=True)
        elif region == "kumaon":
            st.markdown('<div class="badge-kumaon">🏔️ Kumaon Region</div>', unsafe_allow_html=True)
        
        with st.chat_message("assistant", avatar="🏔️"):
            with st.spinner("🏔️"):
                resp = get_response(st.session_state.msgs, ctx, region)
                st.markdown(resp)
        st.session_state.msgs.append({"role": "assistant", "content": resp})


if __name__ == "__main__":
    main()
