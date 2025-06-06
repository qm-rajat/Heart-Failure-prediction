import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import hashlib
import pickle
import numpy as np

# MongoDB connection
def get_mongo_client():
    uri = "mongodb+srv://rajatdash2004:xoPLUbElIlYWbgXo@heartfailure.jan7w.mongodb.net/?retryWrites=true&w=majority&appName=heartfailure"
    try:
        client = MongoClient(uri, server_api=ServerApi('1'))
        return client["heartfailure_db"]
    except Exception as e:
        st.error(f"Error connecting to MongoDB: {e}")
        return None

db = get_mongo_client()
users_collection = db["users"] if db is not None else None


# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Authentication functions
def login_user(username, password):
    if users_collection is not None:
        # Hash the entered password and check against the stored hash in the database
        hashed_password = hash_password(password)
        user = users_collection.find_one({"username": username, "password": hashed_password})
        if user is not None:
            # Set logged_in to True and store the username in session state
            st.session_state.logged_in = True
            st.session_state.username = username
            # Set the page to "home" to simulate redirect
            st.session_state.page = "home"
            return True
        else:
            st.error("Invalid credentials")
            return False
    return False

def register_user(username, password):
   if users_collection is not None:

        hashed_password = hash_password(password)
        if users_collection.find_one({"username": username}):
            st.warning("Username already exists.")
        else:
            users_collection.insert_one({"username": username, "password": hashed_password})
            st.success("User registered successfully!")

# Prediction function
def load_model():
    try:
        with open('model.pkl', 'rb') as model_file:
            return pickle.load(model_file)
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_model()

def predict_heart_failure(input_data):
    try:
        return model.predict(input_data)
    except Exception as e:
        st.error(f"Prediction error: {e}")
        return None

# Input mapping for the model
def map_user_input(input_data):
    try:
        sex_map = {"Male": 1, "Female": 0}
        fasting_bs_map = {"Yes": 1, "No": 0}
        exercise_angina_map = {"Yes": 1, "No": 0}
        chest_pain_map = {"Typical Angina": 0, "Atypical Angina": 1, "Non-Anginal Pain": 2, "Asymptomatic": 3}
        resting_ecg_map = {"Normal": 0, "ST-T Wave Abnormality": 1, "Left Ventricular Hypertrophy": 2}
        st_slope_map = {"Upsloping": 0, "Flat": 1, "Downsloping": 2}
        
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
        return input_vector
    except KeyError as e:
        st.error(f"Invalid or missing input: {e}")
        return None
# Display functions
def display_login():
    st.subheader("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login", key="login_button"):
        if login_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Logged in successfully!")
        else:
            st.error("Invalid credentials")

def display_registration():
    st.subheader("Register")
    username = st.text_input("Choose a Username", key="register_username")
    password = st.text_input("Choose a Password", type="password", key="register_password")
    if st.button("Register", key="register_button"):
        register_user(username, password)

def display_home():
         st.header("The Heart Disease")

         st.write("""A heart attack, or myocardial infarction, occurs when a section of the heart muscle is deprived of oxygen-rich blood, leading to potential damage. In India, coronary artery disease (CAD) is the primary culprit, often stemming from lifestyle factors such as poor diet, lack of exercise, and increasing stress levels. 

          The significance of timely treatment cannot be overstated; every moment counts in restoring blood flow to minimize damage to the heart. Additionally, while CAD is the leading cause, there are instances where severe spasms of the coronary arteries can also halt blood flow, although this is less common.

          In India, awareness around heart health is crucial, especially given the rise in risk factors like diabetes, hypertension, and obesity. Promoting a balanced diet, regular physical activity, and stress management can significantly help in preventing heart attacks. Community health initiatives and regular health check-ups can play an important role in early detection and intervention..""")

         st.image("ty.jpg")
         st.subheader("Symptoms")

         st.write("""
                      The major symptoms of a heart attack are

          - Chest pain or discomfort. Most heart attacks involve discomfort in the center or left side of the chest that lasts for more than a few minutes or that goes away and comes back. The discomfort can feel like uncomfortable pressure, squeezing, fullness, or pain.
          - Feeling weak, light-headed, or faint. You may also break out into a cold sweat.
          - Pain or discomfort in the jaw, neck, or back.
          - Pain or discomfort in one or both arms or shoulders.
          - Shortness of breath. This often comes along with chest discomfort, but shortness of breath also can happen before chest discomfort.
          """)

         st.subheader("Risk factors")

         st.write("""Several health conditions, your lifestyle, and your age and family history can increase your risk for heart disease and heart attack. These are called risk factors. About half of all Americans have at least one of the three key risk factors for heart disease: high blood pressure, high blood cholesterol, and smoking.

          Some risk factors cannot be controlled, such as your age or family history. But you can take steps to lower your risk by changing the factors you can control.
          """)

         st.subheader("Recover after a heart attack")

         st.write("""
                  If you’ve had a heart attack, your heart may be damaged. This could affect your heart’s rhythm and its ability to pump blood to the rest of the body. You may also be at risk for another heart attack or conditions such as stroke, kidney disorders, and peripheral arterial disease (PAD).

          You can lower your chances of having future health problems following a heart attack with these steps:

          - Physical activity—Talk with your health care team about the things you do each day in your life and work. Your doctor may want you to limit work, travel, or sexual activity for some time after a heart attack.
          - Lifestyle changes—Eating a healthier diet, increasing physical activity, quitting smoking, and managing stress—in addition to taking prescribed medicines—can help improve your heart health and quality of life. Ask your health care team about attending a program called cardiac rehabilitation to help you make these lifestyle changes.
          - Cardiac rehabilitation—Cardiac rehabilitation is an important program for anyone recovering from a heart attack, heart failure, or other heart problem that required surgery or medical care. Cardiac rehab is a supervised program that includes
          1. Physical activity
          2. Education about healthy living, including healthy eating, taking medicine as prescribed, and ways to help you quit smoking
          3. Counseling to find ways to relieve stress and improve mental health

          A team of people may help you through cardiac rehab, including your health care team, exercise and nutrition specialists, physical therapists, and counselors or mental health professionals.
          """)
