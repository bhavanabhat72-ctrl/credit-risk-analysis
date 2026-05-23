import streamlit as st
import numpy as np
import pickle
import time

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

/* ── Base ───────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #F5F3EE;
}

.stApp {
    background: linear-gradient(160deg, #F5F3EE 0%, #EAE6DE 100%);
    min-height: 100vh;
}

/* ── Hide Streamlit chrome ──────────────── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Typography ─────────────────────────── */
.brand-name {
    font-family: 'Playfair Display', serif;
    font-size: 13px;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #8B6F4E;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 52px;
    font-weight: 700;
    color: #1C2B3A;
    line-height: 1.15;
    letter-spacing: -0.5px;
}

.hero-subtitle {
    font-family: 'DM Sans', sans-serif;
    font-size: 16px;
    font-weight: 300;
    color: #6B7B8D;
    letter-spacing: 0.02em;
    margin-top: 8px;
}

/* ── Layout containers ──────────────────── */
.page-wrapper {
    display: flex;
    min-height: 100vh;
}

.left-panel {
    width: 420px;
    min-width: 420px;
    background: #1C2B3A;
    padding: 48px 40px;
    display: flex;
    flex-direction: column;
    position: relative;
    overflow: hidden;
}

.left-panel::before {
    content: '';
    position: absolute;
    top: -120px; right: -120px;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(139,111,78,0.15) 0%, transparent 70%);
    pointer-events: none;
}

.left-panel::after {
    content: '';
    position: absolute;
    bottom: -80px; left: -80px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(59,130,246,0.08) 0%, transparent 70%);
    pointer-events: none;
}

.right-panel {
    flex: 1;
    padding: 48px 52px;
    overflow-y: auto;
}

/* ── Decorative number / stat ───────────── */
.stat-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 100px;
    padding: 8px 16px;
    margin-top: 28px;
}

.stat-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #4CAF82;
}

.stat-label {
    font-size: 12px;
    color: rgba(255,255,255,0.6);
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* ── Feature badges ─────────────────────── */
.feature-list {
    margin-top: auto;
    padding-top: 40px;
}

.feature-item {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    margin-bottom: 20px;
}

.feature-icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.1);
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    font-size: 16px;
}

.feature-title {
    font-size: 13px;
    font-weight: 600;
    color: rgba(255,255,255,0.9);
    margin: 0 0 2px;
}

.feature-desc {
    font-size: 12px;
    color: rgba(255,255,255,0.4);
    margin: 0;
    line-height: 1.5;
}

/* ── Form section header ────────────────── */
.section-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #8B6F4E;
    margin-bottom: 16px;
    margin-top: 32px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #D8D2C8;
}

/* ── Streamlit input overrides ──────────── */
div[data-testid="stTextInput"] input {
    background: #FFFFFF !important;
    border: 1.5px solid #E0D8CE !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    color: #1C2B3A !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #8B6F4E !important;
    box-shadow: 0 0 0 3px rgba(139,111,78,0.12) !important;
    outline: none !important;
}

div[data-testid="stTextInput"] label,
div[data-testid="stSelectbox"] label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #4A5568 !important;
    letter-spacing: 0.01em !important;
}

div[data-testid="stSelectbox"] > div > div {
    background: #FFFFFF !important;
    border: 1.5px solid #E0D8CE !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    color: #1C2B3A !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
}

/* ── Buttons ────────────────────────────── */
div.stButton > button {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    border-radius: 12px !important;
    height: 48px !important;
    border: none !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}

