'''
User enters:
- income
- loan amount
- education
- credit history
↓
Model predicts:
Approved or Rejected


'''
import pickle
import numpy as np
import streamlit as st
model = pickle.load(open("models/loan_model.pkl", "rb"))
st.title("Loan Approval Prediction")
gender = st.selectbox(
    "Gender",
    ["Male", "Female"]
)

married = st.selectbox(
    "Married",
    ["Yes", "No"]
)

dependents = st.selectbox(
    "Dependents",
    [0, 1, 2, 3]
)

education = st.selectbox(
    "Education",
    ["Graduate", "Not Graduate"]
)

self_employed = st.selectbox(
    "Self Employed",
    ["Yes", "No"]
)

applicant_income = st.number_input(
    "Applicant Income",
    value=5000
)

coapplicant_income = st.number_input(
    "Coapplicant Income",
    value=0
)

loan_amount = st.number_input(
    "Loan Amount (in thousands)",
    min_value=1,
    max_value=700,
    value=120
)

loan_term = st.number_input(
    "Loan Amount Term",
    min_value=1,
    max_value=360,
    value=360
)

credit_history = st.selectbox(
    "Credit History",
    [1, 0]
)

property_area = st.selectbox(
    "Property Area",
    ["Urban", "Semiurban", "Rural"]
)
if gender == "Male":
    gender = 1
else:
    gender = 0
if married == "Yes":
    married = 1
else:
    married = 0
if education == "Graduate":
    education = 1
else:
    education = 0
if self_employed == "Yes":
    self_employed = 1
else:
    self_employed = 0
if property_area == "Urban":
    property_area = 2
elif property_area == "Semiurban":
    property_area = 1
else:
    property_area = 0
if st.button("Predict"):
    input_data = np.array([
        [gender, 
         married, 
         dependents,
           education, 
           self_employed,
             applicant_income, 
             coapplicant_income, 
             loan_amount, 
             loan_term, 
             credit_history, 
             property_area]
        ])
    prediction = model.predict(input_data)
    approval_prob = model.predict_proba(input_data)[0][1] * 100

    if prediction[0] == 1:

        st.success("Loan Approved")

        st.write("Positive Factors:")

        if credit_history == 1:
            st.write("- Good credit history")

        if applicant_income > 4000:
            st.write("- Stable income")

        if education == 1:
            st.write("- Graduate applicant")

    else:

        st.error("Loan Rejected")

        reasons = []

        if credit_history == 0:
            reasons.append(
                "Poor credit history"
            )

        if applicant_income < 2500:
            reasons.append(
                "Low applicant income"
            )

        if loan_amount > 300:
            reasons.append(
                "High loan amount"
            )

        if education == 0:
            reasons.append(
                "Applicant is not graduate"
            )

        st.write("Possible Reasons:")

        for reason in reasons:
            st.write(f"- {reason}")

        if approval_prob > 80:
            st.success("Low Risk Applicant")

        elif approval_prob > 50:
            st.warning("Medium Risk Applicant")

        else:
            st.error("High Risk Applicant")
        
        debt_ratio = loan_amount / applicant_income
        st.write(
            f"Loan-to-Income Ratio: {debt_ratio:.2f}"
        )