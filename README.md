# Smart Household Electricity Consumption & Electricity Bill Prediction System

A Machine Learning and Django-based web application that predicts household monthly electricity consumption and estimated electricity bills using household usage, appliance, occupancy, temperature, seasonal, and historical consumption information.

## 🖥️ Application Preview

### Home Page

![Smart Energy Analytics Home Page](screenshots/home-page.png)

### User Dashboard

![Smart Energy User Dashboard](screenshots/user-dashboard.png)

### Prediction Result

![Smart Energy Electricity Consumption and Bill Prediction Result](screenshots/prediction-result.png)

### User Analytics

![Smart Energy User Analytics Dashboard](screenshots/user-analytics.png)

### Admin Dashboard

![Smart Energy Admin Dashboard Analytics](screenshots/admin-dashboard.png)


## 📌 Project Overview

The Smart Household Electricity Consumption & Electricity Bill Prediction System is designed to help households estimate their monthly electricity consumption and electricity bill.

The application combines a trained Machine Learning model with a Django web application. Users enter household and electricity-usage information, and the system generates:

- Monthly electricity consumption prediction in kWh
- Estimated monthly electricity bill in ₹
- Consumption level
- Energy consumption factors
- Energy-saving recommendations
- Downloadable PDF prediction report

The system also provides an Admin Dashboard for monitoring users, predictions, consumption statistics, and analytics.

---

## 🎯 Objectives

- Predict monthly household electricity consumption.
- Estimate the corresponding monthly electricity bill.
- Identify important household energy-consumption factors.
- Provide personalized energy-saving recommendations.
- Maintain prediction history for users.
- Provide analytics for administrators.
- Provide downloadable prediction reports.
- Build a practical end-to-end Machine Learning web application using Django.

---

## 🚀 Key Features

### 👤 User Features

- User registration and login
- Profile photo support
- User dashboard
- Household electricity prediction form
- Monthly electricity consumption prediction
- Estimated electricity bill calculation
- Consumption-level classification
- Energy consumption insights
- Energy-saving recommendations
- Prediction history
- Detailed prediction view
- Downloadable PDF report
- Personal energy analytics
- Smart Energy chatbot
- Logout functionality
- Password reset functionality

### 👨‍💼 Admin Features

- Separate Admin Login
- Admin Dashboard
- Registered user management
- User details
- User prediction history
- Prediction details
- Total users statistics
- Total predictions statistics
- Average consumption analytics
- Average estimated bill analytics
- Highest consumption information
- Prediction activity chart
- Monthly consumption chart
- Monthly estimated bill chart
- Top users by consumption
- Consumption level distribution
- PDF prediction report access

---

## 🤖 Machine Learning

The application uses a pre-trained Machine Learning regression model for electricity consumption prediction.

The trained deployment package is reused by the Django application rather than retraining the model during prediction.

### Model

**Gradient Boosting Regressor**

The model was trained and tuned for household electricity consumption prediction.

### Model Performance

| Metric | Result |
|---|---:|
| Best Cross-Validation R² | 0.9601 |
| Tuned R² | 0.9609 |
| MAE (kWh) | 43.58 |
| RMSE (kWh) | 61.74 |

### Best Tuned Parameters

- Learning Rate: `0.1`
- Maximum Depth: `3`
- Number of Estimators: `150`

---

## 📊 Input Features

The prediction system uses household, appliance, usage, environmental, seasonal, and historical consumption information.

Major input features include:

- Month
- Number of People
- Number of Rooms
- AC Count
- Fan Count
- Refrigerator
- Washing Machine
- Television Count
- Geyser
- Water Pump
- Computer Count
- Temperature
- Occupancy Hours
- Weekend Usage
- Daily AC Hours
- Daily Fan Hours
- Daily TV Hours
- Daily Geyser Hours
- Daily Washing Machine Hours
- Average Daily Usage Hours
- Previous Month Consumption
- Season
- Cooling Degree
---

## 🧠 Feature Engineering

The application performs feature preparation before sending data to the trained model.

Examples include:

- Converting month information into a numerical representation.
- Encoding seasonal information.
- Calculating Cooling Degree based on temperature.
- Preparing the feature set in the expected order for the trained model.

The trained deployment package contains the required model and encoders used during prediction.

---

## 💰 Electricity Bill Calculation

After predicting monthly electricity consumption, the application estimates the electricity bill using slab-based billing logic.

This allows the predicted consumption to be converted into an estimated monthly electricity cost in Indian Rupees.

