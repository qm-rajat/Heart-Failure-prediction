# Heart Failure Prediction System

A machine learning-based web application that predicts the risk of heart failure using various health parameters. This project uses Streamlit for the frontend interface and a trained machine learning model for predictions.

## 🚀 Features

- Interactive web interface for easy data input
- Real-time heart failure risk prediction
- Comprehensive health parameter analysis
- User-friendly navigation
- Detailed explanation of medical terms and parameters
- Responsive design with modern UI

## 📋 Prerequisites

Before running this project, make sure you have Python 3.8+ installed on your system. The project uses several Python packages which are listed in `requirements.txt`.

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/qm-rajat/Heart-Failure-prediction.git
cd Heart-Failure-prediction
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## 🏃‍♂️ Running the Application

To run the application, execute the following command in your terminal:
```bash
streamlit run z2.py
```

The application will start and open in your default web browser at `http://localhost:8501`.

## 📊 Project Structure

- `z2.py` - Main Streamlit application file
- `a.pkl` - Trained machine learning model
- `heart.csv` - Dataset used for training
- `requirements.txt` - Project dependencies
- `ty.jpg` - Application image assets
- `HeartFailurepred2.ipynb` - Jupyter notebook containing model training and analysis

## 🧪 Model Details

The prediction model takes into account various health parameters including:
- Age
- Sex
- Chest Pain Type
- Resting Blood Pressure
- Cholesterol Level
- Fasting Blood Sugar
- Resting ECG Results
- Maximum Heart Rate
- Exercise-Induced Angina
- ST Depression
- ST Slope

## 📝 Input Parameters

The application requires the following inputs for prediction:

1. **Personal Information**
   - Age
   - Sex (Male/Female)

2. **Medical Parameters**
   - Chest Pain Type (Typical Angina, Atypical Angina, Non-Anginal Pain, Asymptomatic)
   - Resting Blood Pressure (mm Hg)
   - Cholesterol Level (mg/dl)
   - Fasting Blood Sugar (> 120 mg/dl)
   - Resting ECG Results
   - Maximum Heart Rate Achieved
   - Exercise-Induced Angina
   - ST Depression (Oldpeak)
   - ST Slope

## ⚠️ Disclaimer

This application is for educational and informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/qm-rajat/Heart-Failure-prediction/issues).

## 📄 License

This project is licensed under the terms of the license included in the repository.

## 👥 Authors

- **Rajat Kumar Dash** - *Initial work* - [GitHub Profile](https://github.com/qm-rajat)
  - Student at GIET University
  - Deep interest in Machine Learning, Data Science, and Cybersecurity
  - Passionate about developing practical solutions using AI/ML

## 🙏 Acknowledgments

- Dataset providers
- Streamlit team for the amazing framework
- GIET University for academic support
- All contributors who have helped in the development of this project

## 🔗 Connect with Me

- GitHub: [qm-rajat](https://github.com/qm-rajat)
- Email: rajatdash2004@gmil.com

Feel free to reach out for collaborations or discussions about ML, DS, and Cybersecurity! 