from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.router import api_router

app = FastAPI(
    title="HR Agentic Automation Assistant",
    description="An AI-powered HR automation platform with agentic workflows, RPA orchestration, and governance.",
    version="0.1.0"
)

# Optional: CORS setup for frontend or Moveworks-style webhook
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routes
app.include_router(api_router)

# Health check
@app.get("/health")
def health_check():
    return {"status": "ok"}
