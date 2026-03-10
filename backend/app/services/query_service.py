import pandas as pd
import numpy as np
from app.database.connection import get_db_connection
from app.services.llm_service import generate_sql


def run_natural_language_query(user_prompt):

    sql_query = generate_sql(user_prompt)

    conn = get_db_connection()

    df = pd.read_sql(sql_query, conn)

    conn.close()

    # Convert NaN and infinite values to None
    df = df.replace([np.nan, np.inf, -np.inf], None)

    return {
        "sql": sql_query,
        "data": df.to_dict(orient="records")
    }