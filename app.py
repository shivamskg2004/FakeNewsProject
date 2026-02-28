import streamlit as st
import pickle

# Page config
st.set_page_config(
    page_title="FakeRadar - News Detector",
    page_icon="🔍",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

* {
    font-family: 'DM Sans', sans-serif;
}

html, body, [class*="css"] {
    background-color: #0a0a0f;
    color: #e8e8f0;
}

.stApp {
    background: radial-gradient(ellipse at top left, #1a0533 0%, #0a0a0f 50%, #001a33 100%);
    min-height: 100vh;
}

/* Hide streamlit defaults */
#MainMenu, footer, header {visibility: hidden;}

/* Hero section */
.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
}

.hero-badge {
    display: inline-block;
    background: rgba(139, 92, 246, 0.15);
    border: 1px solid rgba(139, 92, 246, 0.4);
    color: #a78bfa;
    padding: 0.3rem 1rem;
    border-radius: 20px;
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.5rem, 6vw, 4rem);
    font-weight: 800;
    line-height: 1.1;
    margin: 0 0 0.5rem;
    background: linear-gradient(135deg, #ffffff 0%, #a78bfa 50%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-sub {
    font-size: 1rem;
    color: #6b7280;
    font-weight: 300;
    letter-spacing: 0.02em;
    margin-bottom: 0;
}

/* Input card */
.input-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 2rem;
    margin: 1.5rem 0;
    backdrop-filter: blur(10px);
}

.input-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.85rem;
    font-weight: 600;
    color: #9ca3af;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
    display: block;
}

/* Textarea styling */
.stTextArea textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #e8e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
    padding: 1rem !important;
    resize: vertical !important;
    transition: border-color 0.2s ease !important;
}

.stTextArea textarea:focus {
    border-color: rgba(139, 92, 246, 0.5) !important;
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1) !important;
}

.stTextArea textarea::placeholder {
    color: #374151 !important;
}

/* Button */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 2rem !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    margin-top: 0.5rem !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(124, 58, 237, 0.4) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* Result boxes */
.result-fake {
    background: linear-gradient(135deg, rgba(239,68,68,0.1), rgba(239,68,68,0.05));
    border: 1px solid rgba(239,68,68,0.3);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    text-align: center;
    margin-top: 1rem;
}

.result-real {
    background: linear-gradient(135deg, rgba(34,197,94,0.1), rgba(34,197,94,0.05));
    border: 1px solid rgba(34,197,94,0.3);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    text-align: center;
    margin-top: 1rem;
}

.result-icon {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

.result-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0 0 0.3rem;
}

.result-fake .result-title { color: #f87171; }
.result-real .result-title { color: #4ade80; }

.result-desc {
    font-size: 0.85rem;
    color: #6b7280;
    margin: 0;
}

/* Stats bar */
.stats-row {
    display: flex;
    gap: 1rem;
    margin: 1.5rem 0;
}

.stat-box {
    flex: 1;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}

.stat-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #a78bfa;
}

.stat-label {
    font-size: 0.7rem;
    color: #4b5563;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.2rem;
}

/* Divider */
.divider {
    height: 1px;
    background: rgba(255,255,255,0.05);
    margin: 1rem 0;
}

/* Warning for empty */
.stAlert {
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# Load model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Hero
st.markdown("""
<div class="hero">
    <div class="hero-badge">🔍 AI-Powered Detection</div>
    <div class="hero-title">FakeRadar</div>
    <div class="hero-sub">Paste any news article and instantly detect if it's real or fabricated</div>
</div>
""", unsafe_allow_html=True)

# Stats row
st.markdown("""
<div class="stats-row">
    <div class="stat-box">
        <div class="stat-value">98%</div>
        <div class="stat-label">Accuracy</div>
    </div>
    <div class="stat-box">
        <div class="stat-value">44K+</div>
        <div class="stat-label">Articles Trained</div>
    </div>
    <div class="stat-box">
        <div class="stat-value">< 1s</div>
        <div class="stat-label">Detection Time</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Input card
st.markdown('<div class="input-card">', unsafe_allow_html=True)
st.markdown('<span class="input-label">📰 News Article Text</span>', unsafe_allow_html=True)

news = st.text_area(
    "",
    placeholder="Paste a news headline or full article here...",
    height=180,
    label_visibility="collapsed"
)

if st.button("🔍 Analyze Article"):
    if not news.strip():
        st.warning("Please enter some news text to analyze.")
    else:
        vec = vectorizer.transform([news])
        prediction = model.predict(vec)
        proba = model.predict_proba(vec)[0]
        confidence = max(proba) * 100

        if prediction[0] == 0:
            st.markdown(f"""
            <div class="result-fake">
                <div class="result-icon">⚠️</div>
                <div class="result-title">FAKE NEWS DETECTED</div>
                <div class="result-desc">Confidence: {confidence:.1f}% — This article shows signs of misinformation</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-real">
                <div class="result-icon">✅</div>
                <div class="result-title">REAL NEWS</div>
                <div class="result-desc">Confidence: {confidence:.1f}% — This article appears to be legitimate</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align:center; margin-top: 2rem; color: #374151; font-size: 0.75rem;">
    Built with Streamlit · Powered by Machine Learning
</div>
""", unsafe_allow_html=True)
