"""
Smart Resume Analyzer — with Login Page & Student Dashboard
A Streamlit web app with a beautiful glassmorphic login page,
a detailed student dashboard, and resume ATS analysis.
"""

import streamlit as st
import re
from collections import Counter

# ═══════════════════════════════════════════════════════════════════
#  PAGE CONFIG  (must be first Streamlit call)
# ═══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="ResumeIQ – Smart Resume Analyzer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ═══════════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ═══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp { height: 100%; }
.stApp {
    font-family: 'DM Sans', sans-serif;
    background: #0a0e1a;
    color: #e8eaf6;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Animated background ─────────────────────────────────────── */
.starfield {
    position: fixed; inset: 0; z-index: 0;
    background:
        radial-gradient(ellipse at 20% 50%, rgba(99,102,241,.18) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 20%, rgba(168,85,247,.15) 0%, transparent 55%),
        radial-gradient(ellipse at 60% 80%, rgba(59,130,246,.12) 0%, transparent 50%),
        linear-gradient(135deg, #0a0e1a 0%, #0d1224 50%, #0a0e1a 100%);
}
.star {
    position: absolute; border-radius: 50%;
    background: #fff; animation: twinkle linear infinite;
}
@keyframes twinkle {
    0%,100% { opacity:.1; transform:scale(1); }
    50%      { opacity:.9; transform:scale(1.4); }
}
.grid-overlay {
    position: fixed; inset: 0; z-index: 0;
    background-image:
        linear-gradient(rgba(99,102,241,.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,102,241,.05) 1px, transparent 1px);
    background-size: 60px 60px;
}

/* ── Login card ──────────────────────────────────────────────── */
@keyframes fadeSlideUp {
    from { opacity:0; transform:translateY(40px); }
    to   { opacity:1; transform:translateY(0); }
}
.login-logo {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem; font-weight: 900;
    background: linear-gradient(135deg, #818cf8, #c084fc, #60a5fa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    text-align: center; margin-bottom: .2rem; line-height: 1.1;
    animation: fadeSlideUp .6s ease both;
}
.login-tagline {
    text-align: center; color: rgba(255,255,255,.4);
    font-size: .82rem; letter-spacing: .1em; text-transform: uppercase;
    margin-bottom: 2rem;
    animation: fadeSlideUp .7s ease both;
}
.login-footer {
    text-align: center; font-size: .76rem;
    color: rgba(255,255,255,.25); margin-top: 1.2rem;
}

/* ── Input overrides ─────────────────────────────────────────── */
div[data-testid="stTextInput"] input,
div[data-testid="stTextInput"] input[type="password"],
div[data-testid="stTextInput"] input[type="text"] {
    background: rgba(10,14,30,.9) !important;
    border: 1px solid rgba(129,140,248,.3) !important;
    border-radius: 12px !important;
    color: #e8eaf6 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: .92rem !important;
    padding: .7rem 1rem !important;
    transition: border-color .2s, box-shadow .2s;
    caret-color: #818cf8;
}
div[data-testid="stTextInput"] input::placeholder { color: rgba(255,255,255,.3) !important; }
div[data-testid="stTextInput"] input:focus {
    border-color: rgba(129,140,248,.75) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,.22) !important;
    background: rgba(15,20,45,.95) !important;
}
div[data-testid="stTextInput"] label,
div[data-testid="stTextArea"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label {
    color: rgba(255,255,255,.6) !important;
    font-size: .82rem !important;
    font-weight: 500 !important;
    font-family: 'DM Sans', sans-serif !important;
}
textarea,
div[data-testid="stTextArea"] textarea {
    background: rgba(10,14,30,.9) !important;
    border: 1px solid rgba(129,140,248,.3) !important;
    border-radius: 12px !important;
    color: #e8eaf6 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: .92rem !important;
    caret-color: #818cf8;
    line-height: 1.6 !important;
}
div[data-testid="stTextArea"] textarea::placeholder {
    color: rgba(255,255,255,.3) !important;
}
div[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(129,140,248,.75) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,.22) !important;
    background: rgba(15,20,45,.95) !important;
    color: #ffffff !important;
}
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: .7rem 1.5rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: .95rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    transition: all .2s !important;
    box-shadow: 0 8px 24px rgba(99,102,241,.35) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 32px rgba(99,102,241,.5) !important;
}

/* ── Dashboard header ────────────────────────────────────────── */
.dash-header {
    padding: 1.5rem 2.5rem .75rem;
    border-bottom: 1px solid rgba(255,255,255,.06);
    display: flex; align-items: center; justify-content: space-between;
}
.dash-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.7rem; font-weight: 900;
    background: linear-gradient(135deg, #818cf8, #c084fc);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.dash-greeting {
    color: rgba(255,255,255,.35); font-size: .85rem; margin-left: 1rem;
}

/* ── Profile hero ────────────────────────────────────────────── */
.profile-hero {
    background: linear-gradient(135deg,
        rgba(99,102,241,.2), rgba(139,92,246,.15), rgba(96,165,250,.12));
    border: 1px solid rgba(255,255,255,.1);
    border-radius: 24px; padding: 2.2rem 2.5rem;
    display: flex; align-items: center; gap: 2rem;
    margin-bottom: 2rem; position: relative; overflow: hidden;
    animation: fadeSlideUp .5s ease both;
}
.profile-hero::before {
    content:''; position:absolute; top:-60px; right:-60px;
    width:220px; height:220px; border-radius:50%;
    background:radial-gradient(circle, rgba(129,140,248,.2), transparent 70%);
    pointer-events:none;
}
.avatar-ring {
    width: 88px; height: 88px; border-radius: 50%;
    background: linear-gradient(135deg, #6366f1, #8b5cf6, #60a5fa);
    display: flex; align-items: center; justify-content: center;
    font-size: 2.2rem; flex-shrink: 0; font-weight: 700; color: #fff;
    box-shadow: 0 0 0 4px rgba(99,102,241,.3), 0 8px 24px rgba(0,0,0,.4);
}
.profile-name {
    font-family: 'Playfair Display', serif;
    font-size: 1.9rem; font-weight: 700; color: #e8eaf6; margin-bottom: .2rem;
}
.profile-role {
    color: #818cf8; font-size: .85rem; font-weight: 500;
    letter-spacing: .06em; text-transform: uppercase; margin-bottom: .6rem;
}
.badges { display:flex; gap:.5rem; flex-wrap:wrap; }
.badge {
    padding: .25rem .8rem; border-radius: 20px;
    font-size: .72rem; font-weight: 600; letter-spacing: .04em;
}
.badge-blue   { background:rgba(96,165,250,.15); color:#60a5fa; border:1px solid rgba(96,165,250,.3); }
.badge-purple { background:rgba(139,92,246,.15); color:#a78bfa; border:1px solid rgba(139,92,246,.3); }
.badge-amber  { background:rgba(251,191,36,.15);  color:#fbbf24; border:1px solid rgba(251,191,36,.3); }
.badge-green  { background:rgba(52,211,153,.15);  color:#34d399; border:1px solid rgba(52,211,153,.3); }

/* ── Info cards ──────────────────────────────────────────────── */
.info-card {
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 18px; padding: 1.4rem;
    transition: all .2s; cursor: default;
    position: relative; overflow: hidden;
    animation: fadeSlideUp .5s ease both;
}
.info-card:hover {
    background: rgba(255,255,255,.07);
    border-color: rgba(99,102,241,.4);
    transform: translateY(-3px);
    box-shadow: 0 16px 40px rgba(0,0,0,.4);
}
.info-card::after {
    content:''; position:absolute;
    top:0; left:0; right:0; height:2px; border-radius:18px 18px 0 0;
}
.c-indigo::after  { background:linear-gradient(90deg,#6366f1,#818cf8); }
.c-purple::after  { background:linear-gradient(90deg,#8b5cf6,#c084fc); }
.c-blue::after    { background:linear-gradient(90deg,#3b82f6,#60a5fa); }
.c-emerald::after { background:linear-gradient(90deg,#059669,#34d399); }
.c-amber::after   { background:linear-gradient(90deg,#d97706,#fbbf24); }
.c-rose::after    { background:linear-gradient(90deg,#e11d48,#fb7185); }
.c-sky::after     { background:linear-gradient(90deg,#0284c7,#38bdf8); }
.c-teal::after    { background:linear-gradient(90deg,#0d9488,#2dd4bf); }

.card-icon {
    width:42px; height:42px; border-radius:11px;
    display:flex; align-items:center; justify-content:center;
    font-size:1.2rem; margin-bottom:.9rem;
}
.ci-indigo  { background:rgba(99,102,241,.2); }
.ci-purple  { background:rgba(139,92,246,.2); }
.ci-blue    { background:rgba(59,130,246,.2); }
.ci-emerald { background:rgba(5,150,105,.2); }
.ci-amber   { background:rgba(217,119,6,.2); }
.ci-rose    { background:rgba(225,29,72,.2); }
.ci-sky     { background:rgba(2,132,199,.2); }
.ci-teal    { background:rgba(13,148,136,.2); }

.card-label { font-size:.7rem; color:rgba(255,255,255,.38); font-weight:500; letter-spacing:.08em; text-transform:uppercase; margin-bottom:.3rem; }
.card-value { font-size:.95rem; color:#e8eaf6; font-weight:600; word-break:break-all; }

/* ── Stat strip ──────────────────────────────────────────────── */
.stat-strip { display:grid; gap:1rem; margin-bottom:2rem; }
.stat-box {
    background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.08);
    border-radius:16px; padding:1.25rem; text-align:center;
    transition:transform .2s;
}
.stat-box:hover { transform:translateY(-2px); }
.stat-num {
    font-family:'Playfair Display',serif; font-size:2rem; font-weight:700;
    background:linear-gradient(135deg,#818cf8,#c084fc);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.stat-lbl { font-size:.72rem; color:rgba(255,255,255,.38); margin-top:.2rem; letter-spacing:.05em; text-transform:uppercase; }

/* ── Timeline ────────────────────────────────────────────────── */
.timeline { position:relative; padding-left:1.5rem; }
.timeline::before {
    content:''; position:absolute; left:0; top:8px; bottom:8px; width:2px;
    background:linear-gradient(180deg,#6366f1,transparent);
}
.tl-item { position:relative; margin-bottom:1.5rem; padding-left:.75rem; }
.tl-item::before {
    content:''; position:absolute; left:-1.55rem; top:6px;
    width:10px; height:10px; border-radius:50%; background:#6366f1;
    box-shadow:0 0 0 3px rgba(99,102,241,.25);
}
.tl-title { font-weight:600; color:#e8eaf6; font-size:.92rem; }
.tl-sub   { color:#818cf8; font-size:.8rem; margin:.12rem 0; }
.tl-date  { color:rgba(255,255,255,.32); font-size:.73rem; }

/* ── Skills ──────────────────────────────────────────────────── */
.skills-wrap { display:flex; flex-wrap:wrap; gap:.5rem; }
.skill-tag {
    padding:.35rem .9rem; border-radius:30px;
    background:rgba(99,102,241,.15); border:1px solid rgba(99,102,241,.3);
    color:#a5b4fc; font-size:.78rem; font-weight:500;
    transition:all .15s;
}
.skill-tag:hover { background:rgba(99,102,241,.3); color:#e0e7ff; }

/* ── Section title ───────────────────────────────────────────── */
.section-title {
    font-family:'Playfair Display',serif;
    font-size:1.3rem; font-weight:700; color:#e8eaf6;
    margin-bottom:1rem; display:flex; align-items:center; gap:.4rem;
}
.accent { color:#818cf8; }

/* ── ATS score ───────────────────────────────────────────────── */
.score-ring {
    text-align:center; padding:1.5rem;
    background:rgba(255,255,255,.03);
    border-radius:16px; border:1px solid rgba(255,255,255,.06);
}
.score-big {
    font-family:'Playfair Display',serif; font-size:3.5rem; font-weight:900;
    background:linear-gradient(135deg,#34d399,#60a5fa);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.score-big.mid { background:linear-gradient(135deg,#fbbf24,#fb923c); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.score-big.low { background:linear-gradient(135deg,#f87171,#fb7185); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }

/* ── Keyword pills ───────────────────────────────────────────── */
.pill-wrap { display:flex; flex-wrap:wrap; gap:.4rem; }
.kw-pill { padding:.28rem .7rem; border-radius:20px; font-size:.73rem; font-weight:600; }
.kw-green { background:rgba(52,211,153,.15); color:#34d399; border:1px solid rgba(52,211,153,.3); }
.kw-red   { background:rgba(248,113,113,.15); color:#f87171; border:1px solid rgba(248,113,113,.3); }

/* ── Tip cards ───────────────────────────────────────────────── */
.tip-card {
    background:rgba(99,102,241,.08); border:1px solid rgba(99,102,241,.2);
    border-radius:12px; padding:.9rem 1.1rem; margin-bottom:.65rem;
    font-size:.86rem; color:#c7d2fe; line-height:1.55;
}

/* ── Tabs ────────────────────────────────────────────────────── */
div[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background:rgba(255,255,255,.04) !important;
    border-radius:12px !important; padding:.25rem !important;
    gap:.2rem !important; border:1px solid rgba(255,255,255,.07) !important;
}
div[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius:9px !important; color:rgba(255,255,255,.5) !important;
    font-family:'DM Sans',sans-serif !important; font-weight:500 !important;
    padding:.5rem 1.1rem !important;
}
div[data-testid="stTabs"] [aria-selected="true"] {
    background:linear-gradient(135deg,#6366f1,#8b5cf6) !important;
    color:#fff !important;
}

/* ── File uploader ───────────────────────────────────────────── */
div[data-testid="stFileUploader"] {
    background:rgba(255,255,255,.03) !important;
    border:1.5px dashed rgba(99,102,241,.4) !important;
    border-radius:14px !important;
}

/* ── Progress bar ────────────────────────────────────────────── */
.stProgress > div > div { border-radius:10px !important; }
.stProgress > div { background:rgba(255,255,255,.07) !important; border-radius:10px !important; }

/* ── Selectbox ───────────────────────────────────────────────── */
div[data-testid="stSelectbox"] > div > div {
    background: rgba(10,14,30,.9) !important;
    border: 1px solid rgba(129,140,248,.3) !important;
    border-radius: 12px !important;
    color: #e8eaf6 !important;
}
div[data-testid="stSelectbox"] > div > div > div,
div[data-testid="stSelectbox"] span,
div[data-testid="stSelectbox"] p {
    color: #e8eaf6 !important;
}

/* ── Number input ────────────────────────────────────────────── */
div[data-testid="stNumberInput"] input {
    background: rgba(10,14,30,.9) !important;
    border: 1px solid rgba(129,140,248,.3) !important;
    border-radius: 12px !important;
    color: #e8eaf6 !important;
    font-family: 'DM Sans', sans-serif !important;
    caret-color: #818cf8;
}
div[data-testid="stNumberInput"] input:focus {
    border-color: rgba(129,140,248,.75) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,.22) !important;
    background: rgba(15,20,45,.95) !important;
}

/* ── Global text visibility fix for all input-like widgets ───── */
.stTextInput input, .stTextArea textarea,
.stNumberInput input, .stSelectbox div[role="combobox"] {
    color: #e8eaf6 !important;
}

/* typed text inside ANY widget must be light */
input, textarea, select {
    color: #e8eaf6 !important;
}

/* Streamlit renders typed text as a div inside BaseWeb inputs sometimes */
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea {
    color: #e8eaf6 !important;
    background: rgba(10,14,30,.9) !important;
}

hr { border-color:rgba(255,255,255,.07) !important; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
#  STARFIELD BACKGROUND
# ═══════════════════════════════════════════════════════════════════
def render_bg():
    import random, hashlib
    # Deterministic stars so they don't re-randomise on every rerun
    seed = 42
    random.seed(seed)
    stars = ""
    for i in range(80):
        x, y   = random.randint(0,100), random.randint(0,100)
        sz     = round(random.uniform(1, 3), 1)
        dur    = round(random.uniform(2, 7), 1)
        delay  = round(random.uniform(0, 5), 1)
        stars += (f'<div class="star" style="left:{x}%;top:{y}%;'
                  f'width:{sz}px;height:{sz}px;'
                  f'animation-duration:{dur}s;animation-delay:{delay}s;"></div>')
    st.markdown(f'<div class="starfield">{stars}</div>'
                '<div class="grid-overlay"></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
#  SESSION STATE
# ═══════════════════════════════════════════════════════════════════
def init_state():
    defaults = dict(
        logged_in=False,
        student=dict(
            name="", email="", mobile="", dob="", gender="",
            education="", branch="", passout_year="", cgpa="",
            college="", city="", linkedin="", github="",
            skills=[], languages=[],
            projects=0, internships=0, certifications=0,
            ats_score=None,
        )
    )
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()
s = st.session_state.student   # shorthand

# ═══════════════════════════════════════════════════════════════════
#  NLP HELPERS
# ═══════════════════════════════════════════════════════════════════
STOP_WORDS = {
    "a","an","the","and","or","but","in","on","at","to","for","of","with",
    "by","from","is","are","was","were","be","been","have","has","had",
    "do","does","did","will","would","could","should","may","might","i",
    "you","he","she","it","we","they","this","that","these","those","my",
    "your","his","her","its","our","their","me","him","us","them","what",
    "which","who","how","when","where","why","all","any","both","each",
    "more","most","other","some","such","no","not","only","own","same",
    "than","too","very","just","as","if","so","then","about","up","down",
    "out","can","also","etc","per","new","use","used","using","make","get",
    "well","work","need","able","must","good","great","strong","experience",
    "knowledge","skills","skill","ability","team","role","job","company",
    "looking","seeking","required","preferred","including","across",
}

def tokenize(text):
    text = re.sub(r"[^a-z0-9\s+#]", " ", text.lower())
    return [t for t in text.split() if t not in STOP_WORDS and len(t) > 2]

def extract_keywords(text, top_n=50):
    return [w for w, _ in Counter(tokenize(text)).most_common(top_n)]

def compute_ats(resume_text, jd_keywords):
    tokens  = set(tokenize(resume_text))
    matched = [k for k in jd_keywords if k in tokens]
    missing = [k for k in jd_keywords if k not in tokens]
    score   = round(len(matched)/len(jd_keywords)*100, 1) if jd_keywords else 0.0
    return score, matched, missing

def extract_pdf(f):
    try:
        from pypdf import PdfReader; import io
        return "\n".join(p.extract_text() or "" for p in PdfReader(io.BytesIO(f.read())).pages)
    except Exception as e:
        st.error(f"PDF error: {e}"); return ""

def extract_docx(f):
    try:
        import docx, io
        return "\n".join(p.text for p in docx.Document(io.BytesIO(f.read())).paragraphs)
    except Exception as e:
        st.error(f"DOCX error: {e}"); return ""

def build_tips(score, missing):
    tips = []
    if   score < 40: tips.append("⚠️ Your resume matches fewer than 40% of job keywords. Consider a significant rewrite to align with this role.")
    elif score < 70: tips.append("📝 Moderate match. Tailor your resume more closely to the job description language.")
    else:            tips.append("✅ Great match! Fine-tune a few areas and you are ready to apply.")
    if missing:
        tips.append(f"🔑 Naturally weave in these missing keywords: **{', '.join(missing[:8])}**.")
    tips += [
        "📌 Mirror exact terminology from the job posting (e.g. 'REST API' not 'RESTful API').",
        "📐 Use a simple single-column layout — ATS parsers struggle with tables and text boxes.",
        "📊 Quantify achievements wherever possible (e.g. 'Improved speed by 35%').",
        "🗂️ Add a dedicated **Skills** section so parsers can find keywords instantly.",
        "🔗 Mirror the job title in your resume summary / objective statement.",
    ]
    return tips

# ═══════════════════════════════════════════════════════════════════
#  LOGIN PAGE
# ═══════════════════════════════════════════════════════════════════
def login_page():
    render_bg()

    # Centre the form using columns — no raw HTML overlay so nothing blocks inputs
    _, mid, _ = st.columns([1, 1.1, 1])
    with mid:
        # Card styling applied to the column container via CSS class trick
        st.markdown("""
        <div style="
            background:rgba(255,255,255,.06);
            backdrop-filter:blur(20px);
            -webkit-backdrop-filter:blur(20px);
            border:1px solid rgba(255,255,255,.12);
            border-radius:28px;
            padding:2.5rem 2.2rem 1.8rem;
            box-shadow:0 24px 64px rgba(0,0,0,.55), 0 0 0 1px rgba(255,255,255,.04) inset;
            margin-top:3rem;
        ">
        <div class="login-logo">ResumeIQ</div>
        <div class="login-tagline">✦ Student Career Intelligence Platform ✦</div>
        </div>
        """, unsafe_allow_html=True)

        # Input card wrapper
        st.markdown("""
        <div style="
            background:rgba(255,255,255,.05);
            backdrop-filter:blur(16px);
            -webkit-backdrop-filter:blur(16px);
            border:1px solid rgba(255,255,255,.1);
            border-radius:20px;
            padding:1.8rem 1.6rem 1.4rem;
            margin-top:.8rem;
            box-shadow:0 12px 40px rgba(0,0,0,.4);
        ">
        <p style="color:rgba(255,255,255,.45);font-size:.8rem;letter-spacing:.06em;
                  text-transform:uppercase;margin-bottom:1rem;text-align:center;">
            🔐 Sign in to your account
        </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)

        name  = st.text_input("👤  Full Name",      placeholder="e.g. Arjun Sharma",       key="ln_name")
        email = st.text_input("📧  Email Address",  placeholder="arjun@example.com",        key="ln_email")
        pwd   = st.text_input("🔒  Password",        type="password",
                               placeholder="Create or enter your password",                   key="ln_pwd")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚀  Get Started →", use_container_width=True):
            if not name.strip():
                st.error("Please enter your name.")
            elif "@" not in email or "." not in email:
                st.error("Please enter a valid email address.")
            elif len(pwd) < 4:
                st.error("Password must be at least 4 characters.")
            else:
                st.session_state.logged_in   = True
                st.session_state.student["name"]  = name.strip()
                st.session_state.student["email"] = email.strip()
                st.rerun()

        st.markdown("""
        <div class="login-footer">
            🔐 Your data stays on your device &nbsp;·&nbsp; No account stored
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
#  DASHBOARD
# ═══════════════════════════════════════════════════════════════════
def dashboard():
    render_bg()

    # ── Top bar ─────────────────────────────────────────────────
    bar_l, bar_r = st.columns([5, 1])
    with bar_l:
        first = s["name"].split()[0] if s["name"] else "Student"
        st.markdown(f"""
        <div style="padding:1.5rem 2.5rem .75rem;">
            <span class="dash-logo">ResumeIQ</span>
            <span class="dash-greeting">Welcome back, {first} 👋</span>
        </div>""", unsafe_allow_html=True)
    with bar_r:
        st.markdown("<div style='padding:1.5rem 2rem .75rem 0;text-align:right'>",
                    unsafe_allow_html=True)
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='padding:0 2.5rem 3rem;'>", unsafe_allow_html=True)

    # ── Tabs ────────────────────────────────────────────────────
    t_profile, t_edu, t_skills, t_analyzer = st.tabs([
        "🎓  My Profile", "🏛️  Education", "🛠️  Skills & Projects", "📊  Resume Analyzer"
    ])

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 1 — PROFILE
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with t_profile:

        # Avatar initials
        words    = (s["name"] or "S U").split()
        initials = "".join(w[0].upper() for w in words[:2])

        # ATS badge
        ats_badge = ""
        if s["ats_score"] is not None:
            c = "#34d399" if s["ats_score"]>=70 else "#fbbf24" if s["ats_score"]>=40 else "#f87171"
            ats_badge = (f'<span class="badge" style="background:rgba(52,211,153,.12);'
                         f'color:{c};border:1px solid {c}55;">⚡ ATS {s["ats_score"]}%</span>')

        st.markdown(f"""
        <div class="profile-hero">
            <div class="avatar-ring">{initials}</div>
            <div>
                <div class="profile-name">{s['name'] or 'Your Name'}</div>
                <div class="profile-role">
                    {s['branch'] or 'Branch / Specialisation'} &nbsp;·&nbsp; {s['education'] or 'Degree'}
                </div>
                <div class="badges">
                    <span class="badge badge-blue">🏫 {s['college'] or 'College'}</span>
                    <span class="badge badge-purple">📅 Class of {s['passout_year'] or '----'}</span>
                    <span class="badge badge-amber">📍 {s['city'] or 'City'}</span>
                    {ats_badge}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Info cards (3 columns)
        cards = [
            ("c-indigo",  "ci-indigo",  "📧", "Email Address",   s["email"]   or "—"),
            ("c-purple",  "ci-purple",  "📱", "Mobile Number",   s["mobile"]  or "—"),
            ("c-blue",    "ci-blue",    "🎂", "Date of Birth",   s["dob"]     or "—"),
            ("c-emerald", "ci-emerald", "⚧️", "Gender",         s["gender"]  or "—"),
            ("c-amber",   "ci-amber",   "🏙️", "City / Location", s["city"]    or "—"),
            ("c-rose",    "ci-rose",    "🔗", "LinkedIn",        s["linkedin"]or "—"),
            ("c-sky",     "ci-sky",     "🐙", "GitHub",          s["github"]  or "—"),
            ("c-teal",    "ci-teal",    "📊", "CGPA / Marks",    s["cgpa"]    or "—"),
        ]
        cols = st.columns(4)
        for i, (card_cls, icon_cls, icon, label, value) in enumerate(cards):
            with cols[i % 4]:
                st.markdown(f"""
                <div class="info-card {card_cls}" style="animation-delay:{i*0.07}s">
                    <div class="card-icon {icon_cls}">{icon}</div>
                    <div class="card-label">{label}</div>
                    <div class="card-value">{value}</div>
                </div>
                """, unsafe_allow_html=True)

        # Edit form
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">✏️ Edit <span class="accent">Personal Details</span></div>',
                    unsafe_allow_html=True)

        f1, f2 = st.columns(2)
        with f1:
            s["name"]    = st.text_input("👤 Full Name",      value=s["name"],    key="p_name")
            s["email"]   = st.text_input("📧 Email Address",  value=s["email"],   key="p_email")
            s["mobile"]  = st.text_input("📱 Mobile Number",  value=s["mobile"],  key="p_mob",
                                          placeholder="+91 98765 43210")
            s["dob"]     = st.text_input("🎂 Date of Birth",  value=s["dob"],     key="p_dob",
                                          placeholder="DD / MM / YYYY")
        with f2:
            gender_opts  = ["", "Male", "Female", "Non-binary", "Prefer not to say"]
            gi = gender_opts.index(s["gender"]) if s["gender"] in gender_opts else 0
            s["gender"]   = st.selectbox("⚧️ Gender", gender_opts, index=gi, key="p_gen")
            s["city"]     = st.text_input("🏙️ City / Location",  value=s["city"],     key="p_city",
                                           placeholder="Hyderabad")
            s["linkedin"] = st.text_input("🔗 LinkedIn Profile",  value=s["linkedin"], key="p_li",
                                           placeholder="linkedin.com/in/yourname")
            s["github"]   = st.text_input("🐙 GitHub Profile",    value=s["github"],   key="p_gh",
                                           placeholder="github.com/yourname")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 2 — EDUCATION
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with t_edu:
        st.markdown('<div class="section-title">🏛️ Academic <span class="accent">Information</span></div>',
                    unsafe_allow_html=True)

        e1, e2 = st.columns(2)
        deg_opts  = ["","B.Tech","B.E","B.Sc","B.Com","BBA","M.Tech","M.Sc","MBA","Ph.D","Diploma","Other"]
        year_opts = [""] + [str(y) for y in range(2018, 2031)]

        with e1:
            di = deg_opts.index(s["education"]) if s["education"] in deg_opts else 0
            s["education"]    = st.selectbox("🎓 Degree / Level", deg_opts, index=di, key="e_deg")
            s["branch"]       = st.text_input("📘 Branch / Specialisation", value=s["branch"], key="e_br",
                                               placeholder="Computer Science & Engineering")
            s["college"]      = st.text_input("🏫 College / University", value=s["college"], key="e_col",
                                               placeholder="JNTU Hyderabad")
        with e2:
            yi = year_opts.index(s["passout_year"]) if s["passout_year"] in year_opts else 0
            s["passout_year"] = st.selectbox("📅 Pass-out Year", year_opts, index=yi, key="e_yr")
            s["cgpa"]         = st.text_input("📊 CGPA / Percentage", value=s["cgpa"], key="e_cg",
                                               placeholder="e.g. 8.7 / 87%")

        # Timeline
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">📅 Education <span class="accent">Timeline</span></div>',
                    unsafe_allow_html=True)
        st.markdown(f"""
        <div class="timeline">
            <div class="tl-item">
                <div class="tl-title">🎓 {s['education'] or 'Degree'} — {s['branch'] or 'Branch'}</div>
                <div class="tl-sub">{s['college'] or 'College / University'}</div>
                <div class="tl-date">Pass-out: {s['passout_year'] or '—'} &nbsp;·&nbsp; {s['cgpa'] or 'CGPA / %'}</div>
            </div>
            <div class="tl-item">
                <div class="tl-title">📘 Intermediate / 12th Standard</div>
                <div class="tl-sub">State Board / CBSE / ICSE</div>
                <div class="tl-date">Higher Secondary Education</div>
            </div>
            <div class="tl-item">
                <div class="tl-title">📗 10th Grade / SSC</div>
                <div class="tl-sub">State Board</div>
                <div class="tl-date">Secondary School Foundation</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Stats
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">📈 Quick <span class="accent">Stats</span></div>',
                    unsafe_allow_html=True)
        st.markdown(f"""
        <div class="stat-strip" style="grid-template-columns:repeat(4,1fr);">
            <div class="stat-box"><div class="stat-num">{s['cgpa'] or '—'}</div><div class="stat-lbl">CGPA / %</div></div>
            <div class="stat-box"><div class="stat-num">{s['passout_year'] or '—'}</div><div class="stat-lbl">Pass-out Year</div></div>
            <div class="stat-box"><div class="stat-num">{s['projects']}</div><div class="stat-lbl">Projects</div></div>
            <div class="stat-box"><div class="stat-num">{s['certifications']}</div><div class="stat-lbl">Certifications</div></div>
        </div>
        """, unsafe_allow_html=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 3 — SKILLS & PROJECTS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with t_skills:
        sk1, sk2 = st.columns(2)

        with sk1:
            st.markdown('<div class="section-title">🛠️ Technical <span class="accent">Skills</span></div>',
                        unsafe_allow_html=True)
            raw_sk = st.text_area("Skills (comma-separated)",
                value=", ".join(s["skills"]) if s["skills"] else "",
                placeholder="Python, SQL, React, Machine Learning, Git, Docker, Figma…", height=80, key="sk_in")
            if raw_sk.strip():
                s["skills"] = [x.strip() for x in raw_sk.split(",") if x.strip()]
            pills = " ".join(f'<span class="skill-tag">{sk}</span>' for sk in s["skills"]) or \
                    '<span style="color:rgba(255,255,255,.3)">No skills added yet.</span>'
            st.markdown(f'<div class="skills-wrap" style="margin-top:.75rem">{pills}</div>',
                        unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-title">🌐 Languages <span class="accent">Known</span></div>',
                        unsafe_allow_html=True)
            raw_lang = st.text_area("Languages (comma-separated)",
                value=", ".join(s["languages"]) if s["languages"] else "",
                placeholder="English, Telugu, Hindi, Tamil…", height=60, key="lang_in")
            if raw_lang.strip():
                s["languages"] = [x.strip() for x in raw_lang.split(",") if x.strip()]

            lang_pills = " ".join(f'<span class="skill-tag" style="background:rgba(96,165,250,.15);border-color:rgba(96,165,250,.3);color:#93c5fd">{l}</span>' for l in s["languages"]) or \
                         '<span style="color:rgba(255,255,255,.3)">No languages added yet.</span>'
            st.markdown(f'<div class="skills-wrap" style="margin-top:.75rem">{lang_pills}</div>',
                        unsafe_allow_html=True)

        with sk2:
            st.markdown('<div class="section-title">📁 Activity <span class="accent">Counter</span></div>',
                        unsafe_allow_html=True)
            s["projects"]       = st.number_input("🗂️ Projects Completed",   min_value=0, max_value=50, value=s["projects"],       key="sk_proj")
            s["internships"]    = st.number_input("💼 Internships Done",      min_value=0, max_value=20, value=s["internships"],    key="sk_int")
            s["certifications"] = st.number_input("🏆 Certifications Earned", min_value=0, max_value=50, value=s["certifications"], key="sk_cert")

            st.markdown(f"""
            <div class="stat-strip" style="grid-template-columns:repeat(3,1fr);margin-top:1.5rem;">
                <div class="stat-box"><div class="stat-num">{s['projects']}</div><div class="stat-lbl">Projects</div></div>
                <div class="stat-box"><div class="stat-num">{s['internships']}</div><div class="stat-lbl">Internships</div></div>
                <div class="stat-box"><div class="stat-num">{s['certifications']}</div><div class="stat-lbl">Certifications</div></div>
            </div>
            """, unsafe_allow_html=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TAB 4 — RESUME ANALYZER
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with t_analyzer:
        a1, a2 = st.columns(2)

        with a1:
            st.markdown('<div class="section-title">📄 Upload <span class="accent">Resume</span></div>',
                        unsafe_allow_html=True)
            uploaded    = st.file_uploader("PDF or DOCX", type=["pdf","docx"], key="resume_up")
            resume_text = ""
            if uploaded:
                with st.spinner("Extracting text…"):
                    resume_text = (extract_pdf(uploaded)
                                   if uploaded.name.lower().endswith(".pdf")
                                   else extract_docx(uploaded))
                if resume_text.strip():
                    st.success(f"✅ {len(resume_text.split())} words from *{uploaded.name}*")
                    with st.expander("📖 Preview text"):
                        st.text_area("", resume_text, height=180, label_visibility="collapsed")
                else:
                    st.warning("No text extracted — is this a scanned / image-only PDF?")

        with a2:
            st.markdown('<div class="section-title">💼 Job <span class="accent">Description</span></div>',
                        unsafe_allow_html=True)
            jd_text = st.text_area("Paste full job description here",
                                   height=220,
                                   placeholder="We are seeking a Data Analyst with experience in Python, SQL, Power BI…",
                                   key="jd_in")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🔍  Analyse My Resume Now", use_container_width=True):
            if not (uploaded and resume_text.strip()):
                st.error("Please upload your resume first.")
            elif not jd_text.strip():
                st.error("Please paste a job description.")
            else:
                with st.spinner("Running ATS analysis…"):
                    jd_kw              = extract_keywords(jd_text, 50)
                    score, matched, missing = compute_ats(resume_text, jd_kw)
                    tips               = build_tips(score, missing)
                s["ats_score"] = score

                st.markdown("---")
                st.markdown('<div class="section-title">📊 Analysis <span class="accent">Results</span></div>',
                            unsafe_allow_html=True)

                res1, res2 = st.columns([1, 2], gap="large")
                with res1:
                    cls   = "low" if score < 40 else "mid" if score < 70 else ""
                    label = "Strong Match 🟢" if score>=70 else "Moderate Match 🟡" if score>=40 else "Weak Match 🔴"
                    st.markdown(f"""
                    <div class="score-ring">
                        <div class="score-big {cls}">{score}%</div>
                        <div style="font-size:.78rem;color:rgba(255,255,255,.38);margin-top:.3rem">ATS Score</div>
                        <div style="font-weight:600;margin-top:.3rem;font-size:.88rem">{label}</div>
                        <div style="font-size:.75rem;color:rgba(255,255,255,.3);margin-top:.4rem">
                            {len(matched)} / {len(jd_kw)} keywords matched
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with res2:
                    st.markdown("**ATS Compatibility**")
                    st.progress(int(score) / 100)
                    st.caption(f"Your resume matched **{len(matched)}** out of **{len(jd_kw)}** important job-description terms.")

                    kw1, kw2 = st.columns(2)
                    with kw1:
                        st.markdown(f"**✅ Matched Keywords ({len(matched)})**")
                        pills = " ".join(
                            f'<span class="kw-pill kw-green">{k}</span>'
                            for k in sorted(matched)
                        )
                        st.markdown(f'<div class="pill-wrap">{pills or "—"}</div>',
                                    unsafe_allow_html=True)
                    with kw2:
                        st.markdown(f"**❌ Missing Keywords ({len(missing)})**")
                        pills = " ".join(
                            f'<span class="kw-pill kw-red">{k}</span>'
                            for k in missing[:25]
                        )
                        st.markdown(f'<div class="pill-wrap">{pills or "None — perfect! 🎉"}</div>',
                                    unsafe_allow_html=True)
                        if len(missing) > 25:
                            st.caption(f"…and {len(missing)-25} more.")

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="section-title">💡 Improvement <span class="accent">Tips</span></div>',
                            unsafe_allow_html=True)
                for tip in tips:
                    st.markdown(f'<div class="tip-card">{tip}</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # close padding div

# ═══════════════════════════════════════════════════════════════════
#  ROUTER
# ═══════════════════════════════════════════════════════════════════
if st.session_state.logged_in:
    dashboard()
else:
    login_page()
