import streamlit as st
import pickle
import numpy as np

# Load the trained model
with open('hf/a.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Title of the web app
st.markdown("<h1 style='text-align: center;'>Heart Failure Detection</h1>", unsafe_allow_html=True)

# Create two columns: one for the image and buttons, the other for dynamic content
col1, col2 = st.columns([1, 3])  # 30% left, 70% right

# Left column for the image and navigation
with col1:
    st.image("https://static.vecteezy.com/system/resources/thumbnails/021/360/193/small_2x/doctor-character-illustration-free-png.png", width=100)
    st.markdown("<h3>Navigation</h3>", unsafe_allow_html=True)

    # Buttons for navigation with session state to manage content
    if 'page' not in st.session_state:
        st.session_state.page = 'home'  # Default page is 'home'

    if st.button("Home"):
        st.session_state.page = 'home'
    if st.button("Prediction"):
        st.session_state.page = 'prediction'
    if st.button("Dataset"):
        st.session_state.page = 'dataset'
    if st.button("About"):
        st.session_state.page = 'about'

# Function to display user input and make predictions
def display_prediction(input_data):
    # Mapping user inputs to model-friendly format
    sex_map = {"Male": 1, "Female": 0}
    fasting_bs_map = {"Yes": 1, "No": 0}
    exercise_angina_map = {"Yes": 1, "No": 0}
    chest_pain_map = {"Typical Angina": 0, "Atypical Angina": 1, "Non-Anginal Pain": 2, "Asymptomatic": 3}
    resting_ecg_map = {"Normal": 0, "ST-T Wave Abnormality": 1, "Left Ventricular Hypertrophy": 2}
    st_slope_map = {"Upsloping": 0, "Flat": 1, "Downsloping": 2}

    # Prepare the input for the model prediction
    input_vector = np.array([
        input_data['age'],
        sex_map[input_data['sex']],
        chest_pain_map[input_data['chest_pain_type']],
        input_data['resting_bp'],
        input_data['cholesterol'],
        fasting_bs_map[input_data['fasting_bs']],
        resting_ecg_map[input_data['resting_ecg']],
        input_data['max_hr'],
        exercise_angina_map[input_data['exercise_angina']],
        input_data['oldpeak'],
        st_slope_map[input_data['st_slope']]
    ]).reshape(1, -1)

    # Predict heart failure based on user input
    prediction = model.predict(input_vector)

    # Display the input data provided by the user
    st.subheader("Your Input Data:")
    st.markdown(f"""
    **Age**: {input_data['age']}  
    **Sex**: {input_data['sex']}  
    **Chest Pain Type**: {input_data['chest_pain_type']}  
    **Resting Blood Pressure**: {input_data['resting_bp']} mm Hg  
    **Cholesterol**: {input_data['cholesterol']} mg/dl  
    **Fasting Blood Sugar > 120 mg/dl**: {input_data['fasting_bs']}  
    **Resting ECG**: {input_data['resting_ecg']}  
    **Maximum Heart Rate Achieved**: {input_data['max_hr']} bpm  
    **Exercise-Induced Angina**: {input_data['exercise_angina']}  
    **Oldpeak (ST Depression)**: {input_data['oldpeak']}  
    **ST Slope**: {input_data['st_slope']}
    """)

    # Display prediction result with styles inside a box
    st.subheader("Prediction Result:")
    if prediction[0] == 1:
        st.markdown(f'<div style="border: 2px solid red; padding: 10px;"><h4 style="color:red;">⚠️ Warning: {st.session_state.user_name}, the model predicts a high risk of heart failure.</h4></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="border: 2px solid green; padding: 10px;"><h4 style="color:green;">✅ Good news: {st.session_state.user_name}, the model predicts a low risk of heart failure.</h4></div>', unsafe_allow_html=True)

# Right column for dynamic content based on the selected button
with col2:
    if st.session_state.page == 'home':
        st.markdown('<h2>Welcome to the Heart Failure Detection app!</h2>', unsafe_allow_html=True)
        st.write("Use the inputs to predict the risk of heart failure.")

        # Ask for the user's name
        user_name = st.text_input("Please enter your name")
        
        # Input fields for user to provide attributes, with default blank or reasonable placeholders
        age = st.number_input("Age", min_value=5, max_value=120, value=None)
        sex = st.selectbox("Sex", options=["", "Male", "Female"], index=0)
        chest_pain_type = st.selectbox("Chest Pain Type", options=["", "Typical Angina", "Atypical Angina", "Non-Anginal Pain", "Asymptomatic"], index=0)

        resting_bp = st.number_input("Resting Blood Pressure (mm Hg)", min_value=50, max_value=200, value=None)
        cholesterol = st.number_input("Cholesterol (mg/dl)", min_value=100, max_value=400, value=None)
        fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", options=["", "Yes", "No"], index=0)
        resting_ecg = st.selectbox("Resting ECG", options=["", "Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"], index=0)
        max_hr = st.number_input("Maximum Heart Rate Achieved", min_value=60, max_value=220, value=None)
        exercise_angina = st.selectbox("Exercise-Induced Angina", options=["", "Yes", "No"], index=0)
        oldpeak = st.number_input("Oldpeak (ST Depression)", min_value=0.0, max_value=10.0, step=0.1, value=None)
        st_slope = st.selectbox("ST Slope", options=["", "Upsloping", "Flat", "Downsloping"], index=0)

        # Store the user input in session state
        if st.button("Predict"):
            if user_name:
                st.session_state.user_name = user_name  # Store the name in session state
            else:
                st.error("Please enter your name.")

            # Check if all inputs are valid before proceeding
            if (resting_bp is not None and resting_bp >= 50 and 
                cholesterol is not None and cholesterol >= 100 and 
                max_hr is not None and max_hr >= 60 and 
                oldpeak is not None and oldpeak >= 0.0):
                
                st.session_state.page = 'prediction'
                st.session_state.input_data = {
                    'age': age,
                    'sex': sex,
                    'chest_pain_type': chest_pain_type,
                    'resting_bp': resting_bp,
                    'cholesterol': cholesterol,
                    'fasting_bs': fasting_bs,
                    'resting_ecg': resting_ecg,
                    'max_hr': max_hr,
                    'exercise_angina': exercise_angina,
                    'oldpeak': oldpeak,
                    'st_slope': st_slope
                }
            else:
                st.error("Please provide valid inputs for all fields within the specified ranges.")

    elif st.session_state.page == 'prediction':
        st.markdown('<h2>Prediction Results</h2>', unsafe_allow_html=True)
        if 'input_data' not in st.session_state:
            st.error("No input data found! Please go to the Home page and provide the necessary inputs.")
        else:
            display_prediction(st.session_state.input_data)

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

    elif st.session_state.page == 'dataset':
        st.subheader("About the Dataset")
        st.write("""
            The dataset used to train this model includes several key indicators of 
            cardiovascular health. These include measurements such as age, cholesterol 
            levels, resting blood pressure, and other health markers that are crucial 
            for detecting potential heart issues.
        """)
