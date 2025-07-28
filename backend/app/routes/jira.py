import httpx
import base64
import os
from fastapi import APIRouter
from app.services.jira_service import search_issues
from config import settings

router = APIRouter()

@router.post("/prompt")
async def handle_user_prompt(query: dict):
    user_input = query.get("query", "").lower()

    if "bug" in user_input:
        jql = 'issuetype = Bug'
    else:
        return {"error": "Could not understand query."}

    url = f"{settings.jira_protocol}://{settings.jira_host}/rest/api/3/search"
    auth = f"{settings.jira_email}:{settings.jira_api_token}"
    encoded = base64.b64encode(auth.encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json"
    }

    params = {
        "jql": jql,
        # "fields": "key,summary"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "details": e.response.text}


@router.get("/jira/search")
async def jira_search():
    jql = 'issuetype = Bug'
    return await search_issues(jql)
