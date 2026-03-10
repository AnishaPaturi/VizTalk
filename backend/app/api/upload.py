import pandas as pd
from fastapi import APIRouter, UploadFile, File
from app.database.connection import get_db_connection

router = APIRouter()

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):

    df = pd.read_csv(file.file)

    conn = get_db_connection()

    df.to_sql("uploaded_data", conn, if_exists="replace", index=False)

    conn.close()

    return {
        "message": "File uploaded successfully",
        "columns": list(df.columns)
    }