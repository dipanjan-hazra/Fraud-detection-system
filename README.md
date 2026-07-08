# 💳 AI-Powered Transaction Fraud Detection System
### Live - https://fraud-detection-system-o6grrllfqcwejaywfchnvu.streamlit.app/

An intelligent fraud detection platform that analyzes financial transactions and predicts the likelihood of fraudulent activity using Machine Learning.

## 🚀 Features

### 🔐 User Authentication

* User Registration
* Secure Login System
* Password Hashing using BCrypt
* Session Management

### 🤖 Fraud Detection

* Manual Transaction Analysis
* Batch CSV/Excel Transaction Analysis
* Fraud Probability Prediction
* Risk Score Generation
* Real-time Fraud Alerts

### 📊 Analytics & Monitoring

* Prediction History
* User-specific Transaction Records
* Fraud vs Legitimate Transaction Statistics
* Risk Score Visualization
* Historical Trend Analysis

### 📧 Email Alerts

* Automatic Email Notification for High-Risk Transactions
* Fraud Probability Included in Alert
* Transaction Amount Details Included

---

## 🛠️ Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### Database

* Supabase

### Machine Learning

* XGBoost
* Scikit-Learn
* Pandas
* NumPy

### Security

* BCrypt Password Hashing

### Notifications

* Gmail SMTP (Yagmail)

---

## 📂 Project Structure

```text
fraud-detection-system/
│
├── app.py
│
├── Database/
│   ├── auth.py
│   ├── config.py
│   └── history.py
│
├── pages/
│   ├── login.py
│   ├── register.py
│   ├── dashboard.py
│   ├── upload_page.py
│   └── history.py
│
├── Util/
│   └── mail.py
│
├── Models/
│   ├── fraud_model.pkl
│   └── feature_columns.pkl
│
├── .streamlit/
│   └── config.toml
│
├── requirements.txt
│
└── README.md
```

---

## 🧠 Machine Learning Workflow

1. Transaction Data Input
2. Feature Engineering
3. Data Preprocessing
4. XGBoost Prediction
5. Fraud Probability Calculation
6. Risk Score Generation
7. Email Alert Trigger (High Risk)
8. Prediction History Storage

---

## 📥 Manual Prediction Inputs

* Amount Received
* Amount Paid
* Transaction Date
* Transaction Time
* Payment Method
* Same Bank Indicator
* Same Currency Indicator
* Sender Bank Frequency
* Sender Account Frequency
* Receiver Account Frequency

---

## 📤 Batch Prediction

Upload:

* CSV Files
* XLSX Files
* XLS Files

The system automatically:

* Processes transactions
* Generates predictions
* Calculates risk scores
* Saves prediction history

---

## 📧 Email Alert System

If Fraud Probability exceeds the defined threshold:

* Alert Email is generated
* User receives notification instantly
* Risk details are included in the email

---

## 🔒 Security Features

* BCrypt Password Hashing
* Secure User Authentication
* Session-Based Access Control
* User-Specific Prediction History

---


## 📈 Future Improvements

* SHAP Explainability Dashboard
* PDF Report Generation
* Admin Dashboard
* User Profile Management
* Real-time Fraud Monitoring
* Multi-Factor Authentication (MFA)
* Advanced Analytics Dashboard

---

## 👨‍💻 Author

Dipanjan Hazra

Final Year B.Tech (Information Technology)

---

## ⭐ Project Goal

To develop a secure, scalable, and intelligent fraud detection platform capable of identifying suspicious financial transactions and assisting users in proactive fraud prevention.
