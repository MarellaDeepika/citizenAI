 CitizenAI 🏛️

**CitizenAI** is a powerful AI-powered civic engagement platform designed to help users understand and interact with government services in real-time. Built with Flask and integrated with OpenRouter’s Claude 3.5 Sonnet, this platform provides intelligent, structured responses to queries on topics like voting, infrastructure, public safety, and more.

---

##  Features

-  **AI Chat Assistant** – Ask civic-related questions and get real-time answers from Claude 3.5 Sonnet (OpenRouter)
-  **Dashboard** – Visual insights on citizen concerns
-  **Concern Reporting** – Submit and manage local issues
-  **Sentiment Analysis** – Get emotional tone analysis from text
-  **User Authentication** – Secure login system
-  **Structured UI Pages** – Index, About, Chat, Services, Dashboard

---

##  Project Structure
citizen_ai/
│
├── app.py # Main Flask app
├── config.py # Configuration with secret keys and API tokens
├── requirements.txt # Python dependencies
├── .gitignore # Files ignored by Git
├── templates/ # HTML templates (UI pages)
│ ├── index.html
│ ├── about.html
│ ├── login.html
│ ├── chat.html
│ ├── dashboard.html
│ └── report.html
├── static/ # CSS/JS files (optional)
│ └── style.css
├── routes/
│ ├── chat_routes.py
│ ├── sentiment_routes.py
│ └── report_routes.py
└── utils/
├── openrouter_ai.py # AI response logic via OpenRouter
├── sentiment.py # Sentiment classification logic
└── db.py # Concern storage logic

2. Set Up Virtual Environment

    python -m venv venv
    venv\Scripts\activate    # On Windows
    # or
    source venv/bin/activate  # On macOS/Linux
3. Install Dependencies

    pip install -r requirements.txt
4. Configure API Key & Secrets
  Create a .env or edit config.py with your:
   # config.py
    OPENROUTER_API_KEY = "sk-or-v1-xxxxxxxxxxxxxxxxxxxx"
    FLASK_SECRET_KEY = "your-secret-key"
    To generate a Flask secret key:
   
     " import secrets
      print(secrets.token_hex(16)) "
AI Assistant (Claude 3.5 Sonnet via OpenRouter)
The assistant is configured to respond to queries like:

“How do I register to vote in Norway?”
“What is the process for reporting potholes in my city?”

It sends your query securely to OpenRouter’s Claude 3.5 Sonnet and returns structured, helpful info.

Concern Reporting
-Submit issues (e.g., garbage, streetlight, road)

-Stored in memory (extendable to SQLite/PostgreSQL)

-Accessible via admin dashboard
 
Sentiment Analysis
 Uses openrouter sentiment classifier to show:
    Positive, Negative, Neutral tone

Useful for understanding public emotions

💻 Running the App

  "python app.py"
  
