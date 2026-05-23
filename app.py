import streamlit as st
import numpy as np
import pickle

# Load model + scaler
model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

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
    st.session_state.clear()
    st.rerun()

# =============================
# INPUTS
# =============================

duration = st.number_input("Loan Duration (Months)", min_value=1, step=1)

amount = st.number_input("Credit Amount", min_value=1, step=100)

savings = st.selectbox(
    "Savings Level",
    options=[0, 1, 2],
    format_func=lambda x: {
        0: "0 - Little Savings",
        1: "1 - Moderate Savings",
        2: "2 - Rich Savings"
    }[x]
)

credit_history = st.selectbox(
    "Credit History",
    options=[0, 1, 2],
    format_func=lambda x: {
        0: "0 - Poor",
        1: "1 - Average",
        2: "2 - Good"
    }[x]
)

employment_duration = st.number_input("Employment Duration (Years)", min_value=0, step=1)

age = st.number_input("Age", min_value=18, step=1)

housing = st.selectbox(
    "Housing Type",
    options=[0, 1, 2],
    format_func=lambda x: {
        0: "0 - Rent",
        1: "1 - Own",
        2: "2 - Free"
    }[x]
)

job = st.selectbox(
    "Job Skill Level",
    options=[0, 1, 2],
    format_func=lambda x: {
        0: "0 - Unskilled",
        1: "1 - Skilled",
        2: "2 - Highly Skilled"
    }[x]
)

st.markdown("---")

# =============================
# BUTTONS (SAME LINE)
# =============================

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    predict_btn = st.button("🔍 Predict")

with col2:
    reset_btn = st.button("🔄 Reset")

# Reset action
if reset_btn:
    reset_inputs()

# =============================
# PREDICTION
# =============================

if predict_btn:

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

    scaled_data = scaler.transform(input_data)

    prediction = model.predict(scaled_data)[0]
    probability = model.predict_proba(scaled_data)[0]

    default_prob = probability[1]

    st.markdown("---")

    # =============================
    # RESULT + EXPLANATION
    # =============================

    if default_prob < 0.40:
        st.success("🟢 LOW RISK")
        st.write(f"Probability of Default: {default_prob*100:.2f}%")

        st.info(
            "📌 Reason: Borrower shows strong financial stability "
            "(good credit history, sufficient savings, stable employment)."
        )

    elif default_prob < 0.70:
        st.warning("🟠 MEDIUM RISK")
        st.write(f"Probability of Default: {default_prob*100:.2f}%")

        st.info(
            "📌 Reason: Borrower has mixed signals such as moderate savings "
            "or average credit history, leading to uncertain repayment ability."
        )

    else:
        st.error("🔴 HIGH RISK")
        st.write(f"Probability of Default: {default_prob*100:.2f}%")

        st.info(
            "📌 Reason: Borrower shows weak financial indicators such as low savings, "
            "poor credit history, or unstable employment, increasing default risk."
        )
