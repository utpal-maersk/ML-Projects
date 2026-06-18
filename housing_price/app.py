import streamlit as st
import pickle
import numpy as np

model = pickle.load(
    open("model/house_price_model.pkl", "rb")
)
st.sidebar.title("About")

st.sidebar.write(
    "House price prediction using Linear Regression"
)
st.title("House Price Prediction")

overall_qual = st.slider(
    "Overall Quality",
    1,
    10,
    5
)

gr_liv_area = st.number_input(
    "Living Area (sq ft)",
    value=1500
)

garage_cars = st.number_input(
    "Garage Capacity",
    value=2
)

total_bsmt_sf = st.number_input(
    "Basement Area (sq ft)",
    value=800
)

full_bath = st.number_input(
    "Full Bathrooms",
    value=2
)

bedrooms = st.number_input(
    "Bedrooms Above Ground",
    value=3
)

if st.button("Predict House Price"):
    input_data = np.array(
        [overall_qual, gr_liv_area, garage_cars, total_bsmt_sf, full_bath, bedrooms]
    ).reshape(1, -1)

    prediction = model.predict(input_data)
    st.success(f"Predicted House Price: ${prediction[0]:,.2f}")