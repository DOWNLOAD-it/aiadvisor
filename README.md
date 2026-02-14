# AI Financial Advisor 🤖💰

A powerful full-stack application leveraging **Machine Learning** and **Large Language Models** to provide personalized financial advice. This project features a **Django backend** handling AI logic and a **Next.js frontend** for a modern, interactive user interface.

---

## 🌟 Key Features

- **Predictive Modeling:** Analyzes financial data using trained ML models (Keras & Joblib).  
- **AI Chatbot Integration:** High-speed, intelligent financial advisory powered by Groq.  
- **Data Analysis:** Includes a dedicated EDA (Exploratory Data Analysis) module with Jupyter notebooks.  
- **Full-Stack Architecture:** Separate backend (REST API) and frontend (React/Next.js) for scalability.

---

## 📂 Project Structure

financial_advisor/      # Django Backend (API, ML Models, Logic)  
ai-financial-advisor/   # Next.js Frontend (UI, React Components)  
Data/                   # Datasets & Jupyter Notebooks (EDA)

---

## 🚀 Getting Started

Follow these steps to run the project locally.

### 1. Backend Setup (Django)

cd financial_advisor

# Install Python dependencies
pip install -r requirements.txt 

# Run database migrations
python manage.py migrate

# Start the Django server
python manage.py runserver

> The backend will be running at http://127.0.0.1:8000

### 2. Frontend Setup (Next.js)

cd ai-financial-advisor

# Install Node.js dependencies
npm install

# Start the development server
npm run dev

> The frontend will be available at http://localhost:3000

---

## 🛠️ Configuration & Secrets

Create a `.env` file inside the `financial_advisor/` folder and add your Groq API key:

GROQ_API_KEY=your_actual_api_key_here

> **Important:** Do **not** commit this `.env` file to your GitHub repository.
