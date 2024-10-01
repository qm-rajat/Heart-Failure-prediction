import pickle
import numpy as np

# Load the trained model from the pickle file
with open('a.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Display the title
print("=== Heart Failure Detection ===\n")

# User input (hardcoded for now as per your provided values)
age = 40
sex = "Male"  # M
chest_pain_type = "Atypical Angina"  # ATA
resting_bp = 140
cholesterol = 289
fasting_bs = "No"  # 0 means fasting blood sugar <= 120 mg/dl
resting_ecg = "Normal"
max_hr = 172
exercise_angina = "No"  # N
oldpeak = 0.0
st_slope = "Upsloping"  # Up

# Mapping user inputs to the format expected by the model
sex_map = {"Male": 1, "Female": 0}
fasting_bs_map = {"Yes": 1, "No": 0}
exercise_angina_map = {"Yes": 1, "No": 0}
chest_pain_map = {"Typical Angina": 0, "Atypical Angina": 1, "Non-Anginal Pain": 2, "Asymptomatic": 3}
resting_ecg_map = {"Normal": 0, "ST-T Wave Abnormality": 1, "Left Ventricular Hypertrophy": 2}
st_slope_map = {"Upsloping": 0, "Flat": 1, "Downsloping": 2}

# Create an input vector for the model using the mapped values
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

# Debug: Print input data before prediction
print("\n=== Debug: Input Data for Model ===")
print(input_data)

# Display the inputs for reference
print("\nYour Input Data:")
print(f"Age: {age}")
print(f"Sex: {sex}")
print(f"Chest Pain Type: {chest_pain_type}")
print(f"Resting Blood Pressure: {resting_bp} mm Hg")
print(f"Cholesterol: {cholesterol} mg/dl")
print(f"Fasting Blood Sugar > 120 mg/dl: {fasting_bs}")
print(f"Resting ECG: {resting_ecg}")
print(f"Maximum Heart Rate Achieved: {max_hr}")
print(f"Exercise-Induced Angina: {exercise_angina}")
print(f"Oldpeak (ST Depression): {oldpeak}")
print(f"ST Slope: {st_slope}")

# Predict heart failure based on user input
prediction = model.predict(input_data)

# Display the prediction result
print("\n=== Prediction Result ===")
if prediction[0] == 1:
    print("⚠️ Warning: The model predicts a high risk of heart failure.")
else:
    print("✅ Good news: The model predicts a low risk of heart failure.")
