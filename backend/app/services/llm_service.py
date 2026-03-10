import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")


def generate_sql(user_prompt):

    schema = """
Table: campaigns

Columns:
Campaign_ID
Campaign_Type
Target_Audience
Duration
Channel_Used
Impressions
Clicks
Leads
Conversions
Revenue
Acquisition_Cost
ROI
Language
Engagement_Score
Customer_Segment
Date
"""

    prompt = f"""
You are a data analyst.

Convert the user's request into:

1) SQL query
2) Best chart type
3) X axis column
4) Y axis column

Database schema:
{schema}

Return JSON ONLY in this format:

{{
 "sql": "SQL QUERY",
 "chart": "bar | line | pie",
 "x_axis": "column",
 "y_axis": "column"
}}

Rules:
- Use SQLite syntax
- Do NOT explain anything
- Do NOT include markdown
- Aggregated columns MUST have aliases
- Always filter NULL values using WHERE column IS NOT NULL

Example:
SUM(Revenue) AS Total_Revenue

User request:
{user_prompt}
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "HTTP-Referer": "http://localhost:5173",
            "X-Title": "Conversational BI Dashboard"
        },
        json={
            "model": "deepseek/deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )

    result = response.json()

    print("OPENROUTER RESPONSE:", result)

    if "choices" not in result:
        raise Exception(f"OpenRouter API error: {result}")

    content = result["choices"][0]["message"]["content"]

    # Clean markdown if present
    content = content.replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(content)
    except:
        raise Exception(f"Invalid JSON from LLM: {content}")

    return parsed

import sqlite3

def get_schema():

    conn = sqlite3.connect("marketing.db")

    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(campaigns)")

    columns = cursor.fetchall()

    conn.close()

    return [col[1] for col in columns]