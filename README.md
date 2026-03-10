# Conversational BI Dashboard

An AI-powered Business Intelligence dashboard that allows non-technical users to generate interactive data visualizations using natural language queries.

Users can type questions like:

```
Show revenue by campaign type
Compare ROI across channels
Show clicks by language
```

The system automatically:

1. Converts natural language → SQL query using an LLM
2. Executes the query on a marketing dataset
3. Selects an appropriate chart type
4. Generates an interactive dashboard

---

# Project Architecture

```
User Prompt
    ↓
React Frontend
    ↓
FastAPI Backend
    ↓
LLM (OpenRouter / DeepSeek)
    ↓
SQL Query Generation
    ↓
SQLite Database
    ↓
Query Execution
    ↓
Chart Rendering (Recharts)
```

---

# Tech Stack

Frontend

* React (Vite)
* Recharts
* Axios

Backend

* Python
* FastAPI
* Pandas
* SQLite

AI Integration

* OpenRouter API
* DeepSeek Chat Model

Dataset

* Nykaa Digital Marketing Campaign Data

---

# Folder Structure

```
conversational-bi-dashboard
│
├── frontend
│   ├── src
│   │   ├── components
│   │   │   ├── PromptInput.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   └── ChartRenderer.jsx
│   │   │
│   │   ├── services
│   │   │   └── api.js
│   │   │
│   │   └── App.jsx
│   │
│   └── package.json
│
├── backend
│   ├── app
│   │   ├── database
│   │   │   ├── connection.py
│   │   │   └── db_setup.py
│   │   │
│   │   ├── services
│   │   │   ├── llm_service.py
│   │   │   └── query_service.py
│   │   │
│   │   └── main.py
│   │
│   ├── marketing.db
│   └── requirements.txt
│
├── data
│   └── nykaa_marketing.csv
│
└── README.md
```

---

# Prerequisites

Install the following before running the project:

* Python 3.9+
* Node.js 18+
* npm
* Git

---

# 1. Clone Repository

```
git clone https://github.com/YOUR_USERNAME/conversational-bi-dashboard.git

cd conversational-bi-dashboard
```

---

# 2. Backend Setup (FastAPI)

Navigate to backend folder

```
cd backend
```

Create virtual environment

```
python -m venv venv
```

Activate environment

Windows

```
venv\Scripts\activate
```

Mac / Linux

```
source venv/bin/activate
```

Install dependencies

```
pip install fastapi uvicorn pandas numpy python-dotenv requests
```

Save dependencies

```
pip freeze > requirements.txt
```

---

# 3. Setup Environment Variables

Create `.env` file inside backend folder.

```
backend/.env
```

Add your OpenRouter API key.

```
OPENROUTER_API_KEY=your_api_key_here
```

You can obtain a key from:

https://openrouter.ai

---

# 4. Load Dataset into SQLite

Place dataset inside:

```
data/nykaa_marketing.csv
```

Run database setup script.

```
python app/database/db_setup.py
```

This converts the CSV file into a SQLite database:

```
marketing.db
```

---

# 5. Run Backend Server

From the backend folder run:

```
uvicorn app.main:app --reload
```

Backend will start at:

```
http://127.0.0.1:8000
```

API documentation is available at:

```
http://127.0.0.1:8000/docs
```

---

# 6. Frontend Setup (React)

Open a new terminal.

Navigate to frontend folder.

```
cd frontend
```

Install dependencies

```
npm install
```

Install chart library

```
npm install recharts axios
```

---

# 7. Run Frontend

```
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

# How It Works

1. User enters a natural language query.
2. React sends the prompt to the FastAPI backend.
3. Backend sends prompt + database schema to the LLM.
4. LLM generates:

   * SQL query
   * chart type
   * x-axis column
   * y-axis column
5. Backend executes SQL on SQLite database.
6. Results are returned to React.
7. Recharts renders the interactive visualization.

---

# Example Queries

Try prompts such as:

```
Show revenue by campaign type
Compare ROI across marketing channels
Show clicks by language
Show conversions by target audience
```

---

# Example API Response

```
{
 "sql": "SELECT Campaign_Type, SUM(Revenue) AS Total_Revenue FROM campaigns GROUP BY Campaign_Type",
 "chart": "bar",
 "x": "Campaign_Type",
 "y": "Total_Revenue",
 "data": [...]
}
```

---

# Features Implemented

* Natural language to SQL generation
* AI powered query engine
* Automatic chart selection
* Interactive visualizations
* FastAPI backend API
* React dashboard interface

---

# Future Improvements

* Multi-chart dashboards
* CSV upload for custom datasets
* Follow-up conversational queries
* Chart filtering and drilldowns
* Dashboard export

---

# Author

Ani
Engineering Student – KMIT Hyderabad

---
