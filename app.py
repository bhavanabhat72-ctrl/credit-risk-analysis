import streamlit as st
import numpy as np
import pickle

model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

# ── debug: print classes order once ──────────────────────
# Uncomment the line below temporarily to check your model's class order
# st.write("Model classes:", model.classes_)

st.set_page_config(
    page_title="CreditLens — Risk Intelligence",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Session state ──────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "input"

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

# ── Shared CSS ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
#MainMenu, footer, header   { visibility: hidden; }
.block-container            { padding: 0 !important; max-width: 100% !important; }
[data-testid="stSidebar"]   { display: none !important; }

div[data-testid="stTextInput"] input {
    background:#fff !important; border:1.5px solid #D8D0C4 !important;
    border-radius:10px !important; padding:12px 15px !important;
    font-family:'DM Sans',sans-serif !important; font-size:17px !important;
    color:#1C2B3A !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color:#8B6F4E !important;
    box-shadow:0 0 0 3px rgba(139,111,78,0.13) !important;
}
div[data-testid="stTextInput"] label,
div[data-testid="stSelectbox"] label {
    font-size:15px !important; font-weight:500 !important; color:#4A5568 !important;
}
div[data-testid="stSelectbox"] > div > div {
    background:#fff !important; border:1.5px solid #D8D0C4 !important;
    border-radius:10px !important; font-size:17px !important;
    font-family:'DM Sans',sans-serif !important; color:#1C2B3A !important;
}

div.stButton > button {
    font-family:'DM Sans',sans-serif !important; font-size:16px !important;
    font-weight:600 !important; border-radius:10px !important;
    height:50px !important; border:none !important; transition:all 0.2s !important;
}
div.stButton > button[kind="primary"] {
    background:#1C2B3A !important; color:white !important;
}
div.stButton > button[kind="primary"]:hover {
    background:#2D4A62 !important;
    box-shadow:0 4px 16px rgba(28,43,58,0.28) !important;
    transform:translateY(-1px) !important;
}
div.stButton > button[kind="secondary"] {
    background:#fff !important; color:#6B7B8D !important;
    border:1.5px solid #D8D0C4 !important;
}
div.stButton > button[kind="secondary"]:hover {
    border-color:#8B6F4E !important; color:#8B6F4E !important;
}
</style>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════╗
# ║  PAGE 1 — INPUT FORM                                ║
# ╚══════════════════════════════════════════════════════╝
if st.session_state.page == "input":

    st.markdown("<style>.stApp { background:#F2EFE8 !important; }</style>",
                unsafe_allow_html=True)

    # nav bar
    st.markdown("""
    <div style="background:#1C2B3A;padding:15px 40px;
         display:flex;align-items:center;justify-content:space-between;">
      <span style="font-family:'Playfair Display',serif;font-size:20px;
            font-weight:700;color:#C9A96E;">CreditLens</span>
      <span style="font-size:12px;color:rgba(255,255,255,0.38);
            letter-spacing:0.1em;text-transform:uppercase;">Applicant Assessment</span>
    </div>
    """, unsafe_allow_html=True)

    # progress
    st.markdown("""
    <div style="background:#EAE6DE;padding:10px 40px;
         display:flex;align-items:center;gap:10px;border-bottom:1px solid #D8D0C4;">
      <span style="width:24px;height:24px;border-radius:50%;background:#1C2B3A;
            color:white;font-size:12px;font-weight:700;display:inline-flex;
            align-items:center;justify-content:center;flex-shrink:0;">1</span>
      <span style="font-size:13px;font-weight:600;color:#1C2B3A;">Enter Details</span>
      <span style="color:#D8D0C4;margin:0 6px;">──────</span>
      <span style="width:24px;height:24px;border-radius:50%;background:#D8D0C4;
            color:#8B96A3;font-size:12px;font-weight:700;display:inline-flex;
            align-items:center;justify-content:center;flex-shrink:0;">2</span>
      <span style="font-size:13px;color:#8B96A3;">View Results</span>
    </div>
    """, unsafe_allow_html=True)

    _, form_col, _ = st.columns([1, 5, 1])
    with form_col:

        st.markdown("""
        <div style="padding:36px 0 6px;">
          <p style="font-family:'Playfair Display',serif;font-size:30px;font-weight:700;
             color:#1C2B3A;margin:0 0 6px;">Borrower Details</p>
          <p style="font-size:17px;color:#8B96A3;margin:0;">
            Fill in all fields and click
            <strong style="color:#1C2B3A;">Analyse Risk</strong>.
          </p>
        </div>
        """, unsafe_allow_html=True)

        def sec(label):
            st.markdown(f"""
            <div style="font-size:11px;font-weight:700;letter-spacing:0.18em;
                 text-transform:uppercase;color:#8B6F4E;display:flex;
                 align-items:center;gap:10px;margin:26px 0 14px;">
              {label}
              <span style="flex:1;height:1px;background:#D8D0C4;display:block;"></span>
            </div>
            """, unsafe_allow_html=True)

        sec("Loan Details")
        c1, c2 = st.columns(2, gap="medium")
        with c1:
            duration = st.text_input("Loan Duration (Months)", placeholder="e.g. 24", key="duration")
        with c2:
            amount = st.text_input("Credit Amount (₹ / $)", placeholder="e.g. 50000", key="amount")

        sec("Financial Profile")
        c3, c4 = st.columns(2, gap="medium")
        with c3:
            savings = st.selectbox("Savings Level", options=[0,1,2],
                format_func=lambda x:{0:"🪙  Little Savings",1:"💰  Moderate Savings",2:"💎  Rich Savings"}[x],
                key="savings")
        with c4:
            credit_history = st.selectbox("Credit History", options=[0,1,2],
                format_func=lambda x:{0:"⚠️  Poor",1:"📊  Average",2:"✅  Good"}[x],
                key="credit_history")

        c5, c6 = st.columns(2, gap="medium")
        with c5:
            employment_duration = st.text_input("Employment Duration (Years)", placeholder="e.g. 5", key="employment_duration")
        with c6:
            age = st.text_input("Age", placeholder="e.g. 34", key="age")

        sec("Personal Context")
        c7, c8 = st.columns(2, gap="medium")
        with c7:
            housing = st.selectbox("Housing Type", options=[0,1,2],
                format_func=lambda x:{0:"🏠  Rent",1:"🏡  Own",2:"🆓  Free"}[x],
                key="housing")
        with c8:
            job = st.selectbox("Job Skill Level", options=[0,1,2],
                format_func=lambda x:{0:"🔧  Unskilled",1:"💼  Skilled",2:"🎓  Highly Skilled"}[x],
                key="job")

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
                scaled = scaler.transform(input_data)

                # ── FIX: check actual class order from model ──────────
                # model.classes_ tells us which index = default (1) vs good (0)
                # Most credit models: class 1 = default/bad, class 0 = good
                classes = list(model.classes_)
                proba   = model.predict_proba(scaled)[0]

                if 1 in classes:
                    # class label 1 means "default / bad credit"
                    default_idx = classes.index(1)
                else:
                    # fallback: use index 0
                    default_idx = 0

                dp = float(proba[default_idx])
                rp = 1.0 - dp

                # ── risk thresholds ───────────────────────────────────
                if dp < 0.40:
                    tier, icon = "low",    "🟢"
                    verdict  = "Low Risk Applicant"
                    tagline  = "Strong financial indicators — recommended for approval."
                    reason   = "<strong>Positive signals detected.</strong> This applicant demonstrates solid financial stability — good credit history, adequate savings, and consistent employment. The probability of default is low."
                elif dp < 0.70:
                    tier, icon = "medium", "🟡"
                    verdict  = "Medium Risk Applicant"
                    tagline  = "Mixed indicators — consider with additional due diligence."
                    reason   = "<strong>Mixed signals present.</strong> Some factors support repayment capacity while others introduce moderate uncertainty. Review employment stability and savings depth before proceeding."
                else:
                    tier, icon = "high",   "🔴"
                    verdict  = "High Risk Applicant"
                    tagline  = "Weak financials — recommend declining or requiring collateral."
                    reason   = "<strong>Significant risk factors identified.</strong> Poor credit history, minimal savings, or limited employment history. High probability of default."

                st.session_state.result = {
                    "tier":tier, "icon":icon, "verdict":verdict,
                    "tagline":tagline, "reason":reason, "dp":dp, "rp":rp,
                    "inputs":{
                        "Duration":     f"{duration} months",
                        "Amount":       amount,
                        "Savings":      {0:"Little",1:"Moderate",2:"Rich"}[int(savings)],
                        "Credit History":{0:"Poor",1:"Average",2:"Good"}[int(credit_history)],
                        "Employment":   f"{employment_duration} yrs",
                        "Age":          f"{age} yrs",
                        "Housing":      {0:"Rent",1:"Own",2:"Free"}[int(housing)],
                        "Job Level":    {0:"Unskilled",1:"Skilled",2:"Highly Skilled"}[int(job)],
                    }
                }
                go("result")

            except ValueError:
                st.markdown("""
                <div style="background:#FEF2F2;border:1.5px solid #FECACA;border-radius:12px;
                     padding:16px 20px;font-size:16px;color:#B91C1C;
                     display:flex;gap:12px;align-items:center;margin-top:16px;">
                  <span style="font-size:22px;">⚠️</span>
                  <span>Please enter valid numbers in <strong>Duration</strong>,
                  <strong>Amount</strong>, <strong>Employment Duration</strong>,
                  and <strong>Age</strong>.</span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("""
        <div style="margin-top:48px;padding-top:18px;border-top:1px solid #D8D0C4;
             font-size:13px;color:#A09585;display:flex;justify-content:space-between;
             margin-bottom:32px;">
          <span>CreditLens Risk Intelligence</span>
          <span>Powered by scikit-learn · For authorized use only</span>
        </div>
        """, unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════╗
# ║  PAGE 2 — RESULTS                                   ║
# ╚══════════════════════════════════════════════════════╝
elif st.session_state.page == "result":

    st.markdown("<style>.stApp { background:#F2EFE8 !important; }</style>",
                unsafe_allow_html=True)

    r = st.session_state.result
    if r is None:
        go("input")

    dp, rp, tier = r["dp"], r["rp"], r["tier"]

    cfg = {
        "low":    ("#E6F4EC","#89CFA8","#145C35","#D1EDDC"),
        "medium": ("#FEF3E2","#F5C97E","#7D4E00","#FDEBC8"),
        "high":   ("#FDECEA","#F5A99F","#881515","#FAD7D4"),
    }
    hdr_bg, hdr_bdr, verd_col, badge_bg = cfg[tier]

    # nav bar
    st.markdown("""
    <div style="background:#1C2B3A;padding:15px 40px;
         display:flex;align-items:center;justify-content:space-between;">
      <span style="font-family:'Playfair Display',serif;font-size:20px;
            font-weight:700;color:#C9A96E;">CreditLens</span>
      <span style="font-size:12px;color:rgba(255,255,255,0.38);
            letter-spacing:0.1em;text-transform:uppercase;">Risk Assessment Report</span>
    </div>
    """, unsafe_allow_html=True)

    # progress — step 2
    st.markdown("""
    <div style="background:#EAE6DE;padding:10px 40px;
         display:flex;align-items:center;gap:10px;border-bottom:1px solid #D8D0C4;">
      <span style="width:24px;height:24px;border-radius:50%;background:#4CAF82;
            color:white;font-size:12px;font-weight:700;display:inline-flex;
            align-items:center;justify-content:center;flex-shrink:0;">✓</span>
      <span style="font-size:13px;font-weight:600;color:#4CAF82;">Details Entered</span>
      <span style="color:#D8D0C4;margin:0 6px;">──────</span>
      <span style="width:24px;height:24px;border-radius:50%;background:#1C2B3A;
            color:white;font-size:12px;font-weight:700;display:inline-flex;
            align-items:center;justify-content:center;flex-shrink:0;">2</span>
      <span style="font-size:13px;font-weight:600;color:#1C2B3A;">Risk Report</span>
    </div>
    """, unsafe_allow_html=True)

    _, res_col, _ = st.columns([1, 5, 1])
    with res_col:

        st.markdown("<div style='padding-top:32px;'></div>", unsafe_allow_html=True)

        # verdict card
        st.markdown(f"""
        <div style="background:{hdr_bg};border:1.5px solid {hdr_bdr};border-radius:18px;
             padding:26px 30px;display:flex;align-items:center;gap:18px;margin-bottom:14px;">
          <span style="font-size:50px;line-height:1;">{r['icon']}</span>
          <div style="flex:1;">
            <p style="font-family:'Playfair Display',serif;font-size:28px;font-weight:700;
               color:{verd_col};margin:0 0 5px;">{r['verdict']}</p>
            <p style="font-size:15px;color:#6B7B8D;margin:0;">{r['tagline']}</p>
          </div>
          <span style="background:{badge_bg};color:{verd_col};font-size:14px;font-weight:700;
                padding:9px 20px;border-radius:100px;white-space:nowrap;flex-shrink:0;">
            Default: {dp*100:.1f}%
          </span>
        </div>
        """, unsafe_allow_html=True)

        # probability bars
        st.markdown(f"""
        <div style="background:#fff;border:1.5px solid #DDD7CE;border-radius:16px;
             padding:22px 26px;margin-bottom:14px;">
          <p style="font-size:11px;font-weight:700;letter-spacing:0.15em;
             text-transform:uppercase;color:#8B96A3;margin:0 0 18px;">
             Probability Breakdown
          </p>
          <div style="display:flex;align-items:center;gap:14px;margin-bottom:14px;">
            <span style="font-size:15px;font-weight:500;color:#1C2B3A;
                  width:190px;flex-shrink:0;">Default Risk</span>
            <div style="flex:1;height:10px;background:#EDE8E1;border-radius:100px;overflow:hidden;">
              <div style="width:{dp*100:.1f}%;height:100%;border-radius:100px;
                   background:linear-gradient(90deg,#E24B4A,#B91C1C);"></div>
            </div>
            <span style="font-size:16px;font-weight:700;color:#B91C1C;
                  width:54px;text-align:right;">{dp*100:.1f}%</span>
          </div>
          <div style="display:flex;align-items:center;gap:14px;">
            <span style="font-size:15px;font-weight:500;color:#1C2B3A;
                  width:190px;flex-shrink:0;">Repayment Probability</span>
            <div style="flex:1;height:10px;background:#EDE8E1;border-radius:100px;overflow:hidden;">
              <div style="width:{rp*100:.1f}%;height:100%;border-radius:100px;
                   background:linear-gradient(90deg,#22C55E,#15803D);"></div>
            </div>
            <span style="font-size:16px;font-weight:700;color:#15803D;
                  width:54px;text-align:right;">{rp*100:.1f}%</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # insight
        st.markdown(f"""
        <div style="background:#fff;border:1.5px solid #DDD7CE;border-radius:16px;
             padding:20px 24px;display:flex;gap:14px;align-items:flex-start;
             margin-bottom:14px;">
          <span style="font-size:24px;flex-shrink:0;">📋</span>
          <p style="font-size:15px;color:#4A5568;line-height:1.65;margin:0;">
            {r['reason']}
          </p>
        </div>
        """, unsafe_allow_html=True)

        # input summary
        rows = "".join([
            f"""<div style="display:flex;justify-content:space-between;
                padding:10px 0;border-bottom:1px solid #F0EBE3;">
              <span style="font-size:14px;color:#8B96A3;">{k}</span>
              <span style="font-size:14px;font-weight:600;color:#1C2B3A;">{v}</span>
            </div>"""
            for k, v in r["inputs"].items()
        ])
        st.markdown(f"""
        <div style="background:#fff;border:1.5px solid #DDD7CE;border-radius:16px;
             padding:20px 24px;margin-bottom:20px;">
          <p style="font-size:11px;font-weight:700;letter-spacing:0.15em;
             text-transform:uppercase;color:#8B96A3;margin:0 0 12px;">
             Input Summary
          </p>
          {rows}
        </div>
        """, unsafe_allow_html=True)

        # new borrower banner
        st.markdown("""
        <div style="background:linear-gradient(135deg,#1C2B3A,#2D4A62);
             border-radius:18px;padding:28px 32px;text-align:center;margin-bottom:16px;">
          <p style="font-family:'Playfair Display',serif;font-size:22px;font-weight:700;
             color:#FFFFFF;margin:0 0 8px;">Analyse Another Borrower?</p>
          <p style="font-size:15px;color:rgba(255,255,255,0.48);margin:0 0 24px;">
            Clear the form and assess a new applicant instantly.
          </p>
        </div>
        """, unsafe_allow_html=True)

        a1, a2 = st.columns(2, gap="medium")
        with a1:
            if st.button("🔄  New Borrower Assessment", use_container_width=True, type="primary"):
                reset_and_go_input()
        with a2:
            if st.button("🏠  Back to Input", use_container_width=True, type="secondary"):
                go("input")

        st.markdown("""
        <div style="margin-top:40px;padding-top:18px;border-top:1px solid #D8D0C4;
             font-size:13px;color:#A09585;display:flex;justify-content:space-between;
             margin-bottom:32px;">
          <span>CreditLens Risk Intelligence</span>
          <span>Powered by scikit-learn · For authorized use only</span>
        </div>
        """, unsafe_allow_html=True)
