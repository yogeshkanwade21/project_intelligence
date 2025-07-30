import logging
import httpx
from config import settings


logger = logging.getLogger(__name__)

JIRA_API_BASE = f"{settings.jira_protocol}://{settings.jira_host}/rest/api/3"
# JIRA_API_BASE = f"{Config.jira_protocol}://{Config.jira_host}/rest/api/3"

def get_headers():
    return {
        "Authorization": f"Basic {httpx.BasicAuth(settings.jira_email, settings.jira_api_token)}",
        "Accept": "application/json"
    }

async def search_issues(jql: str):
  url = f"{JIRA_API_BASE}/search"
  other_headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
  params = {
    "jql": jql,
    # "fields": "key,summary"
  }
  headers = get_headers()
  logger.info(f"Searching Jira with JQL: {jql}")
  logger.info(f"Jira API URL: {url}")
  logger.info(f"Jira API params: {params}")
  # --- ADD THIS DEBUG LINE ---
  import urllib.parse
  # logger.info(f"Jira API headers prepared: {headers}")
  full_url_with_params = f"{url}?{urllib.parse.urlencode(params)}"
  logger.info(f"Full URL sent to Jira: {full_url_with_params}")
  # --- END ADDITION ---
  async with httpx.AsyncClient() as client:
    response = await client.get(url, headers=other_headers, params=params, auth=(settings.jira_email, settings.jira_api_token))
    response.raise_for_status()
    return response.json()
