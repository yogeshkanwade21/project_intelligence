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

@app.get("/health")
def read_root():
    return {"message": "FastAPI backend is running"}
