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

st.title("💳 Credit Risk Analysis System")
st.write("Predict whether a customer is Low Risk or High Risk")

st.markdown("---")

# =============================
# RESET FUNCTION
# =============================

def reset_inputs():
    st.session_state.duration = 1
    st.session_state.amount = 1000
    st.session_state.savings = 0
    st.session_state.credit_history = 1
    st.session_state.employment_duration = 0
    st.session_state.age = 18
    st.session_state.housing = 0
    st.session_state.job = 0
    st.rerun()

# =============================
# INPUT FIELDS
# =============================

duration = st.number_input("Loan Duration (Months)", min_value=1, step=1, key="duration")

amount = st.number_input("Credit Amount", min_value=1, step=100, key="amount")

savings = st.selectbox(
    "Savings Level",
    options=[0, 1, 2],
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
    format_func=lambda x: {
        0: "0 - Poor",
        1: "1 - Average",
        2: "2 - Good"
    }[x],
    key="credit_history"
)

employment_duration = st.number_input(
    "Employment Duration (Years)",
    min_value=0,
    step=1,
    key="employment_duration"
)

age = st.number_input("Age", min_value=18, step=1, key="age")

housing = st.selectbox(
    "Housing Type",
    options=[0, 1, 2],
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
    format_func=lambda x: {
        0: "0 - Unskilled",
        1: "1 - Skilled",
        2: "2 - Highly Skilled"
    }[x],
    key="job"
)

st.markdown("---")

# =============================
# BUTTONS (SAME LINE)
# =============================

col1, col2 = st.columns(2)

with col1:
    predict_btn = st.button("🔍 Predict Credit Risk")

with col2:
    reset_btn = st.button("🔄 Reset")

if reset_btn:
    reset_inputs()

# =============================
# PREDICTION
# =============================

if predict_btn:

    # Feature vector (MUST match training order)
    input_data = np.array([[
        duration,
        amount,
        savings,
        credit_history,
        employment_duration,
        age,
        housing,
        job
    ]])

    # Convert safely
    input_data = input_data.astype(float)

    # Scale
    scaled_data = scaler.transform(input_data)

    # Predict
    prediction = model.predict(scaled_data)[0]
    probability = model.predict_proba(scaled_data)[0]

    default_prob = probability[1]

    st.markdown("---")

    # =============================
    # RESULT SECTION
    # =============================

    if default_prob < 0.40:
        st.success("🟢 LOW RISK")

        st.write(f"🔴 Default Risk: {default_prob*100:.2f}%")
        st.write(f"🟢 Repayment Probability: {(1-default_prob)*100:.2f}%")

        st.info(
            "📌 Reason: Strong financial profile with good credit history, "
            "stable income, and sufficient savings."
        )

    elif default_prob < 0.70:
        st.warning("🟠 MEDIUM RISK")

        st.write(f"🔴 Default Risk: {default_prob*100:.2f}%")
        st.write(f"🟢 Repayment Probability: {(1-default_prob)*100:.2f}%")

        st.info(
            "📌 Reason: Mixed financial signals such as average credit history "
            "or moderate savings leading to uncertainty."
        )

    else:
        st.error("🔴 HIGH RISK")

        st.write(f"🔴 Default Risk: {default_prob*100:.2f}%")
        st.write(f"🟢 Repayment Probability: {(1-default_prob)*100:.2f}%")

        st.info(
            "📌 Reason: Weak financial profile including low savings, poor credit history, "
            "or unstable employment increases default probability."
        )
