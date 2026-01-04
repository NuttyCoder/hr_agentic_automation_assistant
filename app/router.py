from fastapi import APIRouter
from src.conversation.gateway import handle_webhook
from src.orchestration.agent import run_agentic_workflow

api_router = APIRouter()

# Moveworks-style webhook endpoint
@api_router.post("/webhook")
async def webhook_entrypoint(payload: dict):
    return await handle_webhook(payload)

# Direct agentic workflow trigger (for testing)
@api_router.post("/run-workflow")
async def run_workflow(payload: dict):
    return await run_agentic_workflow(payload)
