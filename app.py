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
    "duration": "",
    "amount": "",
    "employment_duration": "",
    "age": "",
    "savings": 0,
    "credit_history": 0,
    "housing": 0,
    "job": 0,
    "result": None,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =============================
# FUNCTIONS
# =============================

def go(page):
    st.session_state.page = page
    st.rerun()


def reset_and_go_input():

    keys_to_clear = [
        "duration",
        "amount",
        "employment_duration",
        "age",
        "savings",
        "credit_history",
        "housing",
        "job"
    ]

    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

    st.session_state.result = None
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

.stApp {
    background: #F2EFE8 !important;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

[data-testid="stSidebar"] {
    display: none !important;
}

/* INPUTS */

div[data-testid="stTextInput"] input {
    background: #FFFFFF !important;
    border: 1.5px solid #D8D0C4 !important;
    border-radius: 12px !important;
    padding: 14px 16px !important;
    font-size: 17px !important;
    color: #1C2B3A !important;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #8B6F4E !important;
    box-shadow: 0 0 0 3px rgba(139,111,78,0.13) !important;
}

div[data-testid="stTextInput"] label,
div[data-testid="stSelectbox"] label {
    font-size: 15px !important;
    font-weight: 600 !important;
    color: #4A5568 !important;
}

div[data-testid="stSelectbox"] > div > div {
    background: #FFFFFF !important;
    border: 1.5px solid #D8D0C4 !important;
    border-radius: 12px !important;
    font-size: 17px !important;
    color: #1C2B3A !important;
}

/* BUTTONS */

div.stButton > button {
    font-size: 16px !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    height: 52px !important;
    border: none !important;
    transition: all 0.2s ease !important;
}

div.stButton > button[kind="primary"] {
    background: #1C2B3A !important;
    color: white !important;
}

div.stButton > button[kind="primary"]:hover {
    background: #2D4A62 !important;
    transform: translateY(-1px);
}

div.stButton > button[kind="secondary"] {
    background: white !important;
    color: #6B7B8D !important;
    border: 1.5px solid #D8D0C4 !important;
}

/* SECTION LABEL */

.sec-label {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #8B6F4E;
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 32px 0 18px;
}

.sec-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #D8D0C4;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# PAGE 1 — WELCOME
# =========================================================

if st.session_state.page == "welcome":

    st.markdown("""
    <style>

    .stApp {
        background: #1C2B3A !important;
    }

    .welcome-wrap {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 60px 20px;
    }

    .welcome-title {
        font-family: 'Playfair Display', serif;
        font-size: 68px;
        font-weight: 700;
        color: white;
        text-align: center;
        line-height: 1.15;
        margin-bottom: 18px;
    }

    .welcome-title span {
        color: #C9A96E;
    }

    .welcome-sub {
        font-size: 18px;
        color: rgba(255,255,255,0.6);
        text-align: center;
        max-width: 700px;
        line-height: 1.7;
        margin-bottom: 50px;
    }

    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3,1fr);
        gap: 18px;
        max-width: 900px;
        width: 100%;
        margin-top: 20px;
        margin-bottom: 50px;
    }

    .feat-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 24px;
    }

    .feat-title {
        font-size: 16px;
        font-weight: 700;
        color: white;
        margin-top: 12px;
        margin-bottom: 8px;
    }

    .feat-desc {
        font-size: 13px;
        color: rgba(255,255,255,0.5);
        line-height: 1.6;
    }

    </style>

    <div class="welcome-wrap">

        <h1 class="welcome-title">
            Smarter Lending Starts<br>
            with <span>Better Risk Intelligence</span>
        </h1>

        <p class="welcome-sub">
            Analyse borrower profiles instantly using machine learning powered
            credit intelligence and risk probability scoring.
        </p>

        <div class="feature-grid">

            <div class="feat-card">
                <div style="font-size:30px;">🧠</div>
                <div class="feat-title">ML Engine</div>
                <div class="feat-desc">
                    Trained using real credit behaviour and lending patterns.
                </div>
            </div>

            <div class="feat-card">
                <div style="font-size:30px;">📊</div>
                <div class="feat-title">Visual Analytics</div>
                <div class="feat-desc">
                    View probability scores and repayment insights instantly.
                </div>
            </div>

            <div class="feat-card">
                <div style="font-size:30px;">⚡</div>
                <div class="feat-title">Fast Assessment</div>
                <div class="feat-desc">
                    Analyse multiple borrowers in seconds with automated scoring.
                </div>
            </div>

        </div>

    </div>

    """, unsafe_allow_html=True)

    _, c1, _ = st.columns([3,2,3])

    with c1:
        if st.button(
            "🚀 Begin Assessment",
            use_container_width=True,
            type="primary"
        ):
            go("input")

# =========================================================
# PAGE 2 — INPUT FORM
# =========================================================

elif st.session_state.page == "input":

    st.markdown("""
    <div style="
        background:#1C2B3A;
        padding:16px 40px;
        display:flex;
        justify-content:space-between;
        align-items:center;
    ">

        <span style="
            font-family:'Playfair Display',serif;
            font-size:22px;
            color:#C9A96E;
            font-weight:700;
        ">
            CreditLens
        </span>

        <span style="
            color:rgba(255,255,255,0.45);
            font-size:13px;
            letter-spacing:0.08em;
            text-transform:uppercase;
        ">
            Applicant Assessment
        </span>

    </div>
    """, unsafe_allow_html=True)

    _, form_col, _ = st.columns([1,5,1])

    with form_col:

        st.markdown("""
        <div style="padding:42px 0 14px;text-align:center;">

            <p style="
               font-family:'Playfair Display',serif;
               font-size:34px;
               font-weight:700;
               color:#1C2B3A;
               margin:0 0 10px;">
               Borrower Details
            </p>

            <p style="
               font-size:17px;
               color:#6B7B8D;
               margin:0;
               line-height:1.7;">
               Fill in all borrower information carefully and click
               <strong style="color:#1C2B3A;">Analyse Risk</strong>.
            </p>

        </div>
        """, unsafe_allow_html=True)

        # LOAN DETAILS

        st.markdown(
            '<div class="sec-label">Loan Details</div>',
            unsafe_allow_html=True
        )

        c1, c2 = st.columns(2)

        with c1:
            duration = st.text_input(
                "Loan Duration (Months)",
                placeholder="e.g. 24",
                key="duration"
            )

        with c2:
            amount = st.text_input(
                "Credit Amount",
                placeholder="e.g. 50000",
                key="amount"
            )

        # FINANCIAL PROFILE

        st.markdown(
            '<div class="sec-label">Financial Profile</div>',
            unsafe_allow_html=True
        )

        c3, c4 = st.columns(2)

        with c3:
            savings = st.selectbox(
                "Savings Level",
                [0,1,2],
                format_func=lambda x: {
                    0:"🪙 Little Savings",
                    1:"💰 Moderate Savings",
                    2:"💎 Rich Savings"
                }[x],
                key="savings"
            )

        with c4:
            credit_history = st.selectbox(
                "Credit History",
                [0,1,2],
                format_func=lambda x: {
                    0:"⚠️ Poor",
                    1:"📊 Average",
                    2:"✅ Good"
                }[x],
                key="credit_history"
            )

        c5, c6 = st.columns(2)

        with c5:
            employment_duration = st.text_input(
                "Employment Duration (Years)",
                placeholder="e.g. 5",
                key="employment_duration"
            )

        with c6:
            age = st.text_input(
                "Age",
                placeholder="e.g. 30",
                key="age"
            )

        # PERSONAL CONTEXT

        st.markdown(
            '<div class="sec-label">Personal Context</div>',
            unsafe_allow_html=True
        )

        c7, c8 = st.columns(2)

        with c7:
            housing = st.selectbox(
                "Housing Type",
                [0,1,2],
                format_func=lambda x: {
                    0:"🏠 Rent",
                    1:"🏡 Own",
                    2:"🆓 Free"
                }[x],
                key="housing"
            )

        with c8:
            job = st.selectbox(
                "Job Skill Level",
                [0,1,2],
                format_func=lambda x: {
                    0:"🔧 Unskilled",
                    1:"💼 Skilled",
                    2:"🎓 Highly Skilled"
                }[x],
                key="job"
            )

        # BUTTONS

        st.markdown(
            "<div style='margin-top:40px;'></div>",
            unsafe_allow_html=True
        )

        left, center1, center2, right = st.columns([2,2,2,2])

        with center1:
            predict_btn = st.button(
                "🔍 Analyse Risk",
                use_container_width=True,
                type="primary"
            )

        with center2:
            reset_btn = st.button(
                "↺ Clear Form",
                use_container_width=True,
                type="secondary"
            )

        if reset_btn:
            reset_and_go_input()

        # PREDICTION

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

                probability = model.predict_proba(scaled_data)[0]

                default_prob = probability[0]
                repay_prob = 1 - default_prob

                if default_prob < 0.35:

                    result = "🟢 LOW RISK"

                elif default_prob < 0.80:

                    result = "🟡 MEDIUM RISK"

                else:

                    result = "🔴 HIGH RISK"

                st.markdown(f"""
                <div style="
                    margin-top:40px;
                    background:white;
                    border-radius:18px;
                    padding:30px;
                    border:1px solid #DDD7CE;
                    text-align:center;
                ">

                    <h2 style="
                        font-size:38px;
                        margin-bottom:18px;
                        color:#1C2B3A;
                    ">
                        {result}
                    </h2>

                    <p style="
                        font-size:18px;
                        color:#555;
                    ">
                        Default Probability:
                        <strong>{default_prob*100:.2f}%</strong>
                    </p>

                    <p style="
                        font-size:18px;
                        color:#555;
                    ">
                        Repayment Probability:
                        <strong>{repay_prob*100:.2f}%</strong>
                    </p>

                </div>
                """, unsafe_allow_html=True)

            except:
                st.error("Please enter valid numeric values.")

        st.markdown("""
        <div style="
            margin-top:50px;
            padding-top:20px;
            border-top:1px solid #D8D0C4;
            font-size:13px;
            color:#8B96A3;
            text-align:center;
        ">
            CreditLens Risk Intelligence · Powered by Machine Learning
        </div>
        """, unsafe_allow_html=True)
