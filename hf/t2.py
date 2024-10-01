import streamlit as st
import pickle
import numpy as np

# Load the trained model
with open('a.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Title of the web app
st.title("Heart Failure Detection")

# Create two columns: one for the image and buttons, the other for dynamic content
col1, col2 = st.columns([1, 3])  # 30% left, 70% right

# Left column for the image and navigation
with col1:
    st.image("https://static.vecteezy.com/system/resources/thumbnails/021/360/193/small_2x/doctor-character-illustration-free-png.png", caption="Your Doctor", use_column_width=True)  # Update with your doctor's image file
    st.markdown("<h3>Navigation</h3>", unsafe_allow_html=True)

    # Buttons for navigation with session state to manage content
    if 'page' not in st.session_state:
        st.session_state.page = 'home'  # Default page is 'home'

    if st.button("Home"):
        st.session_state.page = 'home'
    if st.button("About"):
        st.session_state.page = 'about'
    if st.button("Contact"):
        st.session_state.page = 'contact'

# Right column for dynamic content based on the selected button
with col2:
    if st.session_state.page == 'home':
        st.markdown('<h2>Welcome to the Heart Failure Detection app!</h2>', unsafe_allow_html=True)
        st.write("Use the inputs to predict the risk of heart failure.")

        # Input fields for user to provide attributes
        age = st.number_input("Age", min_value=0, max_value=120, value=25)
        sex = st.selectbox("Sex", options=["Male", "Female"])
        chest_pain_type = st.selectbox("Chest Pain Type", options=["Typical Angina", "Atypical Angina", "Non-Anginal Pain", "Asymptomatic"])
        resting_bp = st.number_input("Resting Blood Pressure (mm Hg)", min_value=50, max_value=200, value=120)
        cholesterol = st.number_input("Cholesterol (mg/dl)", min_value=100, max_value=400, value=200)
        fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", options=["Yes", "No"])
        resting_ecg = st.selectbox("Resting ECG", options=["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"])
        max_hr = st.number_input("Maximum Heart Rate Achieved", min_value=60, max_value=220, value=150)
        exercise_angina = st.selectbox("Exercise-Induced Angina", options=["Yes", "No"])
        oldpeak = st.number_input("Oldpeak (ST Depression)", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
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
            st.write(f"**Age**: {age}")
            st.write(f"**Sex**: {sex}")
            st.write(f"**Chest Pain Type**: {chest_pain_type}")
            st.write(f"**Resting Blood Pressure**: {resting_bp} mm Hg")
            st.write(f"**Cholesterol**: {cholesterol} mg/dl")
            st.write(f"**Fasting Blood Sugar > 120 mg/dl**: {fasting_bs}")
            st.write(f"**Resting ECG**: {resting_ecg}")
            st.write(f"**Maximum Heart Rate Achieved**: {max_hr}")
            st.write(f"**Exercise-Induced Angina**: {exercise_angina}")
            st.write(f"**Oldpeak (ST Depression)**: {oldpeak}")
            st.write(f"**ST Slope**: {st_slope}")

            # Predict heart failure based on user input
            prediction = model.predict(input_data)

            # Display prediction result with styles
            st.subheader("Prediction Result:")
            if prediction[0] == 1:
                st.error("⚠️ **Warning**: The model predicts a high risk of heart failure.")
            else:
                st.success("✅ **Good news**: The model predicts a low risk of heart failure.")

    elif st.session_state.page == 'about':
        st.subheader("About This Project")
        st.write("""
            This Heart Failure Detection application leverages machine learning 
            techniques to assist in predicting the risk of heart failure based on 
            various health parameters. By inputting attributes such as age, sex, 
            chest pain type, and others, users can receive insights into their 
            heart health. The model has been trained on a comprehensive dataset 
            to provide accurate predictions, thereby promoting awareness and timely 
            medical consultations for heart-related issues.
        """)

    elif st.session_state.page == 'contact':
        st.subheader("Contact Us")
        st.write("For inquiries, please reach out to us at contact@example.com.")