div.stButton > button[kind="primary"],
div.stButton > button:first-child {
    background: linear-gradient(135deg, #1C2B3A 0%, #2D4A62 100%) !important;
    color: white !important;
}

div.stButton > button[kind="primary"]:hover,
div.stButton > button:first-child:hover {
    background: linear-gradient(135deg, #2D4A62 0%, #1C2B3A 100%) !important;
    box-shadow: 0 4px 16px rgba(28,43,58,0.3) !important;
    transform: translateY(-1px) !important;
}

div.stButton > button[kind="secondary"],
div.stButton > button:nth-child(2) {
    background: #FFFFFF !important;
    color: #6B7B8D !important;
    border: 1.5px solid #E0D8CE !important;
}

div.stButton > button[kind="secondary"]:hover {
    background: #F5F3EE !important;
    border-color: #8B6F4E !important;
    color: #8B6F4E !important;
}

/* ── Result cards ───────────────────────── */
.result-wrapper {
    margin-top: 36px;
    animation: slideUp 0.5s ease;
}

@keyframes slideUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

.result-header {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 28px 32px;
    border-radius: 20px;
    margin-bottom: 16px;
}

.result-header.low-risk {
    background: linear-gradient(135deg, #E8F5EE 0%, #D1EDE1 100%);
    border: 1.5px solid #9CD4B5;
}

.result-header.medium-risk {
    background: linear-gradient(135deg, #FEF3E2 0%, #FDEAC8 100%);
    border: 1.5px solid #F5C97E;
}

.result-header.high-risk {
    background: linear-gradient(135deg, #FDECEA 0%, #FAD7D4 100%);
    border: 1.5px solid #F5A99F;
}

.result-icon {
    font-size: 44px;
    line-height: 1;
}

.result-verdict {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    font-weight: 700;
    margin: 0 0 4px;
}

.low-risk .result-verdict   { color: #1A6640; }
.medium-risk .result-verdict { color: #7D4E00; }
.high-risk .result-verdict   { color: #8B1C1C; }

.result-tagline {
    font-size: 14px;
    color: #6B7B8D;
    margin: 0;
}

/* ── Probability bar ────────────────────── */
.prob-card {
    background: #FFFFFF;
    border: 1.5px solid #E0D8CE;
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 14px;
}

.prob-label {
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #6B7B8D;
    margin-bottom: 10px;
}

.prob-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
}

.prob-name {
    font-size: 14px;
    font-weight: 500;
    color: #1C2B3A;
    width: 140px;
    flex-shrink: 0;
}

.prob-bar-bg {
    flex: 1;
    height: 8px;
    background: #F0EBE3;
    border-radius: 100px;
    overflow: hidden;
}

.prob-bar-fill {
    height: 100%;
    border-radius: 100px;
    transition: width 1s ease;
}

.prob-bar-fill.risk   { background: linear-gradient(90deg, #E24B4A, #C0392B); }
.prob-bar-fill.repay  { background: linear-gradient(90deg, #2ECC71, #1A9B52); }

.prob-value {
    font-size: 15px;
    font-weight: 600;
    width: 52px;
    text-align: right;
    flex-shrink: 0;
}

.prob-value.risk   { color: #C0392B; }
.prob-value.repay  { color: #1A9B52; }

/* ── Insight card ───────────────────────── */
.insight-card {
    background: #FFFFFF;
    border: 1.5px solid #E0D8CE;
    border-radius: 16px;
    padding: 20px 24px;
    display: flex;
    gap: 14px;
    align-items: flex-start;
}

.insight-icon-wrap {
    width: 40px; height: 40px;
    border-radius: 12px;
    background: #F5F3EE;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
}

.insight-text {
    font-size: 14px;
    color: #4A5568;
    line-height: 1.6;
    margin: 0;
}

.insight-text strong {
    color: #1C2B3A;
    font-weight: 600;
}

/* ── Input group row ────────────────────── */
.stHorizontalBlock { gap: 16px !important; }

/* ── Footer ─────────────────────────────── */
.page-footer {
    margin-top: 52px;
    padding-top: 20px;
    border-top: 1px solid #D8D2C8;
    font-size: 12px;
    color: #A09585;
    display: flex;
    justify-content: space-between;
}

/* ── Error state ────────────────────────── */
.error-box {
    background: #FEF3F2;
    border: 1.5px solid #FECACA;
    border-radius: 12px;
    padding: 16px 20px;
    font-size: 14px;
    color: #B91C1C;
    display: flex;
    gap: 10px;
    align-items: center;
    margin-top: 16px;
}

</style>
""", unsafe_allow_html=True)

# =============================
# SESSION STATE
# =============================

defaults = {
    "duration": "", "amount": "", "employment_duration": "", "age": "",
    "savings": 0, "credit_history": 0, "housing": 0, "job": 0,
    "show_result": False, "result_data": None
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def reset_inputs():
    for k, v in defaults.items():
        st.session_state[k] = v
    st.rerun()

# =============================
# LAYOUT: TWO COLUMNS
# =============================

left_col, right_col = st.columns([4, 7], gap="large")

# ─────────────────────────────
# LEFT PANEL
# ─────────────────────────────
with left_col:
    st.markdown("""
    <div style="padding: 40px 32px; background: #1C2B3A; border-radius: 24px; min-height: 88vh; display: flex; flex-direction: column; position: relative; overflow: hidden;">

        <div style="position:absolute;top:-100px;right:-100px;width:340px;height:340px;
             background:radial-gradient(circle,rgba(139,111,78,0.2) 0%,transparent 70%);
             pointer-events:none;"></div>
        <div style="position:absolute;bottom:-80px;left:-60px;width:260px;height:260px;
             background:radial-gradient(circle,rgba(59,130,246,0.1) 0%,transparent 70%);
             pointer-events:none;"></div>

        <div>
            <p style="font-family:'DM Sans',sans-serif;font-size:11px;font-weight:600;
               letter-spacing:0.25em;text-transform:uppercase;color:#8B6F4E;margin:0 0 20px;">
                CreditLens · Risk Intelligence
            </p>

            <h1 style="font-family:'Playfair Display',serif;font-size:40px;font-weight:700;
                color:#FFFFFF;line-height:1.2;letter-spacing:-0.5px;margin:0 0 14px;">
                Know the<br/>risk before<br/>you lend.
            </h1>

            <p style="font-family:'DM Sans',sans-serif;font-size:14px;font-weight:300;
               color:rgba(255,255,255,0.5);line-height:1.7;margin:0;">
               Machine-learning powered credit analysis. Enter applicant details to receive
               an instant risk assessment with confidence metrics.
            </p>

            <div style="display:inline-flex;align-items:center;gap:10px;
                 background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);
                 border-radius:100px;padding:10px 18px;margin-top:28px;">
                <div style="width:8px;height:8px;border-radius:50%;background:#4CAF82;
                     box-shadow:0 0 6px rgba(76,175,130,0.6);"></div>
                <span style="font-size:12px;color:rgba(255,255,255,0.55);
                      letter-spacing:0.06em;">Model Active</span>
            </div>
        </div>

        <div style="margin-top:auto;padding-top:48px;">

            <div style="display:flex;align-items:flex-start;gap:14px;margin-bottom:22px;">
                <div style="width:38px;height:38px;border-radius:11px;
                     background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.1);
                     display:flex;align-items:center;justify-content:center;
                     font-size:16px;flex-shrink:0;">🧠</div>
                <div>
                    <p style="font-size:13px;font-weight:600;color:rgba(255,255,255,0.88);margin:0 0 3px;">
                        ML-Powered Analysis</p>
                    <p style="font-size:12px;color:rgba(255,255,255,0.38);margin:0;line-height:1.5;">
                        Trained on real credit datasets with calibrated probability outputs</p>
                </div>
            </div>

            <div style="display:flex;align-items:flex-start;gap:14px;margin-bottom:22px;">
                <div style="width:38px;height:38px;border-radius:11px;
                     background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.1);
                     display:flex;align-items:center;justify-content:center;
                     font-size:16px;flex-shrink:0;">⚡</div>
                <div>
                    <p style="font-size:13px;font-weight:600;color:rgba(255,255,255,0.88);margin:0 0 3px;">
                        Instant Results</p>
                    <p style="font-size:12px;color:rgba(255,255,255,0.38);margin:0;line-height:1.5;">
                        Real-time scoring with breakdown of key risk factors</p>
                </div>
            </div>

            <div style="display:flex;align-items:flex-start;gap:14px;">
                <div style="width:38px;height:38px;border-radius:11px;
                     background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.1);
                     display:flex;align-items:center;justify-content:center;
                     font-size:16px;flex-shrink:0;">🎯</div>
                <div>
                    <p style="font-size:13px;font-weight:600;color:rgba(255,255,255,0.88);margin:0 0 3px;">
                        3-Tier Classification</p>
                    <p style="font-size:12px;color:rgba(255,255,255,0.38);margin:0;line-height:1.5;">
                        Low · Medium · High risk with percentage confidence</p>
                </div>
            </div>

        </div>

        <p style="font-size:11px;color:rgba(255,255,255,0.2);margin:36px 0 0;
           letter-spacing:0.05em;">
            © 2025 CreditLens · For internal use only
        </p>

    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────
# RIGHT PANEL
# ─────────────────────────────
with right_col:

    st.markdown("""
    <div style="padding: 12px 0 0;">
        <p style="font-family:'Playfair Display',serif;font-size:28px;font-weight:700;
           color:#1C2B3A;margin:0 0 4px;">Applicant Assessment</p>
        <p style="font-size:14px;color:#8B96A3;margin:0 0 32px;">
            Fill in the details below and click <strong style="color:#1C2B3A;">Analyse</strong> to generate a risk report.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── LOAN DETAILS ──
    st.markdown('<div class="section-label">Loan Details</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        duration = st.text_input("Loan Duration (Months)", placeholder="e.g. 24", key="duration")
    with c2:
        amount = st.text_input("Credit Amount (₹ / $)", placeholder="e.g. 50000", key="amount")

    # ── FINANCIAL PROFILE ──
    st.markdown('<div class="section-label">Financial Profile</div>', unsafe_allow_html=True)

    c3, c4 = st.columns(2)
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

    c5, c6 = st.columns(2)
    with c5:
        employment_duration = st.text_input("Employment Duration (Years)", placeholder="e.g. 5", key="employment_duration")
    with c6:
        age = st.text_input("Age", placeholder="e.g. 34", key="age")

    # ── PERSONAL CONTEXT ──
    st.markdown('<div class="section-label">Personal Context</div>', unsafe_allow_html=True)

    c7, c8 = st.columns(2)
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

    # ── ACTIONS ──
    st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
    btn1, btn2, _ = st.columns([3, 2, 3])

    with btn1:
        predict_btn = st.button("🔍  Analyse Risk", use_container_width=True, type="primary")
    with btn2:
        reset_btn = st.button("↺  Clear Form", use_container_width=True, type="secondary")

    # ── RESET ──
    if reset_btn:
        reset_inputs()

    # ── PREDICTION ──
    if predict_btn:
        try:
            input_data = np.array([[
                float(duration),
                float(amount),
                float(savings),
                float(credit_history),
                float(employment_duration),
                float(age),
                float(housing),
                float(job)
            ]])

            scaled_data = scaler.transform(input_data)
            prediction = model.predict(scaled_data)[0]
            probability = model.predict_proba(scaled_data)[0]
            default_prob = probability[0]
            repay_prob = 1 - default_prob

            # Determine tier
            if default_prob < 0.35:
                tier = "low"
                verdict = "Low Risk Applicant"
                tagline = "Strong financial indicators. Recommended for approval."
                icon = "🟢"
                reason = (
                    "<strong>Positive signals detected.</strong> This applicant demonstrates solid "
                    "financial stability — good credit history, adequate savings, and consistent "
                    "employment. The probability of default is low, suggesting a reliable repayment profile."
                )
                risk_class = "low-risk"
            elif default_prob < 0.80:
                tier = "medium"
                verdict = "Medium Risk Applicant"
                tagline = "Mixed indicators. Consider with additional due diligence."
                icon = "🟡"
                reason = (
                    "<strong>Mixed signals present.</strong> Some factors support repayment "
                    "capacity while others introduce moderate uncertainty. Recommend reviewing "
                    "employment stability and savings depth before proceeding."
                )
                risk_class = "medium-risk"
            else:
                tier = "high"
                verdict = "High Risk Applicant"
                tagline = "Weak financials. Recommend declining or additional collateral."
                icon = "🔴"
                reason = (
                    "<strong>Significant risk factors identified.</strong> The applicant's profile "
                    "shows indicators of financial instability — poor credit history, minimal savings, "
                    "or limited employment history. High probability of default observed."
                )
                risk_class = "high-risk"

            # ── RESULT DISPLAY ──
            st.markdown("<div style='margin-top: 36px;'>", unsafe_allow_html=True)

            # Verdict header
            st.markdown(f"""
            <div class="result-header {risk_class}" style="animation: slideUp 0.5s ease;">
                <div style="font-size:48px;line-height:1;">{icon}</div>
                <div>
                    <p class="result-verdict" style="font-family:'Playfair Display',serif;
                       font-size:26px;font-weight:700;margin:0 0 4px;">
                        {verdict}
                    </p>
                    <p style="font-size:13px;color:#6B7B8D;margin:0;">{tagline}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Probability bars
            st.markdown(f"""
            <div class="prob-card">
                <p class="prob-label">Probability Breakdown</p>

                <div class="prob-row">
                    <span class="prob-name">Default Risk</span>
                    <div class="prob-bar-bg">
                        <div class="prob-bar-fill risk" style="width:{default_prob*100:.1f}%"></div>
                    </div>
                    <span class="prob-value risk">{default_prob*100:.1f}%</span>
                </div>

                <div class="prob-row" style="margin-bottom:0;">
                    <span class="prob-name">Repayment Probability</span>
                    <div class="prob-bar-bg">
                        <div class="prob-bar-fill repay" style="width:{repay_prob*100:.1f}%"></div>
                    </div>
                    <span class="prob-value repay">{repay_prob*100:.1f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Insight card
            st.markdown(f"""
            <div class="insight-card">
                <div class="insight-icon-wrap">📋</div>
                <p class="insight-text">{reason}</p>
            </div>
            """, unsafe_allow_html=True)

            # Input summary table
            st.markdown("""
            <div style="margin-top:16px;">
            <details style="background:#FFFFFF;border:1.5px solid #E0D8CE;
                    border-radius:16px;padding:16px 20px;cursor:pointer;">
                <summary style="font-size:13px;font-weight:600;color:#4A5568;
                        letter-spacing:0.03em;list-style:none;outline:none;">
                    ▸ &nbsp;View Input Summary
                </summary>
            """, unsafe_allow_html=True)

            st.markdown(f"""
                <table style="width:100%;margin-top:14px;font-size:13px;border-collapse:collapse;">
                    <tr style="background:#F5F3EE;">
                        <td style="padding:8px 12px;color:#6B7B8D;border-radius:6px 0 0 6px;">Loan Duration</td>
                        <td style="padding:8px 12px;color:#1C2B3A;font-weight:500;">{duration} months</td>
                        <td style="padding:8px 12px;color:#6B7B8D;">Credit Amount</td>
                        <td style="padding:8px 12px;color:#1C2B3A;font-weight:500;">{amount}</td>
                    </tr>
                    <tr>
                        <td style="padding:8px 12px;color:#6B7B8D;">Employment</td>
                        <td style="padding:8px 12px;color:#1C2B3A;font-weight:500;">{employment_duration} years</td>
                        <td style="padding:8px 12px;color:#6B7B8D;">Age</td>
                        <td style="padding:8px 12px;color:#1C2B3A;font-weight:500;">{age} years</td>
                    </tr>
                </table>
            </details>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        except ValueError:
            st.markdown("""
            <div class="error-box">
                <span style="font-size:20px;">⚠️</span>
                <span>Please enter valid numeric values in <strong>Duration</strong>,
                <strong>Amount</strong>, <strong>Employment Duration</strong>, and <strong>Age</strong>.</span>
            </div>
            """, unsafe_allow_html=True)

    # ── FOOTER ──
    st.markdown("""
    <div class="page-footer">
        <span>CreditLens Risk Intelligence Platform</span>
        <span>Powered by scikit-learn · For authorized use only</span>
    </div>
    """, unsafe_allow_html=True)
