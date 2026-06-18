import streamlit as st
import pickle
import numpy as np

# load saved model
loaded_model = pickle.load(
    open("models/parkinsons_model.sav", "rb")
)
st.title("Parkinson Disease Prediction App")
fo = st.number_input("MDVP:Fo(Hz)")
fhi = st.number_input("MDVP:Fhi(Hz)")
flo = st.number_input("MDVP:Flo(Hz)")
jitter_percent = st.number_input("MDVP:Jitter(%)")
jitter_abs = st.number_input("MDVP:Jitter(Abs)")
rap = st.number_input("MDVP:RAP")
ppq = st.number_input("MDVP:PPQ")
ddp = st.number_input("Jitter:DDP")
shimmer = st.number_input("MDVP:Shimmer")
shimmer_db = st.number_input("MDVP:Shimmer(dB)")
apq3 = st.number_input("Shimmer:APQ3")
apq5 = st.number_input("Shimmer:APQ5")
apq = st.number_input("MDVP:APQ")
dda = st.number_input("Shimmer:DDA")
nhr = st.number_input("NHR")
hnr = st.number_input("HNR")
rpde = st.number_input("RPDE")
dfa = st.number_input("DFA")
spread1 = st.number_input("spread1")
spread2 = st.number_input("spread2")
d2 = st.number_input("D2")
ppe = st.number_input("PPE")

diagnosis = ""

if st.button("Predict"):

    input_data = [(
        fo,
        fhi,
        flo,
        jitter_percent,
        jitter_abs,
        rap,
        ppq,
        ddp,
        shimmer,
        shimmer_db,
        apq3,
        apq5,
        apq,
        dda,
        nhr,
        hnr,
        rpde,
        dfa,
        spread1,
        spread2,
        d2,
        ppe
    )]

    input_data_as_numpy_array = np.asarray(input_data)

    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)

    prediction = loaded_model.predict(input_data_reshaped)

    if prediction[0] == 0:
        diagnosis = "Healthy Person"

    else:
        diagnosis = "Person has Parkinson Disease"
    probability = loaded_model.predict_proba(input_data_reshaped)
    healthy_prob = probability[0][0] * 100
    parkinson_prob = probability[0][1] * 100

    st.write(
            f"Healthy Probability: {healthy_prob:.2f}%")

    st.write(
            f"Parkinson Probability: {parkinson_prob:.2f}%")
    st.write(probability)

    st.success(diagnosis)
    