import streamlit as st
import numpy as np
import pickle

# =============================
# LOAD MODEL + SCALER
# =============================

model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

# =============================
# PAGE CONFIG
# =============================

st.set_page_config(
    page_title="CreditLens — Risk Intelligence",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================
# CUSTOM CSS
# =============================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #F5F3EE !important;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding: 0 2rem 2rem 2rem !important;
    max-width: 100% !important;
}

/* ── Sidebar panel ── */
[data-testid="stSidebar"] {
    background: #1C2B3A !important;
    min-width: 320px !important;
    max-width: 320px !important;
}
[data-testid="stSidebar"] * { color: white !important; }
[data-testid="stSidebarContent"] { padding: 2.5rem 1.8rem !important; }

/* ── Form inputs ── */
div[data-testid="stTextInput"] input {
    background: #FFFFFF !important;
    border: 1.5px solid #D8D0C4 !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    color: #1C2B3A !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #8B6F4E !important;
    box-shadow: 0 0 0 3px rgba(139,111,78,0.12) !important;
}
div[data-testid="stTextInput"] label,
div[data-testid="stSelectbox"] label {
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #4A5568 !important;
}
div[data-testid="stSelectbox"] > div > div {
    background: #FFFFFF !important;
    border: 1.5px solid #D8D0C4 !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
}

/* ── Buttons ── */
div.stButton > button {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    height: 46px !important;
    border: none !important;
    transition: all 0.2s ease !important;
}
div.stButton > button[kind="primary"] {
    background: #1C2B3A !important;
    color: white !important;
}
div.stButton > button[kind="primary"]:hover {
    background: #2D4A62 !important;
    box-shadow: 0 4px 14px rgba(28,43,58,0.28) !important;
    transform: translateY(-1px) !important;
}
div.stButton > button[kind="secondary"] {
    background: #FFFFFF !important;
    color: #6B7B8D !important;
    border: 1.5px solid #D8D0C4 !important;
}
div.stButton > button[kind="secondary"]:hover {
    border-color: #8B6F4E !important;
    color: #8B6F4E !important;
}

/* ── Section divider label ── */
.sec-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #8B6F4E;
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 24px 0 14px;
}
.sec-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #D8D0C4;
}

