import streamlit as st
import numpy as np
import pickle

# ============================================
# LOAD MODEL + SCALER
# ============================================

model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="Credit Risk Prediction",
    page_icon="🏦",
    layout="centered"
)

# ============================================
# SESSION STATE
# ============================================

if "reset_counter" not in st.session_state:
    st.session_state.reset_counter = 0

# ============================================
# RESET FUNCTION
# ============================================

def reset_form():
    st.session_state.reset_counter += 1

# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
<style>

.stApp {
    background-color: #f5f7fa;
}

.main-title {
    text-align: center;
    font-size: 44px;
    font-weight: bold;
    color: #1f2937;
    margin-bottom: 8px;
}

.sub-title {
    text-align: center;
    font-size: 19px;
    color: #6b7280;
    margin-bottom: 40px;
}

.result-box {
    padding: 28px;
    border-radius: 16px;
    text-align: center;
    margin-top: 35px;
    font-size: 24px;
    font-weight: bold;
}

.low-risk {
    background-color: #dcfce7;
    color: #166534;
    border: 2px solid #22c55e;
}

.medium-risk {
    background-color: #fef9c3;
    color: #854d0e;
    border: 2px solid #eab308;
}

.high-risk {
    background-color: #fee2e2;
    color: #991b1b;
    border: 2px solid #ef4444;
}

div[data-testid="stNumberInput"] input {
    font-size: 17px !important;
}

div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label {
    font-size: 16px !important;
    font-weight: 600 !important;
}

</style>
""", unsafe_allow_html=True)

# ============================================
# TITLE
# ============================================

st.markdown(
    "<div class='main-title'>🏦 Credit Risk Prediction</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='sub-title'>Enter borrower details to predict loan default risk</div>",
    unsafe_allow_html=True
)

# ============================================
# INPUT FIELDS
# ============================================

col1, col2 = st.columns(2)

with col1:

    duration = st.number_input(
        "Loan Duration (Months)",
        min_value=1,
        step=1,
        key=f"duration_{st.session_state.reset_counter}"
    )

    amount = st.number_input(
        "Credit Amount",
        min_value=0,
        step=1000,
        key=f"amount_{st.session_state.reset_counter}"
    )

    savings = st.selectbox(
        "Savings Level",
        ["Little Savings", "Moderate Savings", "Rich Savings"],
        key=f"savings_{st.session_state.reset_counter}"
    )

    employment_duration = st.number_input(
        "Employment Duration (Years)",
        min_value=0,
        step=1,
        key=f"employment_{st.session_state.reset_counter}"
    )

with col2:

    credit_history = st.selectbox(
        "Credit History",
        ["Poor", "Average", "Good"],
        key=f"credit_{st.session_state.reset_counter}"
    )

    age = st.number_input(
        "Age",
        min_value=18,
        step=1,
        key=f"age_{st.session_state.reset_counter}"
    )

    housing = st.selectbox(
        "Housing Type",
        ["Rent", "Own", "Free"],
        key=f"housing_{st.session_state.reset_counter}"
    )

    job = st.selectbox(
        "Job Skill Level",
        ["Unskilled", "Skilled", "Highly Skilled"],
        key=f"job_{st.session_state.reset_counter}"
    )

# ============================================
# CATEGORY MAPPING
# ============================================

savings_map = {
    "Little Savings": 0,
    "Moderate Savings": 1,
    "Rich Savings": 2
}

credit_map = {
    "Poor": 0,
    "Average": 1,
    "Good": 2
}

housing_map = {
    "Rent": 0,
    "Own": 1,
    "Free": 2
}

job_map = {
    "Unskilled": 0,
    "Skilled": 1,
    "Highly Skilled": 2
}

# ============================================
# BUTTONS
# ============================================

st.markdown("<br>", unsafe_allow_html=True)

left, center1, center2, right = st.columns([1,2,2,1])

with center1:
    predict_btn = st.button(
        "🔍 Predict Risk",
        use_container_width=True,
        type="primary"
    )

with center2:
    reset_btn = st.button(
        "↺ Reset Form",
        use_container_width=True
    )

# ============================================
# RESET
# ============================================

if reset_btn:
    reset_form()
    st.rerun()

# ============================================
# PREDICTION
# ============================================

if predict_btn:

    input_data = np.array([[
        duration,
        amount,
        savings_map[savings],
        credit_map[credit_history],
        employment_duration,
        age,
        housing_map[housing],
        job_map[job]
    ]])

    scaled_data = scaler.transform(input_data)

    # ============================================
    # PROBABILITY FIX
    # ============================================

    probability = model.predict_proba(scaled_data)[0]

    # Automatically detect default class
    classes = model.classes_

    if 1 in classes:
        default_index = list(classes).index(1)
    else:
        default_index = 0

    default_prob = probability[default_index]
    repay_prob = 1 - default_prob

    # ============================================
    # DEBUG INFO
    # ============================================

    st.write("Model Classes:", classes)
    st.write("Prediction Probabilities:", probability)

    # ============================================
    # RISK CLASSIFICATION
    # ============================================

    if default_prob < 0.35:

        risk = "🟢 LOW RISK"
        risk_class = "low-risk"

        reason = """
        Borrower shows strong financial indicators such as
        good credit behaviour, stable employment, and better repayment capacity.
        """

    elif default_prob < 0.75:

        risk = "🟡 MEDIUM RISK"
        risk_class = "medium-risk"

        reason = """
        Borrower shows mixed financial indicators.
        Some factors indicate repayment capability while others introduce moderate risk.
        """

    else:

        risk = "🔴 HIGH RISK"
        risk_class = "high-risk"

        reason = """
        Borrower shows weaker financial indicators such as
        poor credit history, low savings, or unstable employment.
        """

    # ============================================
    # RESULT DISPLAY
    # ============================================

    st.markdown(f"""
    <div class='result-box {risk_class}'>

        {risk}

        <br><br>

        🔴 Default Risk: {default_prob*100:.2f}%

        <br><br>

        🟢 Repayment Probability: {repay_prob*100:.2f}%

        <br><br>

        📌 Reason:
        {reason}

    </div>
    """, unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================

st.markdown("""
<br><br>

<div style="
    text-align:center;
    color:#6b7280;
    font-size:14px;
">
    CreditLens Risk Intelligence <br>
    Powered by scikit-learn · For authorized use only
</div>
""", unsafe_allow_html=True)
