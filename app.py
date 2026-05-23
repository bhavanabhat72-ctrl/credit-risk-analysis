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

# -----------------------------
# RESET FUNCTION
# -----------------------------
def reset_inputs():
    st.session_state.duration = 12
    st.session_state.amount = 5000
    st.session_state.savings = 0
    st.session_state.credit_history = 1
    st.session_state.employment = 2
    st.session_state.age = 30
    st.session_state.housing = 0
    st.session_state.job = 1


# Initialize session state
if "duration" not in st.session_state:
    reset_inputs()

# -----------------------------
# INPUT FIELDS (SAFE UI)
# -----------------------------

duration = st.number_input(
    "Loan Duration (Months)",
    min_value=1,
    max_value=120,
    key="duration"
)

amount = st.number_input(
    "Credit Amount",
    min_value=100,
    max_value=100000,
    key="amount"
)

savings = st.selectbox(
    "Savings Level",
    options=[0, 1, 2],
    format_func=lambda x: ["Little", "Moderate", "Rich"][x],
    key="savings"
)

credit_history = st.selectbox(
    "Credit History",
    options=[0, 1, 2],
    format_func=lambda x: ["Poor", "Average", "Good"][x],
    key="credit_history"
)

employment_duration = st.number_input(
    "Employment Duration (Years)",
    min_value=0,
    max_value=40,
    key="employment"
)

age = st.number_input(
    "Age",
    min_value=18,
    max_value=100,
    key="age"
)

housing = st.selectbox(
    "Housing Type",
    options=[0, 1, 2],
    format_func=lambda x: ["Rent", "Own", "Free"][x],
    key="housing"
)

job = st.selectbox(
    "Job Skill Level",
    options=[0, 1, 2],
    format_func=lambda x: ["Unskilled", "Skilled", "Highly Skilled"][x],
    key="job"
)

# -----------------------------
# BUTTONS
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    predict_btn = st.button("🔍 Predict Credit Risk")

with col2:
    reset_btn = st.button("🔄 Reset")

if reset_btn:
    reset_inputs()
    st.rerun()

# -----------------------------
# PREDICTION
# -----------------------------

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

    st.markdown("---")

    if prediction == 1:
        st.error("⚠️ High Credit Risk")
        st.write(f"Probability of Default: {probability[1]*100:.2f}%")
    else:
        st.success("✅ Low Credit Risk")
        st.write(f"Probability of Repayment: {probability[0]*100:.2f}%")