def help():
        st.markdown("<h2 style='text-align: fill;'>Help</h2>", unsafe_allow_html=True)
        # Chest Pain Type Information
        st.subheader('''Chest Pain Type:''')
        st.markdown('''
        - **Typical Angina (TA):** This type of chest pain occurs when the heart doesn't get enough oxygen due to reduced blood flow. It's usually triggered by physical activity or stress and relieved by rest or medication.
        - **Atypical Angina (ATA):** This pain is not typical of heart-related pain, and may appear as indigestion or discomfort. It’s less likely to be linked to heart disease.
        - **Non-Anginal Pain (NAP):** This chest pain is usually not heart-related and might be due to other causes like muscle strains or gastroesophageal reflux.
        - **Asymptomatic (ASY):** This condition is where no chest pain is experienced, but there may still be underlying heart issues. It is often called "silent" angina.''')

        # Resting ECG Information
        st.subheader('''Resting ECG (Electrocardiogram):''')
        st.markdown('''
        - **Normal:** The ECG shows no abnormal signs. The heart's electrical activity is functioning as expected.
        - **ST-T Wave Abnormality (ST):** This indicates changes in the electrical activity of the heart that might suggest ischemia (reduced blood flow) or other cardiac conditions.
        - **Left Ventricular Hypertrophy (LVH):** This shows that the heart's left ventricle is enlarged, often due to high blood pressure or other heart conditions.''')

        # ST Slope Information
        st.subheader('''ST Slope:''')
        st.markdown('''
        - **Upsloping:** The ST segment rises upward in an ECG tracing, and this pattern can be normal or indicative of early-stage ischemia.
        - **Flat:** A flat ST segment could be a sign of heart disease or ischemia.
        - **Downsloping:** A downsloping ST segment is often a concerning sign and could indicate more severe heart issues like ischemia or a blockage in the heart arteries.''')

        # Additional Help
        st.subheader('Additional Help:')
        st.markdown('''
        If you are unsure about any of the inputs, refer to the following:
        
        - **Age:** Enter your age in years.
        - **Sex:** Choose your biological sex (Male/Female).
        - **Resting Blood Pressure:** Enter your resting blood pressure in mm Hg.
        - **Cholesterol Level:** Enter your cholesterol level in mg/dL.
        - **Fasting Blood Sugar:** This is your blood sugar level after fasting (1 = fasting blood sugar > 120 mg/dL, 0 = otherwise).
        - **Maximum Heart Rate (MaxHR):** This is the highest heart rate achieved during exercise.
        - **Exercise-Induced Angina:** Choose if you experience chest pain during physical activity (Y/N).
        - **Oldpeak:** This measures the ST depression induced by exercise relative to rest (enter the value in millimeters).''')

        # End of Help Page
        st.markdown("For further assistance, consult a medical professional.")



    # Page content
             

def display_prediction_form():
    st.subheader("Provide Patient Information")
    user_inputs = {
        'age': st.number_input("Age", min_value=5, max_value=120, key="age" ,  value=None),
        'sex': st.selectbox("Sex", ["","Male", "Female"], key="sex",index=0),
        'chest_pain_type': st.selectbox("Chest Pain Type", ["","Typical Angina", "Atypical Angina", "Non-Anginal Pain", "Asymptomatic"], key="chest_pain_type",index=0),
        'resting_bp': st.number_input("Resting Blood Pressure (mm Hg)", min_value=50, max_value=200, key="resting_bp",value=None),
        'cholesterol': st.number_input("Cholesterol (mg/dl)", min_value=125, max_value=400, key="cholesterol",value=None),
        'fasting_bs': st.selectbox("Fasting Blood Sugar > 120 mg/dl", ["","Yes", "No"], key="fasting_bs",index=0),
        'resting_ecg': st.selectbox("Resting ECG", ["","Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"], key="resting_ecg",index=0),
        'max_hr': st.number_input("Maximum Heart Rate", min_value=60, max_value=220, key="max_hr",value=None),
        'exercise_angina': st.selectbox("Exercise-Induced Angina", ["","Yes", "No"], key="exercise_angina",index=0),
        'oldpeak': st.number_input("Oldpeak (ST Depression)", min_value=0.0, max_value=10.0, step=0.1, key="oldpeak",value=None),
        'st_slope': st.selectbox("ST Slope", ["","Upsloping", "Flat", "Downsloping"], key="st_slope",index=0)
    }
    if st.button("Predict", key="predict_button"):
        input_vector = map_user_input(user_inputs)
        if input_vector is not None:
            prediction = predict_heart_failure(input_vector)
            display_prediction_result(prediction)

