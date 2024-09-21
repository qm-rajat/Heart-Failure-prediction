import streamlit as st
import pickle
import numpy as np
import json


# Load the trained model
with open('a.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Title of the web app
st.title("Heart Failure Detection")

# Input fields for user to provide attributes
st.header("Please input the following attributes:")

age = st.number_input("Age", min_value=0, max_value=120, value=25)
sex = st.selectbox("Sex", options=["Male", "Female"])
chest_pain_type = st.selectbox("Chest Pain Type", options=["Typical Angina", "Atypical Angina", "Non-Anginal Pain", "Asymptomatic"])
resting_bp = st.number_input("Resting Blood Pressure (mm Hg)", min_value=50, max_value=200, value=120)
cholesterol = st.number_input("Cholesterol (mg/dL)", min_value=100, max_value=400, value=200)
fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dL", options=["Yes", "No"])
resting_ecg = st.selectbox("Resting ECG", options=["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"])
max_hr = st.number_input("Maximum Heart Rate Achieved", min_value=60, max_value=220, value=150)
exercise_angina = st.selectbox("Exercise-Induced Angina", options=["Yes", "No"])
oldpeak = st.number_input("Oldpeak (ST depression)", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
st_slope = st.selectbox("ST Slope", options=["Upsloping", "Flat", "Downsloping"])

# Mapping user inputs to the format expected by the model
sex_map = {"Male": 1, "Female": 0}
fasting_bs_map = {"Yes": 1, "No": 0}
exercise_angina_map = {"Yes": 1, "No": 0}
chest_pain_map = {"Typical Angina": 0, "Atypical Angina": 1, "Non-Anginal Pain": 2, "Asymptomatic": 3}
resting_ecg_map = {"Normal": 0, "ST-T Wave Abnormality": 1, "Left Ventricular Hypertrophy": 2}
st_slope_map = {"Upsloping": 0, "Flat": 1, "Downsloping": 2}

# Create an input vector for the model
input_data = np.array([
    age,
    sex_map[sex],
    chest_pain_map[chest_pain_type],
    resting_bp,
    cholesterol,
    fasting_bs_map[fasting_bs],
    resting_ecg_map[resting_ecg],
    max_hr,
    exercise_angina_map[exercise_angina],
    oldpeak,
    st_slope_map[st_slope]
]).reshape(1, -1)

# When the user clicks the "Predict" button, display input data and prediction result
if st.button("Predict"):
    st.subheader("Your Input Data:")
    st.write(f"**Age:** {age}")
    st.write(f"**Sex:** {sex}")
    st.write(f"**Chest Pain Type:** {chest_pain_type}")
    st.write(f"**Resting Blood Pressure:** {resting_bp} mm Hg")
    st.write(f"**Cholesterol:** {cholesterol} mg/dL")
    st.write(f"**Fasting Blood Sugar > 120 mg/dL:** {fasting_bs}")
    st.write(f"**Resting ECG:** {resting_ecg}")
    st.write(f"**Maximum Heart Rate Achieved:** {max_hr}")
    st.write(f"**Exercise-Induced Angina:** {exercise_angina}")
    st.write(f"**Oldpeak (ST depression):** {oldpeak}")
    st.write(f"**ST Slope:** {st_slope}")

    # Predict heart failure based on user input
    prediction = model.predict(input_data)
    
    # Display prediction result
    st.subheader("Prediction Result:")
    if prediction[0] == 1:
        st.error("Warning: The model predicts a high risk of heart failure.")
    else:
        st.success("Good news: The model predicts a low risk of heart failure.")
