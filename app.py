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
# SESSION STATE
# =============================

if "page" not in st.session_state:
    st.session_state.page = "welcome"

defaults = {
    "duration": "", "amount": "", "employment_duration": "", "age": "",
    "savings": 0, "credit_history": 0, "housing": 0, "job": 0,
    "result": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def go(page):
    st.session_state.page = page
    st.rerun()

def reset_and_go_input():
    for k, v in defaults.items():
        st.session_state[k] = v
    st.session_state.page = "input"
    st.rerun()

# =============================
# SHARED CSS
# =============================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
.stApp { background: #F2EFE8 !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

[data-testid="stSidebar"] { display: none !important; }

/* ── Inputs ── */
div[data-testid="stTextInput"] input {
    background: #FFFFFF !important;
    border: 1.5px solid #D8D0C4 !important;
    border-radius: 10px !important;
    padding: 11px 15px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 16px !important;
    color: #1C2B3A !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #8B6F4E !important;
    box-shadow: 0 0 0 3px rgba(139,111,78,0.13) !important;
}
div[data-testid="stTextInput"] label,
div[data-testid="stSelectbox"] label {
    font-size: 14px !important;
    font-weight: 500 !important;
    color: #4A5568 !important;
}
div[data-testid="stSelectbox"] > div > div {
    background: #FFFFFF !important;
    border: 1.5px solid #D8D0C4 !important;
    border-radius: 10px !important;
    font-size: 16px !important;
    font-family: 'DM Sans', sans-serif !important;
    color: #1C2B3A !important;
}

/* ── Buttons ── */
div.stButton > button {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    height: 48px !important;
    border: none !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}
div.stButton > button[kind="primary"] {
    background: #1C2B3A !important;
    color: white !important;
}
div.stButton > button[kind="primary"]:hover {
    background: #2D4A62 !important;
    box-shadow: 0 4px 16px rgba(28,43,58,0.28) !important;
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

/* ── Section label ── */
.sec-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #8B6F4E;
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 26px 0 14px;
}
.sec-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #D8D0C4;
}
</style>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════╗
# ║           PAGE 1 — WELCOME              ║
# ╚══════════════════════════════════════════╝

if st.session_state.page == "welcome":

    st.markdown("""
    <style>
    .stApp { background: #1C2B3A !important; }

    .welcome-wrap {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 60px 20px;
        position: relative;
        overflow: hidden;
    }

    /* big blurred orbs */
    .orb1 {
        position: fixed; top: -140px; right: -140px;
        width: 520px; height: 520px; border-radius: 50%;
        background: radial-gradient(circle, rgba(139,111,78,0.22) 0%, transparent 70%);
        pointer-events: none;
    }
    .orb2 {
        position: fixed; bottom: -120px; left: -100px;
        width: 420px; height: 420px; border-radius: 50%;
        background: radial-gradient(circle, rgba(59,130,246,0.1) 0%, transparent 70%);
        pointer-events: none;
    }

    .brand-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.13);
        border-radius: 100px;
        padding: 9px 20px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: rgba(255,255,255,0.55);
        margin-bottom: 36px;
        animation: fadeDown 0.7s ease;
    }
    .dot-live {
        width: 8px; height: 8px; border-radius: 50%;
        background: #4CAF82;
        box-shadow: 0 0 7px rgba(76,175,130,0.8);
    }

    .welcome-title {
        font-family: 'Playfair Display', serif;
        font-size: clamp(40px, 6vw, 72px);
        font-weight: 700;
        color: #FFFFFF;
        text-align: center;
        line-height: 1.15;
        letter-spacing: -1px;
        margin: 0 0 22px;
        animation: fadeDown 0.8s ease 0.1s both;
    }
    .welcome-title span { color: #C9A96E; }

    .welcome-sub {
        font-size: 17px;
        font-weight: 300;
        color: rgba(255,255,255,0.5);
        text-align: center;
        max-width: 540px;
        line-height: 1.75;
        margin: 0 0 52px;
        animation: fadeDown 0.8s ease 0.2s both;
    }

    .stats-row {
        display: flex;
        gap: 24px;
        flex-wrap: wrap;
        justify-content: center;
        margin-bottom: 56px;
        animation: fadeDown 0.8s ease 0.3s both;
    }
    .stat-box {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 22px 32px;
        text-align: center;
        min-width: 140px;
    }
    .stat-num {
        font-family: 'Playfair Display', serif;
        font-size: 32px;
        font-weight: 700;
        color: #C9A96E;
        margin: 0 0 4px;
    }
    .stat-lbl {
        font-size: 12px;
        color: rgba(255,255,255,0.4);
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }

    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
        max-width: 720px;
        width: 100%;
        margin-bottom: 56px;
        animation: fadeDown 0.8s ease 0.4s both;
    }
    .feat-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 16px;
        padding: 22px 20px;
    }
    .feat-icon { font-size: 26px; margin-bottom: 10px; }
    .feat-title {
        font-size: 14px;
        font-weight: 600;
        color: rgba(255,255,255,0.85);
        margin: 0 0 5px;
    }
    .feat-desc {
        font-size: 12px;
        color: rgba(255,255,255,0.35);
        line-height: 1.55;
        margin: 0;
    }

    .cta-wrap { animation: fadeDown 0.8s ease 0.5s both; text-align: center; }

    @keyframes fadeDown {
        from { opacity: 0; transform: translateY(-14px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    </style>

    <div class="welcome-wrap">
        <div class="orb1"></div>
        <div class="orb2"></div>

        <div class="brand-badge">
            <div class="dot-live"></div>
            CreditLens &nbsp;·&nbsp; Risk Intelligence Platform
        </div>

        <h1 class="welcome-title">
            Smarter Lending<br/>Starts with <span>Better Risk</span><br/>Intelligence.
        </h1>

        <p class="welcome-sub">
            Analyse any borrower's credit profile in seconds. 
            Our machine-learning engine delivers precise risk scores,
            probability breakdowns, and actionable insights.
        </p>

        <div class="stats-row">
            <div class="stat-box">
                <p class="stat-num">3</p>
                <p class="stat-lbl">Risk Tiers</p>
            </div>
            <div class="stat-box">
                <p class="stat-num">8</p>
                <p class="stat-lbl">Input Factors</p>
            </div>
            <div class="stat-box">
                <p class="stat-num">ML</p>
                <p class="stat-lbl">Powered</p>
            </div>
            <div class="stat-box">
                <p class="stat-num">⚡</p>
                <p class="stat-lbl">Instant Score</p>
            </div>
        </div>

        <div class="feature-grid">
            <div class="feat-card">
                <div class="feat-icon">🧠</div>
                <p class="feat-title">ML-Powered Engine</p>
                <p class="feat-desc">Trained on real credit data with calibrated probability outputs.</p>
            </div>
            <div class="feat-card">
                <div class="feat-icon">📊</div>
                <p class="feat-title">Visual Breakdown</p>
                <p class="feat-desc">Animated probability bars and confidence scores at a glance.</p>
            </div>
            <div class="feat-card">
                <div class="feat-icon">🔄</div>
                <p class="feat-title">Multi-Borrower</p>
                <p class="feat-desc">Analyse multiple applicants one after another, instantly.</p>
            </div>
        </div>

    </div>
    """, unsafe_allow_html=True)

    # CTA Button centered
    _, cta_col, _ = st.columns([3, 2, 3])
    with cta_col:
        if st.button("🚀  Begin Assessment", use_container_width=True, type="primary"):
            go("input")

    st.markdown("""
    <p style="text-align:center;font-size:12px;color:rgba(255,255,255,0.2);
       margin-top:28px;letter-spacing:0.05em;">
        For authorized personnel only &nbsp;·&nbsp; © 2025 CreditLens
    </p>
    """, unsafe_allow_html=True)


# ╔══════════════════════════════════════════╗
# ║           PAGE 2 — INPUT FORM           ║
# ╚══════════════════════════════════════════╝

elif st.session_state.page == "input":

    # Top bar
    st.markdown("""
    <div style="background:#1C2B3A;padding:14px 40px;display:flex;
         align-items:center;justify-content:space-between;">
        <span style="font-family:'Playfair Display',serif;font-size:20px;
              font-weight:700;color:#C9A96E;letter-spacing:0.02em;">
            CreditLens
        </span>
        <span style="font-size:12px;color:rgba(255,255,255,0.4);
              letter-spacing:0.08em;text-transform:uppercase;">
            Applicant Assessment
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Progress indicator
    st.markdown("""
    <div style="background:#EAE6DE;padding:10px 40px;
         display:flex;align-items:center;gap:10px;border-bottom:1px solid #D8D0C4;">
        <span style="width:24px;height:24px;border-radius:50%;background:#1C2B3A;
              color:white;font-size:12px;font-weight:700;display:inline-flex;
              align-items:center;justify-content:center;">1</span>
        <span style="font-size:13px;font-weight:600;color:#1C2B3A;">Enter Details</span>
        <span style="color:#D8D0C4;margin:0 4px;">──────</span>
        <span style="width:24px;height:24px;border-radius:50%;background:#D8D0C4;
              color:#8B96A3;font-size:12px;font-weight:700;display:inline-flex;
              align-items:center;justify-content:center;">2</span>
        <span style="font-size:13px;color:#8B96A3;">View Results</span>
    </div>
    """, unsafe_allow_html=True)

    # Centered form container
    _, form_col, _ = st.columns([1, 5, 1])

    with form_col:
        st.markdown("""
        <div style="padding:36px 0 10px;">
            <p style="font-family:'Playfair Display',serif;font-size:28px;font-weight:700;
               color:#1C2B3A;margin:0 0 6px;">Borrower Details</p>
            <p style="font-size:15px;color:#8B96A3;margin:0;">
                Fill in all fields and click <strong style="color:#1C2B3A;">Analyse Risk</strong>.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # ── LOAN DETAILS
        st.markdown('<div class="sec-label">Loan Details</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2, gap="medium")
        with c1:
            duration = st.text_input("Loan Duration (Months)", placeholder="e.g. 24", key="duration")
        with c2:
            amount = st.text_input("Credit Amount (₹ / $)", placeholder="e.g. 50000", key="amount")

        # ── FINANCIAL PROFILE
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

        # ── PERSONAL CONTEXT
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

        # ── BUTTONS
        st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
        b1, b2 = st.columns([3, 1.5], gap="medium")
        with b1:
            predict_btn = st.button("🔍  Analyse Risk", use_container_width=True, type="primary")
        with b2:
            reset_btn = st.button("↺  Clear Form", use_container_width=True, type="secondary")

        if reset_btn:
            reset_and_go_input()

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
                    tier = "low"
                    icon    = "🟢"
                    verdict = "Low Risk Applicant"
                    tagline = "Strong financial indicators — recommended for approval."
                    reason  = "<strong>Positive signals detected.</strong> This applicant demonstrates solid financial stability — good credit history, adequate savings, and consistent employment. The probability of default is low, indicating a reliable repayment profile."
                elif default_prob < 0.80:
                    tier = "medium"
                    icon    = "🟡"
                    verdict = "Medium Risk Applicant"
                    tagline = "Mixed indicators — consider with additional due diligence."
                    reason  = "<strong>Mixed signals present.</strong> Some factors support repayment capacity while others introduce moderate uncertainty. Review employment stability and savings depth before proceeding."
                else:
                    tier = "high"
                    icon    = "🔴"
                    verdict = "High Risk Applicant"
                    tagline = "Weak financials — recommend declining or requiring collateral."
                    reason  = "<strong>Significant risk factors identified.</strong> The applicant's profile shows indicators of financial instability — poor credit history, minimal savings, or limited employment history. High probability of default."

                st.session_state.result = {
                    "tier": tier, "icon": icon, "verdict": verdict,
                    "tagline": tagline, "reason": reason,
                    "default_prob": default_prob, "repay_prob": repay_prob,
                    "inputs": {
                        "Duration": f"{duration} months",
                        "Amount": amount,
                        "Savings": {0:"Little",1:"Moderate",2:"Rich"}[int(savings)],
                        "Credit History": {0:"Poor",1:"Average",2:"Good"}[int(credit_history)],
                        "Employment": f"{employment_duration} yrs",
                        "Age": f"{age} yrs",
                        "Housing": {0:"Rent",1:"Own",2:"Free"}[int(housing)],
                        "Job Level": {0:"Unskilled",1:"Skilled",2:"Highly Skilled"}[int(job)],
                    }
                }
                go("result")

            except ValueError:
                st.markdown("""
                <div style="background:#FEF2F2;border:1.5px solid #FECACA;border-radius:12px;
                     padding:16px 20px;font-size:15px;color:#B91C1C;
                     display:flex;gap:12px;align-items:center;margin-top:16px;">
                    <span style="font-size:22px;">⚠️</span>
                    <span>Please enter valid numbers in <strong>Duration</strong>,
                    <strong>Amount</strong>, <strong>Employment Duration</strong>, and <strong>Age</strong>.</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("""
        <div style="margin-top:48px;padding-top:18px;border-top:1px solid #D8D0C4;
             font-size:12px;color:#A09585;display:flex;justify-content:space-between;">
            <span>CreditLens Risk Intelligence</span>
            <span>Powered by scikit-learn · For authorized use only</span>
        </div>
        """, unsafe_allow_html=True)


# ╔══════════════════════════════════════════╗
# ║           PAGE 3 — RESULTS              ║
# ╚══════════════════════════════════════════╝

elif st.session_state.page == "result":

    r = st.session_state.result
    if r is None:
        go("input")

    dp  = r["default_prob"]
    rp  = r["repay_prob"]
    tier = r["tier"]

    if tier == "low":
        hdr_bg    = "#E6F4EC"
        hdr_bdr   = "#89CFA8"
        verd_col  = "#145C35"
        badge_bg  = "#D1EDDC"
        badge_col = "#145C35"
    elif tier == "medium":
        hdr_bg    = "#FEF3E2"
        hdr_bdr   = "#F5C97E"
        verd_col  = "#7D4E00"
        badge_bg  = "#FDEBC8"
        badge_col = "#7D4E00"
    else:
        hdr_bg    = "#FDECEA"
        hdr_bdr   = "#F5A99F"
        verd_col  = "#881515"
        badge_bg  = "#FAD7D4"
        badge_col = "#881515"

    # Top nav bar
    st.markdown("""
    <div style="background:#1C2B3A;padding:14px 40px;display:flex;
         align-items:center;justify-content:space-between;">
        <span style="font-family:'Playfair Display',serif;font-size:20px;
              font-weight:700;color:#C9A96E;">CreditLens</span>
        <span style="font-size:12px;color:rgba(255,255,255,0.4);
              letter-spacing:0.08em;text-transform:uppercase;">Risk Assessment Report</span>
    </div>
    """, unsafe_allow_html=True)

    # Progress bar — step 2
    st.markdown("""
    <div style="background:#EAE6DE;padding:10px 40px;
         display:flex;align-items:center;gap:10px;border-bottom:1px solid #D8D0C4;">
        <span style="width:24px;height:24px;border-radius:50%;background:#4CAF82;
              color:white;font-size:12px;font-weight:700;display:inline-flex;
              align-items:center;justify-content:center;">✓</span>
        <span style="font-size:13px;font-weight:600;color:#4CAF82;">Details Entered</span>
        <span style="color:#D8D0C4;margin:0 4px;">──────</span>
        <span style="width:24px;height:24px;border-radius:50%;background:#1C2B3A;
              color:white;font-size:12px;font-weight:700;display:inline-flex;
              align-items:center;justify-content:center;">2</span>
        <span style="font-size:13px;font-weight:600;color:#1C2B3A;">Risk Report</span>
    </div>
    """, unsafe_allow_html=True)

    # Centered results
    _, res_col, _ = st.columns([1, 5, 1])

    with res_col:
        st.markdown("<div style='padding-top:36px;'></div>", unsafe_allow_html=True)

        # Verdict header card
        st.markdown(f"""
        <div style="background:{hdr_bg};border:1.5px solid {hdr_bdr};border-radius:18px;
             padding:28px 32px;display:flex;align-items:center;gap:20px;
             animation:fadeUp 0.5s ease;margin-bottom:16px;">
            <span style="font-size:52px;line-height:1;">{r['icon']}</span>
            <div>
                <p style="font-family:'Playfair Display',serif;font-size:28px;font-weight:700;
                   color:{verd_col};margin:0 0 5px;">{r['verdict']}</p>
                <p style="font-size:14px;color:#6B7B8D;margin:0;">{r['tagline']}</p>
            </div>
            <div style="margin-left:auto;">
                <span style="background:{badge_bg};color:{badge_col};font-size:13px;
                      font-weight:700;padding:8px 18px;border-radius:100px;
                      letter-spacing:0.05em;">
                    Default: {dp*100:.1f}%
                </span>
            </div>
        </div>
        <style>
        @keyframes fadeUp {{
            from {{ opacity:0; transform:translateY(14px); }}
            to   {{ opacity:1; transform:translateY(0); }}
        }}
        </style>
        """, unsafe_allow_html=True)

        # Probability bars
        st.markdown(f"""
        <div style="background:#FFFFFF;border:1.5px solid #DDD7CE;border-radius:16px;
             padding:22px 26px;margin-bottom:14px;animation:fadeUp 0.5s ease 0.1s both;">
            <p style="font-size:11px;font-weight:700;letter-spacing:0.15em;
               text-transform:uppercase;color:#8B96A3;margin:0 0 18px;">
               Probability Breakdown
            </p>
            <div style="display:flex;align-items:center;gap:14px;margin-bottom:14px;">
                <span style="font-size:14px;font-weight:500;color:#1C2B3A;width:180px;flex-shrink:0;">
                    Default Risk
                </span>
                <div style="flex:1;height:10px;background:#EDE8E1;border-radius:100px;overflow:hidden;">
                    <div style="width:{dp*100:.1f}%;height:100%;border-radius:100px;
                         background:linear-gradient(90deg,#E24B4A,#B91C1C);"></div>
                </div>
                <span style="font-size:15px;font-weight:700;color:#B91C1C;width:52px;text-align:right;">
                    {dp*100:.1f}%
                </span>
            </div>
            <div style="display:flex;align-items:center;gap:14px;">
                <span style="font-size:14px;font-weight:500;color:#1C2B3A;width:180px;flex-shrink:0;">
                    Repayment Probability
                </span>
                <div style="flex:1;height:10px;background:#EDE8E1;border-radius:100px;overflow:hidden;">
                    <div style="width:{rp*100:.1f}%;height:100%;border-radius:100px;
                         background:linear-gradient(90deg,#22C55E,#15803D);"></div>
                </div>
                <span style="font-size:15px;font-weight:700;color:#15803D;width:52px;text-align:right;">
                    {rp*100:.1f}%
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Insight
        st.markdown(f"""
        <div style="background:#FFFFFF;border:1.5px solid #DDD7CE;border-radius:16px;
             padding:20px 24px;display:flex;gap:14px;align-items:flex-start;
             margin-bottom:14px;animation:fadeUp 0.5s ease 0.2s both;">
            <span style="font-size:24px;flex-shrink:0;">📋</span>
            <p style="font-size:15px;color:#4A5568;line-height:1.65;margin:0;">
                {r['reason']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Input summary
        inputs = r["inputs"]
        rows_html = "".join([
            f"""<div style="display:flex;justify-content:space-between;padding:9px 0;
                border-bottom:1px solid #F0EBE3;">
                <span style="font-size:14px;color:#8B96A3;">{k}</span>
                <span style="font-size:14px;font-weight:600;color:#1C2B3A;">{v}</span>
            </div>"""
            for k, v in inputs.items()
        ])
        st.markdown(f"""
        <div style="background:#FFFFFF;border:1.5px solid #DDD7CE;border-radius:16px;
             padding:20px 24px;margin-bottom:28px;animation:fadeUp 0.5s ease 0.3s both;">
            <p style="font-size:11px;font-weight:700;letter-spacing:0.15em;
               text-transform:uppercase;color:#8B96A3;margin:0 0 12px;">
               Input Summary
            </p>
            {rows_html}
        </div>
        """, unsafe_allow_html=True)

        # CTA buttons
        st.markdown("""
        <div style="background:linear-gradient(135deg,#1C2B3A,#2D4A62);
             border-radius:18px;padding:28px 32px;text-align:center;
             margin-bottom:32px;animation:fadeUp 0.5s ease 0.4s both;">
            <p style="font-family:'Playfair Display',serif;font-size:22px;font-weight:700;
               color:#FFFFFF;margin:0 0 8px;">Analyse Another Borrower?</p>
            <p style="font-size:14px;color:rgba(255,255,255,0.5);margin:0 0 24px;">
                Clear the form and assess a new applicant instantly.
            </p>
        </div>
        """, unsafe_allow_html=True)

        a1, a2 = st.columns(2, gap="medium")
        with a1:
            if st.button("🔄  New Borrower Assessment", use_container_width=True, type="primary"):
                reset_and_go_input()
        with a2:
            if st.button("🏠  Back to Home", use_container_width=True, type="secondary"):
                go("welcome")

        st.markdown("""
        <div style="margin-top:40px;padding-top:18px;border-top:1px solid #D8D0C4;
             font-size:12px;color:#A09585;display:flex;justify-content:space-between;">
            <span>CreditLens Risk Intelligence</span>
            <span>Powered by scikit-learn · For authorized use only</span>
        </div>
        """, unsafe_allow_html=True)