def display_prediction_result(prediction):
    if prediction is not None:
        st.subheader("Prediction Result")
        if prediction[0] == 1:
            st.markdown('<div style="border: 2px solid red; padding: 10px;"><h4 style="color:red;">High risk of heart failure.</h4></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="border: 2px solid green; padding: 10px;"><h4 style="color:green;">Low risk of heart failure.</h4></div>', unsafe_allow_html=True)

# Main application logic
def main():
    st.markdown("<h1 style='text-align: center;'>Heart Failure Detection</h1>", unsafe_allow_html=True)
    st.markdown('''<style>.stApp {background-image: url("https://rare-gallery.com/uploads/posts/5002028-dark-gradient-artist-artwork-digital-art-hd-4k-blur-simple-background.jpg");
                    background-size: cover; background-position: top;}</style>''', unsafe_allow_html=True)
    
    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "page" not in st.session_state:
        st.session_state.page = 'login'

    # Sidebar for navigation
    st.sidebar.header("Navigation")
    if st.session_state.logged_in:
        st.sidebar.button("Home", on_click=lambda: st.session_state.update({"page": "home"}))
        st.sidebar.button("Prediction", on_click=lambda: st.session_state.update({"page": "predict"}))
        st.sidebar.button("Help", on_click=lambda: st.session_state.update({"page": "help"}))
        st.sidebar.button("About", on_click=lambda: st.session_state.update({"page": "about"}))
        st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False, "page": "login"}))
    else:
        st.sidebar.button("Login", on_click=lambda: st.session_state.update({"page": "login"}))
        st.sidebar.button("Register", on_click=lambda: st.session_state.update({"page": "register"}))
    


    if st.session_state.page == "home":
        display_home()
    elif st.session_state.page == "predict":
        display_prediction_form()
    elif st.session_state.page == "login":
        display_login()
    elif st.session_state.page == "register":
        display_registration()
    elif st.session_state.page == "about":
        st.markdown("<h2 style='text-align: center;'>About</h2>", unsafe_allow_html=True)

        # Introduction to the App
        st.subheader("Heart Failure Detection App")
        st.markdown('''
        This web application is designed to help users assess their risk of heart failure using a machine learning model. By providing key health indicators such as age, blood pressure, cholesterol level, and more, the app offers a prediction based on medical data. 
        The goal of this app is to raise awareness and encourage individuals to take proactive steps in managing their heart health.
        ''')

        # Purpose and Motivation
        st.subheader("Purpose")
        st.markdown('''
        Heart failure is a serious condition where the heart is unable to pump enough blood to meet the body's needs. Early detection and management of heart failure risk can significantly improve the quality of life and reduce health complications. 
        This app aims to provide a quick and accessible tool for individuals to check their heart condition and make informed decisions about seeking medical advice.
        ''')

        # How the App Works
        st.subheader("How It Works")
        st.markdown('''
        The app uses a trained machine learning model to predict heart failure risk. The model is based on a dataset of patients with various health conditions, and it learns patterns and correlations between the input features and heart failure outcomes. 
        By inputting your personal health data, the app evaluates the likelihood of heart failure based on the same model, offering a prediction in just a few clicks.
        ''')

        # Technologies Used
        st.subheader("Technologies Used")
        st.markdown('''
        This app is built using several technologies:
        - **Frontend:** Streamlit for a user-friendly interface
        - **Backend:** Python with machine learning libraries for prediction
        - **Model:** A machine learning model trained on patient data to predict heart failure
        - **Deployment:** Hosted as a web app for easy access from any device
        ''')

        # Disclaimer
        st.subheader("Disclaimer")
        st.markdown('''
        Please note that this application is not a substitute for professional medical advice, diagnosis, or treatment. The prediction results provided by this app should not be considered definitive and should be followed up with a healthcare provider for a thorough examination. 
        Always consult a medical professional if you have concerns about your heart health or any of the results shown by this app.
        ''')

        # Contact Information
        st.subheader("Contact")
        st.markdown('''
        If you have any questions about this app or its predictions, feel free to contact us at: 
        - **Email:** support@heartapp.com
        - **Phone:** +123 456 7890
        ''')
    elif st.session_state.page == 'help':
        help()




if __name__ == "__main__":
    main()