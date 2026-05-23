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
# TITLE
# =============================

st.title("💳 Credit Risk Analysis System")

st.write(
    "Predict whether a customer is Low Risk or High Risk"
)

st.markdown("---")

# =============================
# RESET FUNCTION
# =============================

def reset_inputs():

    keys = [
        "duration",
        "amount",
        "employment_duration",
        "age"
    ]

    for key in keys:
        if key in st.session_state:
            del st.session_state[key]

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
# BUTTONS
# =============================

col1, col2, col3 = st.columns([1, 1, 1])

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
        # SCALING
        # =============================

        scaled_data = scaler.transform(input_data)

        # =============================
        # PREDICTION
        # =============================

        prediction = model.predict(scaled_data)[0]

        probability = model.predict_proba(scaled_data)[0]

        # IMPORTANT FIX
        default_prob = probability[0]

        st.markdown("---")

        # =============================
        # LOW RISK
        # =============================

        if default_prob < 0.40:

            st.success("🟢 LOW RISK")

            st.write(
                f"🔴 Default Risk: {default_prob*100:.2f}%"
            )

            st.write(
                f"🟢 Repayment Probability: {(1-default_prob)*100:.2f}%"
            )

            st.info(
                "📌 Reason: Borrower shows strong financial stability with "
                "good credit history, better savings, and stable employment."
            )

        # =============================
        # MEDIUM RISK
        # =============================

        elif default_prob < 0.70:

            st.warning("🟠 MEDIUM RISK")

            st.write(
                f"🔴 Default Risk: {default_prob*100:.2f}%"
            )

            st.write(
                f"🟢 Repayment Probability: {(1-default_prob)*100:.2f}%"
            )

            st.info(
                "📌 Reason: Borrower has moderate financial stability. "
                "Some indicators suggest repayment ability while others "
                "show possible repayment uncertainty."
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
                "such as poor credit history, low savings, or unstable employment."
            )

    except:

        st.error("⚠️ Please enter valid numeric values in all text fields.")
