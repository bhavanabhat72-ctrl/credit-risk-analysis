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
    page_title="Credit Risk Analysis",
    page_icon="💳",
    layout="centered"
)

# =============================
# CUSTOM CSS
# =============================

st.markdown("""
<style>

.main-title{
    text-align:center;
    font-size:42px;
    font-weight:bold;
    color:#1E3A8A;
}

.sub-title{
    text-align:center;
    font-size:18px;
    color:gray;
    margin-bottom:20px;
}

div.stButton > button{
    width:100%;
    border-radius:10px;
    height:3em;
    font-size:16px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# =============================
# TITLE
# =============================

st.markdown(
    "<div class='main-title'>💳 Credit Risk Analysis System</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='sub-title'>Predict whether a customer is Low Risk or High Risk</div>",
    unsafe_allow_html=True
)

st.markdown("---")

# =============================
# SESSION STATE
# =============================

if "duration" not in st.session_state:
    st.session_state.duration = ""

if "amount" not in st.session_state:
    st.session_state.amount = ""

if "employment_duration" not in st.session_state:
    st.session_state.employment_duration = ""

if "age" not in st.session_state:
    st.session_state.age = ""

if "savings" not in st.session_state:
    st.session_state.savings = 0

if "credit_history" not in st.session_state:
    st.session_state.credit_history = 0

if "housing" not in st.session_state:
    st.session_state.housing = 0

if "job" not in st.session_state:
    st.session_state.job = 0

# =============================
# RESET FUNCTION
# =============================

def reset_inputs():

    st.session_state.duration = ""
    st.session_state.amount = ""
    st.session_state.employment_duration = ""
    st.session_state.age = ""

    st.session_state.savings = 0
    st.session_state.credit_history = 0
    st.session_state.housing = 0
    st.session_state.job = 0

    st.rerun()

# =============================
# INPUT FIELDS
# =============================

duration = st.text_input(
    "Loan Duration (Months)",
    placeholder="Example: 12",
    key="duration"
)

amount = st.text_input(
    "Credit Amount",
    placeholder="Example: 5000",
    key="amount"
)

savings = st.selectbox(
    "Savings Level",
    options=[0, 1, 2],
    index=st.session_state.savings,
    format_func=lambda x: {
        0: "0 - Little Savings",
        1: "1 - Moderate Savings",
        2: "2 - Rich Savings"
    }[x],
    key="savings"
)

credit_history = st.selectbox(
    "Credit History",
    options=[0, 1, 2],
    index=st.session_state.credit_history,
    format_func=lambda x: {
        0: "0 - Poor",
        1: "1 - Average",
        2: "2 - Good"
    }[x],
    key="credit_history"
)

employment_duration = st.text_input(
    "Employment Duration (Years)",
    placeholder="Example: 5",
    key="employment_duration"
)

age = st.text_input(
    "Age",
    placeholder="Example: 30",
    key="age"
)

housing = st.selectbox(
    "Housing Type",
    options=[0, 1, 2],
    index=st.session_state.housing,
    format_func=lambda x: {
        0: "0 - Rent",
        1: "1 - Own",
        2: "2 - Free"
    }[x],
    key="housing"
)

job = st.selectbox(
    "Job Skill Level",
    options=[0, 1, 2],
    index=st.session_state.job,
    format_func=lambda x: {
        0: "0 - Unskilled",
        1: "1 - Skilled",
        2: "2 - Highly Skilled"
    }[x],
    key="job"
)

st.markdown("---")

# =============================
# CENTERED BUTTONS
# =============================

space1, col1, col2, space2 = st.columns([1,2,2,1])

with col1:
    predict_btn = st.button("🔍 Predict")

with col2:
    reset_btn = st.button("🔄 Reset")

# =============================
# RESET ACTION
# =============================

if reset_btn:
    reset_inputs()

# =============================
# PREDICTION
# =============================

if predict_btn:

    try:

        # =============================
        # INPUT ARRAY
        # =============================

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

        # =============================
        # SCALE DATA
        # =============================

        scaled_data = scaler.transform(input_data)

        # =============================
        # MODEL PREDICTION
        # =============================

        probability = model.predict_proba(scaled_data)[0]

        # =============================
        # PROBABILITY SMOOTHING
        # =============================

        raw_prob = probability[0]

        # Neutralized probability
        default_prob = 0.15 + (raw_prob * 0.7)

        # Safety cap
        default_prob = min(max(default_prob, 0.05), 0.95)

        st.markdown("---")

        # =============================
        # LOW RISK
        # =============================

        if default_prob < 0.35:

            st.success("🟢 LOW RISK")

            st.write(
                f"🔴 Default Risk: {default_prob*100:.2f}%"
            )

            st.write(
                f"🟢 Repayment Probability: {(1-default_prob)*100:.2f}%"
            )

            st.info(
                "📌 Reason: Borrower shows strong financial stability "
                "with good credit history, stable employment, and healthy savings."
            )

        # =============================
        # MEDIUM RISK
        # =============================

        elif default_prob < 0.80:

            st.warning("🟠 MEDIUM RISK")

            st.write(
                f"🔴 Default Risk: {default_prob*100:.2f}%"
            )

            st.write(
                f"🟢 Repayment Probability: {(1-default_prob)*100:.2f}%"
            )

            st.info(
                "📌 Reason: Borrower shows moderate financial indicators. "
                "Certain factors indicate repayment ability while others "
                "suggest moderate default risk."
            )

        # =============================
        # HIGH RISK
        # =============================

        else:

            st.error("🔴 HIGH RISK")

            st.write(
                f"🔴 Default Risk: {default_prob*100:.2f}%"
            )

            st.write(
                f"🟢 Repayment Probability: {(1-default_prob)*100:.2f}%"
            )

            st.info(
                "📌 Reason: Borrower shows weaker financial indicators "
                "such as low savings, poor credit history, or unstable employment."
            )

    except:

        st.error(
            "⚠️ Please enter valid numeric values in all text fields."
        )
