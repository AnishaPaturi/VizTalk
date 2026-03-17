import pandas as pd
import sqlite3
import os

# Get project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Go up to root folder
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../../"))

# Correct data path
DATA_PATH = os.path.join(ROOT_DIR, "data", "nykaa_marketing.csv")

# DB path
DB_PATH = os.path.join(ROOT_DIR, "marketing.db")


# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
# DATA_PATH = os.path.join(BASE_DIR, "..", "data", "nykaa_marketing.csv")

# DB_PATH = os.path.join(BASE_DIR, "marketing.db")

columns = [
    "Campaign_ID",
    "Campaign_Type",
    "Target_Audience",
    "Duration",
    "Channel_Used",
    "Impressions",
    "Clicks",
    "Leads",
    "Conversions",
    "Revenue",
    "Acquisition_Cost",
    "ROI",
    "Language",
    "Engagement_Score",
    "Customer_Segment",
    "Date"
]

def load_csv_to_db():

    df = pd.read_csv(
        DATA_PATH,
        skiprows=2,
        header=None,
        names=columns,
        encoding="latin1"
    )

    conn = sqlite3.connect(DB_PATH)

    df.to_sql(
        "campaigns",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print("Database created successfully!")

if __name__ == "__main__":
    load_csv_to_db()