import streamlit as st
from groq import Groq

# Page config
st.set_page_config(
    page_title="FakeRadar - AI News Detector",
    page_icon="🔍",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

* { font-family: 'DM Sans', sans-serif; }

html, body, [class*="css"] {
    background-color: #0a0a0f;
    color: #e8e8f0;
}

.stApp {
    background: radial-gradient(ellipse at top left, #1a0533 0%, #0a0a0f 50%, #001a33 100%);
    min-height: 100vh;
}

#MainMenu, footer, header {visibility: hidden;}

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
}

.input-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 2rem;
    margin: 1.5rem 0;
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

.stTextArea textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #e8e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
    padding: 1rem !important;
}

.stTextArea textarea:focus {
    border-color: rgba(139, 92, 246, 0.5) !important;
    box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1) !important;
}

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
    margin-top: 0.5rem !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(124, 58, 237, 0.4) !important;
}

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

.result-uncertain {
    background: linear-gradient(135deg, rgba(234,179,8,0.1), rgba(234,179,8,0.05));
    border: 1px solid rgba(234,179,8,0.3);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    text-align: center;
    margin-top: 1rem;
}

.result-icon { font-size: 2.5rem; margin-bottom: 0.5rem; }

.result-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0 0 0.3rem;
}

.result-fake .result-title { color: #f87171; }
.result-real .result-title { color: #4ade80; }
.result-uncertain .result-title { color: #facc15; }

.analysis-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-top: 1rem;
    font-size: 0.9rem;
    color: #9ca3af;
    line-height: 1.7;
}

.analysis-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    color: #6b7280;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

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
</style>
""", unsafe_allow_html=True)

# Configure Groq - Replace with your Groq API key
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

def analyze_news(text):
    prompt = f"""
    You are a professional fake news detector. Analyze the following news text carefully.

    News Text:
    "{text}"

    Respond in this EXACT format:
    VERDICT: [FAKE or REAL or UNCERTAIN]
    CONFIDENCE: [percentage like 95%]
    REASON: [2-3 sentences explaining why in simple language]
    RED FLAGS: [list 2-3 specific things that indicate fake or real, or None]

    Be accurate, fair, and base your analysis on:
    - Writing style and tone
    - Factual claims
    - Source credibility indicators
    - Sensationalism or emotional manipulation
    - Logical consistency
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def parse_response(response):
    lines = response.strip().split('\n')
    result = {"verdict": "UNCERTAIN", "confidence": "N/A", "reason": "", "red_flags": ""}
    for line in lines:
        if line.startswith("VERDICT:"):
            result["verdict"] = line.replace("VERDICT:", "").strip()
        elif line.startswith("CONFIDENCE:"):
            result["confidence"] = line.replace("CONFIDENCE:", "").strip()
        elif line.startswith("REASON:"):
            result["reason"] = line.replace("REASON:", "").strip()
        elif line.startswith("RED FLAGS:"):
            result["red_flags"] = line.replace("RED FLAGS:", "").strip()
    return result

# Hero
st.markdown("""
<div class="hero">
    <div class="hero-badge">🤖 Powered by Groq AI</div>
    <div class="hero-title">FakeRadar</div>
    <div class="hero-sub">AI-powered fake news detection for any topic, any year, any language</div>
</div>
""", unsafe_allow_html=True)

# Stats
st.markdown("""
<div class="stats-row">
    <div class="stat-box">
        <div class="stat-value">AI</div>
        <div class="stat-label">Powered</div>
    </div>
    <div class="stat-box">
        <div class="stat-value">Any</div>
        <div class="stat-label">Topic & Year</div>
    </div>
    <div class="stat-box">
        <div class="stat-value">< 3s</div>
        <div class="stat-label">Analysis Time</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Input
st.markdown('<div class="input-card">', unsafe_allow_html=True)
st.markdown('<span class="input-label">📰 Paste News Article</span>', unsafe_allow_html=True)

news = st.text_area(
    "",
    placeholder="Paste any news article, headline, or text here...",
    height=180,
    label_visibility="collapsed"
)

if st.button("🔍 Analyze with AI"):
    if not news.strip():
        st.warning("Please enter some news text to analyze.")
    else:
        with st.spinner("🤖 AI is analyzing..."):
            try:
                response = analyze_news(news)
                result = parse_response(response)
                verdict = result["verdict"].upper()

                if "FAKE" in verdict:
                    st.markdown(f"""
                    <div class="result-fake">
                        <div class="result-icon">⚠️</div>
                        <div class="result-title">FAKE NEWS DETECTED</div>
                        <div style="color:#f87171; font-size:0.85rem;">Confidence: {result['confidence']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                elif "REAL" in verdict:
                    st.markdown(f"""
                    <div class="result-real">
                        <div class="result-icon">✅</div>
                        <div class="result-title">REAL NEWS</div>
                        <div style="color:#4ade80; font-size:0.85rem;">Confidence: {result['confidence']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="result-uncertain">
                        <div class="result-icon">🤔</div>
                        <div class="result-title">UNCERTAIN</div>
                        <div style="color:#facc15; font-size:0.85rem;">Confidence: {result['confidence']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="analysis-box">
                    <div class="analysis-title">🧠 AI Analysis</div>
                    <b>Reason:</b> {result['reason']}<br><br>
                    <b>Key Indicators:</b> {result['red_flags']}
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error: {str(e)} — Check your API key!")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin-top: 2rem; color: #374151; font-size: 0.75rem;">
    Built with Streamlit · Powered by Groq AI
</div>
""", unsafe_allow_html=True)
