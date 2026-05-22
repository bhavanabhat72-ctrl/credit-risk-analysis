import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load Model and Scaler

model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

# Page Title

st.title("Credit Risk Analysis System")

st.write("Enter Borrower Details to Predict Credit Risk")

# User Inputs

status = st.number_input("Status", min_value=0, max_value=4, value=1)

duration = st.number_input("Duration (Months)", min_value=1, max_value=72, value=12)

credit_history = st.number_input("Credit History", min_value=0, max_value=4, value=2)

purpose = st.number_input("Purpose", min_value=0, max_value=10, value=1)

amount = st.number_input("Credit Amount", min_value=100, max_value=50000, value=3000)

savings = st.number_input("Savings", min_value=0, max_value=4, value=1)

employment_duration = st.number_input("Employment Duration", min_value=0, max_value=4, value=2)

installment_rate = st.number_input("Installment Rate", min_value=1, max_value=4, value=2)

personal_status_sex = st.number_input("Personal Status Sex", min_value=0, max_value=4, value=2)

other_debtors = st.number_input("Other Debtors", min_value=0, max_value=2, value=0)

present_residence = st.number_input("Present Residence", min_value=1, max_value=4, value=2)

property = st.number_input("Property", min_value=0, max_value=3, value=1)

age = st.number_input("Age", min_value=18, max_value=100, value=30)

other_installment_plans = st.number_input("Other Installment Plans", min_value=0, max_value=2, value=0)

housing = st.number_input("Housing", min_value=0, max_value=2, value=1)

number_credits = st.number_input("Number of Credits", min_value=1, max_value=10, value=1)

job = st.number_input("Job", min_value=0, max_value=3, value=2)

people_liable = st.number_input("People Liable", min_value=1, max_value=2, value=1)

telephone = st.number_input("Telephone", min_value=0, max_value=1, value=1)

foreign_worker = st.number_input("Foreign Worker", min_value=0, max_value=1, value=1)

# Prediction Button

if st.button("Predict Credit Risk"):

    input_data = np.array([[
        status,
        duration,
        credit_history,
        purpose,
        amount,
        savings,
        employment_duration,
        installment_rate,
        personal_status_sex,
        other_debtors,
        present_residence,
        property,
        age,
        other_installment_plans,
        housing,
        number_credits,
        job,
        people_liable,
        telephone,
        foreign_worker
    ]])

    # Scale Data

    scaled_data = scaler.transform(input_data)

    # Prediction

    prediction = model.predict(scaled_data)[0]

    probability = model.predict_proba(scaled_data)[0]

    # Output

    if prediction == 1:

        st.error("High Credit Risk")

        st.write(f"Probability of Default: {probability[1]*100:.2f}%")

        st.write(f"Probability of Repayment: {probability[0]*100:.2f}%")

    else:

        st.success("Low Credit Risk")

        st.write(f"Probability of Repayment: {probability[0]*100:.2f}%")

        st.write(f"Probability of Default: {probability[1]*100:.2f}%")
