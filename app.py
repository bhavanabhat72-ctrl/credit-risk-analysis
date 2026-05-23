# app.py

```python
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

# =============================
# FUNCTIONS
# =============================

def go(page):
    st.session_state.page = page
    st.rerun()


def reset_form():

    fields = [
        "duration",
        "amount",
        "employment_duration",
        "age",
        "savings",
        "credit_history",
        "housing",
        "job"
    ]

    for field in fields:
        if field in st.session_state:
            del st.session_state[field]

    st.rerun()

# =============================
# GLOBAL CSS
# =============================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #F2EFE8;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    padding-top: 0rem;
    max-width: 100%;
}

/* INPUTS */

div[data-testid="stTextInput"] input {
    background: white;
    border: 1.5px solid #D8D0C4;
    border-radius: 12px;
    padding: 14px 16px;
    font-size: 17px;
    color: #1C2B3A;
}

/* LABELS */

div[data-testid="stTextInput"] label,
div[data-testid="stSelectbox"] label {
    font-size: 15px;
    font-weight: 600;
    color: #4A5568;
}

/* SELECT BOX */

div[data-testid="stSelectbox"] > div > div {
    background: white;
    border: 1.5px solid #D8D0C4;
    border-radius: 12px;
    font-size: 17px;
    color: #1C2B3A;
}

/* BUTTONS */

div.stButton > button {
    font-size: 16px;
    font-weight: 600;
    border-radius: 12px;
    height: 52px;
    border: none;
}

div.stButton > button[kind="primary"] {
    background: #1C2B3A;
    color: white;
}

div.stButton > button[kind="secondary"] {
    background: white;
    color: #6B7B8D;
    border: 1px solid #D8D0C4;
}

.sec-label {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #8B6F4E;
    margin: 32px 0 18px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# PAGE 1 — WELCOME
# =========================================================

if st.session_state.page == "welcome":

    st.markdown("""
    <div style="
        min-height:100vh;
        display:flex;
        flex-direction:column;
        justify-content:center;
        align-items:center;
        background:#1C2B3A;
        padding:40px;
    ">

        <h1 style="
            font-family:'Playfair Display',serif;
            font-size:70px;
            color:white;
            text-align:center;
            line-height:1.1;
        ">
            Smarter Lending Starts<br>
            with <span style='color:#C9A96E;'>Better Risk Intelligence</span>
        </h1>

        <p style="
            color:rgba(255,255,255,0.65);
            font-size:18px;
            text-align:center;
            max-width:700px;
            line-height:1.7;
            margin-top:10px;
        ">
            Analyse borrower profiles instantly using machine learning powered
            credit intelligence and risk scoring.
        </p>

    </div>
    """, unsafe_allow_html=True)

    _, center, _ = st.columns([3,2,3])

    with center:
        if st.button("🚀 Begin Assessment", use_container_width=True, type="primary"):
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
               Fill in all borrower information carefully.
            </p>

        </div>
        """, unsafe_allow_html=True)

        # LOAN DETAILS

        st.markdown('<div class="sec-label">Loan Details</div>', unsafe_allow_html=True)

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

        st.markdown('<div class="sec-label">Financial Profile</div>', unsafe_allow_html=True)

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

        st.markdown('<div class="sec-label">Personal Context</div>', unsafe_allow_html=True)

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

        st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)

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
            reset_form()

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

                    <p style="font-size:18px;color:#555;">
                        Default Probability:
                        <strong>{default_prob*100:.2f}%</strong>
                    </p>

                    <p style="font-size:18px;color:#555;">
                        Repayment Probability:
                        <strong>{repay_prob*100:.2f}%</strong>
                    </p>

                </div>
                """, unsafe_allow_html=True)

            except:
                st.error("Please enter valid numeric values.")

```
