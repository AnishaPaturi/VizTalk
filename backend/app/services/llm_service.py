import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

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
Convert the following request into a valid SQLite SQL query.

Schema:
{schema}

Return ONLY SQL.

User request:
{user_prompt}
"""

    response = client.chat.completions.create(
        model="meta-llama/llama-3-8b-instruct",
        messages=[{"role": "user", "content": prompt}]
    )

    sql = response.choices[0].message.content.strip()

    sql = sql.replace("```sql", "").replace("```", "").strip()

    return sql