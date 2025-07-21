from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import jira

app = FastAPI()

# CORS Middleware
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(jira.router)

@app.post("/query/handle")
async def analyze_query(payload: dict):
    return {"received_query": payload["query"]}

@app.get("/health")
def health_check():
    return {"message": "FastAPI backend is running"}
