import streamlit as st
import pickle

model = pickle.load(open("model/spam_model.pkl", "rb"))
vectorizer = pickle.load(open("model/vectorizer.pkl", "rb"))

st.title("Spam Message Detection")
st.write("Enter a message to check if it's spam or not.")
message = st.text_area("Message")
if st.button("Predict"):
    message_vector = vectorizer.transform([message])
    prediction = model.predict(message_vector)[0]
    if prediction == 1:
        st.error("This message is likely to be spam.")
    else:
        st.success("This message is likely to be ham (not spam).")