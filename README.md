AI Financial Advisor 🤖💰
A powerful full-stack application that leverages Machine Learning and Large Language Models to provide personalized financial advice. This project features a Django backend handling the logic and AI, and a Next.js frontend for a modern, interactive user interface.

🌟 Key Features
Predictive Modeling: Uses trained machine learning models (Keras & Joblib) to analyze financial data.

AI Chatbot Integration: Powered by Groq for high-speed, intelligent financial advisory.

Data Analysis: Includes a dedicated EDA (Exploratory Data Analysis) module with Jupyter notebooks.

Full-Stack Architecture: Separated backend (REST API) and frontend (React/Next.js) for scalability.

📂 Project Structure
Plaintext
├── financial_advisor/      # Django Backend (API, ML Models, Logic)
├── ai-financial-advisor/   # Next.js Frontend (UI, React Components)
└── Data/                   # Datasets & Jupyter Notebooks (EDA)
🚀 Getting Started
Follow these instructions to get the project running locally on your machine.

1. Backend Setup (Django)
Navigate to the backend directory and start the server:

Bash
cd financial_advisor

# Install Python dependencies
pip install -r requirements.txt 

# Run database migrations
python manage.py migrate

# Start the Django server
python manage.py runserver
Note: The backend will be running at http://127.0.0.1:8000.

2. Frontend Setup (Next.js)
Open a new terminal window, navigate to the frontend directory, and launch the UI:

Bash
cd ai-financial-advisor

# Install Node.js dependencies
npm install

# Start the development server
npm run dev
Note: The frontend will be available at http://localhost:3000.

🛠️ Configuration & Secrets
To use the AI features, you must set up your environment variables.

Create a .env file inside the financial_advisor/ folder.

Add your Groq API key:

Plaintext
GROQ_API_KEY=your_actual_api_key_here
(Important: Do not commit this .env file to your GitHub repository!)
