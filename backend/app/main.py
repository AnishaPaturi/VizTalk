from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.api.upload import router as upload_router

app.include_router(upload_router)

from app.services.query_service import run_natural_language_query

app = FastAPI()

# Allow React frontend to call backend
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    prompt: str


@app.get("/")
def home():
    return {"message": "Conversational BI API running"}


@app.post("/query")
def query_data(request: QueryRequest):
    result = run_natural_language_query(request.prompt)
    return result