The application displays both:

- Predicted monthly consumption
- Estimated monthly electricity bill

---

## 🌐 Django Web Application

The Machine Learning model is integrated into a Django web application.

### Technology Stack

- Python
- Django
- Machine Learning
- Gradient Boosting Regression
- Pandas
- NumPy
- Scikit-learn
- MySQL
- HTML
- CSS
- JavaScript
- Bootstrap / responsive web styling
- ReportLab for PDF reports

---

## 🏗️ Application Architecture

 ```text
User
  │
  ▼
Django Web Application
  │
  ├── User Authentication
  │
  ├── Household Prediction Form
  │
  ▼
Feature Preparation
  │
  ▼
Pre-trained ML Model
  │
  ▼
Predicted Electricity Consumption
  │
  ▼
Slab-based Bill Calculation
  │
  ├── Consumption Level
  ├── Energy Factors
  ├── Recommendations
  └── PDF Report
  ```
## 👥 User Workflow

Home Page
    ↓
User Login / Registration
    ↓
User Dashboard
    ↓
New Prediction
    ↓
Enter Household Information
    ↓
Machine Learning Prediction
    ↓
Consumption + Estimated Bill
    ↓
Prediction Details
    ↓
Prediction History / Analytics / PDF Report


## 👨‍💼 Admin Workflow

Home Page
    ↓
Admin Login
    ↓
Admin Dashboard
    ↓
Users / Prediction Records
    ↓
User Details
    ↓
Prediction History
    ↓
Prediction Details
    ↓
Analytics / PDF Report


## 📈 Analytics

The Admin Dashboard provides visual analytics including:
Prediction Activity
Monthly Consumption
Monthly Estimated Bill
Top Users by Consumption
Consumption Level Distribution
Highest Consumption Month
Highest Bill Month
The User Dashboard also provides personal electricity-consumption analytics.

## 📄 PDF Reports

Users and administrators can download prediction reports containing information such as:
Username
Month
Prediction ID
Predicted consumption
Estimated monthly bill
Consumption level
Energy factors
Recommendations
Reports are generated using ReportLab.

## 🤖 Smart Energy Chatbot

The application includes a Smart Energy Assistant that allows users to ask questions related to:
Electricity consumption
Estimated electricity bills
Energy-saving tips
The chatbot communicates with the Django backend and displays the response directly in the application.

## 🗄️ Database

The application uses a relational database to store application and prediction information.
User prediction records can be viewed through:
User prediction history
Admin prediction records
User details
Prediction details
Analytics

## 📁 Project Structure

project/
│
├── manage.py
│
├── smart_electricity_project/
│
├── prediction/
│
├── templates/
│
├── static/
│ └── css/
│ └── smart_energy.css
│
├── ml_models/
│ └── electricity_deployment_package_fixed.pkl
│
├── media/
│ └── profile_photos/
│
├── requirements.txt
│
└── README.md

## ⚙️ Installation

1. Clone the repository

git clone <your-github-repository-url>
cd <project-folder>

2. Create and activate a virtual environment

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Configure environment variables

Create a .env file and configure the required Django and database settings.
Do not upload .env or secret credentials to GitHub.

5. Apply migrations

python manage.py migrate

6. Start the development server

python manage.py runserver
Open the application in your browser:
http://127.0.0.1:8000/

## 🔐 Security Note

Sensitive configuration such as:
Django secret key
Database username
Database password
Database configuration
should be stored in environment variables and should not be committed to a public GitHub repository.

## 🔮 Future Improvements

Possible future enhancements include:
Real-time smart-meter integration
Larger real-world electricity datasets
Advanced time-series forecasting
Electricity tariff configuration by state/provider
More advanced energy-consumption visualizations
Mobile application
Cloud deployment
Personalized energy-saving alerts
Integration with IoT smart-home devices

## 👩‍💻 Developer

Divya Sagar Patil
Electrical Engineering Graduate transitioning into AI/ML, Data Analytics, and Python Development.
Areas of Interest
Python
Machine Learning
Data Analytics
Generative AI
Agentic AI
Django
AI-powered applications

## ⭐ Project Highlights

End-to-end Machine Learning application
Pre-trained ML model integrated with Django
Household electricity consumption prediction
Electricity bill estimation
User and Admin authentication
MySQL database integration
Prediction history
Analytics dashboards
PDF report generation
Energy-saving recommendations
Smart Energy chatbot











