import streamlit as st
import pickle
import numpy as np

# Load model
model = pickle.load(open("models/titanic_model.pkl", "rb"))

# Title
st.title("Titanic Survival Prediction")

# Inputs
pclass = st.selectbox("Passenger Class", [1, 2, 3])

sex = st.selectbox("Sex", ["male", "female"])
if sex == "male":
    sex = 0
else:
    sex = 1

age = st.number_input(
    "Age",
    min_value=0,
    max_value=100,
    value=30
)

sibsp = st.number_input(
    "Number of Siblings/Spouses Aboard",
    min_value=0,
    max_value=10,
    value=0
)

parch = st.number_input(
    "Number of Parents/Children Aboard",
    min_value=0,
    max_value=10,
    value=0
)

fare = st.number_input(
    "Fare",
    min_value=0.0,
    max_value=500.0,
    value=32.0
)

# Embarked Encoding
embarked = st.selectbox(
    "Port of Embarkation",
    ["C", "Q", "S"]
)

if embarked == "S":
    embarked = 0
elif embarked == "C":
    embarked = 1
else:
    embarked = 2

# Prediction Button
if st.button("Predict"):

    # Create feature array
    features = np.array([[
        pclass,
        sex,
        age,
        sibsp,
        parch,
        fare,
        embarked
    ]])

    # Predict
    prediction = model.predict(features)

    # Show prediction
    st.write("Prediction:", prediction[0])

    if prediction[0] == 1:
        st.success("Passenger Survived")
    else:
        st.error("Passenger Did Not Survive")

    # Probability
    probability = model.predict_proba(features)

    survival_prob = probability[0][1] * 100

    st.write(
        f"Survival Probability: {survival_prob:.2f}%"
    )