/* ── Result cards ── */
.result-box {
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 14px;
    animation: fadeUp 0.5s ease;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
.result-low    { background: #E6F4EC; border: 1.5px solid #89CFA8; }
.result-medium { background: #FEF3E2; border: 1.5px solid #F5C97E; }
.result-high   { background: #FDECEA; border: 1.5px solid #F5A99F; }

.verdict {
    font-family: 'Playfair Display', serif;
    font-size: 26px;
    font-weight: 700;
    margin: 0 0 4px;
}
.verdict-low    { color: #145C35; }
.verdict-medium { color: #7D4E00; }
.verdict-high   { color: #881515; }

.prob-card {
    background: #FFFFFF;
    border: 1.5px solid #DDD7CE;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 12px;
}
.prob-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
}
.prob-row:last-child { margin-bottom: 0; }
.prob-name {
    font-size: 13px;
    font-weight: 500;
    color: #1C2B3A;
    width: 160px;
    flex-shrink: 0;
}
.prob-bar-bg {
    flex: 1;
    height: 8px;
    background: #EDE8E1;
    border-radius: 100px;
    overflow: hidden;
}
.prob-fill-risk  { height:100%; border-radius:100px; background: linear-gradient(90deg,#E24B4A,#B91C1C); }
.prob-fill-repay { height:100%; border-radius:100px; background: linear-gradient(90deg,#22C55E,#15803D); }
.prob-pct { font-size:14px; font-weight:700; width:48px; text-align:right; flex-shrink:0; }
.pct-risk  { color: #B91C1C; }
.pct-repay { color: #15803D; }

.insight-card {
    background: #FFFFFF;
    border: 1.5px solid #DDD7CE;
    border-radius: 14px;
    padding: 18px 22px;
    display: flex;
    gap: 14px;
    align-items: flex-start;
    font-size: 14px;
    color: #4A5568;
    line-height: 1.65;
}
</style>
""", unsafe_allow_html=True)

# =============================
# SESSION STATE
# =============================

defaults = {
    "duration": "", "amount": "", "employment_duration": "", "age": "",
    "savings": 0, "credit_history": 0, "housing": 0, "job": 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def reset_inputs():
    for k, v in defaults.items():
        st.session_state[k] = v
    st.rerun()

# =============================
# SIDEBAR  (left panel)
# =============================

with st.sidebar:
    st.markdown("""
    <div style="margin-bottom:8px;">
        <span style="font-size:11px;font-weight:700;letter-spacing:0.22em;
              text-transform:uppercase;color:#8B6F4E;">
            CreditLens &middot; Risk Intelligence
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h1 style="font-family:'Playfair Display',serif;font-size:36px;font-weight:700;
        color:#FFFFFF;line-height:1.2;letter-spacing:-0.3px;margin:12px 0 14px;">
        Know the risk<br/>before you<br/>lend.
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="font-size:13px;font-weight:300;color:rgba(255,255,255,0.5);
       line-height:1.7;margin:0 0 24px;">
        ML-powered credit analysis. Enter applicant details for an instant
        risk assessment with confidence metrics.
    </p>
    """, unsafe_allow_html=True)

    # Status pill
    st.markdown("""
    <div style="display:inline-flex;align-items:center;gap:10px;
         background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.12);
         border-radius:100px;padding:9px 16px;margin-bottom:40px;">
        <div style="width:8px;height:8px;border-radius:50%;background:#4CAF82;
             box-shadow:0 0 6px rgba(76,175,130,0.7);"></div>
        <span style="font-size:12px;color:rgba(255,255,255,0.55);letter-spacing:0.07em;">
            Model Active
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Feature items
    features = [
        ("🧠", "ML-Powered Analysis", "Trained on real credit datasets with calibrated probabilities"),
        ("⚡", "Instant Results", "Real-time scoring with factor breakdown"),
        ("🎯", "3-Tier Classification", "Low · Medium · High risk with % confidence"),
    ]
    for icon, title, desc in features:
        st.markdown(f"""
        <div style="display:flex;align-items:flex-start;gap:13px;margin-bottom:20px;">
            <div style="width:36px;height:36px;border-radius:10px;flex-shrink:0;
                 background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.1);
                 display:flex;align-items:center;justify-content:center;font-size:16px;">
                {icon}
            </div>
            <div>
                <p style="font-size:13px;font-weight:600;color:rgba(255,255,255,0.88);margin:0 0 3px;">{title}</p>
                <p style="font-size:12px;color:rgba(255,255,255,0.38);margin:0;line-height:1.5;">{desc}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <p style="font-size:11px;color:rgba(255,255,255,0.18);margin-top:32px;letter-spacing:0.04em;">
        © 2025 CreditLens &nbsp;·&nbsp; For internal use only
    </p>
    """, unsafe_allow_html=True)

# =============================
# MAIN CONTENT (right panel)
# =============================

st.markdown("""
<div style="padding: 40px 0 0;">
    <p style="font-family:'Playfair Display',serif;font-size:30px;font-weight:700;
       color:#1C2B3A;margin:0 0 6px;">Applicant Assessment</p>
    <p style="font-size:14px;color:#8B96A3;margin:0 0 8px;">
        Fill in the details below and click <strong style="color:#1C2B3A;">Analyse Risk</strong>
        to generate a risk report.
    </p>
</div>
""", unsafe_allow_html=True)

# ── LOAN DETAILS ──────────────────────────
st.markdown('<div class="sec-label">Loan Details</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2, gap="medium")
with c1:
    duration = st.text_input("Loan Duration (Months)", placeholder="e.g. 24", key="duration")
with c2:
    amount = st.text_input("Credit Amount (₹ / $)", placeholder="e.g. 50000", key="amount")

# ── FINANCIAL PROFILE ─────────────────────
st.markdown('<div class="sec-label">Financial Profile</div>', unsafe_allow_html=True)

c3, c4 = st.columns(2, gap="medium")
with c3:
    savings = st.selectbox(
        "Savings Level",
        options=[0, 1, 2],
        format_func=lambda x: {0: "🪙  Little Savings", 1: "💰  Moderate Savings", 2: "💎  Rich Savings"}[x],
        key="savings"
    )
with c4:
    credit_history = st.selectbox(
        "Credit History",
        options=[0, 1, 2],
        format_func=lambda x: {0: "⚠️  Poor", 1: "📊  Average", 2: "✅  Good"}[x],
        key="credit_history"
    )

c5, c6 = st.columns(2, gap="medium")
with c5:
    employment_duration = st.text_input("Employment Duration (Years)", placeholder="e.g. 5", key="employment_duration")
with c6:
    age = st.text_input("Age", placeholder="e.g. 34", key="age")

# ── PERSONAL CONTEXT ──────────────────────
st.markdown('<div class="sec-label">Personal Context</div>', unsafe_allow_html=True)

c7, c8 = st.columns(2, gap="medium")
with c7:
    housing = st.selectbox(
        "Housing Type",
        options=[0, 1, 2],
        format_func=lambda x: {0: "🏠  Rent", 1: "🏡  Own", 2: "🆓  Free"}[x],
        key="housing"
    )
with c8:
    job = st.selectbox(
        "Job Skill Level",
        options=[0, 1, 2],
        format_func=lambda x: {0: "🔧  Unskilled", 1: "💼  Skilled", 2: "🎓  Highly Skilled"}[x],
        key="job"
    )

# ── BUTTONS ───────────────────────────────
st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)
b1, b2, _ = st.columns([2, 1.2, 3], gap="medium")
with b1:
    predict_btn = st.button("🔍  Analyse Risk", use_container_width=True, type="primary")
with b2:
    reset_btn = st.button("↺  Clear", use_container_width=True, type="secondary")

if reset_btn:
    reset_inputs()

# ── PREDICTION ────────────────────────────
if predict_btn:
    try:
        input_data = np.array([[
            float(duration), float(amount), float(savings),
            float(credit_history), float(employment_duration),
            float(age), float(housing), float(job)
        ]])
        scaled_data = scaler.transform(input_data)
        probability = model.predict_proba(scaled_data)[0]
        default_prob = probability[0]
        repay_prob   = 1 - default_prob

        if default_prob < 0.35:
            css_class = "result-low"
            verdict_class = "verdict-low"
            icon    = "🟢"
            verdict = "Low Risk Applicant"
            tagline = "Strong financial indicators — recommended for approval."
            reason  = "<strong>Positive signals detected.</strong> This applicant shows solid financial stability — good credit history, adequate savings, and consistent employment. The probability of default is low, indicating a reliable repayment profile."
        elif default_prob < 0.80:
            css_class = "result-medium"
            verdict_class = "verdict-medium"
            icon    = "🟡"
            verdict = "Medium Risk Applicant"
            tagline = "Mixed indicators — consider with additional due diligence."
            reason  = "<strong>Mixed signals present.</strong> Some factors support repayment capacity while others introduce moderate uncertainty. Review employment stability and savings depth before proceeding."
        else:
            css_class = "result-high"
            verdict_class = "verdict-high"
            icon    = "🔴"
            verdict = "High Risk Applicant"
            tagline = "Weak financials — recommend declining or requiring collateral."
            reason  = "<strong>Significant risk factors identified.</strong> The applicant's profile shows indicators of financial instability — poor credit history, minimal savings, or limited employment history. High probability of default."

        st.markdown(f"""
        <div class="result-box {css_class}" style="margin-top:32px;">
            <div style="display:flex;align-items:center;gap:16px;">
                <span style="font-size:46px;line-height:1;">{icon}</span>
                <div>
                    <p class="verdict {verdict_class}">{verdict}</p>
                    <p style="font-size:13px;color:#6B7B8D;margin:0;">{tagline}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="prob-card">
            <p style="font-size:10px;font-weight:700;letter-spacing:0.14em;
               text-transform:uppercase;color:#8B96A3;margin:0 0 14px;">
               Probability Breakdown
            </p>
            <div class="prob-row">
                <span class="prob-name">Default Risk</span>
                <div class="prob-bar-bg">
                    <div class="prob-fill-risk" style="width:{default_prob*100:.1f}%"></div>
                </div>
                <span class="prob-pct pct-risk">{default_prob*100:.1f}%</span>
            </div>
            <div class="prob-row">
                <span class="prob-name">Repayment Probability</span>
                <div class="prob-bar-bg">
                    <div class="prob-fill-repay" style="width:{repay_prob*100:.1f}%"></div>
                </div>
                <span class="prob-pct pct-repay">{repay_prob*100:.1f}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="insight-card">
            <span style="font-size:22px;flex-shrink:0;">📋</span>
            <p style="margin:0;">{reason}</p>
        </div>
        """, unsafe_allow_html=True)

    except ValueError:
        st.markdown("""
        <div style="background:#FEF2F2;border:1.5px solid #FECACA;border-radius:12px;
             padding:16px 20px;font-size:14px;color:#B91C1C;
             display:flex;gap:10px;align-items:center;margin-top:16px;">
            <span style="font-size:20px;">⚠️</span>
            <span>Please enter valid numbers in <strong>Duration</strong>,
            <strong>Amount</strong>, <strong>Employment Duration</strong>, and <strong>Age</strong>.</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div style="margin-top:52px;padding-top:18px;border-top:1px solid #D8D0C4;
     font-size:12px;color:#A09585;display:flex;justify-content:space-between;">
    <span>CreditLens Risk Intelligence Platform</span>
    <span>Powered by scikit-learn &nbsp;·&nbsp; For authorized use only</span>
</div>
""", unsafe_allow_html=True)
