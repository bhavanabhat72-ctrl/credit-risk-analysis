import streamlit as st
import numpy as np
import pickle

# Load Model and Scaler

model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Credit Risk Analysis",
    page_icon="💳",
    layout="centered"
)

# -----------------------------------
# TITLE
# -----------------------------------

st.title("💳 Credit Risk Analysis System")

st.write(
    "Enter borrower details to predict whether the applicant is a Low Risk or High Risk customer."
)

st.markdown("---")

# -----------------------------------
# USER INPUTS
# -----------------------------------

duration = st.text_input(
    "Loan Duration (Months)",
    placeholder="Example: 12"
)

amount = st.text_input(
    "Credit Amount",
    placeholder="Example: 5000"
)

savings = st.text_input(
    "Savings Account Level",
    placeholder="0 = little, 1 = moderate, 2 = rich"
)

credit_history = st.text_input(
    "Credit History",
    placeholder="0 = poor, 1 = average, 2 = good"
)

employment_duration = st.text_input(
    "Employment Duration",
    placeholder="Example: 4 years"
)

age = st.text_input(
    "Age",
    placeholder="Example: 30"
)

housing = st.text_input(
    "Housing Type",
    placeholder="0 = rent, 1 = own, 2 = free"
)

job = st.text_input(
    "Job Skill Level",
    placeholder="0 = unskilled, 1 = skilled, 2 = highly skilled"
)

# -----------------------------------
# PREDICT BUTTON
# -----------------------------------

if st.button("Predict Credit Risk"):

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

        # Scale Data

        scaled_data = scaler.transform(input_data)

        # Prediction

        prediction = model.predict(scaled_data)[0]

        probability = model.predict_proba(scaled_data)[0]

        st.markdown("---")

        # Result

        if prediction == 1:

            st.error("⚠️ High Credit Risk")

            st.write(
                f"### Probability of Default: {probability[1]*100:.2f}%"
            )

        else:

            st.success("✅ Low Credit Risk")

            st.write(
                f"### Probability of Repayment: {probability[0]*100:.2f}%"
            )

    except:

        st.warning("Please enter valid numeric values in all fields.")
