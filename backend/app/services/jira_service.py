import logging
import httpx
from config import settings


logger = logging.getLogger(__name__)

JIRA_API_BASE = f"{settings.jira_protocol}://{settings.jira_host}/rest/api/3"
# JIRA_API_BASE = f"{Config.jira_protocol}://{Config.jira_host}/rest/api/3"

# def get_headers():
#     return {
#         "Authorization": f"Basic {httpx.BasicAuth(Config.jira_email, Config.jira_api_token)}",
#         "Accept": "application/json"
#     }

async def search_issues(jql: str):
  url = f"{JIRA_API_BASE}/search"
  params = {
    "jql": jql,
    "fields": "key,summary"
  }
  logger.info(f"Searching Jira with JQL: {jql}")
  logger.info(f"Jira API URL: {url}")
  logger.info(f"Jira API params: {params}")
  # logger.info(f"Jira API response status: {response.status_code}")
  async with httpx.AsyncClient() as client:
    response = await client.get(url, headers=get_headers(), params=params)
    response.raise_for_status()
    return response.json()
