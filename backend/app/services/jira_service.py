import httpx
from app.config import settings

JIRA_API_BASE = f"{settings.jira_protocol}://{settings.jira_host}/rest/api/3"

def get_headers():
    return {
        "Authorization": f"Basic {httpx.auth._basic_auth_str(settings.jira_email, settings.jira_api_token)}",
        "Accept": "application/json"
    }

async def search_issues(jql: str):
  url = f"{JIRA_API_BASE}/search"
  params = {
    "jql": jql,
    "fields": "key,summary"
  }
  async with httpx.AsyncClient() as client:
    response = await client.get(url, headers=get_headers(), params=params)
    response.raise_for_status()
    return response.json()
